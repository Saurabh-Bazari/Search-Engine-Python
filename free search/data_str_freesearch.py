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

			page_number=1				
			line_number=1
			text = dict()

			for line in infile:

				key = filename1 + ",page.no"+ `page_number`
				text1=line.split()
				text[line_number] = text1
				corpus[key] = text
				line_number=line_number+1

				if  line_number==31:

					text = dict()
					page_number=page_number+1;
					line_number=1;

	return corpus


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


def create_line_indexing(word,key,line,index_line):

	if word in index_line:

		if key in index_line[word]:
			(index_line[word][key]).append(line)
		else:
			index_line[word][key] = [ line ]

	else:
		temp = dict()
		temp[key] = [ line ]
		index_line[word] = temp


def calculate_average_value(dlt):
	
	sum = 0
	for length in dlt.itervalues():
		sum += length

	return float(sum) / float(len(dlt))


def f2(index_line):
	pickle.dump(index_line, open('text/indexline.p', "wb"))


def f3(index):
	pickle.dump(index, open('text/index.p', "wb"))


def f4(table):
	pickle.dump(table, open('text/table.p', "wb"))


if __name__ == '__main__':

	corpus = create_corpus_dict()

	index = dict()
	table = dict()
	index_line = dict()
	ignore_list = [ 'is' , 'are' , 'the' , 'i' , 'my' ,'' ,' ']

	for key in corpus:
		for line in corpus[key]:
			for word in corpus[key][line]:

				word = word.translate(None,'.,%:;/&!#$^*')     		# remove all characters like .,%:etc
				word = word.strip()
				word = word.lower()									# convert into lower case

				if word not in ignore_list :							# ignore words like is, are, the
					create_indexing(str(word), str(key),index)
					
				create_line_indexing(str(word), str(key),line,index_line)

			length = len(corpus[str(key)])
		table[key] = length

	average_value = calculate_average_value(table)

	pickle.dump(average_value, open('text/average_value.p', "wb"))

	t1 = threading.Thread(target=f2, args=(index_line,))
	t1.start()
	t2 = threading.Thread(target=f3, args=(index,))
	t2.start()
	t3 = threading.Thread(target=f4, args=(table,))
	t3.start()
	t1.join()
	t2.join()
	t3.join()