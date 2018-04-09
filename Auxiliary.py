from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from numpy import sum
import string
import math
import re
import numpy

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

#readFile separates fileToOpen's text into sentences and store them in an array
def readFile(fileToOpen):
    with open(fileToOpen) as f:
        data = f.read().replace("\n\n", " ").replace("\r\r", " ").replace("\n", " ").replace("\r", " ").rstrip("!.?")
        sentences = re.split("([\.\n|\.\r|\.\t|\._|!|?])", data)
        sentences = [''.join(sentences[i:i+2]) for i in range(0,len(sentences),2)]
    #print("Sentences: ", sentences)        #Debug print
    return sentences


#sentencesToWords separates each sentence from sentences into words without punctuation
def sentencesToWords(sentences):
    lines = sentences[:]
    for i in range(0, len(lines)):
        lines[i] = lines[i].replace(string.punctuation, "")  #Remove punctuation (replace with whitespace)
        lines[i] = lines[i].lower()     #Lower case
        lines[i] = lines[i].split()     #Split into words
    #print("Lines array: ", lines)        #Debug print
    return lines

#wordCounter counts the number of occurences of each word in the given array and keeps track of it in a dictionary
def wordCounter(words):
    countWords = {}
    for i in range (0, len(words)):
        for el in words[i]:
            if el not in countWords:
                countWords[el] = 1
            else:
                countWords[el] += 1
    #print("Words: ", countWords)        #Debug print
    return countWords


#totalNumberWords calculates the total number of non similar words in the given dictionary
def totalNumberNonSimilarWords(countWords):
    totalNumbWords = 0
    for el in countWords:
        totalNumbWords += countWords[el]
    totalNumbWordsNonSimilar = len(countWords)
    #print("Total number of non similar words: ", totalNumbWordsNonSimilar)        #Debug print
    return totalNumbWordsNonSimilar


#sentenceWithWordCounter counts the number of sentences each word appears in
def sentenceWithWordCounter(lines):
    sentencesWithWord = {}
    for i in lines:
        words = set(i)
        for el in words:
            if el not in sentencesWithWord:
                sentencesWithWord[el] = 1
            else:
                sentencesWithWord[el] += 1
    #print("Number of sentences with word: ", sentencesWithWord)        #Debug print
    return sentencesWithWord


#Calculate each words score (weight) TF
def TFCalculator(countWords):
    weights = {}
    totalNumbWordsNonSimilar = totalNumberNonSimilarWords(countWords)
    for word in countWords:
        weights[word] = float(countWords[word]) / totalNumbWordsNonSimilar
    #print("Weigths: ", weights)        #Debug print
    return weights

#Calculate each words score (weight) TF
def IDFCalculator(totalSentences, sentenceWithWordCounter):
    weights = {}
    for word in sentenceWithWordCounter:
        weights[word] = math.log(totalSentences / sentenceWithWordCounter[word])
    return weights

def weightCalculator(IDFweights, TFweights):
    weights = {}
    for word in IDFweights:
        weights[word] = IDFweights[word] * TFweights[word]
    return weights


#queryBuilder builds the query to calculate the tf-idf
def queryBuilder(weights):
    query = weights.items()
    query1 = []
    for i in query:
        query1.append(i[1])
    #print("Query: ", query1)        #Debug print
    return query1


#tfIdfMatrix creates a tf-idf matrix
def tfIdfMatrixBuilder(weights, lines):
    tfIdfMatrix = []
    query = weights.items()
    for i in lines:
        tfIdfArray = []
        for el in query:
            if el[0] in i:
                tfIdfArray.append(el[1])
            else:
                tfIdfArray.append(0)
        tfIdfMatrix.append(tfIdfArray)
    #print("tf_idf: ", tfIdfMatrix)        #Debug print
    return tfIdfMatrix


#tfIdfCalculator calculates the cosine similarity between the query and each sentence
def tfIdfCalculator(tfIdfMatrix, weights):
    tfIdfResult = []
    query = queryBuilder(weights)
    for i in tfIdfMatrix:
        tfIdfResult.append(cosine_similarity([query], [i])[0][0])
    #print("TF-IDF result: ", tfIdfResult)        #Debug print
    return tfIdfResult


#calculator calculates the precision, recall and f1 measure based on the given values
def calculator(fileName, truePositive, trueNegative, falsePositive, falseNegative):
    precision = float(truePositive) / (truePositive + falsePositive)
    recall = float(truePositive) / (truePositive + falseNegative)
    if (precision != 0 or recall != 0):
        f1 = (precision * 2 * recall) / (precision + recall)
    else:
        f1 = 0
    print("File name: " + fileName)
    print("Precision: " + str(precision))
    print("Recall: " + str(recall))
    print("F1 Measure: " + str(f1))
    return precision


#MAPCalculator calculates the Mean Precision Average based on the given precisions
def MAPCalculator(precisions):
    total = 0
    for i in precisions:
        total += i
    MAP = total / len(precisions)
    print("MAP: " + str(MAP))
    return MAP

#topXSentences returns the X sentences with the highest score
def topXSentences(x, tfIdfResult, sentences):
    topXSentences = []
    topXIndex = []
    for i in range (0, x):  #Get the index of the top x sentences
        highest = max(tfIdfResult)
        index = tfIdfResult.tolist().index(highest)
        topXIndex.append(index)
        tfIdfResult[index] = -1
    topXIndex.sort()
    for i in range (0, x):  #Get the top x sentences
        topXSentences.append(sentences[topXIndex[i]])
    return topXSentences

def topXSentencesAlt(x, tfIdfResult, sentences):
    topXSentences = []
    topXIndex = []
    for i in range (0, x):  #Get the index of the top x sentences
        highest = max(tfIdfResult)
        index = tfIdfResult.index(highest)
        topXIndex.append(index)
        tfIdfResult[index] = -1
    topXIndex.sort()
    for i in range (0, x):  #Get the top x sentences
        topXSentences.append(sentences[topXIndex[i]])
    return topXSentences

def BM25(D, N , weightMatrix):
    b = 0.75
    k1 = 1.2
    score =[]
    c = -1
    i = -1
    avgdl = D/N
    weightMatrix = weightMatrix.toarray()
    ni = [0] * len(weightMatrix[0])
    for l in  range(0 , len(weightMatrix)):
        for c in range(0, len(weightMatrix[l])):
            if (weightMatrix[l][c] != 0):
                ni[c] += 1

    
    for l in  range(0 , len(weightMatrix)):
        for c in range(0, len(weightMatrix[l])):
            IDF = math.log((N - ni[c] + 0.5)/(ni[c] + 0.5))
            weightMatrix[l][c] = IDF * (weightMatrix[l][c]*(k1 + 1))/(weightMatrix[l][c] + k1 * (1 - b + b *( ( D / avgdl ) )))
    return weightMatrix

