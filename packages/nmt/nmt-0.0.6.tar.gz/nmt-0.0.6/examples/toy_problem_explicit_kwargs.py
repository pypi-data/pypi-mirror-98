#!/usr/bin/env python
# coding: utf-8

# In[33]:


from pathlib import Path
import re
import time
from zipfile import ZipFile
import unicodedata

import pandas as pd
# from sklearn.model_selection import train_test_split
import numpy as np

import torch
# import torch.functional as F
import torch.nn as nn
import torch.optim as optim
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
from torch.utils.data import Dataset, DataLoader

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f'torch.__version__: {torch.__version__}')
print(f'torch device: {device}')


num_examples = 100  # toy problem
BATCH_SIZE = 16
BUFFER_SIZE = num_examples
N_BATCH = BUFFER_SIZE // BATCH_SIZE
EMBEDDING_DIM = 32
ENCODER_UNITS = DECODER_UNITS = 32

# ## Dataset: Phrase pairs (2 languages)
#
# Download [manythings.org/anki/spa-eng.zip](http://www.manythings.org/anki/spa-eng.zip)

# In[34]:


dataset_path = Path('../data/spa.txt')
if not dataset_path.exists():
    with ZipFile('../data/spa-eng.zip', 'r') as zipobj:
        # Get a list of all archived file names from the zip
        # filenames = zipobj.namelist()
        zipobj.extract('spa.txt')

    # df = pd.read_csv(filename)


# In[35]:


lines = dataset_path.open(encoding='UTF-8').read().strip().split('\n')


# In[37]:


# 100 rows = toy problem
df = pd.read_csv(dataset_path, sep='\t', nrows=100, header=None, usecols=range(2))
df.columns = 'english spanish'.split()
df.tail()


# In[38]:


def preprocess_sentence(s):
    """ Tokenize with simple multilingual tokenizer plus add <start> and <stop>	 tokens

    Adds space between a word and the punctuation following it, so token
    >>> preprocess(" Hola!   ¿Que tal?   ")
    "Hola ! ¿ Que tal ?"

    Reference:
        https://stackoverflow.com/questions/3645931/python-padding-punctuation-with-white-spaces-keeping-punctuation
    """
    s = re.sub(r'([?.!,¿""\'])', r' \1 ', s)
    s = re.sub(r'[ ]+', ' ', s)
    # replace everything with space except (a-z, A-Z, "-", ".", "?", "!", ",")
    s = re.sub(r"[^-a-zA-Z?.!,¿]+", " ", s)
    s = s.strip()
    # adding a start and an end token to the sentence so RNN will work on variable length text
    return '<start> ' + s + ' <stop>'


# In[39]:


for c in df.columns:
    df[c] = df[c].apply(lambda s: unicodedata.normalize('NFD', s))
    df[c] = df[c].apply(lambda s: preprocess_sentence(s))
df.sample(5)


# In[55]:


class LanguageIndex():
    """ Create vocabulary mapping and index (inverse mapping)

    >>> langindex = LanguageIndex(df['english'])
    >>> langindex.word2idx.items()[:3]
    {"papa": 5, ...
    >>> langindex.idx2word.items()[:3]
    {5: "papa"}
    """

    def __init__(self, phrases):
        """ `phrases` is a list of phrases in one language """
        self.word2idx = {}
        self.vocab = []
        self.idx2word = self.vocab  # this can just be a list
        self.create_index(phrases)

    def create_index(self, phrases):
        self.vocab = set('<start> <stop>	 <pad>'.split())
        for phrase in phrases:
            self.vocab.update(set(phrase.split()))
        self.vocab = sorted(self.vocab)

        self.idx2word = self.vocab
        self.word2idx = dict(zip(self.vocab, range(len(self.vocab))))

    def __getitem__(self, tok):
        return self.word2idx.get(tok) or self.vocab[tok]


# In[56]:


# index language using the class above
targetlang = "english"
sourcelang = "spanish"
inp_index = LanguageIndex(phrases=df[sourcelang].values)
targ_index = LanguageIndex(phrases=df[targetlang].values)
vocab_inp_size = len(inp_index.word2idx)
vocab_tar_size = len(targ_index.word2idx)

# Vectorize the input and target languages
input_tensors = [[inp_index.word2idx[s] for s in es.split(' ')] for es in df[sourcelang].values.tolist()]
target_tensors = [[targ_index.word2idx[s] for s in eng.split(' ')] for eng in df[targetlang].values.tolist()]
pd.DataFrame(input_tensors[:5])


# In[57]:


pd.DataFrame(target_tensors[:5])


# In[58]:


def max_length(tensor):
    return max(len(t) for t in tensor)


# In[59]:


