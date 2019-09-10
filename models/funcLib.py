# coding=utf-8

# 该 py 文件是一个训练机器学习模型过程中使用的自定义函数集，在机器学习的代码中我们可能使用到这些函数
# 作者：何颖智
# 创建日期：2019-8-21
# 最后修改时间：2019-8-28

import os
import re
import jieba
import nltk
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
import chardet
import pandas
import numpy

# 该函数将从特定位置读取中文垃圾邮件训练集
# 注：如果你的项目文件中没有这些文件，该函数会出错
def readChinese():
    sumTextList = []    # 储存中文数据
    sumLabelList = []   # 储存标签数据

    # 从各个文件夹中读取正常邮件、垃圾邮件
    filenames_a = os.listdir('./data/Chinese/normal')
    filenames_b = os.listdir('./data/Chinese/spam')
    filenames_c = os.listdir('./data/Chinese/test_normal')
    filenames_d = os.listdir('./data/Chinese/test_spam')

    # 获得停用词表
    stopList = readFromFile('./data/Chinese/中文停用词表.txt')
    # 读取邮件内容
    cutTextList = []
    for fileName in filenames_a:  # 读取./data/Chinese/normal下的数据文件
        cutTextList.clear()
        for line in open('./data/Chinese/normal/' + fileName):
            processedLine = processChineseSentence(line)
            cutTextList.append(processedLine)

        cutLine = ''
        for line in cutTextList:
            cutLine += line + ' '
        sumTextList.append(cutLine)
        sumLabelList.append('ham')

    for fileName in filenames_c:  # 读取./data/Chinese/test_normal下的数据文件
        cutTextList.clear()
        for line in open('./data/Chinese/test_normal/' + fileName):
            processedLine = processChineseSentence(line)
            cutTextList.append(processedLine)

        cutLine = ''
        for line in cutTextList:
            cutLine += line + ' '
        sumTextList.append(cutLine)
        sumLabelList.append('ham')

    for fileName in filenames_b:  # 读取./data/Chinese/spam下的数据文件
        cutTextList.clear()
        for line in open('./data/Chinese/spam/' + fileName):
            processedLine = processChineseSentence(line)
            cutTextList.append(processedLine)

        cutLine = ''
        for line in cutTextList:
            cutLine += line + ' '
        sumTextList.append(cutLine)
        sumLabelList.append('spam')

    for fileName in filenames_d:  # 读取./data/Chinese/test_spam下的数据文件
        cutTextList.clear()
        for line in open('./data/Chinese/test_spam/' + fileName):
            processedLine = processChineseSentence(line)
            cutTextList.append(processedLine)

        cutLine = ''
        for line in cutTextList:
            cutLine += line + ' '
        sumTextList.append(cutLine)
        sumLabelList.append('spam')

    return [sumTextList, sumLabelList]

# 从指定文件中读取数据，数据将被逐行保存在列表中
def readFromFile(filename):
    dataFrame = []
    with open(filename, 'r') as f:
        for line in f:
            dataFrame.append(line)
    return dataFrame


# 该函数接受一个中文的字符串变量，对该字符串进行本文预处理、中文分词后，返回经过处理的的字符串
def processChineseSentence(sentence):
    # 获得停用词表
    stopList = readFromFile('./data/Chinese/中文停用词表.txt')

    cutTextList = []
    # 过滤掉非中文字符
    rule = re.compile(r"[^\u4e00-\u9fa5]")
    sentence = rule.sub("", sentence)
    # 将每封邮件出现的词保存在wordsList中
    textList = list(jieba.cut(sentence))
    # 过滤单个字符
    textList = [tok for tok in textList if len(tok) >= 2]
    for i in textList:
        if i not in stopList and i.strip() != '' and i != None:
            cutTextList.append(i)

    cutLine = ''
    for word in cutTextList:
        cutLine += word + ' '
    return cutLine


# 该函数将从特定的位置读取英文垃圾邮件分类训练集
# 注：如果你的项目文件中没有这些文件，该函数会出错
def readEnglish():
    textData = []    # 储存文本数据
    labelData = []   # 储存标签数据
    f = open("./data/English/SMSSpamCollection", "r", encoding='utf-8')

    for line in f:
        array = line.split('\t')
        labelData.append(array[0])
        textData.append(array[1])
    f.close()
    return [textData, labelData]


# 该函数接受一个英文字符串，对该字符串进行特殊字符过滤、词干提取后，返回经过处理的英文文本
def processEnglish(textData):
    processedData = []
    for line in textData:
        # 去除特殊字符
        remove_chars = '[0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
        line = re.sub(remove_chars, ' ', str(line))

        # 去除单个字符
        token_words = nltk.word_tokenize(line)
        token_words = [tok for tok in token_words if len(tok) > 2]
        # print(token_words)

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


# 该函数接受邮件正文的文本内容，以判断该邮件是中文邮件还是英文邮件
def isChineseMail(string):
    english_part = re.compile(r'[a-zA-z]')    # 过滤出英文部分
    chinese_part = re.compile(r'[\u4E00-\u9FA5]')   # 过滤出中文部分

    english_list_len = len(english_part.findall(string))  # 英文字符长度
    chinese_list_len = len(chinese_part.findall(string))  # 中文字符长度

    # 以中英文字符长度的比例作为依据，判断一封邮件是中文邮件还是英文邮件
    if (chinese_list_len == 0 or english_list_len / chinese_list_len > 0.1):
        return 0
    else:
        return 1

