import MySQLdb
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

import utils
import database

class connection_check_event():
    @staticmethod
    def get_page(limit_per_page, offset):
        db = database.Database()
        conn = db.get_connection()
        metadata = MetaData(db)

        connection_check = Table('connection_check', metadata,
                                      Column('id', Integer, primary_key=True),
                                      Column('check_name', String(64)),
                                      Column('ip', String(16)),
                                      Column('description', String(255)),
                                      )

        connection_check_event = Table('connection_check_event', metadata,
                                            Column('id', Integer, primary_key=True),
                                            Column('timestamp', TIMESTAMP(timezone=true), default=func.now()),
                                            Column('connection_check_type', Integer),
                                            Column('status', Integer),
                                            ForeignKeyConstraint(['connection_check_type'], ['connection_check.id']),
                                            )

        connection_check_events = Table('connection_check_event', metadata, autoload=True)

        session = sessionmaker(bind=db.get_engine())
        ses = session()

        num_rows = ses.query(connection_check_event).count()

        number_of_pages = num_rows / limit_per_page

        stm = select([connection_check_events]).limit(limit_per_page).offset(offset)
        # stm = select([connection_check_events.c.status])
        #
        # stm = select([connection_check_events]).where(and_(connection_check_events.c.status))

        # stm = select([connection_check_events]).where(and_(connection_check_events.c.foo > 100,
        #                                 connection_check_events.c.bar < 1000000))

        rs = conn.execute(stm)
        rows = rs.fetchall()

        return rows, number_of_pages
