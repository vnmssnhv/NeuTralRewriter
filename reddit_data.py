import re
import csv
import json

# reproducibility bit ----------------
from random import seed; seed(42)
from numpy.random import seed as np_seed; np_seed(42)
import os; os.environ['PYTHONHASHSEED'] = str(42)
# -----------------------------------

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


def get_sample():
    import random

    data = {}
    samples = {}
    for i, (_id, sent) in enumerate(
      csv.reader(open('./reddit_gender.csv', 'r'))):
        data[i] = sent
        for hit in re.findall(
          r'(?:[^A-Za-z0-9]+)([sS]*[Hh])(e|is|er|im|[^A-Za-z0-9]){1}' +
          r'(self|s)*[^A-Za-z0-9]', sent):
            form = ''.join(hit)
            if not samples.get(form):
                samples[form] = []
            samples[form].append(_id)

    with open('./reddit_test.csv', 'w') as fo:
        for sample in samples:
            for instance in random.sample(samples[sample], n=50):
                fo.write(data[instance])


if __name__ == '__main__':
    get_sample()