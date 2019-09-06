import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import chardet

sw = stopwords.words('english')
sw.append('I')
punctuations = ",.:;?()![]{}@#$%^&*-=+"
with open('../dataset/trec06p/data/000/007', 'rb') as f:
    email = f.read()
    email = email.decode(chardet.detect(email)['encoding'])
    print(email)
    words = word_tokenize(email)

# clean_words1 = [word for word in words if word not in sw and word not in punctuations]
# print(clean_words1)

# freq = nltk.FreqDist(words)
# dic = freq.items()
# for key, val in freq.items():
#     print(str(key) + ':' + str(val))

