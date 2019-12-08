#!/usr/bin/env python
# -*- coding: utf-8 -*-

import data_module as dm
import lubimyczytac_webscraper as lcw
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split 
from sklearn import metrics


if __name__ == '__main__':
	print('[start]')
	#WS = lcw.WebScraper('https://lubimyczytac.pl/katalog')
	Data = dm.Data()
	#Data.readFiles('./lubimyczytac_recenzje/')
	#Data.tfidf()
	df = Data.readCSV()
	print('[readed]')
	col_names = df.columns.values[:-1]
	scores = df.columns.values[-1]
	#print(col_names)
	
	X = df[col_names].values
	y = df[scores].values
	print('[X,Y sets]')
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
	print('[starting LinearRegression]')
	regressor = LinearRegression()
	regressor.fit(X_train, y_train)
	
	y_pred = regressor.predict(X_test)
	df1 = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
	print(df1.head(30))

