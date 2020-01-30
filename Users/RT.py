# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor


def predict(a,b,c,d,e,f,g,h,i,j,k,l):

	y_predAll = []

	for i in range(14,19):


		# Importing the dataset
		dataset = pandas.read_excel('data.xlsx')
		X = dataset.iloc[0:35, 1:13].values
		y = dataset.iloc[0:35, i-1:i].values


		

		#topred = [308,0.00124153,992,53.1,0.1154,0.00125,0.6651088,107,0.000001417,50.47,90366,9.2]
		topred = [a,b,c,d,e,f,g,h,i,j,k,l]
		topred2 = np.array(topred).reshape(1, -1)
		






		X_train,X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=34)

		print(X_test[0])

		# Fitting Random Forest Regression to the dataset

		regressor = RandomForestRegressor(n_estimators = 10, random_state = 42)
		regressor.fit(X_train, y_train.ravel())

		# Predicting a new result
		y_pred = regressor.predict(topred2)
		
		
		
		for x in np.nditer(y_pred):
   			y_predAll.append(str(x))
   			

	
	return y_predAll


		# Calculation of Mean Squared Error (MSE)
		#print(r2_score(y_test,y_pred))


predict(308,0.00124153,992,53.1,0.1154,0.00125,0.6651088,107,0.000001417,50.47,90366,9.2)
