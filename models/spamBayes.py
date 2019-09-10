"""
简介：提取垃圾邮件中的特征词
作者：黄旭
创建时间：2019年8月26日
最后修改时间：2019年8月26日
"""

from joblib import load
import numpy as np


if __name__ == '__main__':
    v = load('vectorizer.joblib')
    feature = np.array(v.get_feature_names())
    with open('../dataset/trec06p/spam50/index') as f:
        indices = f.readlines()
    Ytrain = []
    for i in indices:
        Ytrain.append(i.split()[0])

    # 导入训练数据
    Xtrain = load('Xtrain.joblib')
    spam = np.zeros(5000)

    # 将垃圾邮件的权值相加，找到权值最重的词，依次排序
    for i in range(len(Ytrain)):
        if Ytrain[i] == 'spam':
            spam += Xtrain[i]
    spamsort = np.argsort(-spam)
    np.set_printoptions(threshold=np.inf)
    print(feature[spamsort])
    print(spam[spamsort])
