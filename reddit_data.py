import csv
import json
import random
import re

from tqdm import tqdm
from glob import glob

# reproducibility bit ----------------
from random import seed
from numpy.random import seed as np_seed
import os
seed(42)
np_seed(42)
os.environ['PYTHONHASHSEED'] = str(42)
# -----------------------------------


class DataLoader(object):

    def __init__(self, file_name_in, file_name_out):
        """General DataLoader class for loading and filtering sentences.

        Parameters
        ----------
        file_name_in : str
            Full path to input file to read.
        file_name_out : str
            Full path to file to read.
        """
        self.file_name_in = file_name_in
        self.file_name_out = file_name_out

    @staticmethod
    def find_gender(text):
        """Regex to find gendered text."""
        return re.findall(r'(?:[^A-Za-z0-9]+)' +
                          r'([sS]he|[hH]e|[hH]is|[hH]im|' +
                          r'[hH]er|[hH]ers|[hH]imself|[hH]erself]){1}' +
                          r'[^A-Za-z0-9]', text)

    def _iter(self):
        """Iter through sentences yielding sent if it contains gender."""
        with open(self.file_name_in, 'r') as fo:
            for sent in tqdm(fo.readlines()):
                if self.find_gender(sent):
                    yield sent

    def to_file(self):
        """Dump full dataset as text file in file_out location.

        Parameters
        ----------
        file_out : str, optional
            directory path of dump file, by default './reddit_gender.csv'
        """
        csv_writer = open(self.file_name_out, 'w')
        for sent in tqdm(self._iter()):
            csv_writer.write(sent + '\n')

    def _get_samples(self):
        """Get indexed data and post indices per gender word."""
        data, samples = {}, {}
        for ix, sent in tqdm(enumerate(self._iter())):
            data[ix] = sent
            for hit in self.find_gender(sent):
                form = ''.join(hit).lower()
                if form == 'hisself':  # nope
                    continue
                if not samples.get(form):
                    samples[form] = []
                samples[form].append(ix)
        return data, samples

    def to_train_test_splits(self):
        """Dump train and test splits in dir_out location.

        Parameters
        ----------
        dir_out : str, optional
            directory path to dump train and test, by default './'
        """
        (data, samples), sample_idx = self._get_samples(), []
        out = re.sub(r'\..*', '.', self.file_name_out)
        with open(out + 'train', 'w') as fo:
            for sample in samples:
                for instance in random.sample(samples[sample], 80):
                    sample_idx.append(instance)
                    fo.write(data[instance][1] + '\n')
        with open(out + 'test', 'w') as fo:
            for ix, sent in tqdm(data.items()):
                if ix not in sample_idx:
                    fo.write(sent + '\n')


class OpenSubsLoader(DataLoader):

    def __init__(self, file_name_in='/data/opensubs/opensubs.txt'):
        self.file_name_in = file_name_in


class RedditLoader(DataLoader):

    def __init__(self, snap_dir='/data/reddit', year=2019):
        """Loads and filters Reddit data based on snap zips.

        Parameters
        ----------
        snap_dir : str, optional
            directory containing snaps, by default '/data/reddit'
        year : int, optional
            year of snaps to extract data from, by default 2019
        """
        self.snap_dir = snap_dir
        self.year = year

    @staticmethod
    def preprocess_sent(sent):
        """Remove whitespaces, cut char trails, add period."""
        sent = ' '.join(sent.replace('\n', ' ').split())
        if sent[0] == ' ':
            sent = sent[1:]
        if sent[-1] not in ['.', ',', '?', '!', '*']:
            sent = sent + '.'
        return sent

    def _filter_sents(self, doc):
        """Split doc in sentences, find_gender, preprocess sents."""
        for sent in re.split(r'\.|\?|\!', doc):
            if self.find_gender(sent):
                yield self.preprocess_sent(sent)

    def _iter(self):
        """Iter through snaps yielding id and body per post."""
        for file_name in glob(self.snap_dir + '/*' + self.year + '*'):
            try:
                if 'zst' not in file_name and 'bz2' not in file_name:
                    open_func = open
                elif 'bz2' in file_name:  # NOTE: old format compatibility
                    import bz2
                    open_func = bz2.open
                else:
                    return
                for line in tqdm(open_func(file_name, 'r')):
                    reddit_object = json.loads(line)
                    for sent in self._filter_sents(reddit_object['body']):
                        yield sent
            except Exception as e:
                print(f"Error in: {e}")


if __name__ == '__main__':
    pass
