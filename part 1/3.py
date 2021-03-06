from Auxiliary import *
from sklearn.feature_extraction.text import CountVectorizer
import os

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////// EXC3 ///////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def exc3():
    precisions = []
    truePositive = 0
    falsePositive = 0
    directory = "Textos-fonte_com_titulo/"
    sumDirectory = "sumarios/"
    files = [f for f in os.listdir(directory)]

    for fileToOpen in files:
        
        sentences = readFile(directory + fileToOpen)
        N = len(sentences)
        lines = "".join(sentences)
        D = len(lines.split())
        TFIDFMatrix = CountVectorizer()
        TFIDFMatrix = TFIDFMatrix.fit_transform(sentences)
        
        query = CountVectorizer(ngram_range=(1, 2))
        query = query.fit_transform(sentences)        
        
        query = BM25(D ,N ,query ) 
        TFIDFMatrix = BM25(D ,N ,TFIDFMatrix)
        print(query)
        print(TFIDFMatrix)
        tfIdfResult = []
        tfIdfResult = cosine_similarity(query , TFIDFMatrix)[0]
        
        #top3Sentences = topXSentences(3, tfIdfResult, sentences)
        #print ("Top 3 sentences by order of appearence in the text:")
        #for i in range (0, 3):
            #print(repr(i+1) + " -" + top3Sentences[i])           

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////// END OF EXC3 ///////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


