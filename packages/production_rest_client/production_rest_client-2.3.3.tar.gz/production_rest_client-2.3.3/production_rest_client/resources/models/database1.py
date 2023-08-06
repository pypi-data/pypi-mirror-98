# coding=utf-8
# pylint: disable=broad-except, import-error
import pymysql as mysql


class SqlConnection(object):

    def __init__(self, host="172.29.129.8", port=3306, user="tester", passwd="Cnex!321", db_name="production_test"):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db_name = db_name
        self.conn = mysql.connect(host=self.host, port=self.port, user=self.user,
                                  passwd=self.passwd, db=self.db_name, charset="utf8")
        self.cursor = self.conn.cursor()

    def __del__(self):
        print("SqlConnection del")
        self.cursor.close()
        self.conn.close()

    def execute_sql_command(self, command):
        results = list()
        try:
            self.conn.ping()
            self.cursor.execute(command)
            results = self.cursor.fetchall()
        except BaseException as message:
            print(message)
        return results