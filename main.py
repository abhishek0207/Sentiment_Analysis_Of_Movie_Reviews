import os
import nltk 
import math
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
def createDictionaryOfWords(array): 
    wordDictionary = {}
    for i in array:
        if i in wordDictionary:
            wordDictionary[i] = wordDictionary[i] + 1
        else:
            wordDictionary[i] = 1
    for i in wordDictionary:
        wordDictionary[i] = wordDictionary[i] / len(array)
    return wordDictionary

stop_words = set(stopwords.words('english'))

def preprocess(review):
    review = review.lower()
    tokenizer = word_tokenize(review)
    
    print(tokenizer)
    review_filtered = [w for w in tokenizer if not w in stop_words]
    stemmer = PorterStemmer()
    review_filtered = [stemmer.stem(w) for w in review_filtered]
    review_filtered = [word.lower() for word in review_filtered if word.isalpha()]
    return review_filtered

def scoreArray(array, final_dictionary, sentence):
    score = []
    scoreMap = {}
    finalScore = 0
    for review in array:
        scoreMap = {}
       
        for eachWord in review:
            for eachSentenceWord in sentence:
                if eachSentenceWord == eachWord:
                    if eachSentenceWord in scoreMap:
                        scoreMap[eachSentenceWord] = scoreMap[eachSentenceWord] + 1
                    else:
                        scoreMap[eachSentenceWord] = 1
        if len(scoreMap) != 0:                
            for i in scoreMap:
                finalScore = finalScore + math.log(scoreMap[i] / final_dictionary[i], 10) 
                score.append(finalScore)
    return score



MAX_LIMIT =1000
MAX_TEST_LIMIT = 10
negArray = []
negArrayWords = []
posArray = []
count = 0
negWordDictionary = {}
stemmedNeg = []
matched_pos_reviews = {}
matched_neg_reviews = []
negdirectory = r"C:\Users\abhis\Desktop\northeastern\spring\AI\project\neg"
posdirectory = r"C:\Users\abhis\Desktop\northeastern\spring\AI\project\pos"
testdirectory = r"C:\Users\abhis\Desktop\northeastern\spring\AI\project\txt_sentoken\pos"
for filename in os.listdir(negdirectory):
    count = count + 1
    if(count > MAX_LIMIT):
        break
    folder_file = negdirectory + "\\" + filename
    
    text_file = open(folder_file, "r", encoding='utf8')
   
    review = text_file.read()
    processed = preprocess(review)
    #print("new review is")
    negArray.append(processed)
    #print(str(negArray))
    #print("\n")
negWordArray =    [item for sublist in negArray for item in sublist]
        
count = 0
for filename in os.listdir(posdirectory):
    count = count + 1
    score = 0
    if(count > MAX_LIMIT):
        break
    folder_file = posdirectory + "\\" + filename
    text_file = open(folder_file, "r", encoding='utf8')
    print(str(text_file))
    review = text_file.read()
    processed = preprocess(review)
    posArray.append(processed)

posWordArray=   [item for sublist in posArray for item in sublist]
finalArray = posWordArray + negWordArray
final_dictionary = createDictionaryOfWords(finalArray)

print("******************Starting the tests and prediction*******************")
#test the data

testArray = []
count = 0
for filename in os.listdir(testdirectory):
    count = count + 1
    score = 0
    if(count > MAX_TEST_LIMIT):
        break
    folder_file = testdirectory + "\\" + filename
    text_file = open(folder_file, "r", encoding='utf8')
    test_review = text_file.read()
    testArray.append(test_review)
    
review_count = 0


#prediction logic
print("length of test data is" + str(len(testArray)))
positive_value = 0
negative_value= 0
total_positive=0
total_negative =0
fivenearestneighbours = []
for i in testArray:
    positive_value = 0
    negative_value = 0
    process_review = preprocess(i)
    positivescore = scoreArray(posArray, final_dictionary, process_review)
    positivescore = sorted(positivescore)
    positivescore = positivescore[::-1]  
    positiveneighbors = positivescore[:5]
    print("top 5 positives are")
    print(str(positiveneighbors))
    negativescore = scoreArray(negArray, final_dictionary, process_review)
    negativescore =sorted(negativescore)
    negativescore = negativescore[::-1]   
    negativeneighbors = negativescore[:5]
    print("negative neighbors are")
    print(str(negativeneighbors))
    totalKneighbors = positiveneighbors + negativeneighbors
    print("total neighbors are")
    print(str(totalKneighbors))
    totalKneighbors = sorted(totalKneighbors)
    totalKneighbors = totalKneighbors[::-1]
    print("five nearest neighbors are")
    fiveNearestneighbors = totalKneighbors[:5]
    print(str(fiveNearestneighbors))
    for i in fiveNearestneighbors:
        if i in positiveneighbors:
            positive_value +=1
        if i in negativeneighbors:
            negative_value +=1
    if positive_value > negative_value:
        total_positive += 1
    else:
        total_negative+=1
print("positive reviews are " + str(total_positive))
print("negative reviews are " + str(total_negative))
        
        
        

    


#pre processing the data from the movie reviews
