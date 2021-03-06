import ConfigParser
import os

import MySQLdb

class DB:
    def  getAtpConnection(self):
        cf = ConfigParser.ConfigParser()
        cf.read(os.path.dirname(os.getcwd()) + "/conf/config.ini")
        HOST = cf.get("dbconf_atp", "db_host")
        PORT = cf.get("dbconf_atp", "db_port")
        USER = cf.get("dbconf_atp", "db_user")
        PW = cf.get("dbconf_atp","db_password")
        DB = cf.get("dbconf_atp", "db_name")
        dbConnect = MySQLdb.Connect(host=HOST, port=int(PORT), user=USER, passwd=PW, db=DB,charset="utf8")
        return dbConnect

    def atpQuery(self,sql):
        mysql = DB()
        mysqldb = mysql.getAtpConnection()
        cursor = mysqldb.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        try:
            cursor.execute(sql)
            data = cursor.fetchall()
            #print s
        except:
            print "Error: unable to fecth data"
        mysqldb.close()
        return data

    def atpUpdate(self, sql):
        mysql = DB()
        mysqldb = mysql.getAtpConnection()
        cursor = mysqldb.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        try:
            cursor.execute(sql)
            mysqldb.commit()
        except:
            mysqldb.rollback()
        mysqldb.close()


#a = db()
#a.query("select * from user_info limit 1")

