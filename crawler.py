import logging
import re

import requests
from bs4 import BeautifulSoup


URL_TMPL = 'https://www.zero-emi-points.jp/shop-search/list?search_action=municipality_search&tokyo_wards=on&ward%5B0%5D=1&ward%5B1%5D=2&ward%5B2%5D=3&ward%5B3%5D=4&ward%5B4%5D=5&ward%5B5%5D=6&ward%5B6%5D=7&ward%5B7%5D=8&ward%5B8%5D=9&ward%5B9%5D=10&ward%5B10%5D=11&ward%5B11%5D=12&ward%5B12%5D=13&ward%5B13%5D=14&ward%5B14%5D=15&ward%5B15%5D=16&ward%5B16%5D=17&ward%5B17%5D=18&ward%5B18%5D=19&ward%5B19%5D=20&ward%5B20%5D=21&ward%5B21%5D=22&ward%5B22%5D=23&tokyo_cities=on&city%5B0%5D=24&city%5B1%5D=25&city%5B2%5D=26&city%5B3%5D=27&city%5B4%5D=28&city%5B5%5D=29&city%5B6%5D=30&city%5B7%5D=31&city%5B8%5D=32&city%5B9%5D=33&city%5B10%5D=34&city%5B11%5D=35&city%5B12%5D=36&city%5B13%5D=37&city%5B14%5D=38&city%5B15%5D=39&city%5B16%5D=40&city%5B17%5D=41&city%5B18%5D=42&city%5B19%5D=43&city%5B20%5D=44&city%5B21%5D=45&city%5B22%5D=46&city%5B23%5D=47&city%5B24%5D=48&city%5B25%5D=49&city%5B26%5D=50&city%5B27%5D=51&city%5B28%5D=52&city%5B29%5D=53&city%5B30%5D=54&city%5B31%5D=55&city%5B32%5D=56&city%5B33%5D=57&city%5B34%5D=58&city%5B35%5D=59&city%5B36%5D=60&city%5B37%5D=61&city%5B38%5D=62&ajax=true&per_page={offset}'

ROW_PER_PAGE = 30

log = logging.getLogger(__name__)


def _parse(html):
    bs = BeautifulSoup(html, 'html.parser')
    num_results = int(re.match(
        '検索結果\u3000(\\d+)件', bs.select_one('#search_result').text
        ).group(1))
    shops = [
        {
            'name': row.contents[1].text,
            'address': row.contents[3].text,
            'tel': row.contents[5].text,
        }
        for row in bs.select('tbody > tr')
    ]
    return num_results, shops


def shop_list():
    s = requests.Session()
    try:
        resp = s.get(URL_TMPL.format(offset=0))
        num_results, all_shops = _parse(resp.content)
    except:
        log.exception('failed to fetch/parse page at offset 0')
        raise
    log.info('%s entries in total', num_results)

    for offset in range(ROW_PER_PAGE, num_results, ROW_PER_PAGE):
        try:
            resp = s.get(URL_TMPL.format(offset=offset))
            _, shops = _parse(resp.content)
        except:
            log.exception('failed to fetch/parse page at offset %s, ignoring',
                          offset)
            continue
        all_shops.extend(shops)

    return all_shops


if __name__ == '__main__':
    print(shop_list())
