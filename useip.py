# _*_coding:utf-8 _*_
import MySQLdb
import requests

class Sql():
    def __init__(self):
        self.conn = MySQLdb.connect(
                host = "localhost",
                port = 3306,
                user = "root",
                passwd = "123321",
                db = "book",
                charset = "utf8"
            )
        self.cur = self.conn.cursor()
        
    def mysqldata(self):
        sql = "select * from ip_proxy ORDER BY RAND() LIMIT 1"
        # sql = "insert into ip_proxy (`id`,`type`,`ip_proxy`)values(0,%s,%s)"
        # param = (type,proxy)
        self.cur.execute(sql)
        # print self.cur.fetchall()
        n = self.cur.fetchall()[0]
        # print n
        # for row in self.cur.fetchall():
            # print row[1],row[2]
        proxy = {}
        proxy[n[1]] = n[2]
        # print '您现在正在使用的代理是：',proxy
        # self.conn.commit()
        return proxy
        
if __name__=='__main__':
    mysql = Sql()
    mysql.mysqldata()

