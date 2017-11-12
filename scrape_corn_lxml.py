# -*- coding: utf-8 -*-
import urllib2
import threading
import  datetime
import multiprocessing
import re
import csv
from bs4 import BeautifulSoup
import lxml.html
from lxml import etree
import xml.etree.ElementTree as ET
def download(url, user_agent='wswp', num_retries=2): #对给定的页面进行下载
    print 'Downloading:', url
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0: #下载不成功,则进行两次重试
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # retry 5XX HTTP errors
                html = download(url, user_agent, num_retries-1)
    return html

def download_produce_deal(daily_deal,file_name):  #下载每个表格中的数据以及添加时间
    fp = open(file_name, "a")
    csv_writer = csv.writer(fp)
    daily_deal_html = download(daily_deal)
    tree =lxml.html.fromstring(daily_deal_html)
    daily_soup = BeautifulSoup(daily_deal_html, 'html.parser')
    table = daily_soup.find('table')
    tr_num = table.find_all('tr')  # 下载下来的表格有多少行
    td_num = tr_num[1].find_all('td')  # 下载下来的表格有多少列
    #print table
    ##print table
    contents = []
    for child in tree.iter(tag='td'):  # 将表格中的数据写入contents
        content = ''
        for td_child in child.iter(tag=None):
            try:
                content = content + td_child.text.encode("utf-8").strip()
            except Exception as e:
                pass
        contents.append(content)
    #print len(contents)
    for i in xrange(0, len(tr_num)-1):
        corn_data = []
        for j in xrange(0, 4):
            corn_data.append(contents[(i) * len(td_num) + j])
        csv_writer.writerow(corn_data)

    fp.close()





if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=4)   #使用多进程进行网页的爬取
    par_craft_index = 13079
    craft_index = 13233
    for year in xrange(2014,2018): #爬取的年份
        for mounth in xrange(1,4): #爬取的季度
            if mounth ==1:
                produce_deal ='http://nc.mofcom.gov.cn/channel/gxdj/jghq/jg_list.shtml?par_craft_index='+str(par_craft_index)+'&craft_index='+str(craft_index)+'&startTime='+str(year)+'-01-01&endTime='+str(year)+'-03-31&par_p_index=&p_index=&keyword='
            elif mounth == 2:
                produce_deal = 'http://nc.mofcom.gov.cn/channel/gxdj/jghq/jg_list.shtml?par_craft_index='+str(par_craft_index)+'&craft_index='+str(craft_index)+'&startTime=' + str(
                    year) + '-04-01&endTime=' + str(year) + '-06-30&par_p_index=&p_index=&keyword='
            elif mounth == 3:
                produce_deal = 'http://nc.mofcom.gov.cn/channel/gxdj/jghq/jg_list.shtml?par_craft_index='+str(par_craft_index)+'&craft_index='+str(craft_index)+'&startTime=' + str(
                    year) + '-07-01&endTime=' + str(year) + '-09-30&par_p_index=&p_index=&keyword='
            else:
                produce_deal = 'http://nc.mofcom.gov.cn/channel/gxdj/jghq/jg_list.shtml?par_craft_index='+str(par_craft_index)+'&craft_index='+str(craft_index)+'&startTime=' + str(
                    year) + '-10-01&endTime=' + str(year) + '-12-31&par_p_index=&p_index=&keyword='
            produce_deal_html = download(produce_deal)
            tree = lxml.html.fromstring(produce_deal_html)
            page = tree.cssselect('.pmCon > script:nth-child(2)')[0]
            pattern = re.compile('\d+')
            produce_page = pattern.findall(page.text_content())
            page_sum = int(produce_page[0]) + 1
            for page_num in xrange(1, page_sum):#爬取数据所在的页
                file_name = "/home/yutuo/data/produce/zhurou/" + str(year)+'-'+str(mounth)+'-'+str(page_num)
                produce_deal_page = produce_deal + '&page=' + str(page_num)
                try:
                    pool.apply_async(download_produce_deal, (produce_deal_page, file_name))
                except Exception as e:
                    print e


    pool.close()
    pool.join()