import argparse
import codecs

from depparse import rewritehisher, stanza_init
from genderlang import genderneutral
import language_tool_python


def process_sentences(inf, lang, outf, advanced=False):
    sents = read_file(inf)
    stanza_init(lang)
    lang, sentences = rewriteheshe(sents, lang)
    they_sentences = rewritehisher(sentences)
    if advanced:
        they_sentences = genderneutral(they_sentences)
    corrected = correctgram(they_sentences)
    write_output(outf, corrected)


def read_file(input_file):
    with codecs.open(input_file, 'r') as inF:
        input_sents = inF.readlines()
    return input_sents


def write_output(outputfile, output):
    with codecs.open(outputfile, 'w') as outF:
        outF.write('\n'.join(output))


def rewriteheshe(sentences, language):
    nsents = []
    for sent in sentences:
        nsent = [word if word.lower() != 'she' and word.lower() != 'he' else 
                 'they' if word == "she" or word == "he" else "They" 
                 for word in sent.split()]
        nsents.append(" ".join(nsent))
    return language, nsents


tool = language_tool_python.LanguageTool('en-US')


def correctgram(sents):
    correct_s = []
    for s in sents:
        s = s.replace('they is ', 'they are ')
        s = s.replace('They is ', ' They are ')
        s = s.replace('They was ', 'They were ')
        s = s.replace('they was ', 'they were ')
        s = s.replace('They wasn ', 'They weren ')
        s = s.replace('they wasn ', 'they weren ')
        s = s.replace("they 's ", "they are ")
        s = s.replace("They 's ", "They are ")
        s = s.replace("They does ", "They do ")
        s = s.replace("they does ", "they do ")
        matches = tool.check(s)
        # correct only grammar issues
        new_matches = [match for match in matches if
                       match.category == 'GRAMMAR']
        s = language_tool_python.utils.correct(s, new_matches)  #
        s = s.replace("'t 't", " 't")
        s = s.replace("they doesn", "they don")
        s = s.replace("They doesn", "They don")
        s = s.replace('they isn ', 'they aren ')
        s = s.replace('They isn ', ' They aren ')
        s = s.replace("they hasn", "they haven")
        s = s.replace("They hasn", "They haven")
        correct_s.append(s)
    return correct_s


if __name__ == '__main__':
    # USAGE: python rewrite_neutral.py -i inputF -l en -o outputF
    parser = argparse.ArgumentParser(
        description='parse sentences using stanzaNLP')
    parser.add_argument("-i", "--input_file", required=True)
    parser.add_argument("-l", "--language", required=True,  # EN only v
                        help="Specify language code, e.g. en, es, fr...")
    parser.add_argument("-a", "--advanced", required=False, default=False,
                        action='store_true',
                        help="Invokes the more advanced rewriting")
    parser.add_argument("-o", "--output_file", required=False)
    args = parser.parse_args()
    process_sentences(args.input_file, args.language, args.output_file,
                      args.advanced)
