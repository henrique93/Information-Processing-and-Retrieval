from Auxiliary import *

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////// EXC1 ///////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



def exc1(fileToOpen):
    nrSentences = 5
    sentences = readFile(fileToOpen)
    TFIDFMatrix = TFIDF(sentences)
    query = TFIDFQuery(sentences)
    tfIdfResult = cosine_similarity(query , TFIDFMatrix)[0]
    #Get 5 highest score sentences
    top3Sentences = topXSentences(nrSentences, tfIdfResult, sentences)
    print ("Top 5 sentences by order of appearence in the text:")
    for i in range (0, nrSentences):
        print(repr(i+1) + " -" + top3Sentences[i])    

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////// END OF EXC1 ///////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////