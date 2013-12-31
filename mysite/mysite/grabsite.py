import urllib2
from django.http import HttpResponse
from BeautifulSoup import BeautifulSoup
import re
import simplejson
import string
import os
from selenium import webdriver

def grablist(reqest):
    driver = webdriver.PhantomJS()
    year = 2014
    for i in range(12):
     url = "http://www.chncpa.org/module/rili/index.jsp?year=%d&month=%d&doflag=1&static=yes" % (year,i)
     driver.get(url)
     html = driver.page_source
     path = "source/list/chncpa-%d-%d.html" % (year,i+1) 
     with open(path, 'w') as f:
      f.write(html.encode("utf8"))
    #soup = BeautifulSoup(''.join(html))
    driver.quit()
    return HttpResponse("got the list html!!")

def grabdetail(urls):
    driver = webdriver.PhantomJS()
    for x in xrange(len(urls)):
        jmList = urls[x]['jmList']
        for x in xrange(len(jmList)):
            time = jmList[x]['time']
            title = jmList[x]['title']
            if len(time) != 0 and len(title) != 0:
                href = jmList[x]['href']
                tempPath = href[11:len(href)]
                tempPath = tempPath.replace('/','-')
                #print tempPath
                path = "source/detail/%s" % tempPath 
                #print path
                e = os.path.exists(path)
                if not e:
                    driver.get("http://www.chncpa.org" + href)
                    html = driver.page_source
                    with open(path, 'w') as f:
                        f.write(html.encode("utf8"))

    driver.quit()





