from torch.utils.data import Dataset
import numpy as np
from collections import Counter
from scipy.stats import entropy

SOS_TOKEN = '<start>'
EOS_TOKEN = '<stop>'
PAD_TOKEN = '<pad>'
OOV_TOKEN = '<oov>'
DUMMY_TOKENS = [SOS_TOKEN, EOS_TOKEN, PAD_TOKEN, OOV_TOKEN]


class TranslationDataset(Dataset):

    """
    Convert the data to tensors and pass to the PyTorch Dataset format
    as an batch iterator

    Each batch is a list:
    [input_tensor, target_tensor, input_tensor_length, target_tensor_length]
    """

    def __init__(self, X, y):
        self.data = X
        self.target = y
        # TODO: convert this into torch code is possible
        self.data_length = [np.sum(1 - np.equal(x, 0)) for x in X]
        self.target_length = [np.sum(1 - np.equal(x, 0)) for x in y]

    def __getitem__(self, index):
        x = self.data[index]
        y = self.target[index]
        x_len = self.data_length[index]
        y_len = self.target_length[index]
        return x, y, x_len, y_len

    def __len__(self):
        return len(self.data)


class LanguageIndex():
    """
    # This class creates a word -> index mapping (e.g,. "dad" -> 5) and vice-versa
    # (e.g., 5 -> "dad") for each language,
    """

    def __init__(self, phrases, name=None, **kwargs):
        """ `phrases` is a list of phrases in one language """
        self.name = name  # 'english', 'spanish', etc
        self.word2idx = {}
        self.vocab = []
        self.entropy = None
        self.idx2word = self.vocab  # this can just be a list
        self.max_phrase_length = 0
        self.entropy = None
        self.word_frequency_counter = Counter()
        self.create_index(phrases)
        self.calculate_entropy()

    def create_index(self, phrases):
        self.vocab = set(DUMMY_TOKENS)
        for phrase in phrases:
            tokens = phrase.split()
            print(tokens)
            self.max_phrase_length = max(self.max_phrase_length, len(tokens))
            self.vocab.update(set(tokens))
            self.word_frequency_counter.update(tokens)
        self.vocab = sorted(self.vocab)

        self.idx2word = self.vocab
        self.word2idx = dict(zip(self.vocab, range(len(self.vocab))))

    def calculate_entropy(self, base=2):
        self.entropy = self.entropy or entropy(list(self.word_frequency_counter.values()), base=base)
        return entropy

    def get(self, tok, default=None):
        if isinstance(tok, int):
            if (0 <= tok < len(self)):
                return self.idx2word[tok]
            return None
        return self.word2idx.get(tok, default)

    def __getitem__(self, tok):
        if isinstance(tok, int):
            return self.idx2word[tok]
        return self.word2idx[tok]

    def __len__(self):
        return len(self.vocab)


if __name__ == '__main__':
    phrases = ['<start> i am a man <stop>', '<start> weather is great <stop>']
    test_language_index = LanguageIndex(phrases)
    print(test_language_index.word2idx)
    print(test_language_index.idx2word)
    print(test_language_index.get("ambacadabra"))
