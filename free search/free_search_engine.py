from math import log
import glob,os
import pickle
import decimal
import numpy as np
import operator
from multiprocessing.pool import ThreadPool

k1 = 1.2
k2 = 100
b = 0.75
R = 0.0

def calculate_score(n, f, qf, r, N, dl, average_value):

	K = compute_K(dl, average_value)
	variable1 = log( ( (r + 0.5) / (R - r + 0.5) ) / ( (n - r + 0.5) / (N - n - R + r + 0.5)) )
	variable2 = ((k1 + 1) * f) / (K + f)
	variable3 = ((k2+1) * qf) / (k2 + qf)
	
	return variable1 * variable2 * variable3


def compute_K(dl, average_value):
	return k1 * ((1-b) + b * (float(dl)/float(average_value)) )


def execute_score(query,index,table,average_value):

	query_result = dict()

	for term in query:

		if term in index:
			doc_dict = index[term]

			for key, freq in doc_dict.iteritems(): 
				score = calculate_score( len(doc_dict), freq, 1, 0, len(table), table[key], average_value)

				if key in query_result:
					query_result[key] += score
				else:
					query_result[key] = score

	return query_result

def f1():

	query = []
	inp =raw_input("Enter your Query: ")
	inp = inp.split(" ")
	for word in inp:
		word = word.translate(None,'.,%:;/')
		word = word.strip()
		word = word.lower()
		query.append(word)

	return query

def f2():

	index=dict()
	index=pickle.load(open('text/index.p', "rb"))
	return index 


def f3():

	indexline=dict()
	indexline=pickle.load(open('text/indexline.p', "rb"))
	return indexline


def f4():

	table=dict()
	table=pickle.load(open('text/table.p', "rb"))
	return table


if __name__ == '__main__':

	average_value = pickle.load(open('text/average_value.p', "rb"))

	pool = ThreadPool(processes=1)	
	pool2 = ThreadPool(processes=1)
	pool3 = ThreadPool(processes=1)
	pool4 = ThreadPool(processes=1)

	async_result1 = pool.apply_async(f1, ()) 	
	async_result2 = pool2.apply_async(f2, ()) 	
	async_result3 = pool3.apply_async(f3, ()) 
	async_result4 = pool4.apply_async(f4, ()) 

	query = async_result1.get()
	index = async_result2.get()
	indexline = async_result3.get()
	table = async_result4.get()

	result = execute_score(query,index,table,average_value)
	results = sorted(result.iteritems(), key=operator.itemgetter(1))
	results.reverse()

	ignore_list = [ 'is' , 'are' , 'the' , 'i' , 'my' ,'' ,' ']

	if len(results):

		for i in results[:10]:

			term = i[0]

			value1,value2=term.split(",")
			print ("\n")
			print value1 + " - " + value2 + "\n"

			for word in query:

				if word in indexline:
					if term in indexline[word]:
						data = indexline[word][term]
						print word + " :- " + ' '.join(map(str,data))

	else:
		print ("\nYour search -  " + ' '.join(query) + "  - did not match any documents.\n")