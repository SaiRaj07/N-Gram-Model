#Assignment 2(Sentence Generation using Ngrams Model)
"""
A)Name:Sairaj Amberkar

B)The program was completely implemented by contributions exclusively from me
  without referring to any source beyond the ones taught or referred to in class.There were
   additional sources referred to and have been properly attributed.

C)The program runs without any error and provides the output as required in the assignment.

D)Problem statement:To implement a Python program that	will learn an	 N-gram model from
                    plain	text files and the program	should	generate	a	given	number	of
                    sentences based	on that N-gram model.

E)Examples:
    A)Bigram:1)To their worst commander in the neck , than what it was while the evening.
             2)The colonial industries.

    B)Trigram:1)The sheath itself is removed , its progress may be given.
              2)Certain forms of the biceps may be followed by saline solution.

    C)Quadragram:1)My hand trembled.
                 2)If it were a man he is , and you also know quite well that what I 'm saying?

G)Algorithm:1)Argumnet Parsing for ngram size, number of sentences and files names.
            2)Iterating through the files.
            3)Padding % to the end of the sentences.
            4)Generating CDF dictionary.
            5)Generating Sentences.
            6)Displaying the sentences.
H)Sources:
    A)NLTK Book
    B)Python Programming
    C)http://desilinguist.org/pdf/crossroads.pdf

I)Note:The sentences might end abruptly!!!!

"""
import time
start_time = time.time()
from nltk.probability import ConditionalFreqDist
from nltk.util import ngrams
import random
import argparse
import re
from nltk.tokenize import sent_tokenize,word_tokenize

print("***************Assignment 2 Sentence generation -Authors-Ajinkya Shivdikar and Sairaj Ambekar******************\n\n")
parser = argparse.ArgumentParser()#argument parsing
parser.add_argument("x", type=int, help="max history")#takes ngram size
parser.add_argument("y", type=int, help="max count")#takes number of sentences
parser.add_argument('li', type=str, nargs='+')#takes file names
args = parser.parse_args()
grams=args.x

####Iterate through filenames####
filenames=args.li
for fname in filenames:
    with open(str(fname)) as infile:
        for line in infile:
            allsentences=infile.read()

padend='%'  #pad '%' to end of the sentences, which indicates end of the sentence.
tokenize_sen=sent_tokenize(allsentences)
#####starts of sentences##############
listofallstarts=[]
for k in tokenize_sen:
    listofallstarts.append(re.findall(r'^(.*?)[ ]',k))
#######################################
paddedall=[]
for to in tokenize_sen:
    paddedall.append(to+padend)  #padding '%' at the end of the sentence

alljoinedpaddedall=''.join(paddedall)

wordsearch=word_tokenize(alljoinedpaddedall)

##### Generate Conditional freqency distribution dictionary##############
def generate_CFD(grams):
    emlist=[]
    for i in range(2, grams+1):
        emlist+=ngrams(wordsearch, i)
    return ConditionalFreqDist([(tuple(a), b) for *a,b in emlist])
cfd=generate_CFD(grams)
###### Generating sentences########################
def sentence_generate(root, cfd, grams,count=500): #takes root,cfd, ngram size
    for i in range(count):
        for j in range(grams-1, 0, -1):
            if tuple(root[-j:]) in cfd:           # itererate backward thorugh cfd dictionary for particular word

                cfd_values=cfd[tuple(root[-j:])].values() #key values into the variable
                sumv=sum(cfd_values)        #adding all the values

                val=random.randint(0,sumv)   #randomly picking number between zero and sum
                cfd_keys=cfd[tuple(root[-j:])].keys() #getting keys of all related words in ngram

                for key in cfd_keys:

                    val=val-cfd[tuple(root[-j:])][key]#reducing the value till we hit zero or negative

                    if val <= 0 and not key=='%':
                        root.append(key)   #append the key if value is less than or equal to zero
                        break
                break
            else:
                continue
    return root

limit=args.y
m=1
while m<=limit:
    ranletteres=random.choice(listofallstarts)
    root=ranletteres
    gen_sen=sentence_generate(root, cfd, grams) ## generating sentences

    joisentenced=' '.join(gen_sen)
    if not joisentenced and m<=limit:
        ranletteres=random.choice(listofallstarts)
        root=ranletteres
        gen_sen=sentence_generate(root, cfd, grams)
        print(' '.join(gen_sen)+'\n')
        m=m-1

    else:

        print(joisentenced+'\n')
    m=m+1
    # print("value of m:{}".format(m))
    
#Log File Generation    
file=open('lognew.txt','a+')

time="--- %s seconds ---" % (time.time() - start_time)

alllog=("Time taken{}:with ngram of: {} file names:{}\n".format(time,grams,filenames))

file.write(alllog)
file.close()


