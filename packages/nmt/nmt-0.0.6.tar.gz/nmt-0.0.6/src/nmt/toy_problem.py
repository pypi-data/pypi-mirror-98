#!/usr/bin/env python
# coding: utf-8

# In[33]:
import os
from pathlib import Path
import re
import time
from zipfile import ZipFile
import unicodedata

from tqdm import tqdm
import pandas as pd
# from sklearn.model_selection import train_test_split
import numpy as np

import torch
# import torch.functional as F
from torch import nn
from torch import optim
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
from torch.utils.data import Dataset, DataLoader
from torch.autograd import Variable
from torch import FloatTensor, IntTensor, LongTensor  # noqa

from nmt.utils.data_generator import LanguageIndex
from nmt.utils.load_raw_data import texts_to_tensors
from nmt.utils.preprocess import pad_token_id_list

DATA_DIR = Path(__file__).parent.parent.parent / 'data'
# from nmt.utils.preprocess import sort_batch
# from nmt.models.modules.encoder import Encoder
# from nmt.models.modules.decoder import Decoder
# from nmt.models.helpers import mask_3d

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if str(device) == 'gpu':
    from torch.cuda import FloatTensor, IntTensor, LongTensor  # noqa

print(f'torch.__version__: {torch.__version__}')
print(f'torch device: {device}')
print(f'IntTensor: {IntTensor}')
print(f'LongTensor: {LongTensor}')


# ## Dataset: Phrase pairs (2 languages)
#
# Download [manythings.org/anki/spa-eng.zip](http://www.manythings.org/anki/spa-eng.zip)

# In[34]:


dataset_path = Path(DATA_DIR, 'spa.txt')
if not dataset_path.exists():
    with ZipFile(Path(DATA_DIR, 'spa-eng.zip'), 'r') as zipobj:
        # Get a list of all archived file names from the zip
        # filenames = zipobj.namelist()
        zipobj.extract('spa.txt')

    # df = pd.read_csv(filename)


# In[35]:


lines = dataset_path.open(encoding='UTF-8').read().strip().split('\n')


# In[36]:

# source = input, target = output
# translating from input language to target language
source_lang_name = "spanish"
target_lang_name = "english"
SOS_TOKEN = '<start>'
EOS_TOKEN = '<stop>'
PAD_TOKEN = '<pad>'
OOV_TOKEN = '<oov>'
DUMMY_TOKENS = [SOS_TOKEN, EOS_TOKEN, PAD_TOKEN, OOV_TOKEN]

DEBUG = bool(os.environ.get('DEBUG'))
os.environ['DEBUG'] = str(DEBUG)

# Toy problem:
#    Overfit (memorize the training set) to get low loss, high accuracy
NUM_EXAMPLES = int(os.environ.get('NUM_EXAMPLES') or 10000)
# Hyperparam
NUM_EPOCHS = int(os.environ.get('NUM_EPOCHS') or 40)
LEARNING_RATE = float(os.environ.get('LEARNING_RATE') or 0.03)
BATCH_SIZE = int(os.environ.get('BATCH_SIZE') or 32)
EMBEDDING_DIM = int(os.environ.get('EMBEDDING_DIM') or 20)
LAYER_NUM_UNITS = eval(os.environ.get('LAYER_NUM_UNITS') or '[32]')

print(f"NUM_EPOCHS:{NUM_EPOCHS}\n"
      f"NUM_EXAMPLES:{NUM_EXAMPLES}\n"
      f"LEARNING_RATE:{LEARNING_RATE}\n"
      )


# In[37]:


# In[38]:


