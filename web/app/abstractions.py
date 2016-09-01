import MySQLdb
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

import utils
import database

class connection_check_event():
    def __init__(self):
        self.db = database.Database()
        self.conn = self.db.get_connection()
        self.metadata = MetaData(self.db)

        self.connection_check = Table('connection_check', self.metadata,
                                      Column('id', Integer, primary_key=True),
                                      Column('check_name', String(64)),
                                      Column('ip', String(16)),
                                      Column('description', String(255)),
                                      )

        self.connection_check_event = Table('connection_check_event', self.metadata,
                                            Column('id', Integer, primary_key=True),
                                            Column('timestamp', TIMESTAMP(timezone=true), default=func.now()),
                                            Column('connection_check_type', Integer),
                                            Column('status', Integer),
                                            ForeignKeyConstraint(['connection_check_type'], ['connection_check.id']),
                                            )

        self.session = sessionmaker(bind=self.db.get_engine())
        self.ses = self.session()

    def get_page(self, limit_per_page, offset):

        num_rows = self.ses.query(self.connection_check_event).count()

        number_of_pages = num_rows / limit_per_page

        stm = select([self.connection_check_event]).limit(limit_per_page).offset(offset)
        # stm = select([connection_check_events.c.status])
        #
        # stm = select([connection_check_events]).where(and_(connection_check_events.c.status))

        # stm = select([connection_check_events]).where(and_(connection_check_events.c.foo > 100,
        #                                 connection_check_events.c.bar < 1000000))

        rs = self.conn.execute(stm)
        rows = rs.fetchall()

        return rows, number_of_pages

    def count_failed_connections(self):
        pass
