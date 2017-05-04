#_*_ coding:utf-8 _*_
import proxyip
MVP = proxyip.DownLoad()
html = MVP.get('http://www.xicidaili.com')
print html.text
