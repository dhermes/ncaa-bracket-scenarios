"""Simple module containing a shared base handler for Jinja2 rendering."""


import webapp2
from webapp2_extras import jinja2


class BaseHandler(webapp2.RequestHandler):
    """Base handler for rendering Jinja2 templates."""

    @webapp2.cached_property
    def jinja2(self):
        """Cached property holding a Jinja2 instance.

        Returns:
            A Jinja2 object for the current app.
        """
        return jinja2.get_jinja2(app=self.app)

    def render_response(self, template, **context):
        """Use Jinja2 instance to render template and write to output.

        Args:
            template: filename (relative to $PROJECT/templates) that we are
                rendering.
            context: keyword arguments corresponding to variables in template.
        """
        rendered_value = self.jinja2.render_template(template, **context)
        self.response.write(rendered_value)
