from aux_func import *

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////// EXC1 ///////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def exc1(fileToOpen):
    nrSentencesSum = 5
    sentences = readFile(fileToOpen)
    nrSentences = len(sentences)
    TFIDFMatrix = TFIDF(sentences)
    #DEBUG print(nrSentences)
    graph = createGraph(nrSentences , TFIDFMatrix)
    #DEBUG print(graph)
    PR = PageRank(nrSentences , graph)
    #DEBUG print(PR)
    #Get 3 highest score sentences
    top5Sentences = topXSentences(nrSentencesSum, PR, sentences)
    print ("Top 5 sentences by order of appearence in the text:")
    for i in range (0, nrSentencesSum):
        print(repr(i+1) + " - " + top5Sentences[i])    
    return top5Sentences
