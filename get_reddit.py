import re
import csv

import json
from tqdm import tqdm
from glob import glob
from multiprocessing import Pool


def preprocess_sent(sent):
    sent = ' '.join(sent.replace('\n', ' ').split())
    if sent[0] == ' ':
        sent = sent[1:]
    if sent[-1] not in ['.', ',', '?', '!', '*']:
        sent = sent + '.'
    return sent


def find_gender_in_reddit(reddit_object):
    _id, text = reddit_object['id'], reddit_object['body']
    sents = re.split(r'\.|\?|\!', text)
    for sent in sents:
        if re.findall(
          r'(?:[^A-Za-z0-9]+)([sS]*[Hh])(e|is|er|im|[^A-Za-z0-9]){1}' +
          r'(self|s)*[^A-Za-z0-9]', sent):
            yield _id, preprocess_sent(sent)


def iter_file(file_name):
    try:
        if 'zst' not in file_name and 'bz2' not in file_name:
            open_func = open
        elif 'bz2' in file_name:
            import bz2
            open_func = bz2.open
        else:
            return
        for line in tqdm(open_func(file_name, 'r')):
            yield json.loads(line)
    except Exception as e:
        print(f"Error in: {e}")


def reddit_gender(f):
    csv_writer = csv.writer(open('./reddit_gender.csv', 'a'), delimiter=',',
                            quotechar="'", quoting=csv.QUOTE_ALL)
    for reddit_object in iter_file(f):
        for _id, sent in find_gender_in_reddit(reddit_object):
            csv_writer.writerow([_id, sent])
            # print(_id, sent)


if __name__ == '__main__':
    test_sent = ["Hi! I thought he was lame & he thought she was the best.",
                 "This has a his and hers, so she can wash her face while" +
                 "he gives himself a shave there ."]
    # for sent in test_sent:
    #     print(sent)
    #     print(re.findall(
    #             r'(?:[^A-Za-z0-9]+)([sS]*[Hh])(e|is|er|im|[^A-Za-z0-9])+' +
    #             r'(self|s)*[^A-Za-z0-9]', sent))
    with Pool(10) as p:
        p.map(reddit_gender, glob('/data/reddit/*2019*'))