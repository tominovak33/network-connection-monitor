import jinja2
import os
import site_details
import utils

# set the Jinja environment using autoescaping of html and using the file system loader for templates
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def render_page(template, variables, self):
    # join the 'global' template variables to the page specifc ones
    variables = utils.merge_many(variables, site_details.global_details, {'site_url': self.request.host_url})

    # builds the path to the template
    template_file = "templates/" + template + ".html"
    # loads it into the Jinja environment
    template = JINJA_ENVIRONMENT.get_template(template_file)
    # outputs the HTML from the rendered template and variables
    #self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
    self.response.out.write(template.render(variables))
