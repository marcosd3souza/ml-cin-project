# @author: marcos de souza
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.base import BaseEstimator, ClassifierMixin

class BayesianKnnClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, k=1, log=False):
        self.k = k
        self.log = log
    
    def density(self, label):
        y_arr = [self.y[i] for i in range(0, len(self.y))]
        density = len([l for l in y_arr if l == label]) / len(y_arr)

        return density

    
    def posteriori(self, xi):
        # P(wj/xi) = P(xi/wj)*P(wj)
        n_classes = np.unique(xi)
        estimation = 0
        label = None

        for c in n_classes:
            likelihood = xi.count(c) / len(xi)
            c_density = self.density(c)
            c_estimation = likelihood * c_density

            if c_estimation > estimation:
                estimation = c_estimation
                label = c
        
        return estimation, label


    def fit (self, X, y):
        # construct the neighborhood
        self.y = y
        self.nbh = NearestNeighbors(n_neighbors=self.k, algorithm='auto', metric='euclidean').fit(X)
    
    def get_nn_label(self, X):
        idx_nn = self.nbh.kneighbors(X, return_distance=False)

        nn_labels = []
        for obj in range(0, len(idx_nn)):
            nn_labels.append([])
            for nn in idx_nn[obj]:
                label = [self.y[i] for i in range(0, len(self.y)) if i == nn][0]
                nn_labels[obj].append(label)
        return nn_labels


    def predict(self, X):
        nn_labels = self.get_nn_label(X)
        
        labels = []
        for xi in nn_labels:
            estimation, label = self.posteriori(xi)

            if self.log:
                print('obj: ', xi, 'estimation:', estimation, 'label: ', label)
            labels.append(label)

        return labels
