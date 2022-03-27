# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import urllib.error
import multiprocessing
import re
import csv
from bs4 import BeautifulSoup
import lxml.html

def download(url, user_agent='wswp', num_retries=2):  # 对给定的页面进行下载
    print('Downloading:', url)
    headers = {'User-agent': user_agent}
    # request1 = urllib.request(url, headers=headers)
    try:
        html = urllib.request.urlopen(url).read().decode("utf-8")
    except urllib.error as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:  # 下载不成功,则进行两次重试
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # retry 5XX HTTP errors
                html = download(url, user_agent, num_retries - 1)
    return html


def download_daily_deal(daily_deal, file_name):  # 下载每个表格中的数据以及添加时间
    fp = open(file_name, "a")
    csv_writer = csv.writer(fp)
    daily_deal_html = download(daily_deal)
    tree = lxml.html.fromstring(daily_deal_html) #check
    daily_soup = BeautifulSoup(daily_deal_html,'html.parser')
    time = tree.cssselect('.jzk_newsCenter_meeting > div:nth-child(1) > p:nth-child(2) > span:nth-child(2)')[0]
    print(daily_soup.prettify())
    pattern = re.compile('\d+\-\d+\-\d+')
    daily_time = pattern.findall(str(time.text_content().encode('utf-8')))  # 从网页中获得该表的日期
    table = daily_soup.find('table')
    tr_num = table.find_all('tr')  # 下载下来的表格有多少行
    td_num = tr_num[0].find_all('td')  # 下载下来的表格有多少列
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
    gold_data = []
    for j in range(0, len(td_num)):  # 将数据写入txt
        # print  contents[j].text
        gold_data.append(contents[j])
    gold_data.append('时间')
    csv_writer.writerow(gold_data)
    for i in range(1, len(tr_num)):
        gold_data = []
        for j in range(0, len(td_num)):
            gold_data.append(contents[(i) * len(td_num) + j])
        gold_data.append(str(daily_time[0]))
        csv_writer.writerow(gold_data)
    fp.close()


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=4)  # 使用多进程进行网页的爬取
    error_txt = open("/Users/lanqingyuan/Documents/PycharmProjects/scrape_BulkStock/logg/logg.txt", 'w')
    for i in range(1, 2):
        daily_page = 'http://www.sge.com.cn/sjzx/mrhqsj?p=' + str(i)
        try:
            daily_page_html = download(daily_page)
            soup = BeautifulSoup(daily_page_html, 'html.parser')
            div = soup.find('div', attrs={'class': 'articleList border_ea mt30 mb30'})
            ul = div.find('ul')
            li = ul.find_all('li')  # 提取出所需表格具体所在的网页
            for j in range(0, 10):
                attrs = li[j].a.attrs
                daily_deal = "http://www.sge.com.cn" + attrs['href']
                file_name = "/Users/lanqingyuan/Documents/PycharmProjects/scrape_BulkStock/reports/" + str(
                    (i - 1) * 10 + j)
                pool.apply_async(download_daily_deal, (daily_deal, file_name))
        except Exception as e:
            error_txt.write("**********" + "\n")
            error_txt.write(daily_page)
            error_txt.write(str(e))

    pool.close()
    pool.join()