def preprocess_sentence(s):
    """ Tokenize with simple multilingual tokenizer plus add <start> and <stop> tokens

    Adds space between a word and the punctuation following it, so token
    >>> preprocess_sentence(" Hola!   ¿Que tal?   ")
    '<start> Hola ! ¿ Que tal ? <stop>'

    Reference:
        https://stackoverflow.com/questions/3645931/python-padding-punctuation-with-white-spaces-keeping-punctuation
    """
    s = re.sub(r'([?.!,¿""\'])', r' \1 ', s)
    s = re.sub(r'[ ]+', ' ', s)
    # replace everything with space except (a-z, A-Z, "-", ".", "?", "!", ",")
    s = re.sub(r"[^-a-zA-Z?.!,¿]+", " ", s)
    s = s.strip()
    # adding a start and an end token to the sentence so RNN will work on variable length text
    return SOS_TOKEN + ' ' + s + ' ' + EOS_TOKEN


# In[39]:


def load_dataset(nrows=NUM_EXAMPLES, usecols=range(2)):
    # if we reversed the order of usecols would it reverse them in the dataframe so we could change direction of translation?
    df = pd.read_csv(dataset_path, sep='\t', nrows=nrows, header=None, usecols=usecols)
    df.columns = [target_lang_name, source_lang_name]
    df.tail()

    for c in df.columns:
        df[c] = df[c].apply(lambda s: unicodedata.normalize('NFD', s))
        df[c] = df[c].apply(lambda s: preprocess_sentence(s))

    return df


# In[55]:


# class LanguageIndex():
#     """ Create vocabulary mapping and index (inverse mapping)

#     >>> langindex = LanguageIndex(df['english'], name='English')
#     >>> list(langindex.word2idx.items())[:8]
#     [('!', 0),
#      (',', 1),
#      ('.', 2),
#      ('<oov>', 3),
#      ('<pad>', 4),
#      ('<start>', 5),
#      ('<stop>', 6),
#      ('?', 7)]
#     >>> langindex[3]
#     'oov'
#     >>> langindex['?']
#     7
#     """

#     def __init__(self, phrases, name=None):
#         """ `phrases` is a list of phrases in one language """
#         self.name = name  # 'english', 'spanish', etc
#         self.word2idx = {}
#         self.vocab = []
#         self.size = 0
#         self.idx2word = self.vocab  # this can just be a list
#         self.max_phrase_length = 0
#         self.create_index(phrases)

#     def create_index(self, phrases):
#         self.vocab = set(DUMMY_TOKENS)
#         for phrase in phrases:
#             tokens = phrase.split()
#             self.max_phrase_length = max(self.max_phrase_length, len(tokens))
#             self.vocab.update(set(tokens))
#         self.vocab = sorted(self.vocab)

#         self.idx2word = self.vocab
#         self.size = len(self.idx2word)
#         self.word2idx = dict(zip(self.vocab, range(len(self.vocab))))

#     def get(self, tok, default=None):
#         if isinstance(tok, int):
#             if (0 <= tok < self.size):
#                 return self.idx2word[tok]
#             return None
#         return self.word2idx.get(tok, default)

#     def __getitem__(self, tok):
#         if isinstance(tok, int):
#             return self.idx2word[tok]
#         return self.word2idx[tok]


# In[56]:


# In[58]:


def max_length(tensor):
    return max(len(t) for t in tensor)


# In[59]:


# In[60]:


# In[66]:


# inplace padding
# Show length
# print(len(input_tensor_train), len(target_tensor_train), len(input_tensor_val), len(target_tensor_val))

# In[68]:


# In[69]:


class TranslationDataset(Dataset):
    """ Convert each vector to torch.tensor type and wrap with Dataloader() """

    def __init__(self, X, y):
        """ Dataset of phrase pairs represented as arrays of integers """
        self.data = X
        self.target = y
        # FIXME: vectorize with torch.tensor
        self.length = [np.sum(1 - np.equal(x, 0)) for x in X]

    def __getitem__(self, index):
        x = self.data[index]
        y = self.target[index]
        x_len = self.length[index]
        return x, y, x_len

    def __len__(self):
        return len(self.data)


# In[70]:


# In[71]:


