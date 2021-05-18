import datetime

import requests
import xlsxwriter
from bs4 import BeautifulSoup

proxy = '127.0.0.1:1080'
proxies = {
    'http': proxy,
    'https': proxy
}

keywords = ['China cotton', 'Chinese cotton', 'Xinjiang cotton']

params = {
    'siteName': 'english',
    'dateFlag': 'true',
    'a': 1,
    'b': 1,
    'c': 2010,
    'd': 10,
    'e': 5,
    'f': 2021,
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Referer': 'http://en.people.cn/',
}

workbook = xlsxwriter.Workbook('crawl-people-daily.xlsx')
head = ['关键字', '标题', '链接', '时间']

for keyword in keywords:
    worksheet = workbook.add_worksheet(keyword)
    worksheet.write_row(0, 0, head)

    date_format = workbook.add_format({'num_format': 'yyyy/mm/dd'})
    worksheet.set_column(0, 0, 20)
    worksheet.set_column(1, 1, 80)
    worksheet.set_column(2, 2, 55)
    worksheet.set_column(3, 3, 15, cell_format=date_format)

    row_index = 1

    params['keyword'] = keyword
    pageNum = 1
    flag = True

    while flag:
        params['pageNum'] = pageNum
        response = requests.get('http://search.people.com.cn/language/search.do',
                                params=params, headers=headers, proxies=proxies)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        html_str = response.text
        soup = BeautifulSoup(html_str, 'lxml')
        uls = soup.select('.clear ul')
        # print(len(uls))

        for ul in uls:
            a_tag = ul.find('a')
            if a_tag.font is not None:
                font_str = a_tag.font.string
                a_tag.font.replace_with(font_str)
            title = a_tag.get_text()
            if title[0] == '[':
                title = title[1:len(title) - 1]
            href = a_tag['href']
            print(href)
            start_index = 31
            if 'business' in href:
                start_index += 9
            if 'n3' in href:
                start_index += 1
            date_str = href[start_index:start_index + 9]
            date = datetime.datetime.strptime(date_str, '%Y/%m%d')

            worksheet.write_row(row_index, 0, [keyword, title, href, date])
            row_index += 1

        pages = soup.select('.one .wb_18 a')
        flag = 'Next' in pages[len(pages) - 1].string
        pageNum += 1

workbook.close()