# calculate the max_length of input and output tensor
max_length_inp = max(len(t) for t in input_tensors)
max_length_tar = max(len(t) for t in target_tensors)
max_length_inp, max_length_tar


# In[60]:


def pad_seq(s, max_len, pad_tok_idx):
    padded = pad_tok_idx * np.ones(max_len, dtype=np.int64)  # FIXME: int16 should be pleanty
    s_len = min(max_len, len(s))
    padded[:s_len] = s[:s_len]
    return padded


# In[66]:


# inplace padding
input_tensors = [pad_seq(x, max_length_inp, inp_index['<pad>']) for x in input_tensors]
target_tensors = [pad_seq(x, max_length_tar, targ_index['<pad>']) for x in target_tensors]
print(len(target_tensors))


# In[67]:


# Creating training and validation sets using an 80-20 split
# input_tensor_train, input_tensor_val, target_tensor_train, target_tensor_
# val = train_test_split(input_tensors, target_tensors, test_size=0.2)
input_tensor_train = input_tensor_val = input_tensors
target_tensor_train = target_tensor_val = target_tensors
# Show length
print(len(input_tensor_train), len(target_tensor_train), len(input_tensor_val), len(target_tensor_val))

# In[68]:


# In[69]:


class TranslationDataset(Dataset):
    """ Convert each vector to torch.tensor type and wrap with Dataloader() """

    def __init__(self, X, y):
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


train_dataset = TranslationDataset(input_tensor_train, target_tensor_train)


dataset = DataLoader(train_dataset,
                     batch_size=BATCH_SIZE,
                     drop_last=True,
                     shuffle=True)


# In[71]:


class Encoder(nn.Module):
    def __init__(self, vocab_size, embedding_dim=EMBEDDING_DIM, enc_units=ENCODER_UNITS, batch_sz=BATCH_SIZE):
        super().__init__()
        self.batch_sz = batch_sz
        self.enc_units = enc_units
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.embedding = nn.Embedding(self.vocab_size, self.embedding_dim)
        self.gru = nn.GRU(self.embedding_dim, self.enc_units)

    def forward(self, x, lens, device=device):
        # x: batch_size, max_length

        # x: batch_size, max_length, embedding_dim
        x = self.embedding(x)

        # x transformed = max_len X batch_size X embedding_dim
        # x = x.permute(1,0,2)
        x = pack_padded_sequence(x, lens)  # unpad

        self.hidden = self.initialize_hidden_state(device)

        # output: max_length, batch_size, enc_units
        # self.hidden: 1, batch_size, enc_units
        # gru returns hidden state of all timesteps as well as hidden state at last timestep
        output, self.hidden = self.gru(x, self.hidden)

        # pad the sequence to the max length in the batch
        output, _ = pad_packed_sequence(output)

        return output, self.hidden

    def initialize_hidden_state(self, device=device):
        return torch.zeros((1, self.batch_sz, self.enc_units)).to(device)

# In[88]:


print('Training set pairs (source then target):...')
for rownum, (inp, targ) in enumerate(zip(input_tensors, target_tensors)):
    print()
    print(' '.join([targ_index.idx2word[i] for i in targ]))
    print(' '.join([inp_index.idx2word[i] for i in inp]))
    if rownum > 5:
        break


# ## Testing the Encoder
# Before proceeding with training, we should always try to test out model behavior
# such as the size of outputs just to make that things are going as expected.
# In PyTorch this can be done easily since everything comes in eager execution by default.

# ### Test Encoder

# In[73]:


encoder = Encoder(
    vocab_tar_size,
    embedding_dim=EMBEDDING_DIM,
    enc_units=ENCODER_UNITS,
    batch_sz=BATCH_SIZE)
encoder.to(device)

# obtain one sample from the data iterator
it = iter(dataset)
inp_batch, out_batch, inp_batch_lengths = next(it)


def sort_batch(input_batch, output_batch, input_batch_lengths):
    """ Sort batch function to be able to use with pad_packed_sequence """
    lengths, indx = input_batch_lengths.sort(dim=0, descending=True)
    input_batch = input_batch[indx]
    output_batch = output_batch[indx]
    return input_batch.transpose(0, 1), output_batch, input_batch_lengths  # transpose (batch x seq) to (seq x batch)


# sort the batch first to be able to use with pac_pack_sequence
inp_batch_sorted, out_batch_sorted, lengths = sort_batch(
    input_batch=inp_batch,
    output_batch=out_batch,
    input_batch_lengths=inp_batch_lengths)

enc_output, enc_hidden = encoder(inp_batch_sorted.to(device), lengths, device=device)

