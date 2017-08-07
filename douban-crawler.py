from bs4 import BeautifulSoup
import requests
import csv
import time

cookie_str = 'xxx'

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

print "Wrote to douban_zhanlang.csv"
