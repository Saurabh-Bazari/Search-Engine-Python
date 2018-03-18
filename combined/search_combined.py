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
flag=0

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

def execute_score_order(query,index):

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

	global flag

	while(flag!=2 and flag!=1):
		print ("For relevant line press 1\nFor phrase search press 2")
		flag = input("Enter your choice:")
		print("\n")

	query = []
	inp =raw_input("Enter your Query: ")
	inp = inp.split(" ")
	for word in inp:

		if flag==1:
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
	corpus=dict()
	corpus=pickle.load(open('text/corpus.p', "rb"))
	return corpus

def f4():
	table=dict()
	table=pickle.load(open('text/table.p', "rb"))
	return table

def f5():
	index_order=dict()
	index_order=pickle.load(open('text/indexorder.p', "rb"))
	return index_order

if __name__ == '__main__':

	average_value = pickle.load(open('text/average_value.p', "rb"))

	pool = ThreadPool(processes=1)	
	pool2 = ThreadPool(processes=1)
	pool3 = ThreadPool(processes=1)
	pool4 = ThreadPool(processes=1)
	pool5 = ThreadPool(processes=1)

	async_result1 = pool.apply_async(f1, ()) 	
	async_result2 = pool2.apply_async(f2, ()) 	
	async_result3 = pool3.apply_async(f3, ()) 
	async_result4 = pool4.apply_async(f4, ()) 
	async_result5 = pool5.apply_async(f5, ()) 

	query = async_result1.get()
	index = async_result2.get()
	corpus = async_result3.get()
	table = async_result4.get()	
	index_order = async_result5.get()

	if flag==1:
		result = execute_score(query,index,table,average_value)
	else:
		result = execute_score_order(query,index_order)
	
	results = sorted(result.iteritems(), key=operator.itemgetter(1))
	results.reverse()

	flag1=0

	if len(results):

		for i in results[:100]:

			if flag==2 and i[1]==1:
				break

			flag1=1

			term = i[0]
			value=corpus[term]

			value1,value2=term.split(",")
			print ("\n")
			print value1 + " - " + value2 + "\n"

		 	print ' '.join(map(str, value))

		if flag1==0:
			print ("\nYour search -  " + ' '.join(query) + "  - did not match any documents.\n")

	else:
		print ("\nYour search -  " + ' '.join(query) + "  - did not match any documents.\n")