#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob, re, math
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class Data():

	def __init__(self):
		self.__text_array = list()
		self.__score_array = list()
		self.__stop_words = self.readStopWords('stop_words.txt')


	#	function also removes:
	#	a) all words that contains digits
	#	b) two or more whitespaces
	#	c) one or more _

	def addStringToArray(self, string):
		string = re.sub(r'(.*\d+.*)?', '', string)
		string = re.sub(r'\s+',' ', string)
		string = re.sub(r'_+', '', string)	
		self.__text_array.append(string)


	def readStopWords(self, path):
		stop_words = list()
		with open(path, 'r') as file:
			for line in file:
				stop_words.append(line.strip())
		return stop_words


	def addScoreToArray(self, score):
		self.__score_array.append(score)


	def readFiles(self, dirpath):
		print(dirpath)
		txt_files = glob.glob(dirpath + '*.txt')
		it = 0
		print('[loading files]')
		for filename in txt_files:
			print(f'[loading: {filename}]')
			with open(filename, 'r', encoding='utf-8') as file:
				self.addStringToArray(file.read())
				self.addScoreToArray(int(re.findall(r'.*_(\d|\d\d)\.txt', filename)[0]))
			file.close()
			if it == 5000:
				break
			it += 1
		print('[finished loading]')


	def tfidf(self):
		print('[calculating TFIDF]')
		vectorizer = TfidfVectorizer(stop_words=self.__stop_words, min_df=0.0003, max_df=0.2)#, ngram_range=(1,2))
		vectors = vectorizer.fit_transform(self.__text_array)
		feature_names = vectorizer.get_feature_names()
		dense = vectors.todense()
		denselist = dense.tolist()
		df = pd.DataFrame(denselist, columns=feature_names)
		print(f'[{df.shape}]')
		print('[ending]')
		print('[adding scores to table]')
		final_df = df.assign(scores = self.__score_array)
		print('[saving to csv]')
		final_df.to_csv(r'./tfidf.csv')
		print('[done]')
	
	def readCSV(self):
		df = pd.read_csv('./tfidf.csv')
		return df


'''count_vectorizer = CountVectorizer(stop_words=self.__stop_words, min_df=0.03, max_df=0.8, ngram_range=(1,2))
sf = count_vectorizer.fit_transform(self.__text_array)

transformer = TfidfTransformer()
transformed_weights = transformer.fit_transform(sf)

weights = np.asarray(transformed_weights.mean(axis=0)).ravel().tolist()
weights = np.around(weights, 7)
#print(type(weights))
weights_df = pd.DataFrame({'term': count_vectorizer.get_feature_names(), 'weight': weights})

weights_df.sort_values(by='weight', ascending=False, inplace=True)#.head(20))
print(weights_df.shape)
weights_df.to_csv(r'./idf.csv')'''