import glob, re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer 

class Data():

	def __init__(self):
		self.__text_array = list()
		self.__score_array = list()
		self.__stop_words = self.readStopWords('stop_words.txt')

	def addStringToArray(self, string):
		self.__text_array.append(string)

	def readStopWords(self, path):
		stop_words = list()
		with open(path, 'r') as file:
			for line in file:
				stop_words.append(line.strip())
		return stop_words

	def addScoreToArray(self, score):
		self.__score_array.append(score)

	#function removes all words that contains digits
	def removeDigitsFromText(self):
		for i in range(len(self.__text_array)):
			self.__text_array[i] = re.sub(r'(.*\d+.*)?', '', self.__text_array[i])		

	#def removeMostCommonWords(self):
	#	for i in range(len(self.__text_array)):
	#		for word in self.__most_common_words:
	#			self.__text_array[i] = re.sub(rf'^{word}$', '', self.__text_array[i])	


	def readFiles(self, dirpath):
		txt_files = glob.glob(dirpath + '*.txt')
		#it = 0
		for filename in txt_files:
			with open(filename, 'r', encoding='utf-8') as file:
				self.addStringToArray(file.read())
				self.addScoreToArray(int(re.findall(r'.*_(\d|\d\d)\.txt', filename)[0]))
			file.close()
			#it += 1
			#if it == 15000:
				#break
		self.removeDigitsFromText()


	def tfidf(self):
		tfidf_vectorizer = TfidfVectorizer(stop_words=self.__stop_words)
		tfidf_vectorizer_vectors = tfidf_vectorizer.fit_transform(self.__text_array)
		feature_names = tfidf_vectorizer.get_feature_names()
		#dense = tfidf_vectorizer_vectors.todense()
		#denselist = dense.tolist()
		#df = pd.DataFrame(denselist, columns=feature_names)
		#df = df.replace(0,np.nan).dropna(axis=1,how="all")
		#df.loc[:, (df != 0).any(axis=0)]
		print(len(feature_names))
		#drop_cols = df.columns[(df == 0).sum() > 0.25*df.shape[1]]
		#df.drop(drop_cols, axis=1, inplace=True)
		#df.to_csv('./plik.csv')

D = Data()
D.readFiles('./lubimyczytac_recenzje/')
D.tfidf()