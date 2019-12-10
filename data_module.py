#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob, re, math
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class Data():

	def __init__(self):
		self.__docs_array = list()
		self.__score_array = list()
		self.__stop_words = self.readStopWords('stop_words.txt')
		self.__docs_length = list()


	def addStringToArrays(self, string):
		string = prepareString(string)
		self.__docs_array.append(string)
		self.__docs_length.append(len(string))


	def readStopWords(self, path):
		with open(path, 'r') as file:
			return [line.strip() for line in file]


	def addScoreToArray(self, score):
		self.__score_array.append(score)


	def readFiles(self, dirpath):
		txt_files = glob.glob(dirpath + '*.txt')
		for filename in txt_files:
			print(f'[loading: {filename}]')
			with open(filename, 'r', encoding='utf-8') as file:
				self.addStringToArrays(file.read())
				self.addScoreToArray(int(re.findall(r'.*_(\d|\d\d)\.txt', filename)[0]))
			file.close()


	def tfidf(self):
		vectorizer = TfidfVectorizer(stop_words=self.__stop_words, min_df=0.001, max_df=0.1, ngram_range=(1, 2))
		vectors = vectorizer.fit_transform(self.__docs_array)
		feature_names = vectorizer.get_feature_names()
		print(len(feature_names))
		'''dense = vectors.todense()
		denselist = dense.tolist()
		df = pd.DataFrame(denselist, columns=feature_names)
		df = df.assign(length = self.__docs_length)
		final_df = df.assign(scores = self.__score_array)
		train_validate_test_split(final_df)'''


def writeToCSV(df, path):
	df.to_csv(path)


def readCSV(path):
	return pd.read_csv(path)


def train_validate_test_split(df, train_percent=.6, validate_percent=.2, seed=None):
    np.random.seed(seed)
    perm = np.random.permutation(df.index)
    m = len(df.index)
    train_end = int(train_percent * m)
    validate_end = int(validate_percent * m) + train_end
    train = df.iloc[perm[:train_end]]
    validate = df.iloc[perm[train_end:validate_end]]
    test = df.iloc[perm[validate_end:]]
    writeToCSV(train, './train.csv')
    writeToCSV(test, './test.csv')
    writeToCSV(validate, './validate.csv')


def prepareString(string):
	string = re.sub(r'(.*\d+.*)?', '', string)
	string = re.sub(r'\s+',' ', string)
	string = re.sub(r'_+', '', string)
	return string
