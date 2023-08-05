"""Router models

This file defines two router models. 

Each participant has a main Router. The Router has two 'tracks'. When the 
participant requests a new page, the router moves through the 'request' 
track. The request track compiles and renders a new survey page. When the 
participant submits a page, the router moves through the 'submit' track. The 
submit track records the participant's response, validates it, submits it, 
navigates, and redirects with a new page request.

The secondary Navigator router is nested in the main Router. It handles 
backward and forward navigation.
"""

from ...app import db
from .viewing_page import ViewingPage

from flask import current_app, request, redirect, session, url_for
from flask_worker import RouterMixin, set_route

from datetime import datetime


class Router(RouterMixin, db.Model):
    """
    The main router belongs to a Participant. It handles the request and 
    submit tracks.

    Parameters
    ----------
    gen_root : callable
        Callable which generates the root branch.

    Attributes
    ----------
    part : hemlock.Participant
        Participant to whom this router belongs.

    page : hemlock.Page
        The participant's current page.

    in_progress : bool
        Indicates that a route is being processed. Helps avoid queueing 
        extra routing functions.

    job_in_progress : bool
        Indicates that a worker's job is being processed.

    view_function : str
        Name of the function which generated the root branch. It is also the 
        name of the view function associated with this router. On redirect, 
        the router, redirects to `url_for(self.view_function)`.

    navigator : hemlock.models.private.Navigator
        A navigator router which handles navigation between pages.
    """
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    in_progress = db.Column(db.Boolean, default=False)
    view_function = db.Column(db.String)
    worker_page = db.Column(db.Text)
    worker = db.relationship('Worker', uselist=False)
    navigator = db.relationship('Navigator', backref='router', uselist=False)

    @property
    def page(self):
        return self.part.current_page

    def __init__(self, gen_root):
        self.view_function = gen_root.__name__
        self.navigator = Navigator(gen_root)
        super().__init__(self.compile)

    def __call__(self, *args, **kwargs):
        """Route overload

        If the participant's time has expired, render the current page with 
        a time expired error message.

        The router starts at the beginning of the request track (compile). If 
        the participant has just submitted a page, the router moves to the 
        beginning of the submit track (record response). Then route as normal.

        Returns
        -------
        page : str (html)
            HTML of the participant's next page, or a loading page.
        """
        def render_current_page():
            if self.page.timer and self.page.timer.state != 'running':
                self.page.timer.start()
                db.session.commit()
            return self.page._render()

        def process_request():
            # commit the in_progress flag so future requests will know to 
            # return the loading page
            self.in_progress = True
            db.session.commit()
            if request.method == 'POST' and self.func.name == 'compile':
                # participant has just submitted the page
                self.func = self.record_response
            result = self.func(self, *args, **kwargs)
            self.in_progress = False
            db.session.commit()
            return result

        if self.part.time_expired:
            self.page.error = current_app.time_expired_text
            return self.page._render()
        if self.worker:
            return (
                process_request() if self.worker.job_finished 
                else self.worker_page
            )
        if self.in_progress:
            # send loading page while the next page loads
            return current_app.settings.get('loading_page')
        if request.method == 'GET' and not self.page.run_compile:
            # page refresh or participant went back to this page
            return render_current_page()
        return process_request()

    """Request track"""
    @set_route
    def compile(self):
        return self.run_worker(
            self.page, '_compile', self.page.compile_worker, self.render
        )
    
    def render(self):
        if self.page.terminal and not self.part.completed:
            self.part.end_time = datetime.utcnow()
            self.part.completed = True
        page_html = self.page._render()
        self.part._viewing_pages.append(
            ViewingPage(page_html, first_presentation=not self.page.viewed)
        )
        self.page.viewed = True
        if self.page.timer is not None:
            self.page.timer.start()
        return page_html
    
    """Submit track"""
    def record_response(self):
        if self.page.timer is not None:
            self.page.timer.pause()
        self.part.end_time = datetime.utcnow()
        self.part.completed, self.part.updated = False, True
        self.page._record_response()
        if self.page.direction_from == 'back':
            if self.page.compile_worker:
                self.page.compile_worker.reset()
            self.navigator.back(self.page.back_to)
            return self.redirect()
        return self.validate()
    
    @set_route
    def validate(self):
        if not current_app.settings['validate']:
            # validation may be off for testing purposes
            return self.submit()
        return self.run_worker(
            self.page, '_validate', self.page.validate_worker, self.submit
        )
    
    @set_route
    def submit(self):
        if not self.page.is_valid() and current_app.settings['validate']:
            # will redirect to the same page with error messages
            return self.redirect()
        return self.run_worker(
            self.page, '_submit', self.page.submit_worker, self.forward_prep,
        )

    def forward_prep(self):
        """Prepare for forward navigation
        
        Check if direction_from has been changed by submit functions. If so, 
        navigate appropriately. Otherwise, reset the navigator in preparation 
        for forward navigation.
        """
        page = self.page
        if page.direction_from == 'back':
            self.navigator.back(page.back_to)
        if page.direction_from in ('back', 'invalid') or page.last_page():
            return self.redirect()
        self.navigator.reset()
        return self.forward(page.forward_to)
    
    @set_route
    def forward(self, forward_to):
        """
        Forward navigation uses the Navigator subrouter. If the navigator 
        has not yet started forward navigation (i.e. `not nav.in_progress`), 
        the main router gets a loading page from `nav.forward`. Otherwise, it 
        gets a loading page from `nav.__call__`.

        The navigator may need a worker to generate a new branch. While the 
        worker's job is in progress, the navigator returns a loading page 
        (which is not `None`).

        When it finds the next survey page, the navigator return `None`
        loading page. However, if there is a specified page to which the 
        router is navigating forward (`forward_to is not None`), it may be 
        necessary to call `nav.forward` again.
        
        When the navigator has finished, the router redirects the 
        participant to the new survey page.

        Parameters
        ----------
        forward_to : hemlock.Page
            Page to which to navigate.
        """
        loading_page = (
            self.navigator.func(self.navigator) if self.navigator.in_progress
            else self.navigator.forward(forward_to)
        )
        if loading_page is None and forward_to is not None:
            loading_page = self.navigator.forward(forward_to)
        return loading_page or self.redirect()

    def redirect(self):
        self.reset()
        url_arg = 'hemlock.{}'.format(self.view_function)
        if self.part.meta.get('Test') is None:
            return redirect(url_for(url_arg))
        # during testing, you may have multiple users running at once
        # in this case, participants much be found be ID, not `current_user`
        return redirect(
            url_for(url_arg, part_id=self.part.id, part_key=self.part._key)
        )

    def run_worker(
            self, obj, method_name, worker, next_route, *args, **kwargs
        ):
        """
        Run a worker if applicable.

        Parameters
        ----------
        obj : Page or Branch
            Object whose method should be run.

        method_name : str
            Name of the object's method to run. e.g. '_compile'

        worker : hemlock.WorkerMixin or None
            Worker which executes the method, if applicable.

        next_route : router method
            The next route to navigate to after executing the method.

        \*args, \*\*kwargs :
            Arguments and keyword arguments for `next_route`.

        Returns
        -------
        page : str (html)
            Page for the client. This will be a loading page, if the worker is 
            running, or the next page of the survey.        
        """
        if worker is None:
            getattr(obj, method_name)()
            return next_route(*args, **kwargs)
        if worker.job_finished:
            worker.reset()
            self.worker, self.worker_page = None, None
            return next_route(*args, **kwargs)
        self.worker = worker
        self.worker_page = worker.enqueue_method(obj, method_name)
        return self.worker_page


