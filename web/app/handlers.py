import webapp2

import utils
import templates
import abstractions


class HomeHandler(webapp2.RequestHandler):
    def get(self):
        templates.render_page("home", {}, self)
        return


class StatusHandler(webapp2.RequestHandler):
    def get(self):

        if self.request.get('page'):
            page_number = int(self.request.get('page'))
        else:
            page_number = 1

        limit_per_page = 20
        offset = 0 * limit_per_page if page_number < 1 else (page_number - 1) * limit_per_page

        # self.response.write(page_number)
        # self.response.write("<br />")
        #
        # self.response.write(offset)
        # self.response.write("<br />")
        #
        # self.response.write(limit_per_page)
        # return

        cce = abstractions.connection_check_event()

        rows, number_of_pages = cce.get_page(limit_per_page=limit_per_page, offset=offset)

        form_variables = {
            'rows': rows,
            'page_number': page_number,
            'number_of_pages': number_of_pages,
        }

        templates.render_page("status", form_variables, self)
        return


class NotFoundHandler(webapp2.RequestHandler):
    def get(self, route):
        utils.throw404(self)
        return
