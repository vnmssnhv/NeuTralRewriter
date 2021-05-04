"""we need depparse for sentence with 'his' to distinguish between
   'The book of his.' or 'his book'"""
import stanza


# This part works
def stanza_init(language):
    global nlp
    nlp = stanza.Pipeline(
        lang=language, processors='tokenize,mwt,pos,lemma,depparse',
        tokenize_pretokenized='true')


def rewritehisher(input_sents):
    rewritten_s = []
    punctuation = [',', ':', ';', '.', '!', '?']

    for isent in input_sents:
        end_punct = isent[-1]
        isent = isent[:-1]
        doc = nlp(isent)
        ssent = isent.split()

        for sent in doc.sentences:
            for word in sent.words:
                if word.text == 'his':
                    if word.deprel == "nmod:poss" and sent.words[word.id] \
                      not in punctuation:
                        ssent[word.id-1] = 'their'
                    else:
                        ssent[word.id-1] = 'theirs'

                if word.text == 'her' or word.text == 'her.':
                    if word.xpos == "PRP$" and word.text == 'her':
                        ssent[word.id - 1] = 'their'
                    elif word.xpos == "PRP" and "Poss=Yes" in word.feats:
                        ssent[word.id - 1] = 'their'
                    elif word.text == 'her.':
                        ssent[word.id - 1] = 'them.'
                    else:
                        ssent[word.id - 1] = 'them'
                        # print(word.feats)

        rewritten_s.append(" ".join(ssent)+end_punct)
    # print(rewritten_s)
    return(rewritten_s)


if __name__ == '__main__':
    rewritehisher(["Thank you for calling her .",
                   "Got her wrapped around my little finger .",
                   "A copy of her brain ."], "en")
