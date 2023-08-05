"""# Label"""

from ..app import db, settings
from ..models import Question
from ..tools import markdown

from flask import render_template

settings['Label'] = {'data': 1}

class Label(Question):
    """
    This question contains a label and does not receive input from the 
    participant.

    Parameters
    ----------
    label : str or None, default=None
        Question label.

    template : str, default='hemlock/label.html'
        Path to the Jinja template for the label body.

    Examples
    --------
    ```python
    from hemlock import Label, Page, push_app_context

    app = push_app_context()

    Page(Label('Hello World')).preview()
    ```
    """
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'label'}

    def __init__(self, label=None, template='hemlock/label.html', **kwargs):
        super().__init__(label=label, template=template, **kwargs)

    def _render(self):
        return render_template(
            self.template, 
            q=self, 
            error=markdown(self.error, strip_last_paragraph=True), 
            label=markdown(self.label, strip_last_paragraph=True)
        )

    def _record_data(self):
        return self