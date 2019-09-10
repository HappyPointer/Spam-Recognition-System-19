# coding=utf-8

# 该 py 文件在机器学习模型训练好了以后，调用中文机器学习模型预测位置文本，以测评我们模型的性能如何，能否符合软件的要求
# 作者：何颖智
# 创建日期：2019-8-24
# 最后修改日期：2019-8-27

import funcLib
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib

# 该字符串变量将作为收入到模型的文本内容，让服务器判断此文本内容是否会被识别为垃圾邮件
arg = '今天淘宝天猫特惠，电动牙刷只要887，只此一次，不要错过'

# 将字符串经过中文分词处理
sentence = funcLib.processChineseSentence(arg)
List = [sentence]

# 创建词向量对象
vec = CountVectorizer()
# 从本地文件中读取以及训练好的模型使用的词向量对象
f = open('ChineseVec',"rb")
while 1:
    try:
        vec = pickle.load(f)
    except:
        break
f.close()

# 将需要判断的文本内容处理为词向量
X_test = vec.transform(List)
test = X_test.toarray()

print('特征词数量 ： ' + str(X_test.indptr[1]))

# 加载训练好的模型
loadedModel = joblib.load("ChineseBayesModel.m")

y_predict = loadedModel.predict(X_test)     # 对参数进行预测
y_proba = loadedModel.predict_proba(X_test)[0][0]

# 显示预测结果
print(y_predict)
print(y_proba)













