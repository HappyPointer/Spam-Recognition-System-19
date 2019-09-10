# coding=utf-8

# 该文件提供了调用已有机器学习模型进行垃圾邮件识别的相关函数
# 作者：何颖智、黄旭
# 创建日期：2019-8-26
# 最后修改日期：2019-9-8

import re
import funcLib
from sklearn.feature_extraction.text import CountVectorizer
import pickle
import joblib
import model


# 该类用于创建一个 Agent 对象，通过调用该对象的成员函数，我们可以在其它 py 文件使用此文件中定义的功能函数
class BayesClassifier:
    threshold = None

    def __init__(self):
        self.setThresold(None)   
        
    # 分类函数，函数接受邮件正文内容，将按顺序返回对应每一封邮件的判断结果
    def classify(self, textData):
        predictionList = []
        for textInfo in textData:
            text = textInfo['body']    # 正文内容
            self.setSensitivity(textInfo['intensity'])   # 用户设定的敏感度
            if self.isChineseMail(text) == 1:
                predictionList.append(self.predictChinese(text))  # 调用中文机器学习模型进行判断
            else:
                predictionList.append(self.predictEnglish_cnn(text))  # 调用英文机器学习模型进行判断
        return predictionList

    # 该函数在接受一段邮件文本后，将通过中英字符比例判断邮件是英文邮件还是中文邮件
    # 返回数字 0 或 1，其中 0 代表英文邮件，1 代表中文邮件
    def isChineseMail(self, string):
        english_part = re.compile(r'[a-zA-z]')
        chinese_part = re.compile(r'[\u4E00-\u9FA5]')

        # 使用正则表达式将字符串中的中英文内容分别过滤出来
        english_list_len = len(english_part.findall(string))
        chinese_list_len = len(chinese_part.findall(string))

        if (chinese_list_len == 0 or english_list_len / chinese_list_len > 100):
            return 0
        else:
            return 1

    # 加载已经训练好的中文贝叶斯模型，并对邮件内容进行分类
    def predictChinese(self, string):
        sentence = funcLib.processChineseSentence(string)
        List = [sentence]

        vec = CountVectorizer()

        # 从本地文件中读取 vector 对象
        f = open('./BayesClassifier/Models/ChineseVec', "rb")
        while 1:
            try:
                vec = pickle.load(f)
            except:
                break
        f.close()

        X_test = vec.transform(List)
        # 加载训练好的模型
        loadedModel = model.ChineseBayesModel

        if self.threshold is None:
            y_predict = loadedModel.predict(X_test)  # 对参数进行预测
            return y_predict[0]
        else:
            y_proba = loadedModel.predict_proba(X_test)[0][0]
            if y_proba > self.threshold:   # 判断邮件评分是否大于设定的阈值
                return 'ham'
            else:
                return 'spam'

    # 加载已经训练好的英文贝叶斯模型，并对邮件内容进行分类
    def predictEnglish(self, string):
        textData = funcLib.processEnglish([string])

        vec = CountVectorizer()
        # 从本地文件中读取 vector 对象
        f = open('./BayesClassifier/Models/EnglishVec', "rb")
        while 1:
            try:
                vec = pickle.load(f)
            except:
                break
        f.close()

        X_test = vec.transform(textData)
        # 加载训练好的模型
        loadedModel = joblib.load("./BayesClassifier/Models/EnglishBayesModel.m")

        if self.threshold is None:
            y_predict = loadedModel.predict(X_test)  # 对参数进行预测
            return y_predict[0]
        else:
            y_proba = loadedModel.predict_proba(X_test)[0][0]
            if y_proba > self.threshold:   # 判断邮件评分是否大于设定的阈值
                return 'ham'
            else:
                return 'spam'

    # 加载已经训练好的英文cnn模型，并对邮件内容进行分类
    def predictEnglish_cnn(self, string):
        # 预处理
        textData = funcLib.processEnglish2(string)
        # 载入模型
        with model.sess.as_default():
            with model.graph.as_default():
                prob = model.cnn_model.predict(textData)[0][0]
        if self.threshold is None:
            thr = 0.5
        else:
            thr = self.threshold
        if prob > thr:
            return 'ham'
        else:
            return 'spam'

    # 调用该函数以设置垃圾识别的阈值
    def setThresold(self, value):
        self.threshold = value
        return

    # 该函数接受字符串变量，将根据字符串的不同去改变垃圾识别的阈值
    # 可输入的字符串有 high, medium, low, default，将以此改变 thresold 值
    def setSensitivity(self, string):
        if string == 'high':
            self.setThresold(0.8)
        elif string == 'medium':
            self.setThresold(0.4)
        elif string == 'low':
            self.setThresold(0.1)
        elif string == 'default':
            self.setThresold(None)
        else:
            print('Unknown sensitivity type.')
            self.setThresold(None)
        return
