import re

for j in xrange(1, len(td_num) + 1):
    css_td = '.jzk_newsCenter_meeting > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(' + str(
        j) + ')'
    td = tree.cssselect(css_td)[0]
    td_txt = td.text_content()
    fp.write(td_txt.encode('utf-8') + ' ')
fp.write('时间' + '\n')
for i in xrange(2, len(tr_num) + 1):
    for j in xrange(1, len(td_num) + 1):
        css_td = ' .jzk_newsCenter_meeting > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(' + str(
            i) + ') > td:nth-child(' + str(j) + ')'
        td = tree.cssselect(css_td)[0]
        td_txt = td.text_content()
        fp.write(td_txt.encode('utf-8') + ' ')
    fp.write(str(daily_time[0]) + '\n')

    css_tr = ' table.ke-zeroborder '
    # css_tr = 'table tr' [j]
    d = tree.cssselect(css_tr)[0]
    print d.text_content()

    tr_num = table.find_all('tr')  # 下载下来的表格有多少行
    td_num = tr_num[0].find_all('td')  # 下载下来的表格有多少列
    table = etree.XML(str(table))
    contents = table.xpath("//td")
    csv_writer = csv.writer(fp)
    gold_data = []
    table = etree.XML(str(table))
    contents = table.xpath("//td")
    csv_writer = csv.writer(fp)
    gold_data = []
    for j in xrange(0, len(td_num)):
        #print  contents[j].text
        gold_data.append(contents[j].text.encode('utf-8').strip())
    gold_data.append('时间')
    csv_writer.writerow(gold_data)
    for i in xrange(1, len(tr_num)):
        gold_data = []
        for j in xrange(0, len(td_num)):
            gold_data.append(contents[(i) * len(td_num) + j].text.encode('utf-8').strip())
        gold_data.append(str(daily_time[0]))
        csv_writer.writerow(gold_data)

        gold_data = []
        for j in xrange(0, len(td_num)):
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
