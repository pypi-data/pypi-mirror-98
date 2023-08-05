import numpy as np
import pandas as pd
from sklearn import preprocessing

class linearregression:
    def calculate_weight(x,y):
        """
        this function determines the values of weights and bias
        """
        z = preprocessing.scale(x)

        w = np.zeros(x.shape[1], dtype=float, order='F')
        b = 0

        derivative_w = np.zeros(x.shape[1], dtype=float, order='F')
        derivative_b = 0

        r=0.5

        for i in range(0,1000):
            for j in range(0,x.shape[0]):
                derivative_w = derivative_w + ((-2*z[j]) * (y[j] - np.dot(w,z[j])) - b)
                derivative_b = derivative_b + (-2 * (y[j] - (np.dot(w,z[j])) - b ))

            derivative_w_final = (derivative_w / x.shape[0])
            derivative_b_final = (derivative_b / x.shape[0])

            derivative_b = 0
            derivative_w = np.zeros(x.shape[1], dtype=float, order='F')

            w = w - (r * (derivative_w_final))
            b = b - (r * (derivative_b_final))

            r = (r / 2)

        W=w
        B=b

        return (W,B)

    def prediction(W,B,X):
        """
        to predict the value of target variable
        """
        z = preprocessing.scale(X)
        y_pred=[]
        for i in range(0,X.shape[0]):
            result = (np.dot(W,z[i])) + B
            y_pred.append(np.asscalar(result))
        return y_pred

    def rmse(y,y_pred):
        """
        calculating the root-mean-squared error
        """
        return np.sqrt(np.mean(np.square(y - y_pred)))

    def rsquare(y,y_pred):
        """
        calculate the R-squared error metric
        """
        ss_residue = np.sum(np.square(y - y_pred))
        ss_total = np.sum(np.square(y-np.mean(y)))
        rsquared = 1 - (ss_residue/ss_total)
        return rsquared


