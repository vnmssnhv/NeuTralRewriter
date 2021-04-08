#we need xpos for ambiguity 'her' possessive vs determiner

import codecs
import stanza

def get_parses(input_file,annotation, language):
    input_sents = read_file(input_file)
    parses = fixposparse(input_sents,language)
    return input_sents,parses

def read_file(input_file):
    with codecs.open(input_file,'r') as inF:
        input_sents=inF.readlines()
    return input_sents

def fixposparse(input_sents,language):
    nlp = stanza.Pipeline(lang=language, processors='tokenize,mwt,pos')
    parses=[]
    counter = 0

    if 'xpos' in annotation:
        for sent in input_sents:
            doc=nlp(sent)
            parse_sent = [f'{word.xpos}' for sentence in doc.sentences for word in sentence.words]
            parses.append(" ".join(parse_sent))


    if 'feats' in annotation:
        for sent in input_sents:
            doc = nlp(sent)
            parse_sent = [f'{word.feats}' for sentence in doc.sentences for word in sentence.words]
            parses.append(" ".join(parse_sent))
    return parses

# def write_file(parses,outputfile):
#     with codecs.open(outputfile, 'w') as outF:
#         outF.write('\n'.join(parses))
