import MySQLdb
import MySQLdb.cursors

import sqlalchemy
from sqlalchemy import *

import config


class Database:

    def __init__(self):
        self.engine = create_engine('mysql://root:root@localhost/practicedb')
        self.conn = self.engine.connect()
        self.metadata = MetaData(self.engine)

    def get_connection(self):
        return self.conn

    def get_metadata(self):
        return self.metadata

    def table(self):
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
