import datetime
import re
import xlsxwriter
from bs4 import BeautifulSoup

workbook = xlsxwriter.Workbook('process-nytimes.xlsx')

keywords = ['China+cotton', 'Chinese+cotton', 'Xinjiang+cotton']
filenames = ['nytimes-china-cotton.html', 'nytimes-chinese-cotton.html', 'nytimes-xinjiang-cotton.html']

for i in range(3):
    keyword = keywords[i]
    worksheet = workbook.add_worksheet(keyword)

    head = ['关键字', '标题', '链接', '时间']
    worksheet.write_row(0, 0, head)

    date_format = workbook.add_format({'num_format': 'yyyy/mm/dd'})
    worksheet.set_column(0, 0, 20)
    worksheet.set_column(1, 1, 50)
    worksheet.set_column(2, 2, 70)
    worksheet.set_column(3, 3, 20, cell_format=date_format)

    row_index = 1

    with open(filenames[i], 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'lxml')
        nodes = soup.select('.css-e1lvw9 a')
        # print(len(nodes))

        for node in nodes:
            title = node.find('h4').string
            href = node['href'].split('?')[0]

            try:
                if 'article' in href:
                    date_str = node.parent.parent.parent.span.string + ', ' + year
                    date = datetime.datetime.strptime(date_str, '%B %d, %Y')
                else:
                    date_element = re.findall(r'\d+', href)
                    year = date_element[0]
                    date_str = date_element[0] + '/' + date_element[1] + '/' + date_element[2]
                    date = datetime.datetime.strptime(date_str, '%Y/%m/%d')

                if 'http' not in href:
                    href = 'https://www.nytimes.com' + href

                worksheet.write_row(row_index, 0, [keyword, title, href, date])
                row_index += 1
            except:
                pass

workbook.close()
