#!/usr/bin/env python
#coding:utf-8

import re
import os
import sys
import time
import base64
import urllib2
import threading

ip_list = ['10.1.2.7', '10.1.2.8', '10.1.3.7', '10.1.3.5']

def check_activemq(port="8161", admin="admin"):

    def ip_passwd(ip="127.0.0.1", passwd="admin"):
        date = time.strftime('%Y-%m%d-%H:%M')
        login_url = 'http://%s:%s/admin/xml/queues.jsp' %(ip, port)

        req = urllib2.Request(login_url)
        Username = admin
        Password = passwd

        # 把用户名密码转换成Base64编码
        base64_info = base64.encodestring(
                      '%s:%s' % (Username, Password))[:-1]
        auth_header =  "Basic %s" % base64_info


        # 把用户名和密码添加到HTTP请求头里面
        req.add_header("Authorization", auth_header)
        try:
            handle = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print "your username or password is wrong"
            sys.exit(1)
        except urllib2.URLError, e:
            send_mail = "echo '%s %s activemq 连接失败，可能有问题，请查看！' |mail -s 'activemq error' zhang.jianyou@puscene.com, lu.wanda@puscene.com" % (date, ip)
            os.system(send_mail)
            sys.exit(1)

        html = handle.read()

        # 用正则匹配AMQ"Number of Pending Messages"数值
        r1 = r'size="([0-9]*)"'
        size_list = re.findall(r1, html)

        # 用正则匹配queue
        queue_name=r'queue name="(\S*)"'
        queue_list = re.findall(queue_name, html)

        # 将queue和"Number of Pending Messages"数值关系对应
        queue_size = zip(queue_list, size_list)


        for num in queue_size:

            if int(num[1]) > 1000:
                send_mail = "echo '%s %s activemq queue_name [%s] entry connections is more than [%s]' |mail -s 'Apache amq alarm' zhang.jianyou@puscene.com" % (date, ip, num[0], num[1])
                os.system(send_mail)
        print(" %s activemq is OK!" %ip)
    return ip_passwd
        

def main():
    check_mq = check_activemq(8161, "admin")
    for ip in ip_list: 
        t = threading.Thread(target=check_mq, args=(ip, "activemq password"))
        t.start()

if __name__ == "__main__":
    main()
