"""we need depparse for sentence with 'his' to distinguish between
   'The book of his.' or 'his book'"""
import stanza


# This part works
def stanza_init(language):
    global nlp
    nlp = stanza.Pipeline(
        lang=language, processors='tokenize,mwt,pos,lemma,depparse',
        tokenize_pretokenized='true')


def rewritehisher(input_sents, advanced=False):
    rewritten_s = []
    # punctuation = [',', ':', ';', '.', '!', '?']

    for isent in input_sents:
        # if I change the tokenize/lowercase,
        # I need to fix this punctuation stuff too
        # end_punct=isent[-1]
        # isent=isent[:-1]
        doc = nlp(isent)
        # print(doc)
        ssent = isent.split()

        for sent in doc.sentences:
            for word in sent.words:
                if word.text == 'his' or word.text == 'His':
                    if word.deprel == "nmod:poss" and word.text == 'his':
                        # and sent.words[word.id] not in punctuation:
                        ssent[word.id-1] = 'their'
                    elif word.deprel == "nmod:poss" and word.text == 'His':
                        # and sent.words[word.id] not in punctuation:
                        ssent[word.id-1] = 'Their'
                    else:
                        ssent[word.id-1] = 'theirs'

                if word.text == 'her' or word.text == 'her.' \
                   or word.text == 'Her':
                    if word.xpos == "PRP$" and word.text == 'her':
                        ssent[word.id - 1] = 'their'
                    elif word.xpos == "PRP" and "Poss=Yes" in word.feats:
                        ssent[word.id - 1] = 'their'
                    elif word.xpos == "PRP$" and word.text == 'Her':
                        ssent[word.id - 1] = 'Their'
                    elif word.xpos == "PRP" and "Poss=Yes" in word.feats:
                        ssent[word.id - 1] = 'Their'
                    elif word.text == 'her.':
                        ssent[word.id - 1] = 'them.'
                    else:
                        ssent[word.id - 1] = 'them'

                if word.text == 'himself' or word.text == 'herself':
                    ssent[word.id-1] = 'themselves'

                if word.text == 'hers':
                    ssent[word.id-1] = 'theirs'

                if word.text == 'him':
                    ssent[word.id-1] = 'them'

        rewritten_s.append(" ".join(ssent))  # +end_punct)
    return(rewritten_s)
