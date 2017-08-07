import jieba.analyse
import csv

content = ''
count = 0
csv_reader = csv.reader(open('data/douban_zhanlang.csv', 'rU'), dialect='excel')
for row in csv_reader:
    if len(row) == 4:
        content += row[3]
        count += 1

jieba.analyse.set_stop_words('data/stopword.txt')
tags = jieba.analyse.extract_tags(content, topK=100, withWeight=True)

print count

for tag in tags:
    print tag[0], tag[1]