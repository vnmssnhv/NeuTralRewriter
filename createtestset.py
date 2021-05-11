
# Retrieve he, she, him, his, her, hers, himself, themself sentences
import codecs
import argparse

def maketestset(infile, outfile, pronoun_count):
     sentences = read_file(infile)
     testset= find_sents(sentences, pronoun_count)
     print(len(testset))
     write_output(outfile,testset)

def read_file(input):
    with codecs.open(input,'r') as inF:
        input_sents=inF.readlines()
    return input_sents

def write_output(outputfile,output):
     with codecs.open(outputfile, 'w') as outF:
         outF.write(''.join(output))

def find_sents(sentences, totcount):
     hecounter=0
     shecounter=0
     hercounter=0
     herscounter=0
     hiscounter=0
     himcounter=0
     himselfcounter=0
     herselfcounter=0

     totalcounter=0

     testset = []

     for sent in sentences:
          addSent=False

          if totalcounter < totcount:
               if hecounter < totcount/8:
                    if ' he ' in sent.lower():
                         addSent = True
                         hecount = countOccurences(sent, 'he')
                         hecounter += hecount
                         totalcounter += hecount

               if shecounter < totcount/8:
                    if ' she ' in sent.lower():
                         addSent = True
                         shecount = countOccurences(sent, 'she')
                         shecounter += shecount
                         totalcounter += shecount

               if hercounter < totcount/8:
                    if ' her ' in sent.lower():
                         addSent = True
                         hercount = countOccurences(sent, 'her')
                         hercounter += hercount
                         totalcounter += hercount

               if hiscounter < totcount/8:
                    if ' his ' in sent.lower():
                         addSent = True
                         hiscount = countOccurences(sent, 'his')
                         hiscounter += hiscount
                         totalcounter += hiscount

               if herscounter < totcount/8:
                    if ' hers ' in sent.lower():
                         addSent = True
                         herscount = countOccurences(sent, 'hers')
                         herscounter += herscount
                         totalcounter += herscount

               if himcounter < totcount/8:
                    if ' him ' in sent.lower():
                         addSent = True
                         himcount = countOccurences(sent, 'him')
                         himcounter += himcount
                         totalcounter += himcount

               if herselfcounter < totcount/8:
                    if ' herself ' in sent.lower():
                         addSent = True
                         herselfcount = countOccurences(sent, 'herself')
                         herselfcounter += herselfcount
                         totalcounter += herselfcount

               if himselfcounter < totcount/8:
                    if ' himself ' in sent.lower():
                         addSent = True
                         himselfcount = countOccurences(sent, 'himself')
                         himselfcounter += himselfcount
                         totalcounter += himselfcount

               if addSent == True:
                    testset.append(sent)

     #print("hecounter: " + str(hecounter) + "\n" + "shecounter: " + str(shecounter) + "\n" \
     #     "hercounter: " + str(hercounter) + "\n" + "himcounter: " + str(himcounter) + "\n" \
     #     "herscounter: " + str(herscounter) + "\n" + "hiscounter: " + str(hiscounter) + "\n" \
     #     "herselfcounter: " + str(herselfcounter) + "\n" + "himselfcounter: " + str(himselfcounter) + "\n" \
     #     "totalcounter: " + str(totalcounter))
     #print(testset)
     return testset

def countOccurences(str, word):
     # split the string by spaces in a
     a = str.lower().split(" ")
     #print(str)
     # search for pattern in a
     count = 0
     for i in range(0, len(a)):

          # if match found increase count
          if (word == a[i]):
               count = count + 1
     return count

if __name__ == '__main__':
     # USAGE: python createtestset.py -i inputF -o outputF
     parser = argparse.ArgumentParser(description='parse sentences using stanzaNLP')
     parser.add_argument("-i", "--input-file", required=True)
     parser.add_argument("-t", "--pronoun-count", required=False, default=1000)
     parser.add_argument("-o", "--output-file", required=True)
     args = parser.parse_args()
     maketestset(args.input_file, args.output_file, int(args.pronoun_count))
