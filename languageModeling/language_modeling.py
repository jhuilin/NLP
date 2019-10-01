import os
import sys
import math

# insert word as key and its frequencey as value into a dic
def record_words(lines,words):
    for word in lines.split():
        if word in words:
            words[word] += 1
        else:
            words[word] = 1

def calculate_tokens_types_not_occur(nf,testWords,trainWords,tokens,types):
    check = {}
    for line in nf:
        record_words(line,testWords)
        for word in line.split():
            if word not in trainWords:
                if word not in tokens:
                    tokens[word] = 1
                else:
                    tokens[word] += 1

                if word not in types:
                    types.append(word)
            else:
                if word in check:
                    if check[word] == testWords[word]:
                        if word in tokens:
                            tokens[word] += 1
                        else:
                            tokens[word] = 1
                    else:
                        check[word] += 1
                else:
                    check[word] = 1
    check.clear()
    nf.close()

def replace_unk(fp,nf,list):
    index = 0
    for line in fp:
        while list[index] in line.split():
            line = line.replace(list[index],"<unk>")
            index += 1
        nf.write(line + '\n')
    nf.close()

def get_bigram(line,bigram):
    line = line.split()
    length = len(line) - 1
    for i in range(length):
        temp = (line[i],line[i+1])
        if not temp in bigram:
            bigram[temp] = 1
        else:
            bigram[temp] += 1

def calculate_bigram_tokens_types_not_occur(nf,testBigram,trainBigram,tokenBigram,typeBigram):
    check = {}
    for line in nf:
        get_bigram(line,testBigram)
        line = line.split()
        length = len(line) - 1
        for i in range(length):
            temp = (line[i],line[i+1])
            if not temp in trainBigram:
                if not temp in tokenBigram:
                    tokenBigram[temp] = 1
                else:
                    tokenBigram[temp] += 1
                if not temp in typeBigram:
                    typeBigram.append(temp)
            else:
                if temp in check:
                    if check[temp] == testBigram[temp]:
                        if temp in tokenBigram:
                            tokenBigram[temp] += 1
                        else:
                            tokenBigram[temp] = 1
                    else:
                        check[temp] += 1
                else:
                    check[temp] = 1
    check.clear()
    nf.close()

def add_one_smoothing(bigram):
    for temp in bigram:
        bigram[temp] += 1

def string_replace_unk(sentence,words):
    for index in range(len(sentence)):
        if sentence[index] not in words:
            first[index] = "<unk>"
    return " ".join(sentence)

def unigram(log,sentenceWords,words):
    for word in sentenceWords:
        if word != "<unk>":
            if word in words:
                temp = round(math.log(words[word]/sum(words.values()),2),2)
                log.append(temp)

def call_bigram(log, sentenceBigram, bigram):
    for temp in sentenceBigram:
        temp = round(math.log(sentenceBigram[temp]/sum(bigram.values())),2)
        log.append(temp)