class Encoder(nn.Module):
    def __init__(self,
                 vocab_size,
                 embedding_dim=EMBEDDING_DIM,
                 layer_enc_units=LAYER_NUM_UNITS,
                 batch_size=BATCH_SIZE,
                 device=device):
        super().__init__()
        self.batch_size = batch_size
        self.layer_enc_units = layer_enc_units
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.embedding = nn.Embedding(self.vocab_size, self.embedding_dim)
        self.gru_layers = []
        for enc_units in self.layer_enc_units:
            self.gru_layers.append(nn.GRU(self.embedding_dim, enc_units))
        self.device = device

    def forward(self, X, lengths=None, device=device):
        lengths = LongTensor([len(s) for s in X]) if lengths is None else lengths
        # x: batch_size, max_length

        # x: batch_size, max_length, embedding_dim
        X = self.embedding(X)

        # x transformed = max_len X batch_size X embedding_dim
        # x = x.permute(1,0,2)
        self.output = pack_padded_sequence(X, lengths)  # unpad

        self.hidden = self.initialize_hidden_state()

        # output: max_length, batch_size, enc_units
        # self.hidden: 1, batch_size, enc_units
        # gru returns hidden state of all timesteps as well as hidden state at last timestep
        for gru in self.gru_layers:
            self.output, self.hidden = gru(self.output, self.hidden)

        # pad the sequence to the max length in the batch
        self.output, _ = pad_packed_sequence(self.output)

        return self.output, self.hidden

    def initialize_hidden_state(self):
        return torch.zeros((1, self.batch_size, self.layer_enc_units[-1])).to(self.device)


# In[72]:


def sort_batch(X, y, lengths, descending_length=True):
    """ Sort batch function to be able to use with pad_packed_sequence """
    lengths, idx = lengths.sort(dim=0, descending=descending_length)  # this means
    X = X[idx]
    y = y[idx]
    return X.transpose(0, 1), y, lengths  # transpose (batch x seq) to (seq x batch)


# In[88]:


class Decoder(nn.Module):
    def __init__(self,
                 vocab_size,
                 embedding_dim=EMBEDDING_DIM,
                 layer_enc_units=LAYER_NUM_UNITS,
                 dec_units=LAYER_NUM_UNITS[-1],
                 batch_size=BATCH_SIZE):
        super(Decoder, self).__init__()
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.enc_units = layer_enc_units[-1]
        self.dec_units = dec_units
        self.batch_size = batch_size

        self.embedding = nn.Embedding(self.vocab_size, self.embedding_dim)
        self.gru = nn.GRU(self.embedding_dim + self.enc_units,
                          self.dec_units,
                          batch_first=True)
        self.fc = nn.Linear(self.enc_units, self.vocab_size)

        # used for attention
        self.W1 = nn.Linear(self.enc_units, self.dec_units)
        self.W2 = nn.Linear(self.enc_units, self.dec_units)
        self.V = nn.Linear(self.enc_units, 1)

    def forward(self, X, hidden, enc_output):
        # enc_output original: (max_length, batch_size, enc_units)
        # enc_output converted == (batch_size, max_length, hidden_size)
        enc_output = enc_output.permute(1, 0, 2)
        # hidden shape == (batch_size, hidden size)
        # hidden_with_time_axis shape == (batch_size, 1, hidden size)
        # we are doing this to perform addition to calculate the score

        # hidden shape == (batch_size, hidden size)
        # hidden_with_time_axis shape == (batch_size, 1, hidden size)
        hidden_with_time_axis = hidden.permute(1, 0, 2)

        # score: (batch_size, max_length, hidden_size) # Bahdanaus's
        # we get 1 at the last axis because we are applying tanh(FC(EO) + FC(H)) to self.V
        # It doesn't matter which FC we pick for each of the inputs
        score = torch.tanh(self.W1(enc_output) + self.W2(hidden_with_time_axis))

        # score = torch.tanh(self.W2(hidden_with_time_axis) + self.W1(enc_output))

        # attention_weights shape == (batch_size, max_length, 1)
        # we get 1 at the last axis because we are applying score to self.V
        attention_weights = torch.softmax(self.V(score), dim=1)

        # context_vector shape after sum == (batch_size, hidden_size)
        context_vector = attention_weights * enc_output
        context_vector = torch.sum(context_vector, dim=1)

        # x shape after passing through embedding == (batch_size, 1, embedding_dim)
        # takes case of the right portion of the model above (illustrated in red)
        X = self.embedding(X)

        # x shape after concatenation == (batch_size, 1, embedding_dim + hidden_size)
        # x = tf.concat([tf.expand_dims(context_vector, 1), x], axis=-1)
        # ? Looks like attention vector in diagram of source
        X = torch.cat((context_vector.unsqueeze(1), X), -1)

        # passing the concatenated vector to the GRU
        # output: (batch_size, 1, hidden_size)
        output, state = self.gru(X)

        # output shape == (batch_size * 1, hidden_size)
        output = output.view(-1, output.size(2))

        # output shape == (batch_size * 1, vocab)
        X = self.fc(output)

        return X, state, attention_weights

    def initialize_hidden_state(self):
        return torch.zeros((1, self.batch_sz, self.dec_units))


