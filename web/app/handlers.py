import webapp2
import MySQLdb
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker


import utils
import templates
import database


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

        session = sessionmaker(bind=db.get_engine())
        ses = session()

        num_rows = ses.query(self.connection_check_event).count()

        number_of_pages = num_rows / limit_per_page

        stm = select([connection_check_events]).limit(limit_per_page).offset(offset)
        # stm = select([connection_check_events.c.status])
        #
        # stm = select([connection_check_events]).where(and_(connection_check_events.c.status))

        # stm = select([connection_check_events]).where(and_(connection_check_events.c.foo > 100,
        #                                 connection_check_events.c.bar < 1000000))

        rs = conn.execute(stm)
        rows = rs.fetchall()

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
