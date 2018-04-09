from Auxiliary import *
import os

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////// EXC4 ///////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def exc4():
    directory = "Textos-fonte_com_titulo/"
    files = [f for f in os.listdir(directory)]
    result = []

    precisions = [] #//////////////////////////////////////////////TEST
    for fileToOpen in files:
        _lambda = 0.2
        S = []
        similarities = []
        j = 0
        sentences = readFile(directory + fileToOpen)
        TFIDFMatrix = TFIDF(sentences)
        query = TFIDFQuery(sentences)
        toIgnore = []
        for i in range(0, 5):
            sentenceIndex = -1
            new = (0, 0, 0)
            for s in TFIDFMatrix:
                sentenceIndex += 1
                if (len(toIgnore) > 0):
                    if (s.tolist() in toIgnore):
                        continue
                similarity = cosine_similarity([s], query)
                mmrRight = 0
                if (len(S) > 0):
                    for j in S:
                        mmrRight += (_lambda * cosine_similarity([s], [j[2]]))
                mmr = (1 - _lambda) * similarity - mmrRight
                if(mmr > new[1]):
                    new = (sentences[sentenceIndex], mmr, s)
            S.append(new)
            toIgnore.append(s.tolist())
        aux = []
        for el in S:
            aux.append(el[0])
        result.append(aux)
        
        ##//////////////////////////////////////////////TEST PRECISION
        #truePositive = 0
        #falsePositive = 0
        #sumDirectory = "sumarios/"
        #with open(sumDirectory + "Ext-" +  fileToOpen) as f:
            #data = f.read().replace("\n", " ").rstrip("!.?")
            #sumSentences = re.split("([\.\n|\.\r|\.\t|\._|!|?])", data)
            #sumSentences = [''.join(sumSentences[i:i+2]) for i in range(0,len(sumSentences),2)]
            #for f in aux:
                #if(f in sumSentences):
                    #truePositive += 1
                    #del sumSentences[sumSentences.index(f)]
                #else:
                    #falsePositive += 1
            #falseNegative = len(sumSentences)
            #trueNegative = len(sentences) - truePositive - falsePositive - falseNegative
            #nrSumSenteces = len(sumSentences)
            #precisions.append(calculator(fileToOpen, truePositive, trueNegative, falsePositive, falseNegative))
        ##//////////////////////////////////////////////END TEST    
        
    print("Result: ")
    j = 0
    for n in result:
        j +=1
        print(str(j) + "-" + str(n))
    
    #MAPCalculator(precisions)        
  
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////// END OF EXC4 ///////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////