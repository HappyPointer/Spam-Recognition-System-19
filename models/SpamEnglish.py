# 该 py 文件读取英文垃圾邮件分类的训练集、进行机器学习模型的训练并将训练完成的模型保存到本地文件
# 作者：何颖智
# 创建日期：2019-8-20
# 最后修改日期：2019-8-26

import funcLib
import pickle
from sklearn.model_selection import  train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

# 读取文本数据，并对文本进行预处理
textData, labelData = funcLib.readEnglish()
textData = funcLib.processEnglish(textData)

# 随机采样25%的数据样本作为测试集
X_train,X_test,y_train,y_test = train_test_split(textData, labelData, test_size=0.2)

#文本特征向量化
vec = CountVectorizer(max_features=30000)
X_train = vec.fit_transform(X_train)
X_test = vec.transform(X_test)

# 特征向量保存至本地文件
vec_pickle = pickle.dumps(vec)
with open('EnglishVec',"wb")as f:
    f.write(vec_pickle)


# 使用朴素贝叶斯进行训练
print('Initializing feature matrix.')
mnb = MultinomialNB()   # 使用默认配置初始化朴素贝叶斯

print('Fitting Bayes model.')
mnb.fit(X_train,y_train)    # 利用训练数据对模型参数进行估计
print('Model training complete.')
# 保存训练好的模型
joblib.dump(mnb, "EnglishBayesModel.m")

y_predict = mnb.predict(X_test)     # 对参数进行预测

# 获取结果报告
print('The Accuracy of Naive Bayes Classifier is:', mnb.score(X_test,y_test))
print(classification_report(y_test, y_predict))




