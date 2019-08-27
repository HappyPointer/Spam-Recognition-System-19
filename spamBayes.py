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
    Xtrain = load('Xtrain.joblib')
    spam = np.zeros(5000)
    for i in range(len(Ytrain)):
        if Ytrain[i] == 'spam':
            spam += Xtrain[i]
    spamsort = np.argsort(-spam)
    np.set_printoptions(threshold=np.inf)
    print(feature[spamsort])
    print(spam[spamsort])
