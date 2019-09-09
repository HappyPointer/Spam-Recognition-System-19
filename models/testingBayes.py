import chardet
from joblib import load
import numpy as np
from time import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

if __name__ == '__main__':
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
    t = np.zeros((1, 5000))
    print(clf.predict_proba(t))

    Ypredict = clf.predict(Xtest)
    with open('output.txt', 'w') as out:
        for y in Ypredict:
            out.write(y + '\n')
    print(clf.score(Xtest, Ytest))

    # arg = ''
    # arg = 'Get you free iphone product only for today! Learn more at www.arizona.com. A surprising discount. Be ready!!!'
    # arg = 'Dear Doctor franks, I am planning to apply for a mater degree in USC, will you be happy to write me a recommendation?'
    # arg = 'Hello, I am He Yingzhi. We have met before. I would like to invite you to dinner and get together. It is in the old place. 8.30 p.m. tonight. '
    # arg = 'Hi there,Join Elasticsearch experts for upcoming in-person and virtual events:•Elasticsearch Official ' \
    #       'Training•Video:Tips & best practices for upgrading your Elastic Stack to 7.x•Video: Deploying monitoring for ' \
    #       'the Elastic StackIf you have colleagues who might be interested in these topics, feel free to forward this invite. '

    arg = 'Academic Qualifications available from prestigious NON-ACC REDITED uni versities.' \
          'Do you have the knowledge and the experience but lack the qualifications?' \
          'Are you getting turned down time and time again for the job of your dreams because you just don\'t have the right letters after your name?' \
          'Get the prestige that you deserve today!Move ahead in your career today!' \
          'CALL 1-206-666-5510' \
          'Bachelors, Mas ters and Ph D\'s available in your field!' \
          'No examinations! No classes! No textbooks!' \
          'Call to register and receive your qual ifications within days!24 hours a day 7 days a week!' \
          'Confidentiality assured!1-206-666-5510'
    t0 = time()
    Xtest = v.transform([arg])
    print(clf.predict(Xtest))
    test_time = time() - t0
    print('test time:%0.3fs' % test_time)