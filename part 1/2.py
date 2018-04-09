from Auxiliary import *
import os

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////// EXC2 ///////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def exc2():
    precisions = []
    truePositive = 0
    falsePositive = 0
    directory = "Textos-fonte_com_titulo/"
    sumDirectory = "sumarios/"
    files = [f for f in os.listdir(directory)]

    for fileToOpen in files:
        sentences = readFile(directory + fileToOpen)
        TFIDFMatrix = TFIDF(sentences)
        query = TFIDFQuery(sentences)
        tfIdfResult = cosine_similarity(query , TFIDFMatrix)[0]
        top5Sentences = topXSentences(5, tfIdfResult, sentences)
        
        print("-------------------------------------------------")
        with open(sumDirectory + "Ext-" +  fileToOpen) as f:
            data = f.read().replace("\n", " ").rstrip("!.?")
            sumSentences = re.split("([\.\n|\.\r|\.\t|\._|!|?])", data)
            sumSentences = [''.join(sumSentences[i:i+2]) for i in range(0,len(sumSentences),2)]
            for f in top5Sentences:
                print(f)
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

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////// END OF EXC2 ///////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////// EXC2 ALT /////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def exc2alt():
    precisions = []
    truePositive = 0
    falsePositive = 0
    directory = "Textos-fonte_com_titulo/"
    sumDirectory = "sumarios/"
    files = [f for f in os.listdir(directory)]

    for fileToOpen in files:
        #Separate file's text into sentences and store them in an array
        sentences = readFile(directory + fileToOpen)
        lines = sentencesToWords(sentences)
        countWords = wordCounter(lines)
        totalNumbWordsNonSimilar = totalNumberNonSimilarWords(countWords)
        sentencesWithWord = sentenceWithWordCounter(lines) 
        
        

    for fileToOpen in files:
        sentences = readFile(directory + fileToOpen)
        lines = sentencesToWords(sentences)
        nrSentences = len(lines)
        TFweights = TFCalculator(countWords)
        IDFweights = IDFCalculator(nrSentences ,sentencesWithWord) 
        weights = weightCalculator(IDFweights, TFweights)
        tfIdfMatrix = tfIdfMatrixBuilder(weights, lines)
        tfIdfResult = tfIdfCalculator(tfIdfMatrix, weights)
        top5Sentences = topXSentencesAlt(5, tfIdfResult, sentences)
        
        print("-------------------------------------------------")
        with open(sumDirectory + "Ext-" +  fileToOpen) as f:
            data = f.read().replace("\n", " ").rstrip("!.?")
            sumSentences = re.split("([\.\n|\.\r|\.\t|\._|!|?])", data)
            sumSentences = [''.join(sumSentences[i:i+2]) for i in range(0,len(sumSentences),2)]
            for f in top5Sentences:
                print(f)
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

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////// END OF EXC2 ALT /////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
