"""
简介：将训练集导入并用以训练好的word2vec模型转化成向量，再使用cnn训练邮件分类模型
作者：黄旭
创建时间：2019年9月6日
最后修改时间：2019年9月8日
"""

from gensim.models import Word2Vec
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np
import tensorflow as tf
from tensorflow.data import Dataset
from tensorflow.keras import layers
import re
import chardet
from time import time

# 用词向量表示信中的单词
def email2vec(email):
    X = np.zeros((seq_length, embedding_dim))
    j = 0
    for word in email:
        if word in vec.wv:
            X[j, :] = vec.wv[word]
            j += 1
            if j >= seq_length:
                break
    return X.reshape(1, seq_length, embedding_dim)

if __name__ == '__main__':
    # 载入word2vec模型和labelEncoder模型，训练参数的设置
    vec = Word2Vec.load('word2vec.model')
    label_encoder = LabelEncoder()
    label_encoder.fit(['ham', 'spam'])
    seq_length = 200
    embedding_dim = 100
    lr = 0.001
    drop_prob = 0.25
    epochs = 15

    # 处理数据集
    s = stopwords.words('english')
    punctuations = r',.:;?()![]{}<>@#$%^&*\'-=+\/"‘’“”~·：；——…！@￥'
    sw = s + ['tr', 'html', 'td', 'font', 'title', 'smtp', 'from', 'to', 'div', 'localhost', 'mime', 'charset', 'meta',
              'doctype', 'encoding', 'nbsp', 'href', 'color', 'format', 'content', 'jp', 'iso', 'psy', 'px', 'psych',
              'style', 'nextpart', 'size', 'date', 'type', 'text', 'php', ''] + [s for s in punctuations]
    sw = frozenset(sw)
    t0 = time()
    with open('./trec06p/spam50/index2') as f:
        indices = f.readlines()
    Y = []
    path = []
    for i in indices:
        index = i.split()
        Y.append(index[0])
        path.append((index[1]))
    XtrainPath, XtestPath, Ytrain, Ytest = train_test_split(path, label_encoder.transform(Y),
                                         random_state=42, test_size=0.25)
    print('split done')
    
    train_size = 7500
    test_size = 2500
    batch_size = 500
    st = PorterStemmer()
    Ytrain = tf.keras.utils.to_categorical(Ytrain, 2)
    Ytest = tf.keras.utils.to_categorical(Ytest, 2)
    Xtrain = np.array([])
    Xtest = np.array([])
    # 导入和处理训练集
    for i in range(train_size):
        with open('./trec06p' + XtrainPath[i][2:], 'rb') as f:
            emaillines = f.readlines()
        email = b''
        textPlain = False
        for line in emaillines:
            if textPlain:
                email += line
            if line == b'\n':
                textPlain = True
        encoding = chardet.detect(email)['encoding']
        if encoding is not None:
            email = email.decode(encoding, errors='ignore').lower()
        else:
            email = email.decode('utf8', errors='replace').lower()
        email = re.sub(r'\d+', '', email)
        email = re.sub(r'[a-zA-Z]{20,}', '', email)
        email = re.sub(r'<.+>', '', email)
        email = re.sub('_|\.', ' ', email)
        email = re.sub('[^a-zA-Z]', ' ', email)
        emailwords = word_tokenize(email)
        clean_words = [st.stem(w) for w in emailwords if w not in sw]
        if i == 0:
            Xtrain = email2vec(clean_words)
        else:
            Xtrain = np.vstack((Xtrain, email2vec(clean_words)))
    print("train data done")

    # 导入和处理测试集
    for i in range(test_size):
        with open('./trec06p' + XtestPath[i][2:], 'rb') as f:
            emaillines = f.readlines()
        email = b''
        textPlain = False
        for line in emaillines:
            if textPlain:
                email += line
            if line == b'\n':
                textPlain = True
        encoding = chardet.detect(email)['encoding']
        if encoding is not None:
            email = email.decode(encoding, errors='ignore').lower()
        else:
            email = email.decode('utf8', errors='replace').lower()
        email = re.sub(r'\d+', '', email)
        email = re.sub(r'[a-zA-Z]{20,}', '', email)
        email = re.sub(r'<.+>', '', email)
        email = re.sub('_|\.', ' ', email)
        email = re.sub('[^a-zA-Z]', ' ', email)
        emailwords = word_tokenize(email)
        clean_words = [st.stem(w) for w in emailwords if w not in sw]
        if i == 0:
            Xtest = email2vec(clean_words)
        else:
            Xtest = np.vstack((Xtest, email2vec(clean_words)))
    print("test data done")

    train_data = Dataset.from_tensor_slices((Xtrain, Ytrain[:train_size]))
    test_data = Dataset.from_tensor_slices((Xtest, Ytest[:test_size]))
    train_data = train_data.batch(batch_size).repeat()
    test_data = test_data.batch(batch_size).repeat()
    readin_time = time() - t0
    print(train_data.output_types)
    print(train_data.output_shapes)
    print('read in data time: %0.3fs' % readin_time)

    # 构建卷积神经网络模型
    model = tf.keras.Sequential()
    model.add(layers.Conv1D(input_shape=(200, 100), filters=64, kernel_size=5, activation='relu'))
    model.add(layers.GlobalMaxPool1D())
    model.add(layers.Dense(32, activation='relu'))
    model.add(layers.Dropout(rate=drop_prob))
    model.add(layers.Dense(2, activation='softmax'))
    model.compile(optimizer=tf.keras.optimizers.Adam(lr),
              loss='categorical_crossentropy',
              metrics=['accuracy'])
    callbacks = [tf.keras.callbacks.TensorBoard(log_dir='./logs')]
    # 训练
    model.fit(train_data, epochs=epochs, steps_per_epoch=20, callbacks=callbacks)
    # 测试
    model.evaluate(test_data, steps=20)
    model.save('my_model.h5')
