import webapp2
import MySQLdb

import utils
import templates
import database


class HomeHandler(webapp2.RequestHandler):
    def get(self):
        templates.render_page("home", {}, self)
        return


class StatusHandler(webapp2.RequestHandler):
    def get(self):

        db = database.Database()
        rows = db.db_select_query("SELECT `id`, `timestamp`, `success` FROM `connection_check` WHERE 1")

        templates.render_page("status", {'rows': rows}, self)
        return


class NotFoundHandler(webapp2.RequestHandler):
    def get(self, route):
        utils.throw404(self)
        return
