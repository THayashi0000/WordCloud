#coding:utf-8
import csv
from janome.tokenizer import Tokenizer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from bs4 import BeautifulSoup
from collections import Counter, defaultdict
import codecs
stoplist=[]
#自分のツイート投稿文章で試みた
input_file='tweet.csv'

with codecs.open('Japanese.txt', 'r', 'utf-8') as f:
    for line in f.readlines():
        stoplist.append(line.rstrip('\r\n'))

#名詞だけ抽出、単語をカウント
def counter(texts):
    t = Tokenizer()
    words_count = defaultdict(int)
    words = []
    for text in texts:
        tokens = t.tokenize(text)
        for token in tokens:
            #品詞から名詞だけ抽出
            pos = token.part_of_speech.split(',')[0]
            if pos == '名詞':
                if token.base_form not in stoplist:
                    words_count[token.base_form] += 1
                    words.append(token.base_form)
    return words_count, words

with open('tweets.csv','r', encoding='utf-8_sig') as f:
    reader = csv.reader(f, delimiter='\t')
    texts = []
    for row in reader:
        #print(row)

        if len(row) > 0:
            if "@" in row[0]:
                continue
            if "RT" in row[0]:
                continue
            text = row[0].split("http")
            texts.append(text[0])

words_count, words = counter(texts)
text = ' '.join(words)
#word cloud
fpath = "~/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc" #MacPCの場合
#fpath = "C:/Windows/Fonts/HGRGM.TTC" #Windowsの場合
wordcloud = WordCloud(background_color="white", font_path=fpath, width=900, height=500).generate(text)
#wordcloud.generate(" ".join(text).decode('utf-8'))
wordcloud.to_file(input_file[:-4]+".wordcloud.png")

#今回は図示するためではないので以下は使用せず
"""
plt.figure(figsize=(15,12))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
"""
