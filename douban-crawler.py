from bs4 import BeautifulSoup
import requests
import csv

entries = []
entry = []
urlnumber = 0
maxnum = 300
while urlnumber < 300:

    print type(urlnumber), urlnumber

    url = 'http://movie.douban.com/subject/10574622/comments?start=%d&limit=20&sort=new_score' % urlnumber
    print url

    try:
        r = requests.get(url, timeout=10)
    except Exception, e:
        break

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

    # increase the num so that we can crawler the next page
    urlnumber = urlnumber + 21

with open('douban_zhanlang.csv', 'w') as output:
    writer = csv.writer(output, delimiter=',', lineterminator='\n')
    writer.writerows(entries)
soup.decompose()
print "Wrote to douban_zhanlang.csv"
