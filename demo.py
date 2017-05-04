#_*_ coding:utf-8 _*_
import xici
MVP = xici.DownLoad()
html = MVP.get('http://www.xicidaili.com')
print html.text
