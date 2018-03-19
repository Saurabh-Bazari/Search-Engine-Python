import os,glob
import numpy as np
import pickle
from operator import itemgetter

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


def create_indexing(i,key,index,corpus):

	word = corpus[key][i-1]
	nextword = corpus[key][i]

	if word in index:

		if key in index[word]:
			(index[word][key]).append(nextword)
		else:
			index[word][key] = [nextword]

	else:
		temp = dict()
		temp[key] = [nextword]
		index[word] = temp


if __name__ == '__main__':

	corpus = create_corpus_dict()
	index=dict()

	for key in corpus:
		for i in xrange(1,len(corpus[key])) :
			create_indexing(i,str(key),index,corpus)

	pickle.dump(index, open('text/index.p', "wb"))