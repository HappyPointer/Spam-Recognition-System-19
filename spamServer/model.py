import numpy as np
from tensorflow import keras
import tensorflow as tf
from gensim.models import Word2Vec
import joblib

cnn_model = keras.models.load_model('./BayesClassifier/Models/cnn_model.h5')
sess = keras.backend.get_session()
graph = tf.get_default_graph()
cnn_model.predict(np.random.rand(1,200,100))
graph.finalize()

vec = Word2Vec.load('./BayesClassifier/Models/word2vec.model')
ChineseBayesModel = joblib.load("./BayesClassifier/Models/ChineseBayesModel.m")