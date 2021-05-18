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

params = {}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Referer': 'https://www.bbc.com/',
}

workbook = xlsxwriter.Workbook('crawl-bbc.xlsx')
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

    params['q'] = keyword
    pageNum = 1
    flag = True

    while flag:
        params['page'] = pageNum
        response = requests.get('https://www.bbc.co.uk/search',
                                params=params, headers=headers, proxies=proxies)
        print(response.url)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        html_str = response.text
        soup = BeautifulSoup(html_str, 'lxml')
        nodes = soup.select('.ssrcss-som5se-PromoContent.e1f5wbog7')
        print(len(nodes))

        for node in nodes:
            # print(node)
            a_node = node.select_one('.ssrcss-rjdkox-Stack.e1y4nx260 a')
            title = a_node.select_one('span p span').string
            # print(title)
            href = a_node['href']
            # print(href)

            span_node = node.select_one('.ssrcss-8g95ls-MetadataSnippet.ecn1o5v2')
            span_node.span.clear()
            date_str = span_node.get_text()
            try:
                date = datetime.datetime.strptime(date_str, '%d %B %Y')
            except:
                date_str += ' ' + str(datetime.datetime.now().year)
                date = datetime.datetime.strptime(date_str, '%d %B %Y')
            worksheet.write_row(row_index, 0, [keyword, title, href, date])
            row_index += 1

        pages = soup.select('.ssrcss-a11ok4-ArrowPageButtonContainer.ep93jpm1')
        # print(pages)
        next_btn = pages[len(pages) - 1].select_one('a')
        flag = next_btn is not None
        pageNum += 1

workbook.close()
