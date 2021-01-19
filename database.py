import MySQLdb
from flask_mysqldb import MySQL
import mysql.connector


class Database:

    def __init__(self, host, port, user, passwd, db):

        self.con = mysql.connector.connect(host=host, port=port ,user=user, passwd=passwd, database=db, auth_plugin='mysql_native_password')
        self.cursor = self.con.cursor()
        
    def toggle(self):
        self1 = self
        if (self1.check == 0):
            self1.check = 1
        else:
            self1.check = 0