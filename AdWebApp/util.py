# -*- coding: utf-8 -*-

import codecs, re, math
import pickle
import networkx as nx
import operator
from py4j.java_gateway import JavaGateway

SPECIAL_CHARACTERS = r'`|~|!|@|\$|%|\^|&|\*|\(|\)|-|\+|=|{|}|\[|\]|\||\\|\'|\"|:|;|\.|,|/|\?|<|>|\d'

def read_stopwords():
    stopwords = list()
    f = codecs.open('stopwords.txt', 'r', encoding='utf8')
    line = f.readline()
    while line:
	stopwords.append(line.strip())
        line = f.readline()
    return stopwords

def read_data(filename, stopwords):
    data = dict()
    f = codecs.open(filename, 'r', encoding='utf8')
    print len(stopwords)
    line = f.readline()
    while line:
        tmp = line.strip().split(' ', 1)
        list_of_words = re.sub(SPECIAL_CHARACTERS, ' ', tmp[1].lower()).replace(u'“', ' ').replace(u'”', ' ').replace(u'…', ' ').split()
        data[tmp[0]] = [w for w in list_of_words if w not in stopwords]
        #print line
        #for w in data[tmp[0]]:
	  #print w
        line = f.readline()
    f.close()

    return data

def convert_str_2_vec(content, vocabs):
    list_of_words = re.sub(SPECIAL_CHARACTERS, ' ', content.lower()).strip().replace(u'“', ' ').replace(u'”', ' ').replace(u'…', ' ').split()
    list_of_words = [w for w in list_of_words if w in vocabs.keys()]
    output = dict()
    words_len = len(list_of_words)
    for w in list_of_words:
      if w not in output:
          output[w] = 0
      output[w] += 1
    for w in output.keys():
      output[w] *= vocabs[w]
    return output

# docs = dict(id, list_of_words)
def idf(docs):
    WORDS = dict()
    docs_len = len(docs)
    temp = dict()
    for docId, words in docs.iteritems():
	for word in list(set(words)):
	    if word in WORDS.keys():
		WORDS[word] += 1
	    else:
		WORDS[word] = 1
    for w in WORDS.keys():
	WORDS[w] = math.log(1.0 + docs_len*1.0/WORDS[w])
    return WORDS

def make_vocabs(data):
    vocabs = idf(data)
    pickle.dump(vocabs, open('vocabs.obj', 'wb'))

def load_vocabs():
    vocabs = pickle.load(open('vocabs.obj', 'rb'))
    return vocabs


def vectorization(data, vocabs):
    data_output = dict()
    for docId, words in data.iteritems():
        temp = dict()
        doc_len = len(data[docId])
        for word in list(set(words)):
            tf = len([w for w in words if w == word])*1.0/doc_len
            temp[word] = tf*vocabs[word]
        data_output[docId] = temp
    return data_output

def cosine(A, B):
    A2 = 0.0
    B2 = 0.0
    AB = 0.0
    for word in A.keys():
        A2 += math.pow(A[word], 2)
        if word in B.keys():
            AB += A[word] * B[word]
    for word in B.keys():
        B2 += math.pow(B[word], 2)
    if AB == 0.0:
        return 0.0
    else:
        return AB / math.sqrt(A2) / math.sqrt(B2)

def cosine_v1(A, A2, B, B2):
    AB = 0.0
    words = [w for w in A.keys() if w in B.keys()]
    for w in words:
        AB += A[w] * B[w]
    if AB == 0.0:
        return 0.0
    else:
        return AB / math.sqrt(A2) / math.sqrt(B2)

# data = dict(id, dict(word, tf-idf))
def compute_similarity(data):
    ids = data.keys()
    SIMILARITY = nx.Graph()
    for i in range(0, len(ids)-1):
        for j in range(i+1, len(ids)):
            SIMILARITY.add_edge(ids[i], ids[j], weight = cosine(data[ids[i]], data[ids[j]]))
    return SIMILARITY

def ads_by_content_v4(content, vocabs, ads, N):
    content_vec = convert_str_2_vec(content, vocabs)
    A2 = 0.0
    for w in content_vec.keys():
        A2 += math.pow(content_vec[w], 2)
    ads_sim = dict()
    for key in ads.keys():
        ads_sim[key] = cosine_v1(ads[key]['feature'], ads[key]['square'], content_vec, A2)
    sorted_x = sorted(ads_sim.items(), key=operator.itemgetter(1), reverse=True)
    output = []
    for i in range(0, N):
        print str(sorted_x[i][0]) + '    ' + str(sorted_x[i][1])
        output.append(sorted_x[i][0])
    return output

#call py4j token
def token(content):
    gateway = JavaGateway()
    response = gateway.entry_point.getResponse()
    response.setUETSegmentResponse(content)
    content = response.execute()
    return content

if __name__ == '__main__':
  SPECIAL_CHARACTERS = r'”'
  s = u'…tưởng”'
  s1 = re.sub(SPECIAL_CHARACTERS, ' ', s)
  print s1
  print s1.replace(u'…', ' ')
  
      






