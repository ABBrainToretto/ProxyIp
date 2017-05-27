#_*_ coding:utf-8 _*_
import requests
import random
import time
import MySQLdb
from lxml import etree

url = 'http://www.xicidaili.com/nt/2'

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

##-----爬取西刺代理的类-------##
class Proxy_pool():
    def __init__(self):
        self.ip_list = []
        self.test_url = 'http://cq.meituan.com/category/chuancai'
        self.user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
        ]
    def ip_pool(self,start_page,end_page):
        for i in range(start_page,end_page+1):
            url = 'http://www.xicidaili.com/nt/'+str(i)
            UA = random.choice(self.user_agent_list)
            headers = {'User-Agent':UA}
            html = requests.get(url,headers=headers)

            selector = etree.HTML(html.text)
            ip_list_field = selector.xpath('//table[@id="ip_list"]')
            trs = ip_list_field[0].xpath('tr')
            # print trs

            for ip in trs[1:]:
                IP = ip.xpath('td[2]/text()')[0]
                PORT = ip.xpath('td[3]/text()')[0]
                TYPE = ip.xpath('td[6]/text()')[0]
                POSITION = ip.xpath('td[4]/text()')[0]
                SPEED = ip.xpath('td[7]/div[@class = "bar"]/@title')[0]
                pLAST_CHECK_TIME = ip.xpath('td[10]/text()')[0]#因为是时间

                # print ('%s:%s'%(IP,PORT),TYPE)
                # self.ip_list.append('%s:%s:%s'%(TYPE.lower(),IP,PORT))
                self.ip_list.append([TYPE,'%s:%s'%(IP,PORT)])
        # print self.ip_list
        return self.ip_list


##------------验证ip的可用性------------##
    def ip_examine(self):
        UA = random.choice(self.user_agent_list)
        headers = {'User-Agent':UA}
        mysql = Sql()#执行Sql类
        for i in self.ip_list:
            proxy = {}
            proxy[i[0].lower()] = i[1]
            print '目前正在验证的代理是：',proxy
            try:
                test_web = requests.get(self.test_url,headers=headers,proxies=proxy)
                if test_web.status_code == 200:
                    print 'bingo'
                    str_proxy = str(proxy) #字典字符串化处理
                    mysql.mysqldata(i[0].lower(),i[1])
                    print u'此%s插入成功'% str_proxy
                else:
                    self.ip_list.pop(i)
            except:
                continue
        mysql.cur.close()#关闭游标
        mysql.conn.close()#关闭数据库连接



##-------封装模块，以便以后调用---------##
if __name__ == '__main__':
    MVP = Proxy_pool()
    MVP.ip_pool(1,4)
    MVP.ip_examine()


