"""
简介：根据数据集训练一个word2vec模型，词向量嵌入
作者：黄旭
创建时间：2019年8月29日
最后修改时间：2019年8月30日
"""

from gensim.models import Word2Vec
from time import time
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import chardet
import re

if __name__ == '__main__':
    # 预处理数据集
    t0 = time()
    s = stopwords.words('english')
    punctuations = r',.:;?()![]{}<>@#$%^&*\'-=+\/"‘’“”~·：；——…！@￥'
    sw = s + ['tr', 'html', 'td', 'font', 'title', 'smtp', 'from', 'to', 'div', 'localhost', 'mime', 'charset', 'meta',
              'doctype', 'encoding', 'nbsp', 'href', 'color', 'format', 'content', 'jp', 'iso', 'psy', 'px', 'psych',
              'style', 'nextpart', 'size', 'date', 'type', 'text', 'php', ''] + [s for s in punctuations]
    sw = frozenset(sw)
    with open('../dataset/trec06p/spam50/index2') as f:
        indices = f.readlines()
    Ytrain = []
    path = []
    for i in indices:
        index = i.split()
        Ytrain.append(index[0])
        path.append((index[1]))

    n = len(Ytrain)
    features = 5000
    st = PorterStemmer()
    emails = []
    maxlength = 0
    avglength = 0
    for i in range(n):
        # index = str(i).zfill(3)
        # print('open: ../dataset/trec06p' + path[i][2:])
        with open('../dataset/trec06p' + path[i][2:], 'rb') as f:
            emaillines = f.readlines()
        email = b''
        textPlain = False
        for line in emaillines:
            if textPlain:
                email += line
            if line == b'\n':
                textPlain = True
        encoding = chardet.detect(email)['encoding']
        if encoding is not None:
            email = email.decode(encoding, errors='ignore').lower()
        else:
            email = email.decode('utf8', errors='replace').lower()
        # if path[i] == '../data/007/071':
        #     print(email)
        email = re.sub(r'\d+', '', email)
        email = re.sub(r'[a-zA-Z]{20,}', '', email)
        email = re.sub(r'<.+>', '', email)
        email = re.sub('_|\.', ' ', email)
        email = re.sub('[^a-zA-Z]', ' ', email)
        emailwords = word_tokenize(email)
        clean_words = [st.stem(w) for w in emailwords if w not in sw]
        emails.append(clean_words)
        avglength += len(clean_words)
        if maxlength < len(clean_words):
            maxlength = len(clean_words)
    load_time = time() - t0
    print('load time: %0.3fs' % load_time)
    print(maxlength)
    avglength /= n
    print(avglength)
    print(n)

    # 构建和训练模型
    t0 = time()
    word2vec_model = Word2Vec(emails, size=100, window=5, max_final_vocab=features,
                              sg=1, negative=10, min_count=10, workers=4)
    vec_time = time() - t0
    print('vector time: %0.3fs' % vec_time)
    # 保存模型
    word2vec_model.save('word2vec.model')
    print(len(word2vec_model.wv.vocab))