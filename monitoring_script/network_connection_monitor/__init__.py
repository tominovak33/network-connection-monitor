import MySQLdb
import MySQLdb.cursors
import subprocess


class NetworkConnectionMonitor:

    def __init__(self, database_details):
        self.database_connection = None
        self.success_status = None
        self.db_connect(database_details)
        print "Network Connection Monitor Started"

    def db_connect(self, database_details):
        self.database_connection = MySQLdb.connect(
            host=database_details.get('db_host'),
            db=database_details.get('db_name'),
            user=database_details.get('db_username'),
            passwd=database_details.get('db_password'),
            cursorclass=MySQLdb.cursors.DictCursor
        )

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
        cursor = self.database_connection.cursor()
        # "INSERT INTO connection_check VALUES ({1}".(self.get_success_status()))
        #sql = "INSERT INTO connection_check (`success`) VALUES ({0})".format(self.get_success_status())
        #print sql
        #return
        # cursor.execute("""INSERT INTO connection_check VALUES (%s)""", (self.get_success_status()))

        cursor.execute('''INSERT into connection_check (success) values (%s)''', ('1'))
        # cursor.execute(sql)
        self.database_connection.commit()
        cursor.close()
        return

    def set_success_status(self, status):
        if status != 0 and status != 1:
            return

        self.success_status = status

    def get_success_status(self):
        return self.success_status



#http://codereview.stackexchange.com/questions/13683/pinging-a-list-of-hosts

"""
ping options


-l: Preload: sends that many packets not waiting for reply. Only the super-user may select preload more than 3.

-c: Count: Number of request

-s: Packet Size: Specifies the number of data bytes to be sent. The default is 56, which translates into 64 ICMP data bytes when combined with the 8 bytes of ICMP header data.

-W: Timeout: Time to wait for a response, in seconds. The option affects only timeout in absense of any responses, otherwise ping waits for two RTTs.

"""