criterion = nn.CrossEntropyLoss()


def loss_function(real, pred):
    """ Only consider non-zero inputs in the loss; mask needed """
    # mask = 1 - np.equal(real, 0) # assign 0 to all above 0 and 1 to all 0s
    # print(mask)
    mask = real.ge(1).type(FloatTensor)

    loss_ = criterion(pred, real) * mask
    return torch.mean(loss_)


# - Pass the input through the encoder which return encoder output and the encoder hidden state.
# - The encoder output, encoder hidden state and the decoder input (which is the start token) is passed to the decoder.
# - The decoder returns the predictions and the decoder hidden state.
# - The decoder hidden state is then passed back into the model and the predictions are used to calculate the loss.
# - Use teacher forcing to decide the next input to the decoder.
# - Teacher forcing is the technique where the target word is passed as the next input to the decoder.
# - The final step is to calculate the gradients and apply it to the optimizer and backpropagate.

# In[90]:


# FIXME: make this a function    `def train(encoder, decoder):`

def train(encoder, decoder, optimizer, dataset, num_epochs=NUM_EPOCHS):
    for epoch in tqdm(range(num_epochs)):
        start = time.time()

        encoder.train()
        decoder.train()

        total_loss = 0

        for (batch, (inp, targ, inp_len)) in enumerate(dataset):
            loss = 0

            xs, ys, lengths = sort_batch(X=inp, y=targ, lengths=inp_len)
            enc_output, enc_hidden = encoder(xs.to(device), lengths, device=device)
            dec_hidden = enc_hidden

            # use teacher forcing - feeding the target as the next input (via dec_input)
            dec_input = torch.tensor([[target_word_index.word2idx[SOS_TOKEN]]] * BATCH_SIZE)

            # run code below for every timestep in the ys batch
            for t in range(1, ys.size(1)):
                predictions, dec_hidden, _ = decoder(dec_input.to(device),
                                                     dec_hidden.to(device),
                                                     enc_output.to(device))
                loss += loss_function(ys[:, t].to(device), predictions.to(device))
                # loss += loss_
                dec_input = ys[:, t].unsqueeze(1)

            batch_loss = (loss / int(ys.size(1)))
            total_loss += batch_loss

            optimizer.zero_grad()

            loss.backward()

            # UPDATE MODEL PARAMETERS
            optimizer.step()

        # print('Epoch {} Loss {:.4f}'.format(batch, batch_loss.detach().item()))

        # TODO: Save checkpoint for model
        print(f"Epoch {(epoch+1):03d} Loss {total_loss / N_BATCH:.2f}  Time:{(time.time()-start):03.3f} s")
    return encoder, decoder


def convert_to_sentence(int_seq, word_index):
    token_seq = [word_index[int(tok.item())] for tok in int_seq]
    token_seq = [tok for tok in token_seq if tok not in DUMMY_TOKENS]
    return ' '.join(token_seq)


