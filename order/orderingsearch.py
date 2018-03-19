import glob,os
import pickle
import numpy as np
import operator
from multiprocessing.pool import ThreadPool

def execute_score(query,index):

	query_result = dict()


	for i in xrange(0,len(query)-1):

		term = query[i]
		nextword = query[i+1]

		if term in index:
			doc_dict = index[term]

			for key in doc_dict:

				ss = doc_dict[key]

				value = 0

				if nextword in ss:
					value = 1

				if key in query_result:
					query_result[key] += value
				else:
					query_result[key] = value

	return query_result

def f1():

	query = []

	inp =raw_input("Enter your Query: ")
	inp = inp.split(" ")
	for word in inp:

		if word != "":
			print word
			query.append(word)

	return query

def f2():

	index=dict()

	index=pickle.load(open('text/index.p', "rb"))
	return index 


if __name__ == '__main__':

	pool = ThreadPool(processes=1)	
	pool2 = ThreadPool(processes=1)

	async_result1 = pool.apply_async(f1, ()) 	
	async_result2 = pool2.apply_async(f2, ())

	query = async_result1.get()
	index = async_result2.get()

	result = execute_score(query,index)

	results = sorted(result.iteritems(), key=operator.itemgetter(1))
	results.reverse()

	if len(results):

		for i in results[:100]:

			term = i[0]

			value1,value2=term.split(",")
			print ("\n")
			print value1 + " - " + value2 + "\n"


	else:
		print ("\nYour search -  " + ' '.join(query) + "  - did not match any documents.\n")