print('Encoder output tensor should be size (max_length, batch_size, num_enc_units):')
print(enc_output.size())
print(inp_batch.size())
print(out_batch.size())
print(f'inp_batch_sorted.size() seems wrong: {inp_batch_sorted.size()}')
print(f'out_batch_sorted.size() seems correct: {out_batch_sorted.size()}')
print(f'BATCH_SIZE: {BATCH_SIZE}')


# ### Decoder
#
# Here, we'll implement an encoder-decoder model with attention which you can read about in the TensorFlow
# [Neural Machine Translation (seq2seq) tutorial](https://github.com/tensorflow/nmt).
# This example uses a more recent set of APIs.
# This notebook implements the [attention equations](https://github.com/tensorflow/nmt#background-on-the-attention-mechanism)
#  from the seq2seq tutorial. The following diagram shows that each input word is assigned a weight by the attention
#  mechanism which is then used by the decoder to predict the next word in the sentence.
#
# <img src="https://www.tensorflow.org/images/seq2seq/attention_mechanism.jpg" width="500" alt="attention mechanism">
#
# The input is put through an encoder model which gives us the encoder output of shape
# *(batch_size, max_length, hidden_size)* and the encoder hidden state of shape *(batch_size, hidden_size)*.
#
# Here are the equations that are implemented:
#
# <img src="https://www.tensorflow.org/images/seq2seq/attention_equation_0.jpg" alt="attention equation 0" width="800">
# <img src="https://www.tensorflow.org/images/seq2seq/attention_equation_1.jpg" alt="attention equation 1" width="800">
#
# We're using *Bahdanau attention*. Lets decide on notation before writing the simplified form:
#
# * FC = Fully connected (dense) layer
# * EO = Encoder output
# * H = hidden state
# * X = input to the decoder
#
# And the pseudo-code:
#
# * `score = FC(tanh(FC(EO) + FC(H)))`
# * `attention weights = softmax(score, axis = 1)`.
# Softmax by default is applied on the last axis but here we want to apply it on the *1st axis*,
# since the shape of score is *(batch_size, max_length, 1)*.
# `Max_length` is the length of our input. Since we are trying to assign a weight to each input,
# softmax should be applied on that axis.
# * `context vector = sum(attention weights * EO, axis = 1)`. Same reason as above for choosing axis as 1.
# * `embedding output` = The input to the decoder X is passed through an embedding layer.
# * `merged vector = concat(embedding output, context vector)`
# * This merged vector is then given to the GRU
#
# The shapes of all the vectors at each step have been specified in the comments in the code:

# In[74]:


class Decoder(nn.Module):
    def __init__(self, vocab_size, embedding_dim, dec_units, enc_units, batch_sz):
        super(Decoder, self).__init__()
        self.batch_sz = batch_sz
        self.dec_units = dec_units
        self.enc_units = enc_units
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.embedding = nn.Embedding(self.vocab_size, self.embedding_dim)
        self.gru = nn.GRU(self.embedding_dim + self.enc_units,
                          self.dec_units,
                          batch_first=True)
        self.fc = nn.Linear(self.enc_units, self.vocab_size)

        # used for attention
        self.W1 = nn.Linear(self.enc_units, self.dec_units)
        self.W2 = nn.Linear(self.enc_units, self.dec_units)
        self.V = nn.Linear(self.enc_units, 1)

    def forward(self, x, hidden, enc_output):
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
        x = self.embedding(x)

        # x shape after concatenation == (batch_size, 1, embedding_dim + hidden_size)
        # x = tf.concat([tf.expand_dims(context_vector, 1), x], axis=-1)
        # ? Looks like attention vector in diagram of source
        x = torch.cat((context_vector.unsqueeze(1), x), -1)

        # passing the concatenated vector to the GRU
        # output: (batch_size, 1, hidden_size)
        output, state = self.gru(x)

        # output shape == (batch_size * 1, hidden_size)
        output = output.view(-1, output.size(2))

        # output shape == (batch_size * 1, vocab)
        x = self.fc(output)

        return x, state, attention_weights

    def initialize_hidden_state(self):
        return torch.zeros((1, self.batch_sz, self.dec_units))


# ## Testing the Decoder
# Similarily, try to test the decoder.

# In[75]:


# obtain one sample from the data iterator
it = iter(dataset)
x, y, x_len = next(it)

print("Input: ", x.shape)
print("Output: ", y.shape)

# sort the batch first to be able to use with pac_pack_sequence
xs, ys, lens = sort_batch(x, y, x_len)

enc_output, enc_hidden = encoder(xs.to(device), lens, device=device)
print("Encoder Output: ", enc_output.shape)  # batch_size X max_length X enc_units
print("Encoder Hidden: ", enc_hidden.shape)  # batch_size X enc_units (corresponds to the last state)

