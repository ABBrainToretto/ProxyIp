# _*_ coding:utf-8 _*_
import requests
import random
from bs4 import BeautifulSoup
import MySQLdb

from gevent import monkey
monkey.patch_all()

from gevent.pool import Pool


##------------链接mysql数据库------------##
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
    def mysqldata(self,type,proxy):
        sql = "insert into ip_proxy (`id`,`type`,`ip_proxy`)values(0,%s,%s)"
        param = (type,proxy)
        self.cur.execute(sql,param)
        self.conn.commit()
        return

##-------------爬取快代理ip-----------------##
class Proxy_pool():
    def __init__(self):
        self.ip_list = []
        self.user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
        'Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
        ] # chrome/360/ie/firefox/Tencent/搜狗浏览器/
    def ip_pool(self,start_page,end_page):
        for i in range(start_page,end_page+1):
            url = 'http://www.kuaidaili.com/proxylist/'+str(i)
            UA = random.choice(self.user_agent_list)
            headers = {'User-Agent':UA}
            html = requests.get(url,headers=headers).content
            soup = BeautifulSoup(html,"html.parser")
            trs = soup.table.tbody.find_all('tr')
            for tr in trs:
                if tr.find_all('td')[2].string == u'高匿名':
                    IP = tr.find_all('td')[0].string
                    PORT = tr.find_all('td')[1].string
                    TYPE = tr.find_all('td')[3].string.split(',')[0]
                    self.ip_list.append([TYPE,'%s:%s'%(IP,PORT)])

        return self.ip_list

##------------验证ip的可用性------------##
class IsActivePorxyIP(object):
    def __init__(self):
        self.test_url = 'http://cq.meituan.com/category/chuancai'
        self.user_agent_list = Proxy_pool().user_agent_list
        self.ip_list = Proxy_pool()


    def ip_examine(self,proxy_ip):

        UA = random.choice(self.user_agent_list)
        headers = {'User-Agent':UA}
        mysql = Sql()#执行Sql类

        print '目前正在验证的代理是：',proxy_ip
        try:
            test_web = requests.get(self.test_url,headers=headers,proxies=proxy_ip)
            if test_web.status_code == 200:
                print 'bingo'
                str_proxy = str(proxy_ip) #字典字符串化处理
                mysql.mysqldata(proxy_ip[0].lower(),proxy_ip[1])
                print u'此%s插入成功'% str_proxy
            else:
                self.ip_list.pop(proxy_ip)
        except Exception as e:
            print u'我也不造哪里出错了'
        mysql.cur.close()#关闭游标
        mysql.conn.close()#关闭数据库连接


##-------封装模块，以便以后调用---------##
if __name__ == '__main__':
    MVP = IsActivePorxyIP()
    proxy_ip_list = MVP.ip_list.ip_pool(4,11)

    #异步并发
    pool = Pool(20)
    pool.map(MVP.ip_examine,proxy_ip_list)