def convert_to_sentences(batch, word_index):
    sentences = []
    for int_seq in batch:
        sentences.append(convert_to_sentence(int_seq, word_index=word_index))
    return sentences

# In[ ]:


def predict_batch(dataset, num_batches, source_word_index, target_word_index):
    """ Calculates total (average) loss and returns translated sentences, correct translations (truth) etc """
    target_sentences = []
    translated_sentences = []
    input_sentences = []
    total_loss = 0
    for (batch_num, (inp, targ, inp_len)) in enumerate(dataset):
        if batch_num >= num_batches:
            break
        loss = 0

        # FIXME: don't sort
        Xs, ys, lengths = sort_batch(X=inp, y=targ, lengths=inp_len)
        enc_output, enc_hidden = encoder(Xs.to(device), lengths, device=device)
        dec_hidden = enc_hidden

        final_sentences = Variable(torch.zeros(ys.size()))

        # winnie:   ( use teacher forcing - feeding the target as the next input (via dec_input))
        # dec_input = torch.tensor([target_word_index.word2idx[SOS_TOKEN]] * BATCH_SIZE)

        # original: ( use teacher forcing - feeding the target as the next input (via dec_input))
        dec_input = torch.tensor([[target_word_index.word2idx[SOS_TOKEN]]] * BATCH_SIZE)
        final_sentences[:, 0] = LongTensor([target_word_index.word2idx[SOS_TOKEN]] * BATCH_SIZE)

        # run code below for every timestep in the ys for this batch
        for t in range(1, ys.size(1)):
            predictions, dec_hidden, _ = decoder(dec_input.to(device),
                                                 dec_hidden.to(device),
                                                 enc_output.to(device))
            loss += loss_function(ys[:, t].to(device), predictions.to(device))
            predictions = predictions.squeeze(0)
            final_sentences[:, t] = predictions.argmax(axis=1)

            dec_input = ys[:, t].unsqueeze(1)

        target_sentences.extend(convert_to_sentences(ys, word_index=target_word_index))
        translated_sentences.extend(convert_to_sentences(final_sentences, word_index=target_word_index))
        input_sentences.extend(convert_to_sentences(Xs.numpy().T, word_index=input_word_index))

        batch_loss = (loss / int(ys.size(1)))
        total_loss += batch_loss

    total_loss = total_loss / batch_num
    return dict(
        batch_loss=batch_loss,
        total_loss=total_loss,
        input_sentences=input_sentences,
        target_sentences=target_sentences,
        predicted_sentences=translated_sentences)


def print_results(num_batches=10, results=None):
    print()
    print('=' * 100)
    if results is None:
        results = predict_batch(num_batches=num_batches)
    print('============= Translations of Training Set Examples ================')
    triplets = list(zip(results['input_sentences'], results['predicted_sentences'], results['target_sentences']))
    for triplet in triplets:
        print(triplet[0] + f'<-input ({source_lang_name})')
        print(triplet[1] + f'<-prediction ({target_lang_name})')
        print(triplet[2] + f'<-truth ({target_lang_name})')
        print()
    print(f'============== (total_loss: {results["total_loss"]} ===============')
    print('=' * 100)
    print()
    return pd.DataFrame(triplets, columns=[
        f'{source_lang_name}',
        f'predicted_{target_lang_name}',
        f'truth_{target_lang_name}'])


# ## Final Words
# Notice that we only trained the model and that's it.
# In fact, this notebook is in experimental phase, so there could also be some bugs or something I missed
# during the process of converting code or training.
# Please comment your concerns here or submit it as an issue in the
# [GitHub version](https://github.com/omarsar/pytorch_neural_machine_translation_attention) of this notebook.
# I will appreciate it!
#
# We didn't evaluate the model or analyzed it.
# To encourage you to practice what you have learned in the notebook,
# I will suggest that you try to convert the TensorFlow code used in the
#  [original notebook]
# (https://colab.research.google.com/github/tensorflow/tensorflow/blob/master/tensorflow/contrib/eager/python/examples/nmt_with_attention/nmt_with_attention.ipynb)
# and complete this notebook. I believe the code should be straightforward,
# the hard part was already done in this notebook. If you manage to complete it, please submit a PR on the GitHub
# version of this notebook.
# I will gladly accept your PR.
# Thanks for reading and hope this notebook was useful. Keep tuned for notebooks like this on my Twitter
# ([omarsar0](https://twitter.com/omarsar0)).

