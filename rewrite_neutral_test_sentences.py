import argparse
import codecs
import stanza

from xpos import *
from depparse import rewritehisher
from genderlang import genderneutral
import language_tool_python

#Step 1: Clean OpenSubtitles Data
#OK => write down how it was cleaned

#Step 2: process
# def process_sentences(inf,lang,outf):
#     sents = read_file(inf)
#     lang, sentences = rewriteheshe(sents, lang)
#     they_sentences = rewritehisher(sentences, lang)
#     # neutral_sentences = genderlang(they_sentences)
#     cor_sentences = correctgram(they_sentences)
#     write_output(outf,cor_sentences)

# def read_file(input):
#     with codecs.open(input,'r') as inF:
#         input_sents=inF.readlines()
#     return input_sents

# def write_output(outputfile,output):
#      with codecs.open(outputfile, 'w') as outF:
#          outF.write('\n'.join(output))

def rewriteheshe(sentences,language):
    nsents=[]
    for sent in sentences:
        nsent = [word if word.lower() != 'she' and word.lower() != 'he' else 'they' for word in sent.split()]
        #nsent = [word if word != 'himself' and word != 'herself' else 'they' for word in sent.split()] #when I uncomment this, nothing works
        nsents.append(" ".join(nsent))
    return language,nsents
#strip punctuation: Seems to work better for many cases of possessive vs accusative.

#correct grammaer - they was -> they were, they is => they are + regular verbs using language model
tool = language_tool_python.LanguageTool('en-US')
def correctgram(sents):
    correct_s=[]
    for s in sents:
        s = s.replace("they was", "they were")  # the language model doesn't fix this for some reason
        s = s.replace("they is", "they are")  # the language model doesn't fix this
        s = s.replace('himself', 'themself')
        s = s.replace('herself', 'themself')
        s = s.replace('hers', 'theirs')
        s = s.replace('him', 'them')
        s = tool.correct(s)
        correct_s.append(s)
    print(correct_s)
    return correct_s

# python stanzanlp.py -i test200.en-fr.en -a upos -l en -o upos200.en-fr.en
#Step 3: Neu_t_ral Rewriting Rules


#Neutral Rewriter Rules

# if __name__ == '__main__':
#      # USAGE: python rewrite_neutral.py -i inputF -l en -o outputF
#      parser = argparse.ArgumentParser(description='parse sentences using stanzaNLP')
#      parser.add_argument("-i", "--input_file", required=True)                            #inputfile format: one sentence per line
#      parser.add_argument("-l", "--language", required=True)                              #e.g. en (English), it (Italian)...
#      parser.add_argument("-o", "--output_file", required=False)
#      args = parser.parse_args()
#      process_sentences(args.input_file, args.language, args.output_file)


testsentences=["The farmer gave the teacher a bag of effs and thanked her for teaching him."]

lang, sentences = rewriteheshe(testsentences,"en")
they_sentences = rewritehisher(sentences,"en")
# neutral_sentences = genderlang(they_sentences)
cor_sentences = correctgram(they_sentences)

