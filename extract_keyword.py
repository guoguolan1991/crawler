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
    #print tag

from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import ch
ch.set_ch()

d = path.dirname(__file__)

alice_coloring = imread(path.join(d, "data/timg.png"))

wc = WordCloud(background_color="white",
mask=alice_coloring,
max_font_size=40,
font_path='C:/Windows/fonts/STFANGSO.TTF',
random_state=42)
#wc.generate(text)
items = {}
for tag in tags:
    items[tag[0]] = tag[1]

wc.generate_from_frequencies(items)
image_colors = ImageColorGenerator(alice_coloring)

plt.imshow(wc)
plt.axis("off")
plt.figure()
# recolor wordcloud and show
# we could also give color_func=image_colors directly in the constructor
plt.imshow(wc.recolor(color_func=image_colors))
plt.axis("off")
plt.figure()
plt.imshow(alice_coloring, cmap=plt.cm.gray)
plt.axis("off")
plt.show()
wc.to_file(path.join(d, "zhanlang2.png"))