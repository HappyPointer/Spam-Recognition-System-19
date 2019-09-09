from sklearn.svm import LinearSVC
from joblib import load, dump
from time import time


if __name__ == '__main__':
    # 导入训练集
    vectorizer = load('vectorizer.joblib')
    with open('../dataset/trec06p/spam50/index') as f:
        indices = f.readlines()
    Ytrain = []
    for i in indices:
        Ytrain.append(i.split()[0])
    Xtrain = load('Xtrain.joblib')
    clf = LinearSVC(dual=False)

    # 训练SVM模型
    t0 = time()
    clf.fit(Xtrain, Ytrain)
    training_time = time() - t0
    print("training time:%0.3fs" % training_time)
    dump(clf, 'clf_svm.joblib')

