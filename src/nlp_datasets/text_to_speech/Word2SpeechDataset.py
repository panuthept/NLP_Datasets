import os
import zipfile

from scipy.io.wavfile import read

from ..BaseDataset import BaseDataset
from ..utilities import download_file_from_google_drive
from ..path_config import WORD_TO_SPEECH_BASE_DIR
from ..path_config import WORD_TO_SPEECH_ANAGRAMS_BASE_DIR
from ..path_config import WORD_TO_SPEECH_MISSPELLINGS_BASE_DIR
from ..path_config import WORD_TO_SPEECH_WORDS_BASE_DIR
from ..url_config import WORD_TO_SPEECH_ANAGRAMS_DATA_ID
from ..url_config import WORD_TO_SPEECH_ANAGRAMS_DATA_URL
from ..url_config import WORD_TO_SPEECH_ANAGRAMS_INDEX_ID
from ..url_config import WORD_TO_SPEECH_ANAGRAMS_INDEX_URL
from ..url_config import WORD_TO_SPEECH_MISSPELLINGS_DATA_ID
from ..url_config import WORD_TO_SPEECH_MISSPELLINGS_DATA_URL
from ..url_config import WORD_TO_SPEECH_MISSPELLINGS_INDEX_ID
from ..url_config import WORD_TO_SPEECH_MISSPELLINGS_INDEX_URL
from ..url_config import WORD_TO_SPEECH_WORDS_DATA_ID
from ..url_config import WORD_TO_SPEECH_WORDS_DATA_URL
from ..url_config import WORD_TO_SPEECH_WORDS_INDEX_ID
from ..url_config import WORD_TO_SPEECH_WORDS_INDEX_URL


def download_corpus():
    if not os.path.exists(WORD_TO_SPEECH_BASE_DIR):
        os.makedirs(WORD_TO_SPEECH_BASE_DIR)

    # Anagrams
    if not os.path.exists(WORD_TO_SPEECH_ANAGRAMS_BASE_DIR):
        os.makedirs(WORD_TO_SPEECH_ANAGRAMS_BASE_DIR)

    if not os.path.exists(WORD_TO_SPEECH_ANAGRAMS_BASE_DIR + "/indexing.txt"):
        # Download indexing
        print(f"Downloading: {WORD_TO_SPEECH_ANAGRAMS_INDEX_URL}")
        download_file_from_google_drive(WORD_TO_SPEECH_ANAGRAMS_INDEX_ID, WORD_TO_SPEECH_ANAGRAMS_BASE_DIR + "/indexing.txt")
    if not os.path.exists(WORD_TO_SPEECH_ANAGRAMS_BASE_DIR + "/data"):
        # Download data
        print(f"Downloading: {WORD_TO_SPEECH_ANAGRAMS_DATA_URL}")
        download_file_from_google_drive(WORD_TO_SPEECH_ANAGRAMS_DATA_ID, WORD_TO_SPEECH_ANAGRAMS_BASE_DIR + "/data.zip")
        # Unzip file
        with zipfile.ZipFile(WORD_TO_SPEECH_ANAGRAMS_BASE_DIR + "/data.zip", "r") as zip_ref:
            zip_ref.extractall(WORD_TO_SPEECH_ANAGRAMS_BASE_DIR)
        # Remove zip file
        os.remove(WORD_TO_SPEECH_ANAGRAMS_BASE_DIR + "/data.zip")

    # Misspellings
    if not os.path.exists(WORD_TO_SPEECH_MISSPELLINGS_BASE_DIR):
        os.makedirs(WORD_TO_SPEECH_MISSPELLINGS_BASE_DIR)

    if not os.path.exists(WORD_TO_SPEECH_MISSPELLINGS_BASE_DIR + "/indexing.txt"):
        # Download indexing
        print(f"Downloading: {WORD_TO_SPEECH_MISSPELLINGS_INDEX_URL}")
        download_file_from_google_drive(WORD_TO_SPEECH_MISSPELLINGS_INDEX_ID, WORD_TO_SPEECH_MISSPELLINGS_BASE_DIR + "/indexing.txt")
    if not os.path.exists(WORD_TO_SPEECH_MISSPELLINGS_BASE_DIR + "/data"):
        # Download data
        print(f"Downloading: {WORD_TO_SPEECH_MISSPELLINGS_DATA_URL}")
        download_file_from_google_drive(WORD_TO_SPEECH_MISSPELLINGS_DATA_ID, WORD_TO_SPEECH_MISSPELLINGS_BASE_DIR + "/data.zip")
        # Unzip file
        with zipfile.ZipFile(WORD_TO_SPEECH_MISSPELLINGS_BASE_DIR + "/data.zip", "r") as zip_ref:
            zip_ref.extractall(WORD_TO_SPEECH_MISSPELLINGS_BASE_DIR)
        # Remove zip file
        os.remove(WORD_TO_SPEECH_MISSPELLINGS_BASE_DIR + "/data.zip")

    # Words
    if not os.path.exists(WORD_TO_SPEECH_WORDS_BASE_DIR):
        os.makedirs(WORD_TO_SPEECH_WORDS_BASE_DIR)

    if not os.path.exists(WORD_TO_SPEECH_WORDS_BASE_DIR + "/indexing.txt"):
        # Download indexing
        print(f"Downloading: {WORD_TO_SPEECH_WORDS_INDEX_URL}")
        download_file_from_google_drive(WORD_TO_SPEECH_WORDS_INDEX_ID, WORD_TO_SPEECH_WORDS_BASE_DIR + "/indexing.txt")
    if not os.path.exists(WORD_TO_SPEECH_WORDS_BASE_DIR + "/data"):
        # Download data
        print(f"Downloading: {WORD_TO_SPEECH_WORDS_DATA_URL}")
        download_file_from_google_drive(WORD_TO_SPEECH_WORDS_DATA_ID, WORD_TO_SPEECH_WORDS_BASE_DIR + "/data.zip")
        # Unzip file
        with zipfile.ZipFile(WORD_TO_SPEECH_WORDS_BASE_DIR + "/data.zip", "r") as zip_ref:
            zip_ref.extractall(WORD_TO_SPEECH_WORDS_BASE_DIR)
        # Remove zip file
        os.remove(WORD_TO_SPEECH_WORDS_BASE_DIR + "/data.zip")


