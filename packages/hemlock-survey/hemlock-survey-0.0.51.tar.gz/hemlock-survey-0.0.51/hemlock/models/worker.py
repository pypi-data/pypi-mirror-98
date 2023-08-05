"""# Worker"""

from ..app import db
from .bases import Base

from flask_worker import WorkerMixin


class Worker(WorkerMixin, Base, db.Model):
    """
    Workers simplify interaction with a Redis queue. A worker attaches to a 
    branch or page, and is responsible for one of its methods (compile, 
    validate, submit, or navigate).

    When the method for which a worker is responsible is called, the worker
    sends the method to a Redis queue. While the Redis queue is processing 
    this method, the worker shows participants a loading page. When the Redis
    queue finishes processing this method, the worker sends the client to his
    next page.

    Worker inherits from 
    [`flask_worker.WorkerMixin`](https://dsbowen.github.io.flask-worker/).

    Examples
    --------
    In `survey.py`:

    ```python
    from hemlock import Branch, Compile as C, Label, Page, route

    @route('/survey')
    def start():
    \    return Branch(
    \        Page(
    \            Label('Hello, World!')
    \        ),
    \        Page(
    \            Label(
    \                'Goodbye, Moon!',
    \                compile=C.complex_function(seconds=5)
    \            ),
    \            compile_worker=True,
    \            terminal=True
    \        ),
    \    )

    @C.register
    def complex_function(label, seconds):
    \    import time
    \    for t in range(seconds):
    \        print('Progress: {}%'.format(round(100.*t/seconds)))
    \        time.sleep(1)
    \    print('Progress: 100%')
    ```

    Note that the second page (or rather, one of its questions), needs to run
    a complex compile function. We add a worker to it by setting 
    `compile_worker=True`. Use a similar syntax to add validate, submit, and 
    navigate workers.

    Our `app.py` is standard:

    ```python
    import eventlet
    eventlet.monkey_patch()

    import survey

    from hemlock import create_app

    app = create_app()

    if __name__ == '__main__':
    \    from hemlock.app import socketio
    \    socketio.run(app, debug=True)
    ```

    To run the app locally, you will need to set the `REDIS_URL` environment 
    variable and run a redis queue from your project's root directory.

    ??? warning "Redis on Windows"
    \    Windows cannot run redis natively. To run redis on Windows, use [Windows Subsystem for Linux](../setup/wsl.md).

    If using the hemlock template and hemlock-CLI:

    1. Open `env.yaml` and add the line `REDIS_URL: redis://`.
    2. Open a second terminal in your project's root directory and run the redis queue with `hlk rq`.
    3. Run the app by entering `hlk serve` in your first terminal.

    If not using the template or hemlock-CLI:

    1. Set your environment variable with `export REDIS_URL=redis://`.
    2. Open a second terminal in your project's root directory and enter `rq worker hemlock-task-queue`.
    3. Run the app by entering `python3 app.py` in your first terminal.

    Go to <http://localhost:5000/> in your browser. Notice that, when you click past the first page, you see a loading gif before the second page is loaded. In your second terminal window, you should see:

    ```
    Progress: 0%
    ...
    Progress: 100%
    ```

    Notes
    -----

    To run redis in production on heroku:

    <b>1. Declare a worker process</b>
    
    In the root directory of your project, open `Procfile`. Add the line `worker: rq worker -u $REDIS_URL hemlock-task-queue`. Your `Procfile` should look like:

    ```
    web: gunicorn -k eventlet -w 1 app:app
    worker: rq worker -u $REDIS_URL hemlock-task-queue
    ```

    <b>2. Create a redis addon and provision worker processes</b>

    In the root directory of your project, open `app.json`.

    To create a Redis addon, add `{"plan": "heroku-redis:hobby-dev", "options": {"version": 5}}` to your `addons`. To provision worker processes, add `"worker: {"quantity": 1, "size": "hobby"}` to your `formation`. In sum, the top of `app.json` will look like:

    ```json
    {
    \    "addons": [
    \        "heroku-postgresql:hobby-dev", 
    \        {"plan": "heroku-redis:hobby-dev"}
    \    ],
    \    "formation": {
    \        "web": {"quantity": 1, "size": "hobby"},
    \        "worker": {"quantity": 1, "size": "hobby"}
    \    },
        ...
    ```

    When scaling for production, I recommend using the premium-1 redis plan, 
    quantity 5, size standard-1x. So `app.json` will look like:

    ```json
    {
    \    "addons": [
    \        "heroku-postgresql:standard-1x", 
    \        {"plan": "heroku-redis:premium-1", "options": {"version": 5}}
    \    ],
    \    "formation": {
    \        "web": {"quantity": 10, "size": "standard-1x"},
    \        "worker": {"quantity": 5, "size": "standard-1x"}
    \    },
        ...
    ```

    ??? note "Why redis 5?" 
    \    I recommend redis version 5, rather than the latest version 6. Heroku requires you to manually set up TLS authentication for redis 6, which is a complicated process, whereas you can bypass TLS authentication using redis 5.
    """
    id = db.Column(db.Integer, primary_key=True)
    _compile_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    _validate_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    _submit_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    _navigate_page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    _navigate_branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    _router_id = db.Column(db.Integer, db.ForeignKey('router.id'))