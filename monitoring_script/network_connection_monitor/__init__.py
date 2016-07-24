import MySQLdb
import MySQLdb.cursors
import subprocess
from sqlalchemy import *


class NetworkConnectionMonitor:

    def __init__(self, database_details):
        self.engine = None
        self.database_connection = None
        self.success_status = None
        self.db = Database()
        self.db_tables()
        print "Network Connection Monitor Started"

    def db_tables(self):
        metadata = self.db.get_metadata()
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

        metadata.create_all()

    def check_conenction(self):
        address = '8.8.8.8'
        # address = '192.169.1.200'
        # ping_options = ["ping", "-c", "1", "-l", "1", "-s", "1", "-W", "1"]
        ping_options = ["ping", "-c", "5"]

        ping = subprocess.Popen(
            ping_options + [address],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, error = ping.communicate()
        return_code = ping.returncode

        res = {
            'output': out,
            'error': error,
            'return_code': return_code
        }

        return res

    def store_check_status(self):
        ins = self.connection_check_event.insert().values(connection_check_type=1, status=self.success_status)
        self.db.get_connection().execute(ins)
        # self.db.get_connection().commit()

        # "INSERT INTO connection_check VALUES ({1}".(self.get_success_status()))
        #sql = "INSERT INTO connection_check (`success`) VALUES ({0})".format(self.get_success_status())
        #print sql
        #return
        # cursor.execute("""INSERT INTO connection_check VALUES (%s)""", (self.get_success_status()))

        # cursor.execute('''INSERT into connection_check (success) values (%s)''', ('1'))
        # # cursor.execute(sql)
        # self.database_connection.commit()
        # cursor.close()
        return

    def set_success_status(self, status):
        if status != 0 and status != 1:
            return

        self.success_status = status

    def get_success_status(self):
        return self.success_status


class Database:

    def __init__(self):
        self.engine = create_engine('mysql://root:root@localhost/practicedb')
        self.conn = self.engine.connect()
        self.metadata = MetaData(self.engine)

    def get_connection(self):
        return self.conn

    def get_metadata(self):
        return self.metadata

#http://codereview.stackexchange.com/questions/13683/pinging-a-list-of-hosts

"""
ping options


-l: Preload: sends that many packets not waiting for reply. Only the super-user may select preload more than 3.

-c: Count: Number of request

-s: Packet Size: Specifies the number of data bytes to be sent. The default is 56, which translates into 64 ICMP data bytes when combined with the 8 bytes of ICMP header data.

-W: Timeout: Time to wait for a response, in seconds. The option affects only timeout in absense of any responses, otherwise ping waits for two RTTs.

"""
