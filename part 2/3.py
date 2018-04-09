from sklearn.linear_model import Perceptron
from aux_func import *
import numpy as np
import os

def exc3():
    train_folder = "training/Originais/"
    train_target = "training/Sumarios/"
    train_files = [f for f in os.listdir(train_folder)]
    train = []
    train
    #for fileToOpen in train_files:
        #sentences = readFile(train_folder + fileToOpen)   
        #train_doc = []
        #position = 0
        #for i in sentences:
            #train_doc.append(position)
            #position += 1
        #train.append(train_doc)
    #print(train)
    
    
    train_output = []
    for fileToOpen in train_files:
        sentences_sum = readFile(train_target + "Sum-" + fileToOpen)
        print (fileToOpen)
        print("somario " ,sentences_sum)
        sentences =  readFile(train_folder + fileToOpen)
        print("frases" ,sentences)
        nrSentences = len(sentences)    
        current_phrase = []
        for current in sentences:
            debug = 0
            for compare in sentences_sum:
                if (compare == current):
                    sentence_output = 1
                    debug += 1
                else:
                    sentence_output = 0
            current_phrase.append(sentence_output)
            if (debug != len(sentences_sum)):
                print("error")
        train_output.append(current_phrase)
    print(train_output)
