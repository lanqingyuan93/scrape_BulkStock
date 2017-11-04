# -*- coding: utf-8 -*-
import urllib2
import urlparse
import builtwith
import re
import csv
import json
import demjson
from bs4 import BeautifulSoup
import lxml.html
from lxml import etree
import xml.etree.ElementTree as ET
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
    fp = open(file_name, "a")
    csv_writer = csv.writer(fp)
    daily_deal_html = download(daily_deal)
    tree =lxml.html.fromstring(daily_deal_html)
    daily_soup = BeautifulSoup(daily_deal_html, 'html.parser')
    time =tree.cssselect('.jzk_newsCenter_meeting > div:nth-child(1) > p:nth-child(2) > span:nth-child(2)')[0]
    pattern = re.compile('\d+\-\d+\-\d+')
    daily_time = pattern.findall(str(time.text_content().encode('utf-8'))) #从网页中获得该表的日期
    table = daily_soup.find('table')
    tr_num = table.find_all('tr')  # 下载下来的表格有多少行
    td_num = tr_num[0].find_all('td')  # 下载下来的表格有多少列
    #print table
    ##print table
    contents =[]
    for child in tree.iter(tag='td'):  #将表格中的数据写入contents
        content =''
        for td_child in child.iter(tag=None):
            try:
                content = content + td_child.text.encode("utf-8").strip()
            except Exception as e:
                pass
        contents.append(content)
    gold_data = []
    for j in xrange(0, len(td_num)):  #将数据写入txt
        # print  contents[j].text
        gold_data.append(contents[j])
    gold_data.append('时间')
    csv_writer.writerow(gold_data)
    for i in xrange(1, len(tr_num)):
        gold_data = []
        for j in xrange(0, len(td_num)):
            gold_data.append(contents[(i) * len(td_num) + j])
        gold_data.append(str(daily_time[0]))
        csv_writer.writerow(gold_data)





    fp.close()





if __name__ == '__main__':
    for i in xrange(170,171):
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