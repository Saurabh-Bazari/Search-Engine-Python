import os,glob
import numpy as np
import pickle
from operator import itemgetter
import threading

def create_corpus_dict():

	corpus=dict()

	for filename in glob.glob(os.path.join('files','*.txt')):

		filename1=filename[6:]
		with open(filename) as infile:
				
			line_number=1
			for line in infile:

				key = filename1 + ",line.no:"+ `line_number`
				text=line.split()
				corpus[key]=text
				line_number=line_number+1

	return corpus

def create_indexing_ordering(i,key,index_order,corpus):

	word = corpus[key][i-1]
	nextword = corpus[key][i]

	if word in index_order:

		if key in index_order[word]:
			(index_order[word][key]).append(nextword)
		else:
			index_order[word][key] = [nextword]

	else:
		temp = dict()
		temp[key] = [nextword]
		index_order[word] = temp


def create_indexing(word,key,index):

	if word in index:

		if key in index[word]:
			index[word][key] += 1
		else:
			index[word][key] = 1

	else:
		temp = dict()
		temp[key] = 1
		index[word] = temp


def calculate_average_value(table):

	sum = 0
	for length in table.itervalues():
		sum += length

	return float(sum) / float(len(table))


def f2(corpus):
	pickle.dump(corpus, open('text/corpus.p', "wb"))


def f3(index):
	pickle.dump(index, open('text/index.p', "wb"))


def f4(table):
	pickle.dump(table, open('text/table.p', "wb"))

def f5(index_order):
	pickle.dump(index_order, open('text/indexorder.p', "wb"))



if __name__ == '__main__':

	corpus = create_corpus_dict()

	index=dict()
	table=dict()
	index_order = dict()

	ignore_list = [ 'is' , 'are' , 'the' , 'i' , 'my' ,'' ,' ','a' , 'an']


	for key in corpus:
		for i in xrange(1,len(corpus[key])) :
			create_indexing_ordering(i,str(key),index_order,corpus)

	for key in corpus:
		for word in corpus[key]:

			word = word.translate(None,'.,%:;/')     		# remove all characters like .,%:etc
			word = word.strip()
			word = word.lower()								# convert into lower case

			if word in ignore_list :						# ignore words like is, are, the
				continue

			create_indexing(str(word), str(key),index)

		length = len(corpus[str(key)])

		table[key] = length

	average_value = calculate_average_value(table)

	pickle.dump(average_value, open('text/average_value.p', "wb"))

	t1 = threading.Thread(target=f2, args=(corpus,))
	t1.start()
	t2 = threading.Thread(target=f3, args=(index,))
	t2.start()
	t3 = threading.Thread(target=f4, args=(table,))
	t3.start()
	t4 = threading.Thread(target=f5, args=(index_order,))
	t4.start()
	t1.join()
	t2.join()
	t3.join()
	t4.join()