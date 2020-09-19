import numpy as np

class DataFetcher:

	def fetch_news_file(date_arg):
		news_array = []
		f = open('feeds.txt')
		file_as_list = f.readlines()
		for line in file_as_list:
			news_array = np.append(news_array, line)
		return news_array


	