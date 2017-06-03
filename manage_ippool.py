#_*_ coding:utf-8 _*_
import ippool_gevent_xici
import ippool_gevent_kuaidaili


##-----------调用西刺代理ip------------##
MVP1 = ippool_gevent_xici.IsActivePorxyIP()
proxy_ip_list1 = MVP1.ip_list.ip_pool(1,5)
pool1 = ippool_gevent_xici.Pool(20)
pool1.map(MVP1.ip_examine,proxy_ip_list1)

##-----------调用西刺代理ip------------##
MVP2 = ippool_gevent_kuaidaili.IsActivePorxyIP()
proxy_ip_list2 = MVP2.ip_list.ip_pool(12,15)
pool2 = ippool_gevent_kuaidaili.Pool(20)
pool2.map(MVP1.ip_examine,proxy_ip_list2)
