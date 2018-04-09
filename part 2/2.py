from aux_func import *
import os

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////// EXC1 ///////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def exc2():
    print("this exercise will run multiple improved ranks, so it can take some time")
    for i in range(1,3):
        print("alternative number " + str(i) + ":")
        precisions = []
        truePositive = 0
        falsePositive = 0    
        nrSentencesSum = 5
        directory = "Textos-fonte_com_titulo/"
        sumDirectory = "sumarios/"
        files = [f for f in os.listdir(directory)]
    
        for fileToOpen in files:
            sentences = readFile(directory + fileToOpen)
            nrSentences = len(sentences)
            TFIDFMatrix = TFIDF(sentences)
            
            if(i == 1):
                graph = createGraph(nrSentences , TFIDFMatrix)            
                Prior = calculatePrior(nrSentences)                

            elif(i == 2):
                graph = createGraph(nrSentences , TFIDFMatrix)            
                Prior = priorTFIDF(sentences, TFIDFMatrix)        

            PR = ImprovedPageRank(nrSentences , graph, Prior)
            #Get 3 highest score sentences
            top5Sentences = topXSentences(nrSentencesSum, PR, sentences)
            
            truePositive = 0
            falsePositive = 0            
            with open(sumDirectory + "Ext-" +  fileToOpen) as f:
                data = f.read().replace("\n", " ").rstrip("!.?")
                sumSentences = re.split("([\.\n|\.\r|\.\t|\._|!|?])", data)
                sumSentences = [''.join(sumSentences[i:i+2]) for i in range(0,len(sumSentences),2)]
                for f in top5Sentences:
                    if(f in sumSentences):
                        truePositive += 1
                        del sumSentences[sumSentences.index(f)]
                    else:
                        falsePositive += 1
                falseNegative = len(sumSentences)
                trueNegative = len(sentences) - truePositive - falsePositive - falseNegative
                nrSumSenteces = len(sumSentences)
                precisions.append(calculator(fileToOpen, truePositive, trueNegative, falsePositive, falseNegative))
        MAPCalculator(precisions)
    