class Navigator(RouterMixin, db.Model):
    """    
    The navigator subrouter is nexted in the main router. It handles forward 
    and backward navigation.

    Attributes
    ----------
    router : hemlock.models.private.Router
        Main router with which the navigator is associated.

    in_progress : bool, default=False
        Indicates that navigation is in progress.
    """
    id = db.Column(db.Integer, primary_key=True)
    router_id = db.Column(db.Integer, db.ForeignKey('router.id'))
    in_progress = db.Column(db.Boolean, default=False)

    @property
    def part(self):
        return self.router.part

    @property
    def branch_stack(self):
        return self.part.branch_stack

    @property
    def branch(self):
        return self.part.current_branch

    @branch.setter
    def branch(self, value):
        self.part.current_branch = value

    @property
    def page(self):
        return self.part.current_page

    def reset(self):
        super().reset()
        self.in_progress = False

    """Forward navigation"""
    @set_route
    def forward(self, forward_to=None):
        """Advance forward to specified Page"""
        self.in_progress = True
        if forward_to is None:
            return self.forward_one()
        while self.page != forward_to:
            loading_page = self.forward_one()
            if loading_page is not None:
                return loading_page
    
    def forward_one(self):
        """Advance forward one page"""
        if self.page._eligible_to_insert_branch():
            return self.insert_branch(self.page)
        self.branch._forward()
        return self.forward_recurse()
    
    @set_route
    def insert_branch(self, origin):
        """Grow and insert new branch into the branch stack"""
        # note the parallel between this function and Router.run_worker
        worker = origin.navigate_worker
        if worker is None:
            origin._navigate()
            return self._insert_branch(origin)
        if worker.job_finished:
            worker.reset()
            self.router.worker, self.router.worker_page = None, None
            return self._insert_branch(origin)
        self.router.worker = worker
        self.router.worker_page = worker.enqueue_method(origin, '_navigate')
        return self.router.worker_page
    
    def _insert_branch(self, origin):
        branch = origin.next_branch
        self.branch_stack.insert(self.branch.index+1, branch)
        self.increment_head()
        return self.forward_recurse()

    def forward_recurse(self):
        """Recursive forward function

        Advance forward until the next Page is found (i.e. is not None).
        """
        if self.page is not None:
            return
        if self.branch._eligible_to_insert_branch():
            return self.insert_branch(self.branch)
        self.decrement_head()
        self.branch._forward()
        return self.forward_recurse()
    
    """Back navigation"""
    def back(self, back_to=None):
        """Navigate backward to specified Page"""
        if back_to is None:
            return self.back_one()
        while self.page != back_to:
            self.back_one()
            
    def back_one(self):
        """Navigate backward one Page"""
        # re-run compile functions the next time the participant goes forward 
        # to this page
        self.page.run_compile = True
        if self.page == self.branch.start_page:
            return self.remove_branch()
        self.branch._back()
        return self.back_recurse()
        
    def remove_branch(self):
        """Remove current branch from the branch stack"""
        self.decrement_head()
        self.branch_stack.pop(self.branch.index+1)
        return self.back_recurse()
        
    def back_recurse(self):
        """Recursive back function
        
        Navigate backward until previous Page is found.
        """
        if self.found_previous_page():
            return
        if self.page is None:
            if self.branch.next_branch in self.branch_stack:
                self.increment_head()
            elif not self.branch.pages:
                return self.remove_branch()
            else:
                self.branch._back()
        else:
            self.increment_head()
        return self.back_recurse()
    
    def found_previous_page(self):
        """Indicate that previous page has been found in backward navigation
        
        The previous page has been found when 1) the Page is not None and
        2) it does not branch off to another Branch in the stack.
        """
        return (
            self.page is not None 
            and self.page.next_branch not in self.branch_stack
        )

    """Move the head of the branch stack"""
    def increment_head(self):
        self.branch = self.branch_stack[self.branch.index+1]
    
    def decrement_head(self):
        self.branch = self.branch_stack[self.branch.index-1]