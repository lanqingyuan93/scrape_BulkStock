# -*- coding: utf-8 -*-
import urllib2
import urlparse
import builtwith
import re
from bs4 import BeautifulSoup
import lxml.html
def download(url, user_agent='wswp', num_retries=2): #对给定的页面进行下载
    print 'Downloading:', url
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    try:
        html = urllib2.urlopen(request).read().decode("utf-8")
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0: #下载不成功,则进行两次重试
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # retry 5XX HTTP errors
                html = download(url, user_agent, num_retries-1)
    return html

def download_daily_deal(daily_deal,file_name):  #下载每个表格中的数据以及添加时间
    fp = open(file_name, "w")
    daily_deal_html = download(daily_deal)
    daily_soup = BeautifulSoup(daily_deal_html, 'html.parser')
    title = daily_soup.find('div', attrs={'class': 'jzk_newsCenter_meeting pl30 pr30 pb30'})
    title = title.find('div', attrs={'class': 'title'})
    time = title.find_all('span')
    pattern = re.compile('\d+\-\d+\-\d+')
    daily_time = pattern.findall(str(time[1]))
    table = daily_soup.find('table')
    tr = table.find_all('tr')
    td = tr[0].find_all('td')
    for j in xrange(0, len(td)):  #将爬取的表格写入文本文档
        print str(td[j].p)


if __name__ == '__main__':
    for i in xrange(195,196):
        daily_page ='http://www.sge.com.cn/sjzx/mrhqsj?p='+str(i)
        daily_page_html = download(daily_page)
        soup = BeautifulSoup(daily_page_html, 'html.parser')
        div = soup.find('div', attrs={'class': 'articleList border_ea mt30 mb30'})
        ul = div.find('ul')
        li = ul.find_all('li')
        for j in xrange(0,1):
            attrs = li[j].a.attrs
            daily_deal = "http://www.sge.com.cn" + attrs['href']
            file_name ="/home/yutuo/data/gold/"+str((i-1)*10+j)
            download_daily_deal(daily_deal,file_name)