decoder = Decoder(
    vocab_tar_size,
    embedding_dim=EMBEDDING_DIM,
    enc_units=ENCODER_UNITS,
    dec_units=DECODER_UNITS,
    batch_sz=BATCH_SIZE)
decoder = decoder.to(device)

# print(enc_hidden.squeeze(0).shape)

dec_hidden = enc_hidden  # .squeeze(0)
dec_input = torch.tensor([[targ_index.word2idx['<start>']]] * BATCH_SIZE)
print("Decoder Input: ", dec_input.shape)
print("--------")

for t in range(1, y.size(1)):
    # enc_hidden: 1, batch_size, enc_units
    # output: max_length, batch_size, enc_units
    predictions, dec_hidden, _ = decoder(dec_input.to(device),
                                         dec_hidden.to(device),
                                         enc_output.to(device))

    print("Prediction: ", predictions.shape)
    print("Decoder Hidden: ", dec_hidden.shape)

    # loss += loss_function(y[:, t].to(device), predictions.to(device))

    dec_input = y[:, t].unsqueeze(1)
    print(dec_input.shape)
    break


# In[79]:


criterion = nn.CrossEntropyLoss()


def loss_function(real, pred):
    """ Only consider non-zero inputs in the loss; mask needed """
    # mask = 1 - np.equal(real, 0) # assign 0 to all above 0 and 1 to all 0s
    # print(mask)
    mask = real.ge(1).type(torch.cuda.FloatTensor if device is 'gpu' else torch.FloatTensor)

    loss_ = criterion(pred, real) * mask
    return torch.mean(loss_)


# In[80]:


# TODO: Combine the encoder and decoder into one class
encoder = Encoder(
    vocab_inp_size,
    embedding_dim=EMBEDDING_DIM,
    enc_units=ENCODER_UNITS,
    batch_sz=BATCH_SIZE)
decoder = Decoder(
    vocab_tar_size,
    embedding_dim=EMBEDDING_DIM,
    enc_units=ENCODER_UNITS,
    dec_units=DECODER_UNITS,
    batch_sz=BATCH_SIZE)

encoder.to(device)
decoder.to(device)

optimizer = optim.Adam(list(encoder.parameters()) + list(decoder.parameters()),
                       lr=0.001)


# - Pass the input through the encoder which return encoder output and the encoder hidden state.
# - The encoder output, encoder hidden state and the decoder input (which is the start token) is passed to the decoder.
# - The decoder returns the predictions and the decoder hidden state.
# - The decoder hidden state is then passed back into the model and the predictions are used to calculate the loss.
# - Use teacher forcing to decide the next input to the decoder.
# - Teacher forcing is the technique where the target word is passed as the next input to the decoder.
# - The final step is to calculate the gradients and apply it to the optimizer and backpropagate.

# In[90]:


EPOCHS = 300

for epoch in range(EPOCHS):
    start = time.time()

    encoder.train()
    decoder.train()

    total_loss = 0

    for (batch, (inp, targ, inp_len)) in enumerate(dataset):
        loss = 0

        xs, ys, lens = sort_batch(inp, targ, inp_len)
        enc_output, enc_hidden = encoder(xs.to(device), lens, device=device)
        dec_hidden = enc_hidden

        # use teacher forcing - feeding the target as the next input (via dec_input)
        dec_input = torch.tensor([[targ_index.word2idx['<start>']]] * BATCH_SIZE)

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

        if not batch % 100:
            print('Epoch {} Batch {} Loss {:.4f}'.format(epoch + 1,
                                                         batch,
                                                         batch_loss.detach().item()))

    # TODO: Save checkpoint for model
    print('Epoch {} Loss {:.4f}'.format(epoch + 1,
                                        total_loss / N_BATCH))
    print('Time taken for 1 epoch {} sec\n'.format(time.time() - start))


# In[ ]:


# In[52]:


for (inp, targ, inp_len) in dataset:
    break
print(inp)
print(targ)
print(inp_len)
# xs, ys, lens = sort_batch(inp, targ, inp_len)
# enc_output, enc_hidden = encoder(xs.to(device), lens, device=device)
# dec_hidden = enc_hidden


# In[69]:


def source_to_target(source_sentence):
    source_tensor = [inp_index.word2idx[w] for w in source_sentence.split()]
    inp_len = len(source_tensor)
    # xs, ys, lens = sort_batch(inp, targ, inp_len)
    enc_output, enc_hidden = encoder(torch.tensor([source_tensor] * BATCH_SIZE).to(device), [inp_len] * BATCH_SIZE, device=device)

    return enc_output


# In[70]:


source_to_target('<start> Hola ? <stop>	')


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
