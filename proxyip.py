#_*_ coding:utf-8 _*_
import requests
import random
import time
from lxml import etree

url = 'http://www.xicidaili.com/nn/2'

##-----爬取西刺代理的类-------##
class Proxy_pool():
    def __init__(self):
        self.ip_list = []
        self.user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
        ]
    def ip_pool(self,start_page,end_page):
        for i in range(start_page,end_page+1):
            url = 'http://www.xicidaili.com/nn/'+str(i)
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

##-----设计ip代理的类-------##
class DownLoad():
    def __init__(self):
        self.ip_list = Proxy_pool().ip_pool(1,2)
        self.user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
        ]
        print '代理池下载完成，请继续...'
    def get(self,url,proxy=None,timeout=20,num=5):
        print '正在请求：',url 
        UA = random.choice(self.user_agent_list)
        headers = {'User-Agent':UA}
        
##-------以本机IP开始试验--------##
        # if proxy == None:
        #     try:
        #         return requests.get(url,headers=headers,timeout=timeout)
        #     except:
        #         if num > 0:
        #             time.sleep(10)
        #             return self.get(url,num = num - 1)    
        #         else:
        #             time.sleep(10)
        #             IP = random.choice(self.ip_list)
        #             proxy = {}
        #             proxy[IP[0].lower()] = IP[1]
        #             print '目前的代理是：',proxy
        #             return self.get(url,proxy=proxy,timeout=timeout)


##-------以次{'http':'110.72.29.145:8123'}开始试验--------##
        if proxy == None:
            try:
                return requests.get(url,headers=headers,proxies={'http':'110.72.29.145:8123'},timeout=timeout)
            except:
                IP = random.choice(self.ip_list)
                proxy = {}
                proxy[IP[0].lower()] = IP[1]
                print '目前的代理是：',proxy
                return self.get(url,proxy=proxy,timeout=timeout)
                

        else:
            try:
                IP = random.choice(self.ip_list)
                proxy = {}
                proxy[IP[0].lower()] = IP[1]
                return requests.get(url,headers=headers,proxies=proxy,timeout=timeout)
            
            except:
                if num > 0:
                    time.sleep(10)
                    IP = random.choice(self.ip_list)
                    proxy = {}
                    proxy[IP[0].lower()] = IP[1]
                    print '正在更换代理'
                    print '当前代理：',proxy

                    return self.get(url,proxy=proxy,timeout=timeout)


##-------封装模块，以便以后调用---------##
if __name__ == '__main__':    
    MVP = DownLoad()
    MVP.get('http://www.xicidaili.com')
            