def pre_process(files):

    pre = "<s> "
    post =" </s>"
    words = {}
    bigram = {}

    brownWords = {}
    noBrownTokens = {}
    noBrownTypes = []
    brownBigram = {}
    noBrownTokensBigram = {}
    noBrownTypesBigram = []
    brownLog = []
    brownBigramLog = []
    brownSmoothLog = []

    learnerWords = {}
    noLearnerTokens = {}
    noLearnerTypes = []
    learnerBigram = {}
    noLearnerTokensBigram = {}
    noLearnerTypesBigram = []
    learnerLog = []
    learnerBigramLog = []
    learnerSmoothLog = []



    # check if file exist ot not
    for f in files:
        if not os.path.isfile(f):
            print("file {} doesnt exist".format(f))
            sys.exit

    for f in files:
        with open(f) as fp:
            nf = open(f"new_{f}","w")
            for line in fp:
                nf.write(pre + line.lower().strip() + post + '\n')
            nf.close()

        if f == "brown-train.txt":
            nf = open(f"new_{f}","r")
            for line in nf:
                record_words(line,words)
            
            # total tokens in the txt
            cnt = sum(words.values())

            # get the words only appear once in the txt
            onceWords = [word for word in words.keys() if words.get(word) == 1] 

            # total number of words - words only appear once (unk) + 1
            # +1 because all words appear once only count as 1
            typeWords = len(words) - len(onceWords) + 1 

            nf.close()

        if f == "brown-test.txt":
            nf = open(f"new_{f}","r")
            calculate_tokens_types_not_occur(nf,brownWords,words,noBrownTokens,noBrownTypes)
            brownCnt = sum(brownWords.values())
            onceBrownWords = [word for word in brownWords.keys() if brownWords.get(word) == 1] 

        if f == "learner-test.txt":
            nf = open(f"new_{f}","r")
            calculate_tokens_types_not_occur(nf,learnerWords,words,noLearnerTokens,noLearnerTypes)
            learnerCnt = sum(learnerWords.values())
            onceLearnerWords = [word for word in learnerWords.keys() if learnerWords.get(word) == 1] 


    for f in files:
        with open(f"new_{f}") as fp:
            if f == "brown-train.txt":
                nf = open(f"unk_{f}","w")
                replace_unk(fp,nf,onceWords)
                nf = open(f"unk_{f}","r")
                for line in nf:
                    get_bigram(line,bigram)
                nf.close()

            if f == "brown-test.txt":
                nf = open(f"unk_{f}","w")
                replace_unk(fp,nf,noBrownTypes)
                nf = open(f"unk_{f}","r")
                calculate_bigram_tokens_types_not_occur(nf,brownBigram,bigram,noBrownTokensBigram,noBrownTypesBigram)

            if f == "learner-test.txt":
                nf = open(f"unk_{f}","w")
                replace_unk(fp,nf,noLearnerTypes) 
                nf = open(f"unk_{f}","r")
                calculate_bigram_tokens_types_not_occur(nf,learnerBigram,bigram,noLearnerTokensBigram,noLearnerTypesBigram)

    # unigram(brownLog,brownWords,words)
    # call_bigram(brownBigramLog,brownBigram,bigram)
    # brownSmooth = brownBigram.copy()
    # add_one_smoothing(brownSmooth)
    # call_bigram(brownSmoothLog,brownSmooth,bigram)

    firstLog = []
    firstBigramLog = []
    firstWords = {}
    firstUnigram = {}
    firstBigram = {}
    firstSmooth = {}
    firstSmoothLog = []
    first = "<s> he was laughed off the screen . </s>"

    secondLog = []
    secondBigramLog = []
    secondWords = {}
    secondUnigram = {}
    secondBigram = {}
    secondSmooth = {}
    secondSmoothLog = []
    second = "<s> there was no compulsion behind them . </s>"

    thirdLog = []
    thirdBigramLog = []
    thirdWords = {}
    thirdUnigram = {}
    thirdBigram = {}
    thirdSmooth = {}
    thirdSmoothLog = []
    third = "<s> i look forward to hearing your reply . </s>"


    first = first.split()
    first = string_replace_unk(first,words)
    record_words(first,firstWords)
    unigram(firstLog,firstWords,words)
    get_bigram(first,firstBigram)
    call_bigram(firstBigramLog,firstBigram,bigram)

    second = second.split()
    second = string_replace_unk(second,words)
    record_words(second,secondWords)
    unigram(secondLog,secondWords,words)
    get_bigram(second,secondBigram)
    call_bigram(secondBigramLog,secondBigram,bigram)

    third = third.split()
    third= string_replace_unk(third,words)
    record_words(third,thirdWords)
    unigram(thirdLog,thirdWords,words)
    get_bigram(third,thirdBigram)
    call_bigram(thirdBigramLog,thirdBigram,bigram)

    firstSmooth = firstBigram.copy()
    add_one_smoothing(firstSmooth)
    call_bigram(firstSmoothLog,firstSmooth,bigram)

    secondSmooth = secondBigram.copy()
    add_one_smoothing(secondSmooth)
    call_bigram(secondSmoothLog,secondSmooth,bigram)

    thirdSmooth = thirdBigram.copy()
    add_one_smoothing(thirdSmooth)
    call_bigram(thirdSmoothLog,thirdSmooth,bigram)


    unigram(brownLog,brownWords,words)
    call_bigram(brownBigramLog,brownBigram,bigram)
    brownSmooth = brownBigram.copy()
    add_one_smoothing(brownSmooth)
    call_bigram(brownSmoothLog,brownSmooth,bigram)

    unigram(learnerLog,learnerWords,words)
    call_bigram(learnerBigramLog,learnerBigram,bigram)
    learnerSmooth = learnerBigram.copy()
    add_one_smoothing(learnerSmooth)
    call_bigram(learnerSmoothLog,learnerSmooth,bigram)


    try:
        brownTokensPercentage = sum(noBrownTokens.values())/brownCnt * 100
        brownTypePercentage = len(noBrownTypes)/ len(brownWords) * 100
        learnerTokensPercentage = sum(noLearnerTokens.values())/learnerCnt * 100
        learnerTypePercentage = len(noLearnerTypes)/ len(learnerWords) * 100

        brownTokensBigramPercentage = sum(noBrownTokensBigram.values())/ sum(brownBigram.values()) * 100
        brownTypesBigramPercentage = len(noBrownTypesBigram)/ len(brownBigram) * 100
        learnerTokensBigramPercentage = sum(noLearnerTokensBigram.values())/ sum(learnerBigram.values()) * 100
        learnerTypesBigramPercentage = len(noLearnerTypesBigram)/ len(learnerBigram) * 100
    except ZeroDivisionError as e:
        print(e)

    print('total word types (unique workd) in the training corpus is: '+ str(typeWords) + '\n')
    print('total word tokens are there in training corpus is: '+ str(cnt) + '\n')
    print('\n')
    print('percentage of word tokens in brown-test.txt did not occur is: ' + str(round(brownTokensPercentage,4)) +'%' + '\n')
    print('percentage of word type in brown-test.txt did not occur is: ' + str(round(brownTypePercentage,4)) + '%' + '\n')
    print('percentage of word tokens in learner-test.txt did not occur is: ' + str(round(learnerTokensPercentage,4)) +'%' + '\n')
    print('percentage of word type in learner-test.txt did not occur is: ' + str(round(learnerTypePercentage,4)) + '%' + '\n')
    print('\n')
    print('percentage of bigram tokens in brown-test.txt did not occur is: ' + str(round(brownTokensBigramPercentage,4)) +'%' + '\n')
    print('percentage of bigram type in brown-test.txt did not occur is: ' + str(round(brownTypesBigramPercentage,4)) + '%' + '\n')
    print('percentage of bigram tokens in learner-test.txt did not occur is: ' + str(round(learnerTokensBigramPercentage,4)) +'%' + '\n')
    print('percentage of bigram type in learner-test.txt did not occur is: ' + str(round(learnerTypesBigramPercentage,4)) + '%' + '\n')
    print('\n')
    print("unigram:")
    print(first)
    print('log2(p(<s>))+log2(p(<he>))+log2(p(<was>))+log2(p(<langhed>))+log2(p(<off>))+log2(p(<the>))+log2(p(<screen>))+log2(p(<.>))+log2(p(</s>))')
    print(str(firstLog[0]) + str(firstLog[1]) + str(firstLog[2]) + str(firstLog[3]) + str(firstLog[4]) + str(firstLog[5]) + str(firstLog[6]) + str(firstLog[7]) + str(firstLog[8]) + " = " +str(sum(firstLog)))
    print(second)
    print('log2(p(<s>))+log2(p(<there>))+log2(p(<is>))+log2(p(<no>))+log2(p(<compulsion>))+log2(p(<behind>))+log2(p(<them>))+log2(p(<.>))+log2(p(</s>))')
    print(str(secondLog[0]) + str(secondLog[1]) + str(secondLog[2]) + str(secondLog[3]) + str(secondLog[4]) + str(secondLog[5]) + str(secondLog[6]) + str(secondLog[7]) + str(secondLog[8]) +  " = " +str(round(sum(secondLog),2)))
    print(third)
    print('log2(p(<s>))+log2(p(<he>))+log2(p(<was>))+log2(p(<langhed>))+log2(p(<off>))+log2(p(<the>))+log2(p(<screen>))+log2(p(<.>))+log2(p(</s>))')
    print(str(thirdLog[0]) + str(thirdLog[1]) + str(thirdLog[2]) + str(thirdLog[3]) + str(thirdLog[4]) + str(thirdLog[5]) + str(thirdLog[6]) + str(thirdLog[7]) + str(thirdLog[8]) + str(thirdLog[9]) +" = " +str(sum(thirdLog)))
    print("bigram:")
    print('log2(p(<he>|<s>))+log2(p(<was>|<he>))+log2(p(<langhed>|<was>))+log2(p(<off>|<langhed>))+log2(p(<the>|<off>))+log2(p(<screen>|<the>))+log2(p(<.>|<screen>))+log2(p(</s>|<.>))')
    print(str(firstBigramLog[0]) + str(firstBigramLog[1]) + str(firstBigramLog[2]) + str(firstBigramLog[3]) + str(firstBigramLog[4]) + str(firstBigramLog[5]) + str(firstBigramLog[6]) + str(firstBigramLog[7]) + " = " +str(round(sum(firstBigramLog),2)))
    print('log2(p(<there>|<s>))+log2(p(<was>|<there>))+log2(p(<no>|<was>))+log2(p(<compulsion>|<no>))+log2(p(<behind|<compulsion>))+log2(p(<them>|<behind>))+log2(p(<.>|<them>))+log2(p(</s>|<.>))')
    print(str(secondBigramLog[0]) + str(secondBigramLog[1]) + str(secondBigramLog[2]) + str(secondBigramLog[3]) + str(secondBigramLog[4]) + str(secondBigramLog[5]) + str(secondBigramLog[6]) + str(secondBigramLog[7]) + " = " +str(round(sum(secondBigramLog),2)))
    print('log2(p(<i>|<s>))+log2(p(<look>|<i>))+log2(p(<forward>|<look>))+log2(p(<to>|<forward>))+log2(p(<hearing>|<to>))+log2(p(<your>|<hearing>))+log2(p(reply|<your>))+log2(p(<.>|<replay>))log2(p(</s>|<.>))')
    print(str(thirdBigramLog[0]) + str(thirdBigramLog[1]) + str(thirdBigramLog[2]) + str(thirdBigramLog[3]) + str(thirdBigramLog[4]) + str(thirdBigramLog[5]) + str(thirdBigramLog[6]) + str(thirdBigramLog[7]) + str(thirdBigramLog[8]) +" = " +str(round(sum(thirdBigramLog),2)))
    print("add_smooth one:")
    print('log2(p(<he>|<s>))+log2(p(<was>|<he>))+log2(p(<langhed>|<was>))+log2(p(<off>|<langhed>))+log2(p(<the>|<off>))+log2(p(<screen>|<the>))+log2(p(<.>|<screen>))+log2(p(</s>|<.>))')
    print(str(firstSmoothLog[0]) + str(firstSmoothLog[1]) + str(firstSmoothLog[2]) + str(firstSmoothLog[3]) + str(firstSmoothLog[4]) + str(firstSmoothLog[5]) + str(firstSmoothLog[6]) + str(firstSmoothLog[7]) + " = " +str(round(sum(firstSmoothLog),2)))
    print('log2(p(<there>|<s>))+log2(p(<was>|<there>))+log2(p(<no>|<was>))+log2(p(<compulsion>|<no>))+log2(p(<behind|<compulsion>))+log2(p(<them>|<behind>))+log2(p(<.>|<them>))+log2(p(</s>|<.>))')
    print(str(secondSmoothLog[0]) + str(secondSmoothLog[1]) + str(secondSmoothLog[2]) + str(secondSmoothLog[3]) + str(secondSmoothLog[4]) + str(secondSmoothLog[5]) + str(secondSmoothLog[6]) + str(secondSmoothLog[7]) + " = " +str(round(sum(secondSmoothLog),2)))
    print('log2(p(<i>|<s>))+log2(p(<look>|<i>))+log2(p(<forward>|<look>))+log2(p(<to>|<forward>))+log2(p(<hearing>|<to>))+log2(p(<your>|<hearing>))+log2(p(reply|<your>))+log2(p(<.>|<replay>))log2(p(</s>|<.>))')
    print(str(thirdSmoothLog[0]) + str(thirdSmoothLog[1]) + str(thirdSmoothLog[2]) + str(thirdSmoothLog[3]) + str(thirdSmoothLog[4]) + str(thirdSmoothLog[5]) + str(thirdSmoothLog[6]) + str(thirdSmoothLog[7]) + str(thirdSmoothLog[8]) +" = " +str(round(sum(thirdSmoothLog),2)))
    print('\n')

    firstPerplexities = round(2**(-1*(sum(firstLog)/len(first))),2)
    secondPerplexities = round(2**(-1*(sum(secondLog)/len(second))),2)
    thirdPerplexities = round(2**(-1*(sum(thirdLog)/len(third))),2)
    print("unigram perplexities for first sentence is: "+ str(firstPerplexities))
    print("unigram perplexities for second sentence is: "+ str(secondPerplexities))
    print("unigram perplexities for third sentence is: "+ str(thirdPerplexities))
    firstPerplexities = round(2**(-1*(sum(firstBigramLog)/len(first))),2)
    secondPerplexities = round(2**(-1*(sum(secondBigramLog)/len(second))),2)
    thirdPerplexities = round(2**(-1*(sum(thirdBigramLog)/len(third))),2)
    print("bigram perplexities for first sentence is: "+ str(firstPerplexities))
    print("bigram perplexities for second sentence is: "+ str(secondPerplexities))
    print("bigram perplexities for third sentence is: "+ str(thirdPerplexities))
    firstPerplexities = round(2**(-1*(sum(firstSmoothLog)/len(first))),2)
    secondPerplexities = round(2**(-1*(sum(secondSmoothLog)/len(second))),2)
    thirdPerplexities = round(2**(-1*(sum(thirdSmoothLog)/len(third))),2)
    print("bigram add one smooth perplexities for first sentence is: "+ str(firstPerplexities))
    print("bigram add one smooth perplexities for second sentence is: "+ str(secondPerplexities))
    print("bigram add one smooth perplexities for third sentence is: "+ str(thirdPerplexities))
    print('\n')

    bl = -1 * sum(brownLog)/brownCnt
    ll = -1 * sum(learnerLog)/learnerCnt
    brownPerplexities = round(2**bl,4)
    learnerPerplexities = round(2**ll,4)
    print("unigram perplexities for brown.txt sentence is: "+ str(brownPerplexities))
    print("unigram perplexities for learner.txt sentence is: "+ str(learnerPerplexities))

    bl = -1 * sum(brownBigramLog)/brownCnt
    ll = -1 * sum(learnerBigramLog)/learnerCnt
    brownPerplexities = round(2**bl,4)
    learnerPerplexities = round(2**ll,4)
    print("bigram perplexities for brown.txt sentence is: "+ str(brownPerplexities))
    print("bigram perplexities for learner.txt sentence is: "+ str(learnerPerplexities))

    bl = -1 * sum(brownSmoothLog)/brownCnt
    ll = -1 * sum(learnerSmoothLog)/learnerCnt
    brownPerplexities = round(2**bl,4)
    learnerPerplexities = round(2**ll,4)
    print("bigram add one smooth perplexities for brown.txt sentence is: "+ str(brownPerplexities))
    print("bigram add one smooth perplexities for learner.txt sentence is: "+ str(learnerPerplexities))




def main():


    # user input the txt
    brownTrain = sys.argv[1]
    brownTest = sys.argv[2]
    learnTest = sys.argv[3]
    files = (brownTrain, brownTest, learnTest)
    pre_process(files)

if __name__ == "__main__":
    main()