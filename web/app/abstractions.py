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
        # stm = select([self.connection_check_event.c.status])
        #
        # stm = select([self.connection_check_event]).where(and_(self.connection_check_event.c.status))

        # stm = select([self.connection_check_event]).where(and_(self.connection_check_event.c.foo > 100,
        #                                 self.connection_check_event.c.bar < 1000000))

        rs = self.conn.execute(stm)
        rows = rs.fetchall()

        return rows, number_of_pages

    def get_all_connections(self):
        stm = select([self.connection_check_event])
        rs = self.conn.execute(stm)
        rows = rs.fetchall()
        return rows

    def count_total_connections(self):
        # TODO: use a `count` query instead
        return len(self.get_all_connections()) or 0

    def get_all_successful_connections(self):
        stm = select([self.connection_check_event]).where(and_(self.connection_check_event.c.status == 1))
        rs = self.conn.execute(stm)
        rows = rs.fetchall()
        return rows

    def count_total_successful_connections(self):
        # TODO: use a `count` query instead
        return len(self.get_all_successful_connections()) or 0

    def get_all_failed_connections(self):
        stm = select([self.connection_check_event]).where(and_(self.connection_check_event.c.status == 0))
        rs = self.conn.execute(stm)
        rows = rs.fetchall()
        return rows

    def count_total_failed_connections(self):
        # TODO: use a `count` query instead
        return len(self.get_all_failed_connections()) or 0

    def calculate_successful_connecton_ratio(self):
        try:
            return float(self.count_total_successful_connections()) / float(self.count_total_connections())
        except:
            # TODO: handle error properly
            return False
