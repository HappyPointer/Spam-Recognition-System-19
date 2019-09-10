"""
简介：预载入服务器所用模型
作者：黄旭
创建时间：2019年9月8日
最后修改时间：2019年9月8日
"""

import numpy as np
from tensorflow import keras
import tensorflow as tf
from gensim.models import Word2Vec
import joblib

# 载入CNN模型
cnn_model = keras.models.load_model('./BayesClassifier/Models/cnn_model.h5')
sess = keras.backend.get_session()
graph = tf.get_default_graph()
cnn_model.predict(np.random.rand(1,200,100))
graph.finalize()

# 载入Word2Vec模型
vec = Word2Vec.load('./BayesClassifier/Models/word2vec.model')
# 载入中文贝叶斯模型
ChineseBayesModel = joblib.load("./BayesClassifier/Models/ChineseBayesModel.m")