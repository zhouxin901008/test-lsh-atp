import ConfigParser

import MySQLdb

class db:
    def  getAtpConnection(self):
        cf = ConfigParser.ConfigParser()
        cf.read("/Users/zhouxin/PycharmProjects/testinterface/com/java/conf/db_config.ini")
        HOST = cf.get("dbconf_atp", "db_host")
        PORT = cf.get("dbconf_atp", "db_port")
        USER = cf.get("dbconf_atp", "db_user")
        PW = cf.get("dbconf_atp","db_password")
        DB = cf.get("dbconf_atp", "db_name")
        dbConnect = MySQLdb.Connect(host=HOST, port=int(PORT), user=USER, passwd=PW, db=DB,charset="utf8")
        return dbConnect

    def atpQuery(self,sql):
        mysql = db()
        mysqldb = mysql.getAtpConnection()
        cursor = mysqldb.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        try:
            cursor.execute(sql)
            s = cursor.fetchall()
            #print s
        except:
            print "Error: unable to fecth data"
        mysqldb.close()
        return s

    def atpUpdate(self, sql):
        mysql = db()
        mysqldb = mysql.getAtpConnection()
        cursor = mysqldb.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        try:
            cursor.execute(sql)
            mysqldb.commit()
        except:
            mysqldb.rollback()
        mysqldb.close()

    def  getPaymentConnection(self):
        cf = ConfigParser.ConfigParser()
        cf.read("/Users/zhouxin/PycharmProjects/testinterface/com/java/conf/db_config.ini")
        HOST = cf.get("dbconf_payment", "db_host")
        PORT = cf.get("dbconf_payment", "db_port")
        USER = cf.get("dbconf_payment", "db_user")
        PW = cf.get("dbconf_payment","db_password")
        DB = cf.get("dbconf_payment", "db_name")
        dbConnect = MySQLdb.Connect(host=HOST, port=int(PORT), user=USER, passwd=PW, db=DB,charset="utf8")
        return dbConnect

    def paymentQuery(self,sql):
        mysql = db()
        mysqldb = mysql.getPaymentConnection()
        cursor = mysqldb.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        try:
            cursor.execute(sql)
            s = cursor.fetchall()
            #print s
        except:
            print "Error: unable to fecth data"
        mysqldb.close()
        return s

    def  getTmsConnection(self):
        cf = ConfigParser.ConfigParser()
        cf.read("/Users/zhouxin/PycharmProjects/testinterface/com/java/conf/db_config.ini")
        HOST = cf.get("dbconf_lsh_tms", "db_host")
        PORT = cf.get("dbconf_lsh_tms", "db_port")
        USER = cf.get("dbconf_lsh_tms", "db_user")
        #PW = cf.get("dbconf_lsh_tms","db_password")
        DB = cf.get("dbconf_lsh_tms", "db_name")
        dbConnect = MySQLdb.Connect(host=HOST, port=int(PORT), user=USER, db=DB,charset="utf8")
        return dbConnect

    def tmsQuery(self,sql):
        mysql = db()
        mysqldb = mysql.getTmsConnection()
        cursor = mysqldb.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        try:
            cursor.execute(sql)
            s = cursor.fetchall()
            #print s
        except:
            print "Error: unable to fecth data"
        mysqldb.close()
        return s




#a = db()
#a.query("select * from user_info limit 1")