# ## References
#
# ### Seq2Seq:
#   - Sutskever et al. (2014)
#     - [Sequence to Sequence Learning with Neural Networks](Sequence to Sequence Learning with Neural Networks)
#   - [Sequence to sequence model: Introduction and concepts]
# (https://towardsdatascience.com/sequence-to-sequence-model-introduction-and-concepts-44d9b41cd42d)
#   - [Blog on seq2seq](https://guillaumegenthial.github.io/sequence-to-sequence.html)
#   - [Bahdanau et al. (2016) NMT jointly learning to align and translate](https://arxiv.org/pdf/1409.0473.pdf)
#   - [Attention is all you need](https://arxiv.org/pdf/1706.03762.pdf)


if __name__ == '__main__':
    # TODO: Combine the encoder and decoder into one class
    # calculate the max_length of input and output tensor
    df = load_dataset(int(os.environ['NUM_EXAMPLES'] if 'NUM_EXAMPLES' in os.environ else NUM_EXAMPLES))
    print(df.sample(5))

    input_word_index = LanguageIndex(phrases=df[source_lang_name].values, name=source_lang_name)
    target_word_index = LanguageIndex(phrases=df[target_lang_name].values, name=target_lang_name)

    input_tensors = texts_to_tensors(texts=df[source_lang_name], language_index=input_word_index)
    target_tensors = texts_to_tensors(texts=df[target_lang_name], language_index=target_word_index)

    # calculate the max_length of input and output tensor
    max_length_inp = max(len(t) for t in input_tensors)
    max_length_tar = max(len(t) for t in target_tensors)
    max_length_inp, max_length_tar

    input_tensors = [pad_token_id_list(x, max_length_inp, input_word_index[PAD_TOKEN]) for x in input_tensors]
    target_tensors = [pad_token_id_list(x, max_length_tar, target_word_index[PAD_TOKEN]) for x in target_tensors]
    print(f"len(target_tensors): {len(target_tensors)}")

    # In[67]:

    # Creating training and validation sets using an 80-20 split
    # input_tensor_train, input_tensor_val, target_tensor_train, target_tensor_
    # val = train_test_split(input_tensor, target_tensor, test_size=0.2)
    train_dataset = TranslationDataset(input_tensors, target_tensors)

    BUFFER_SIZE = len(input_tensors)
    N_BATCH = BUFFER_SIZE // BATCH_SIZE

    dataset = DataLoader(train_dataset,
                         batch_size=BATCH_SIZE,
                         drop_last=True,
                         shuffle=True)

    encoder = Encoder(
        len(input_word_index),
        embedding_dim=EMBEDDING_DIM,
        layer_enc_units=LAYER_NUM_UNITS,
        batch_size=BATCH_SIZE)
    decoder = Decoder(
        len(target_word_index),
        embedding_dim=EMBEDDING_DIM,
        layer_enc_units=LAYER_NUM_UNITS,
        dec_units=LAYER_NUM_UNITS[-1],
        batch_size=BATCH_SIZE)

    encoder.to(device)
    decoder.to(device)

    optimizer = optim.Adam(list(encoder.parameters()) + list(decoder.parameters()), lr=LEARNING_RATE)

    encoder, decoder = train(encoder=encoder, decoder=decoder, optimizer=optimizer, num_epochs=NUM_EPOCHS, dataset=dataset)
    results = predict_batch(
        dataset=dataset,
        source_word_index=input_word_index,
        target_word_index=target_word_index,
        num_batches=10)
    triplets = print_results(results=results)
