#!/usr/bin/env python
import urllib2
from HTMLParser import HTMLParser
import re
import os

#fetch task url
#http://www.gtp.cn/gtp/htm/A-Z/A.htm
#list link url
#http://www.gtp.cn/gtp/htm/gtp_a10_more/gtp_a1_1.htm
#download link url,return the encoding file url and name
#http://www.gtp.cn/gtp/asp/list.asp?id=JOGQEQCPN0&action=end&key=http://www.gtp.cn/gtp/asp/play.asp?id=JOGQEQCPN0
#download url
#http://down.gtp.cn/file/2007/10/2007101857340.rar

#config
task_dir='task/'
gtp_dir='gtp/'
proxy_address = '127.0.0.1:8087'


#return a string by the url
def getHtml(url, code, proxy=False):
    try:
	    return urllib2.urlopen(url).read().decode(code).encode('UTF-8')
    except urllib2.HTTPError, e:
        print e.code

def setProxy(address):
    proxy = urllib2.ProxyHandler({'http':address})
    urllib2.install_opener(urllib2.build_opener(proxy))

#return the real download url
def genDownloadURl(url_id):
    template='http://www.gtp.cn/gtp/asp/list.asp?{0}&action=end&key=http://www.gtp.cn/gtp/asp/play.asp?{1}'.format(url_id, url_id)
    page = getHtml(template, 'GBK')
    result = ''
    pt = re.compile(r'(?<=gtpcn\(\')([^\']+)')
    m = pt.search(page)
    if m:
        result = m.group(1)
    if result:
        result = 'http://down.gtp.cn/{0}'.format(decode_gtp(result))
    return result

#save file
def saveFile(url, filename, path):
    if not os.path.exists(path+filename):
        dist = open(path+filename, 'w')
        try:
            dist.write(urllib2.urlopen(url).read())
            print 'logger info save file success  '+path + filename
        except BaseException:
            print 'logger info save file error  '+path + filename
        finally:
            dist.close()
    else:
        print "logger info file " + path+filename +" is exists"
#decode the url
#RMXGERLNLNQIXGYILNXGERLNLNQIYILNYIBAWUQISNSILNXD
def decode_gtp(gtp):
    gtp = gtp.replace('XG', '/')
    gtp = gtp.replace('YI', '1')
    gtp = gtp.replace('ER', '2')
    gtp = gtp.replace('SN', '3')
    gtp = gtp.replace('SI', '4')
    gtp = gtp.replace('WU', '5')
    gtp = gtp.replace('LU', '6')
    gtp = gtp.replace('QI', '7')
    gtp = gtp.replace('BA', '8')
    gtp = gtp.replace('JU', '9')
    gtp = gtp.replace('LN', '0')
    gtp = gtp.replace('XD', '.rar')
    gtp = gtp.replace('RM', 'file')
    return gtp

#parse and handle a html string
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

def getHrefList(url, encoding='UTF-8'):
    page = getHtml(url,encoding)
    parser = IndexParser()
    if page:
        parser.url_value=[]
        parser.feed(page)
    return parser.getUrl()

def generateTask():
    for ch in range(65, 91):
        letter = chr(ch)
        if not os.path.exists(task_dir+letter):
            writeTask(letter)

def writeTask(letter):
    url_template = 'http://www.gtp.cn/gtp/htm/A-Z/{0}.htm'
    lst=getHrefList(url_template.format(letter), 'GBK')
    task_file = open(task_dir+letter, 'w')
    for item in lst:
        if item:
            url = str(item[0])
            if url.__contains__('Music_Singer_List'):
                url = url.replace('../../', '')
                task_file.write(url+'\t'+item[1]+'\n')
    task_file.close()

#handle logic
def handlePageList():
    for ch in range(65, 91):
        letter = chr(ch)
        taskFile = open(task_dir+letter, 'r')
        for line in taskFile:
            line = line[:-1]
            arr = line.split('\t')
            directory = "{0}{1}/{2}/".format(gtp_dir,letter,arr[1])
            if not os.path.exists(directory):
                os.makedirs(directory)
            #not taking care of paging , if pageSize>30 then generate a new url by add 1
            pageList = getHrefList('http://www.gtp.cn/gtp/{0}'.format(arr[0]), 'GBK')
            for item in pageList:
                link = str(item[0])
                if link and link.__contains__('id='):
                    link_Id = link.split("?")[1]
                    download = genDownloadURl(link_Id)
                    saveFile(download,item[1]+'.rar',directory)

def main():
    setProxy(proxy_address)
    generateTask()
    handlePageList()

if __name__=='__main__':main()
