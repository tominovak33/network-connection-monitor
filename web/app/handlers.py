import webapp2
import MySQLdb
from sqlalchemy import *

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
        conn = db.get_connection()
        metadata = MetaData(db)

        self.connection_check = Table('connection_check', metadata,
                                      Column('id', Integer, primary_key=True),
                                      Column('check_name', String(64)),
                                      Column('ip', String(16)),
                                      Column('description', String(255)),
                                      )

        self.connection_check_event = Table('connection_check_event', metadata,
                                            Column('id', Integer, primary_key=True),
                                            Column('timestamp', TIMESTAMP(timezone=true), default=func.now()),
                                            Column('connection_check_type', Integer),
                                            Column('status', Integer),
                                            ForeignKeyConstraint(['connection_check_type'], ['connection_check.id']),
                                            )

        connection_check_events = Table('connection_check_event', metadata, autoload=True)

        stm = select([connection_check_events])
        # stm = select([connection_check_events.c.status])
        #
        # stm = select([connection_check_events]).where(and_(connection_check_events.c.status))

        # stm = select([connection_check_events]).where(and_(connection_check_events.c.foo > 100,
        #                                 connection_check_events.c.bar < 1000000))

        rs = conn.execute(stm)
        rows = rs.fetchall()

        templates.render_page("status", {'rows': rows}, self)
        return


class NotFoundHandler(webapp2.RequestHandler):
    def get(self, route):
        utils.throw404(self)
        return
