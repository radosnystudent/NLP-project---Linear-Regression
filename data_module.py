import glob, re
import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer


class Data():

	def __init__(self):
		self.__text_array = list()
		self.__score_array = list()


	def addStringToArray(self, string):
		self.__text_array.append(string)


	def addScoreToArray(self, score):
		self.__score_array.append(score)


	def readFiles(self, dirpath):
		txt_files = glob.glob(dirpath + '*.txt')
		#it = 0
		for filename in txt_files:
			with open(filename, 'r', encoding='utf-8') as file:
				self.addStringToArray(file.read())
				self.addScoreToArray(int(re.findall(r'.*_(\d|\d\d)\.txt', filename)[0]))
			file.close()
			break
			#it += 1
			#if it == 20:
			#	break

			

D = Data()
D.readFiles('./lubimyczytac_recenzje/')
#print(sys.version)