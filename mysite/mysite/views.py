# -*- coding: UTF-8 -*-
# Create your views here.
import urllib2
from django.http import HttpResponse
from BeautifulSoup import BeautifulSoup
import re
import simplejson
import string
import os
from grabsite import grabdetail
from django.shortcuts import render
import pylibmc

def home(request):
  return  render(request, 'index.html')

mc = pylibmc.Client(["127.0.0.1:12000"], binary=True,
                     behaviors={"tcp_nodelay": True,
                                "ketama": True})

def search(request):
    G = request.GET
    year = int(G.get('year',0))
    mon = int(G.get('month',0))
    if mon > 12 or mon <= 0:
     return HttpResponse("what's the fuck you are doing!")
    
    path = "source/list/chncpa-%d-%d.html" % (year,mon) 
    result = {}
    if mc.get(path) is not None:
      return HttpResponse(mc.get(path),content_type="application/json; charset=utf-8")

    e = os.path.exists(path)
    if not e:
     return HttpResponse("I'm sorry,No performance!")
    with open(path) as file:
     html = file.read()
    soup = BeautifulSoup(''.join(html))
    group_list = []
    
    groups = soup.findAll("table",{ "width":"100%", "border":"0","cellspacing":"0","cellpadding":"0","style":"display:","class":"group"})
    for group in groups:
      days = group.findAll(attrs = {'class':re.compile("^grey_bg4")})
      performances = group.findAll("tr",{"class":"performance"})
      for i in range(len(days)):
        jmxx = {}
        group_list.append(jmxx)
        day = days[i]
        #print day.findAll("span")[1].string
        jmxx['day'] =  day.findAll("span")[1].string
        performance_list = []
        jmxx['jmList'] = performance_list
        for performance in performances:
          p_dic = {}
          performance_list.append(p_dic)
          tds = performance.findAll("td", { "width":"107", "height":"95","align":"center","valign":"top"})
          td = tds[i]
          #print td
          td_href = td.findAll("td", { "align":"left", "valign":"top","class":"line_h18 f12_black1 linkf12_black"})
          time = td.findAll("td", {"height":"20","align":"left","class":"f12_black1"})
          p_dic['href'] = td_href[0].a['href']
          if td_href[0].font is not None:
           p_dic['title'] = td_href[0].font.string
           p_dic['time'] = time[0].findAll("font")[0].string
          else:
           p_dic['title'] = ''
           p_dic['time'] = ''
    result = {};
    result_list = []
    for x in xrange(len(group_list)):
      if group_list[x]['day'] != "&nbsp;":
        result_list.append(group_list[x])
    result['ret'] = 0
    result['data'] = result_list

    mc.set(path,simplejson.dumps(result))

    grabdetail(group_list)
    return HttpResponse(simplejson.dumps(result), content_type="application/json; charset=utf-8")

def detail(request):
    G = request.GET
    path = G.get('path','')
    path = path[11:len(path)]
    path = path.replace('/','-')
    path = "source/detail/%s" % path
    path = path.encode('utf-8')
    result = {}
    if mc.get(path) is not None:
      return HttpResponse(mc.get(path), content_type="application/json; charset=utf-8")

    #print path
    e = os.path.exists(path)
    if not e:
      return HttpResponse("I'm sorry,No performance detail!")
    with open(path) as file:
     html = file.read()
    soup = BeautifulSoup(''.join(html))
    result['ret'] = 0

    #大图
    performanceImage = soup.findAll("img",{ "id":"performanceImage"})
    img = performanceImage[0]
    #print img['src']
    result['performanceImage'] = "http://www.chncpa.org/" + img['src']

    #演出信息
    xwzx_bg = soup.findAll("td", {"width":"755","align":"left","valign":"top","class":"xwzx_bg"})
    width_305 = xwzx_bg[0].findAll("td",{"width":"305","align":"left","valign":"top"})
    align_left = width_305[0].findAll(lambda tag: len(tag.attrs) == 1 and "td",{"align":"left"},)
    trs = align_left[0].findAll("tr")
    info = {}
    result['info'] = info
    tr1 = {}
    tr1['key'] = trs[0].contents[1].string
    tr1['value'] = trs[0].contents[3].string
    info['addr'] = tr1

    tr2 = {}
    tr2['key'] = trs[1].contents[1].string
    tr2['value'] = trs[1].contents[3].span.contents[1].replace('\n','').replace('\t','')
    info['time'] = tr2

    if trs[2].has_key('style') and trs[2]['style'] == "":
      tr3 = {}
      print trs[2]
      tr3['key'] = trs[2].contents[1].string
      tr3['value'] = trs[2].contents[3].string.replace('&nbsp;',' ')
      info['interval'] = tr3

    tr4 = {}
    tr4['key'] = trs[3].contents[1].string
    tr4['value'] = trs[3].contents[3].span.string
    info['price'] = tr4

    #演出介绍、主创、艺术家、演出团体、曲目、剧情、分场演员表、其他图片、视频宣传片、演出回顾
    whlie_bg = soup.findAll("table",{"class":"whlie_bg"})
    tr = whlie_bg[0].findAll('tbody')[0].contents[0]
    alltags = tr.findAll("td",style=True)
    tr1 = whlie_bg[0].findAll('tbody')[0].contents[2]
    alltags1 = tr1.findAll("table",{"width":"720"},style=True)
    contents = []

    for x in xrange(len(alltags)):
      if alltags[x]['style'] == "":
        #print alltags[x].a.string 
        title = alltags[x].a.string.encode('utf-8')
        if title == "演出介绍" or title == "主演" or title == "主创" or title == "剧情" or title == "演出团体" or title == "艺术家" or title == "指挥" or title == "曲目":
          dic = {}
          dic['key'] = alltags[x].a.string
          contents.append(dic)
          str = ''
          ps = alltags1[x].findAll('p')
          for x in xrange(len(ps)):
            p = ps[x]
            for x in xrange(len(p.findAll(text=True))):
              text = p.findAll(text=True)[x].encode('utf-8').replace('\n',"").replace('点击试听','').replace('点击进入','').replace('&nbsp;','')
              str += text
              str += "\n"
          dic['value'] = str
    if len(contents) != 0:
      info['contents'] = contents
    print "no from memcache"
    mc.set(path,simplejson.dumps(result))
    return HttpResponse(simplejson.dumps(result), content_type="application/json; charset=utf-8")














