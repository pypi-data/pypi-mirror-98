import lnregrsn
from sklearn.datasets import load_boston
import pandas as pd
#print("Hello World")

boston = load_boston()
bos = pd.DataFrame(boston.data)
bos['price'] = boston.target
x = bos.drop('price', axis = 1)
y = bos['price']

weight,bias = lnregrsn.linearregression.calculate_weight(x,y)
#print("weight:",weight)
#print("bias:",bias)

y_prediction = lnregrsn.linearregression.prediction(weight,bias,x)
#print(y_prediction[:5])

rmse = lnregrsn.linearregression.rmse(y,y_prediction)
print("RMSE:",rmse)

rsquared = lnregrsn.linearregression.rsquare(y,y_prediction)
print("R-Squared error:",rsquared)