import nltk
import numpy as np
from time import time
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from nltk.tokenize import word_tokenize
import chardet
from joblib import dump

t0 = time()
s = stopwords.words('english')
punctuations = r',.:;?()![]{}<>@#$%^&*\'-=+\/"‘’“”~·：；'
sw = s + ['tr', 'html', 'td', 'font', 'title', 'smtp', 'from', 'to', 'div', 'localhost', 'mime', 'charset', 'meta',
          'doctype', 'encoding', 'nbsp', 'href', 'color', 'format', 'content', 'jp', 'iso', 'psy', 'px', 'psych',
          'style', 'nextpart', 'size', 'date', 'type', 'text', 'php', ''] + [s for s in punctuations]
sw = frozenset(sw)
with open('../dataset/trec06p/spam50/index') as f:
    indices = f.readlines()
Ytrain = []
path = []
for i in indices:
    index = i.split()
    Ytrain.append(index[0])
    path.append((index[1]))

n = len(Ytrain)
features = 5000
emails = []
vectorizer = TfidfVectorizer(decode_error='ignore', stop_words=sw, max_features=features)
for i in range(n):
    # index = str(i).zfill(3)
    # print('open: ../dataset/trec06p' + path[i][2:])
    with open('../dataset/trec06p' + path[i][2:], 'rb') as f:
        email = f.read()
        encoding = chardet.detect(email)['encoding']
        if encoding is not None:
            email = email.decode(encoding, errors='ignore')
        else:
            email = email.decode('utf8', errors='replace')
        # if path[i] == '../data/007/071':
        #     print(email)
        email = re.sub(r'\d+', '', email)
        email = re.sub(r'[a-zA-Z]{20,}', '', email)
        email = re.sub(r'<.+>', '', email)
        email = re.sub('_', ' ', email)
        emails.append(email)
load_time = time() - t0
print('load time: %0.3fs' % load_time)

t0 = time()
X = vectorizer.fit_transform(emails)
print(vectorizer.get_feature_names())
print(len(vectorizer.get_feature_names()))
Xtrain = X.toarray()
vector_time = time() - t0
print('vectoring time: %0.3fs' % vector_time)
print(Xtrain)
dump(vectorizer, 'vectorizer.joblib')
dump(Xtrain, 'Xtrain.joblib')

t0 = time()
clf1 = MultinomialNB()
clf1.fit(Xtrain, Ytrain)
train_time = time() - t0
print('train time: %0.3fs' % train_time)
dump(clf1, 'clf.joblib')

