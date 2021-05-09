import re
import csv
import json

# reproducibility bit ----------------
from random import seed; seed(42)
from numpy.random import seed as np_seed; np_seed(42)
import os; os.environ['PYTHONHASHSEED'] = str(42)
# -----------------------------------

from tqdm import tqdm


class DataLoader(object):

    def __init__(self):
        pass


class RedditLoader(DataLoader):

    def __init__(self):
        pass

    def preprocess_sent(self, sent):
        sent = ' '.join(sent.replace('\n', ' ').split())
        if sent[0] == ' ':
            sent = sent[1:]
        if sent[-1] not in ['.', ',', '?', '!', '*']:
            sent = sent + '.'
        return sent

    def find_gender_in_reddit(self, reddit_object):
        _id, text = reddit_object['id'], reddit_object['body']
        sents = re.split(r'\.|\?|\!', text)
        for sent in sents:
            # NOTE: this should be replaced with get_sample regex
            if re.findall(
              r'(?:[^A-Za-z0-9]+)([sS]*[Hh])(e|is|er|im|[^A-Za-z0-9]){1}' +
              r'(self|s)*[^A-Za-z0-9]', sent):
                yield _id, self.preprocess_sent(sent)

    def iter_file(self, file_name):
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

    def reddit_gender(self, f):
        csv_writer = csv.writer(open('./reddit_gender.csv', 'a'), delimiter=',',
                                quotechar="'", quoting=csv.QUOTE_ALL)
        for reddit_object in self.iter_file(f):
            for _id, sent in self.find_gender_in_reddit(reddit_object):
                csv_writer.writerow([_id, sent])
                # print(_id, sent)

    def get_sample(self):
        import random

        data = {}
        samples = {}
        for i, *row in tqdm(enumerate(
          csv.reader(open('./reddit_gender.csv', 'r'),
                     delimiter=',', quotechar="'", quoting=csv.QUOTE_ALL))):
            _id, sent = row[0]
            data[i] = (_id, sent)
            for hit in re.findall(
              r'(?:[^A-Za-z0-9]+)([sS]he|[hH]e|[hH]is|[hH]im|[hH]er|[hH]ers|' +
              r'[hH]imself|[hH]erself]){1}[^A-Za-z0-9]', sent):
                form = ''.join(hit).lower()
                if form == 'hisself':  # nope
                    continue
                if not samples.get(form):
                    samples[form] = []
                samples[form].append(i)

        sample_idx = []
        print("forms:", {k: len(v) for k, v in samples.items()})
        with open('./reddit_test.csv', 'w') as fo:
            with open('./reddit_test_ids.csv', 'w') as _fo:
                for sample in samples:
                    for instance in random.sample(samples[sample], 80):
                        sample_idx.append(instance)
                        fo.write(data[instance][1] + '\n')
                        _fo.write(str(instance) + '\n')

        csv_writer = csv.writer(open('./reddit_train.csv', 'w'), delimiter=',',
                                quotechar="'", quoting=csv.QUOTE_ALL)
        for i, (_id, sent) in tqdm(data.items()):
            if i not in sample_idx:
                csv_writer.writerow([_id, sent])


if __name__ == '__main__':
    # from glob import glob
    # from multiprocessing import Pool
    # get_sample()
    pass
