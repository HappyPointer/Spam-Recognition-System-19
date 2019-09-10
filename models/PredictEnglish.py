# 该 py 文件在机器学习模型训练好了以后，调用英文机器学习模型预测位置文本，以测评我们模型的性能如何，能否符合软件的要求
# 作者：何颖智
# 创建日期：2019-8-24
# 最后修改日期：2019-8-26

import funcLib
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib

# 该字符串变量将作为收入到模型的文本内容，让服务器判断此文本内容是否会被识别为垃圾邮件
arg = 'Get you free iphone only for today! Learn more at www.iphone.com. A surprising discount. Be ready!!!'
textData = [arg]

# 对英文文本进行预处理，包括特殊字符过滤及词干化提取操作
textData = funcLib.processEnglish(textData)

# 创建词向量对象
vec = CountVectorizer()
# 从本地文件中读取以及训练好的机器学习模型所使用的词向量对象
f = open('EnglishVec',"rb")
while 1:
    try:
        vec = pickle.load(f)
    except:
        break
f.close()

# 将需要被判断的文本转化为词向量
X_test = vec.transform(textData)
print('特征词数量 ： ' + str(X_test.indptr[1]))

# 加载训练好的模型
loadedModel = joblib.load("EnglishBayesModel.m")

y_predict = loadedModel.predict(X_test)     # 对参数进行预测
y_proba = loadedModel.predict_proba(X_test)[0][0]

# 输出预测结果
print(y_predict)
print(y_proba)






