# coding=utf-8

# 该 py 文件是我们在调用机器学习模型进行垃圾邮件判断时经常需要使用的功能函数集
# 作者：何颖智、黄旭
# 创建日期：2019-8-26
# 最后修改日期：2019-9-8

import re
import jieba
import nltk
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import numpy as np
import model


# 读取指定文件名的文本内容
def readFromFile(filename, encoding_way='utf-8'):
    dataFrame = []
    with open(filename, 'r', encoding=encoding_way) as f:
        for line in f.readlines():
            # print(line)
            dataFrame.append(line)
    return dataFrame


# 对一个中文字符串进行分词、筛选操作
def processChineseSentence(sentence):
    # 获得停用词表
    stopList = readFromFile('./BayesClassifier/Models/中文停用词表.txt', '936')

    cutTextList = []
    # 过滤掉非中文字符
    rule = re.compile(r"[^\u4e00-\u9fa5]")
    sentence = rule.sub("", sentence)
    # 将每封邮件出现的词保存在wordsList中
    textList = list(jieba.cut(sentence))
    # 过滤单个字符
    # textList = [tok for tok in textList if len(tok) >= 2]
    for i in textList:
        if i not in stopList and i.strip() != '' and i != None:
            cutTextList.append(i)

    cutLine = ''
    for word in cutTextList:
        cutLine += word + ' '
    return cutLine


# 对一个英文字符串进行分词、词干化提取、特殊字符过滤
def processEnglish(textData):
    processedData = []
    for line in textData:
        # 过滤特殊字符及数字
        remove_chars = '[0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
        line = re.sub(remove_chars, ' ', str(line))

        # 英文分词操作
        token_words = nltk.word_tokenize(line)
        token_words = [tok for tok in token_words if len(tok) > 2]

        # 添加停用词方法
        stopwordList = stopwords.words('english')
        cleaned_words = [word for word in token_words if word not in stopwordList]

        # 词干提取方法
        lancaster_stemmer = LancasterStemmer()
        words_stemmer = [lancaster_stemmer.stem(word) for word in cleaned_words]

        processedSentence = ""
        for word in words_stemmer:
            processedSentence += word + ' '
        processedData.append(processedSentence)

    return processedData

# 用词向量表示信的内容，用于cnn模型的预处理
def processEnglish2(textData):
    st = PorterStemmer()
    stopwordList = stopwords.words('english')
    # 过滤特殊字符串
    textData = re.sub(r'\d+', '', textData)
    textData = re.sub(r'[a-zA-Z]{20,}', '', textData)
    textData = re.sub(r'<.+>', '', textData)
    textData = re.sub('[_|\.]+', ' ', textData)
    textData = re.sub('[^a-zA-Z]', ' ', textData)
    # 英文分词
    textDatawords = nltk.word_tokenize(textData)
    # 去停词
    clean_words = [st.stem(w) for w in textDatawords if w not in stopwordList]

    # 将单词转化为词向量
    dict = model.vec
    X = np.zeros((200, 100))
    j = 0
    for word in clean_words:
        if word in dict.wv:
            X[j, :] = dict.wv[word]
            j += 1
            if j >= 200:
                break
    return X.reshape(1, 200, 100)

