from bs4 import BeautifulSoup
import requests
import csv
import time

cookie_str = 'll="118172"; bid=Z7-HMUKg_b0; __yadk_uid=edxjMbtj4qHVi65LkRStDygY3RDveMjR; gr_user_id=7ab58ce7-ef8f-' \
          '4c68-8dc5-55e4adfc17b2; viewed="26437066_24746415"; _vwo_uuid_v2=FA170A79A6002694A14F6CDFD2448E90|ac5' \
          '94ea245d6b1b86370c68c221cc6c7; ps=y; __utma=30149280.424130412.1495097078.1501725941.1501727857.17; ' \
          '__utmc=30149280; __utmz=30149280.1501676452.14.10.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=' \
          '223695111.1788628307.1495097078.1501725941.1501727857.12; __utmc=223695111; __utmz=223695111.1500599003.7.6.utmcsr' \
          '=baidu|utmccn=(organic)|utmcmd=organic; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1501738005%2C%22https%3A%2F%2Fwww.' \
          'douban.com%2Fsearch%3Fq%3D%25E6%2588%2598%25E7%258B%25BC2%22%5D; ap=1; ue="eefebctx@163.com"; dbcl2="51865548:' \
          'nc/zoMK1iVY"; ck=sajL; _pk_id.100001.4cf6=61796773fef32702.1495097078.15.1501739681.1501728771.; ' \
          '_pk_ses.100001.4cf6=*; push_noty_num=0; push_doumail_num=0'

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/44.0.2403.157 Safari/537.36'}

cookies = {}
lists = cookie_str.split(';')

for item in lists:
    name, value = item.strip().split('=', 1)
    cookies[name] = value


urlnumber = 0
maxnum = 75820


def get_entries(urlnumber):

    entries = []
    entry = []
    print type(urlnumber), urlnumber

    url = 'http://movie.douban.com/subject/26363254/comments?start=%d&limit=20&sort=new_score' % urlnumber
    print url

    try:
        r = requests.get(url, cookies=cookies, timeout=10)
    except Exception, e:
        print 'error'

    data = r.text

    soup = BeautifulSoup(data)
    for div in soup.find_all('div'):
        entry = []
        if div.get('class') is not None and div.get('class')[0] == 'comment':
            ps = div.find_all('p')
            aas = div.find_all('a')
            spans = div.find_all('span')

            # Name
            concat_str = ''
            for a in aas:
                if a.get('class') is not None and a.get('class')[0] == '':
                    for str in a.contents:
                        if str != "<br>" or str != "<br/>":
                            concat_str = (concat_str + ' ' + str.encode('utf-8')).strip()
                    entry.append(concat_str)

                    rate = a.next_sibling.next_sibling.next_sibling.next_sibling
                    star = rate['class'][0]

                    entry.append(star.replace("allstar", ""))

            # Time
            concat_str = ''
            for time in spans:
                if time.get('class') is not None and time.get('class')[0] == '':
                    for str in time.contents:
                        if str != "<br>" or str != "<br/>":
                            concat_str = (concat_str + ' ' + str.encode('utf-8')).strip()
                    entry.append(concat_str)

            # Usefulness
            concat_str = ''
            usefulness = div.find_all("span", "votes")[0]
            for str in usefulness.contents:
                concat_str = (concat_str + ' ' + str.encode('utf-8')).strip()
            entry.append(concat_str)

            # Comment
            concat_str = ''
            for str in ps[0].strings:
                if str != "<br>" or str != "<br/>":
                    concat_str = (concat_str + ' ' + str.encode('utf-8')).strip()
            entry.append(concat_str)

            entries.append(entry)
    return entries
    # increase the num so that we can crawler the next page


with open('douban_zhanlang.csv', 'w') as output:
    writer = csv.writer(output, delimiter=',', lineterminator='\n')
    entries = []
    while urlnumber < maxnum:
        time.sleep(0.4)
        entries.extend(get_entries(urlnumber))
        urlnumber = urlnumber + 21
        if len(entries) % 100 == 0:
            writer.writerows(entries)
            print entries
            entries = []
    writer.writerows(entries)

# soup.decompose()
print "Wrote to douban_zhanlang.csv"
