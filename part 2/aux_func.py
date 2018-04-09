from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from numpy import sum
import os
import sys
import string
import math
import re
import numpy

# Disable prints
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore prints
def enablePrint():
    sys.stdout = sys.__stdout__

def readFile(fileToOpen):
    with open(fileToOpen) as f:
        data = f.read().replace("\n\n", " ").replace("\r\r", " ").replace("\n", " ").replace("\r", " ").rstrip("!.?")
        sentences = re.split("([\.\n|\.\r|\.\t|\._|!|?])", data)
        sentences = [''.join(sentences[i:i+2]) for i in range(0,len(sentences),2)]
    #print("Sentences: ", sentences)        #Debug print
    return sentences

def TFIDF(sentences):
    vector = CountVectorizer()
    vector = vector.fit_transform(sentences).toarray()
    #print(vector)
    maxFreq = max(vector.sum(axis=0))
    vector =  vector / maxFreq
    N = len(vector)
    ni = [0] * len(vector[0])
    for l in  range(0 , len(vector)):
        for c in range(0, len(vector[l])):
            if (vector[l][c] != 0):
                ni[c] += 1
    for l in  range(0 , len(vector)):
        for c in range(0, len(vector[l])):
            vector[l][c] = vector[l][c] * math.log( N / ni[c] )
    return vector

def createGraph(nrSentences , TFIDFMatrix):
    cosineTreshold = 0.2
    sentencesGraph = []
    #cosine_similarity between all the sentences
    #as the graph is unidirectional we only need half of the matrix
    for l in range(0, nrSentences):
        Node = []
        for c in range (0, nrSentences):
            if (l == c):
                Node.append(0)
                continue
            edge = cosine_similarity([TFIDFMatrix[l]] , [TFIDFMatrix[c]])[0][0]
            Node.append(edge)
        sentencesGraph.append(Node)
    #DEBUG print(sentencesGraph)
    return sentencesGraph

def PageRank(N , Graph):
    d = 0.15
    nrIterations = 50
    PRinitial = 1/N
    PR = [PRinitial for i in range(N)]
    links = []
    #DEBUG print(len(links))
    for l in range(0, N):
        links.append(0)
        for c in range(0, N):
            if (Graph[l][c] != 0):
                links[l] += 1
    #DEBUG print(links)
    for i in range(0, nrIterations):
        for l in range(0, N):
            PRsum = 0
            for c in range(0, N):
                if (Graph[l][c] != 0):
                    PRsum += PR[c]/links[c]
            PR[l] = (d / N) + (1 - d) * PRsum
    return PR

def ImprovedPageRank(N , graph, Prior):
    d = 0.15
    nrIterations = 15
    #Prior= calculatePrior(N)
    #Prior using TF-IDF
    #Prior = priorTFIDF(graph)
    #DEBUG print("PRIOR > ", Prior)
    links = []
    PRinitial = 1/N
    PRnew = [PRinitial for i in range(N)]
    for i in range(0, nrIterations):
        priorsum = sum(Prior)
        for l in range(0, N):
            PRsum = 0
            for c in range(0, N):
                if (graph[l][c] != 0):
                    ksum = 0
                    for k in range(0, N):
                        ksum += graph[c][k]
                    PRsum += PRnew[c] * graph[c][l] / ksum
            PRnew[l] = d * (Prior[l] / priorsum) + (1 - d) * PRsum
    return PRnew

#topXSentences returns the X sentences with the highest score
def topXSentences(x, tfIdfResult, sentences):
    topXSentences = []
    topXIndex = []
    for i in range (0, x):  #Get the index of the top x sentences
        highest = max(tfIdfResult)
        index = tfIdfResult.index(highest)
        topXIndex.append(index)
        tfIdfResult[index] = -1
    topXIndex.sort()
    for i in range (0, x):  #Get the top x sentences
        topXSentences.append(sentences[topXIndex[i]].lstrip())
    return topXSentences

def calculator(fileName, truePositive, trueNegative, falsePositive, falseNegative):
    precision = float(truePositive) / (truePositive + falsePositive)
    recall = float(truePositive) / (truePositive + falseNegative)
    if (precision != 0 or recall != 0):
        f1 = (precision * 2 * recall) / (precision + recall)
    else:
        f1 = 0
    #DEBUG print("File name: " + fileName)
    #DEBUG print("Precision: " + str(precision))
    #DEBUG print("Recall: " + str(recall))
    #DEBUG print("F1 Measure: " + str(f1))
    return precision

def MAPCalculator(precisions):
    total = 0
    for i in precisions:
        total += i
    MAP = total / len(precisions)
    print("MAP: " + str(MAP))
    return MAP

#def createTrainOutput():

def calculatePrior(N):
    Prior = []
    for i in range(0, N):
        Prior.append(N-i)
    return Prior;

def priorTFIDF(sentences, TFIDFMatrix):
    query = TFIDFQuery(sentences)
    tfIdfResult = cosine_similarity(query , TFIDFMatrix)[0]
    return tfIdfResult;

def TFIDFQuery(sentences):
    query = ["".join(sentences)]
    vector = CountVectorizer()
    vector = vector.fit_transform(sentences).toarray()    
    queryvector = CountVectorizer()
    queryvector = queryvector.fit_transform(query).toarray()
    maxFreq = max(vector.sum(axis=0))
    queryvector =  queryvector / maxFreq
    N = len(vector)
    ni = [0] * len(vector[0])
    for l in  range(0 , len(vector)):
        for c in range(0, len(vector[l])):
            if (vector[l][c] != 0):
                ni[c] += 1
    for l in  range(0 , len(queryvector)):
        for c in range(0, len(queryvector[l])):
            queryvector[l][c] = queryvector[l][c] * math.log( N / ni[c] )
    return queryvector

