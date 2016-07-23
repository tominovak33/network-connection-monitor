import MySQLdb
import MySQLdb.cursors

import config


class Database:

    def __init__(self):
        self.database_connection = None
        self.success_status = None
        self.db_connect(config.DATABASE_DETAILS)
        print "Network Connection Monitor Started"

    def db_connect(self, database_details):
        self.database_connection = MySQLdb.connect(
            host=database_details.get('db_host'),
            db=database_details.get('db_name'),
            user=database_details.get('db_username'),
            passwd=database_details.get('db_password'),
            cursorclass=MySQLdb.cursors.DictCursor
        )

    def db_select_query(self, sql_query):
        cursor = self.database_connection.cursor()
        cursor.execute(sql_query)

        return cursor.fetchall()
