import sys

import requests
from bs4 import BeautifulSoup

proxy = '127.0.0.1:1080'
proxies = {
    'http': proxy,
    'https': proxy
}

keywords = ['China cotton', 'Chinese cotton', 'Xinjiang cotton']

start_date = '20110101'
end_date = '20210510'

get_params = {
    'startDate': start_date,
    'endDate': end_date,
    'sort': 'newest',
}

get_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Referer': 'https://www.nytimes.com/',
}

for keyword in keywords:
    try:
        get_params['query'] = keyword
        response = requests.get('https://www.nytimes.com/search',
                                params=get_params, headers=get_headers, proxies=proxies)
        print(response.url)
        # response = requests.post('https://samizdat-graphql.nytimes.com/graphql/v2',
        #                          json=payload_data,
        #                          headers=payload_header,
        #                          proxies=proxies)
        print(response.status_code)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        html_str = response.text
        soup = BeautifulSoup(html_str, 'lxml')
        s = soup.select('.css-e1lvw9 p')
        print(len(s))
    except Exception as e:
        e.with_traceback(sys.exc_info()[2])