def load_corpus(max_samples: int=None, include_word: bool=True, include_anagram: bool=True, include_misspelling: bool=True):
    def _load_corpus(corpus_dir):
        # Read indexing
        with open(corpus_dir + "/indexing.txt", "r") as f:
            indexing = {word: str(i) + ".wav" for i, word in enumerate(f.read().strip().split("\n"))}

        # Read audio
        for word, filename in indexing.items():
            audio = read(corpus_dir + "/audios/" + filename)
            yield word, audio

    count = 0
    if include_word:
        for word, audio in _load_corpus(WORD_TO_SPEECH_WORDS_BASE_DIR):
            count += 1
            # Terminate by max_samples
            if (max_samples is not None) and (count > max_samples):
                break
            yield word, audio
    if include_anagram:
        for word, audio in _load_corpus(WORD_TO_SPEECH_ANAGRAMS_BASE_DIR):
            count += 1
            # Terminate by max_samples
            if (max_samples is not None) and (count > max_samples):
                break
            yield word, audio
    if include_misspelling:
        for word, audio in _load_corpus(WORD_TO_SPEECH_MISSPELLINGS_BASE_DIR):
            count += 1
            # Terminate by max_samples
            if (max_samples is not None) and (count > max_samples):
                break
            yield word, audio


class Word2SpeechDataset(BaseDataset):
    local_dir = "word_to_speech_dataset"

    def __init__(self,
                 include_word=True,
                 include_anagram=True,
                 include_misspelling=True,
                 max_samples=None,
                 train_split_ratio=0.8,
                 val_split_ratio=0.1,
                 test_split_ratio=0.1,
                 random_seed=0, 
                 local_dir=None):

        self.include_word = include_word
        self.include_anagram = include_anagram
        self.include_misspelling = include_misspelling
        download_corpus()
        super().__init__(max_samples, train_split_ratio, val_split_ratio, test_split_ratio, random_seed, local_dir)

    def _load_train(self):
        """ Yield data from training set """
        yield from load_corpus(max_samples=self.max_samples, 
                               include_word=self.include_word, 
                               include_anagram=self.include_anagram,
                               include_misspelling=self.include_misspelling)

    def _load_val(self):
        """ Yield data from validation set """
        pass

    def _load_test(self):
        """ Yield data from test set """
        pass

    def _process_data(self, data):
        """ Preprocess and transform data into sample """
        # Extract data
        word, audio = data

        # Transform data into sample
        sample = {"word": word, "audio": audio}
        return sample
