# -*- coding: UTF-8 -*-
#!/usr/bin/env python
import urllib2
from HTMLParser import HTMLParser
from urllib import urlencode
import cookielib
import os


#config
proxy_address = '127.0.0.1:8087'


#return a string by the url
def getHtml(url, code='UTF-8', proxy=False):
    try:
        return urllib2.urlopen(url).read().decode(code).encode('UTF-8')
    except urllib2.HTTPError, e:
        print e.code

def setProxy(address):
    proxy = urllib2.ProxyHandler({'http':address})
    urllib2.install_opener(urllib2.build_opener(proxy))

def login():
    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('Cookie','t=BA32686'), ('Referer','http://www.jita.me/')]
    urllib2.install_opener(opener)
    user_data = {'loginInModalUserName': '氧化yh1314529',
             'loginInModalPassword': '627850427',
             'loginInModal': 'True'
    }
    url_data = urlencode(user_data)
    opener.open("http://www.jita.me/User/LoginAction.aspx", url_data)

class IndexParser(HTMLParser):
    url_id=''
    url_value=[]
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href' and value :
                    self.url_id = value
    def handle_data(self, data):
        if self.url_id and data:
            self.url_value.append((self.url_id, data))
            self.url_id = ''
    def getUrl(self):
        return self.url_value

#save file
def saveFile(url, filename, path):
    if not os.path.exists(path+filename):
        dist = open(path+filename, 'w')
        try:
            dist.write(urllib2.urlopen(url).read())
            print 'logger info save file success  '+path + filename
            dist.flush()
        except BaseException:
            print 'logger info save file error  '+path + filename
        finally:
            dist.close()
    else:
        print "logger info file " + path+filename +" is exists"


def run():
    template = 'http://www.jita.me/File.aspx/Control_ListFileThreads?pageSize=10&sortOrder=Descending&sortBy=StageDownloadCount&categoryID=-1&tagName=&pageIndex={0}&_=1370247479808'
    download = 'http://www.jita.me/Services/FileAttachment.ashx?AttachmentID={0}'
    for i in range(1, 12):
        url = template.format(str(i))
        try:
            page = urllib2.urlopen(url).read()
            parse = IndexParser()
            parse.url_value = []
            parse.feed(page)
            for u in parse.getUrl():
                if u and str(u).__contains__('/File.aspx/t')\
                    and not str(u[1]).__contains__('浏览')\
                    and not str(u[1]).__contains__('下载')\
                    and not str(u[1]).__contains__('评论'):
                    url = download.format(u[0].split('-')[1])
                    print url, u[1]
                    saveFile(url, u[1]+'.rar', 'jitame/')
        except urllib2.HTTPError, e:
            print e.code


def main():
    login()
    run()

if __name__=='__main__':main()
#ASP.NET_SessionId=kwdmi4551gq4rj454hsoso45
#SBVerifyCode=kuTYxsHkxBSQCHiw9IpKgVUftu4=
#.SPBForms=A3DF1C029E20DF55718F4592EAC7675910534A3DED221E4ED85532ECD3D8DD52B2CC472B683F7222164340FD76B715CCCD3227EA8BCF889F41FE6EF0A6069E403FBE47658F7F3614C5466C6363F5A5103CCCEAE24413BFEAE3360663BB92B93BF6A32686
#AJSTAT_ok_pages=38
#www.jita.me=AJSTAT_ok_times