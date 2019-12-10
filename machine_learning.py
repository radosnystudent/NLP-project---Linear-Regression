#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import data_module as dm
import lubimyczytac_webscraper as lcw
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split 
from sklearn import metrics


def prepareSets(name):
	
	train, test, validate = dm.readCSV('./train.csv'), dm.readCSV('./test.csv'), dm.readCSV('./validate.csv')
	X_train = train[train.columns.values[:-1]].values
	y_train = train[train.columns.values[-1]].values
	X_test = validate[validate.columns.values[:-1]].values
	y_test = validate[validate.columns.values[-1]].values
	X_dev = test[test.columns.values[:-1]].values
	y_dev = test[test.columns.values[-1]].values
	if name == 'train':
		return X_train, y_train, X_test, y_test
	elif name == 'dev':
		return X_train, y_train, X_dev, y_dev


def linearRegression(name):
	regressor = LinearRegression()
	X_train, y_train, X_test, y_test = prepareSets(name)
	regressor.fit(X_train, y_train)

	y_pred = regressor.predict(X_test)
	df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred}).round({'Predicted' : 0})
	print(df.head(100))
	print(f'RMSE: {metrics.mean_squared_error(y_test, y_pred, squared=False)}')
	print(f'accuracy score: {round(regressor.score(X_test, y_test) * 100, 0)}%')#, 9)}%') #


if __name__ == '__main__':
	if not os.path.exists('lubimyczytac_recenzje'):
		WS = lcw.WebScraper('https://lubimyczytac.pl/katalog')
		WS.crawling()
	Data = dm.Data()
	Data.readFiles('./lubimyczytac_recenzje/')
	Data.tfidf()
	#linearRegression('train')
	#linearRegression('dev')
