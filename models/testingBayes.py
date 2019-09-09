import chardet
from joblib import load
import numpy as np
from time import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

if __name__ == '__main__':
    # 导入测试集
    Xt = []
    Ytest = []
    with open('../dataset/smsspamcollection/SMSSpamCollection', 'rb') as fin:
        line = fin.readline()
        while line:
            Ytest.append(line.split(maxsplit=1)[0].decode())
            email = line.split(maxsplit=1)[1]
            encoding = chardet.detect(email)['encoding']
            if encoding is not None:
                email = email.decode(encoding, errors='ignore')
            else:
                email = email.decode('utf8', errors='replace')
            Xt.append(email)
            line = fin.readline()
    v = load('vectorizer.joblib')
    Xtest = v.transform(Xt)
    print(len(Ytest))
    print(v.get_feature_names())

    clf = load('clf.joblib')
    # 测试
    Ypredict = clf.predict(Xtest)
    with open('output.txt', 'w') as out:
        for y in Ypredict:
            out.write(y + '\n')
    print(clf.score(Xtest, Ytest))