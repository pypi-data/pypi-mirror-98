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

DATA_DIR = Path(Path(__file__).parent, '..', 'data')
# from nmt.utils.preprocess import sort_batch
# from nmt.models.modules.encoder import Encoder
# from nmt.models.modules.decoder import Decoder
# from nmt.models.helpers import mask_3d

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
from torch import FloatTensor, IntTensor, LongTensor  # noqa
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
NUM_EXAMPLES = int(os.environ.get('NUM_EXAMPLES') or 2000)
os.environ['NUM_EXAMPLES'] = str(NUM_EXAMPLES)

# Hyperparam
NUM_EPOCHS = int(os.environ.get('NUM_EPOCHS') or 50)
os.environ['NUM_EPOCHS'] = str(NUM_EPOCHS)
LEARNING_RATE = float(os.environ.get('LEARNING_RATE') or 0.03)
os.environ['LEARNING_RATE'] = str(LEARNING_RATE)
BATCH_SIZE = 32
EMBEDDING_DIM = 16
NUM_UNITS = 16

print(f"NUM_EPOCHS:{NUM_EPOCHS}  NUM_EXAMPLES:{NUM_EXAMPLES}  LEARNING_RATE:{LEARNING_RATE}")


# In[37]:

df = pd.read_csv(dataset_path, sep='\t', nrows=NUM_EXAMPLES, header=None, usecols=range(2))
df.columns = [target_lang_name, source_lang_name]
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
    return SOS_TOKEN + ' ' + s + ' ' + EOS_TOKEN


# In[39]:


for c in df.columns:
    df[c] = df[c].apply(lambda s: unicodedata.normalize('NFD', s))
    df[c] = df[c].apply(lambda s: preprocess_sentence(s))
print(df.sample(5))


# In[55]:


class LanguageIndex():
    """ Create vocabulary mapping and index (inverse mapping)

    >>> langindex = LanguageIndex(df['english'], name='English')
    >>> list(langindex.word2idx.items())[:8]
    [('!', 0),
     (',', 1),
     ('.', 2),
     ('<oov>', 3),
     ('<pad>', 4),
     ('<start>', 5),
     ('<stop>', 6),
     ('?', 7)]
    >>> langindex[3]
    'oov'
    >>> langindex['?']
    7
    """

    def __init__(self, phrases, name=None):
        """ `phrases` is a list of phrases in one language """
        self.name = name  # 'english', 'spanish', etc
        self.word2idx = {}
        self.vocab = []
        self.size = 0
        self.idx2word = self.vocab  # this can just be a list
        self.max_phrase_length = 0
        self.create_index(phrases)

    def create_index(self, phrases):
        self.vocab = set(DUMMY_TOKENS)
        for phrase in phrases:
            tokens = phrase.split()
            self.max_phrase_length = max(self.max_phrase_length, len(tokens))
            self.vocab.update(set(tokens))
        self.vocab = sorted(self.vocab)

        self.idx2word = self.vocab
        self.size = len(self.idx2word)
        self.word2idx = dict(zip(self.vocab, range(len(self.vocab))))

    def get(self, tok, default=None):
        if isinstance(tok, int):
            if (0 <= tok < self.size):
                return self.idx2word[tok]
            return None
        return self.word2idx.get(tok, default)

    def __getitem__(self, tok):
        if isinstance(tok, int):
            return self.idx2word[tok]
        return self.word2idx[tok]


# In[56]:


# index language using the class above

input_word_index = LanguageIndex(phrases=df[source_lang_name].values, name=source_lang_name)
target_word_index = LanguageIndex(phrases=df[target_lang_name].values, name=target_lang_name)
# Vectorize the input and target languages
input_tensors = [[input_word_index.word2idx[s] for s in es.split(' ')] for es in df[source_lang_name].values.tolist()]
target_tensors = [[target_word_index.word2idx[s] for s in eng.split(' ')] for eng in df[target_lang_name].values.tolist()]
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


def pad_token_id_list(s, max_len, pad_tok_idx):
    """ Add the padding token id to the end of the list of integers to ensure uniform length

    TODO: make this a method within the LanguageIndex so the pad_tok_idx is known within self

    Input:
      max_len (int): maximum number of tokens in a sentence
      pad_tok_idx (int): the id of the token '<pad>' for the sentence (language) being padded
    Output:
      sequence of ints with the integer pad token appended to the end
    """
    padded = pad_tok_idx * np.ones(max_len, dtype=np.int64)  # FIXME: int16 should be plenty
    s_len = min(max_len, len(s))
    padded[:s_len] = s[:s_len]
    return padded


# In[66]:


# inplace padding
input_tensors = [pad_token_id_list(x, max_length_inp, input_word_index[PAD_TOKEN]) for x in input_tensors]
target_tensors = [pad_token_id_list(x, max_length_tar, target_word_index[PAD_TOKEN]) for x in target_tensors]
print(len(target_tensors))


# In[67]:


# Creating training and validation sets using an 80-20 split
# input_tensor_train, input_tensor_val, target_tensor_train, target_tensor_
# val = train_test_split(input_tensor, target_tensor, test_size=0.2)
input_tensor_train = input_tensor_val = input_tensors
target_tensor_train = target_tensor_val = target_tensors
# Show length
print(len(input_tensor_train), len(target_tensor_train), len(input_tensor_val), len(target_tensor_val))

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


train_dataset = TranslationDataset(input_tensor_train, target_tensor_train)


BUFFER_SIZE = len(input_tensor_train)

N_BATCH = BUFFER_SIZE // BATCH_SIZE

vocab_tar_size = target_word_index.size

dataset = DataLoader(train_dataset,
                     batch_size=BATCH_SIZE,
                     drop_last=True,
                     shuffle=True)


# In[71]:


class Encoder(nn.Module):
    def __init__(self,
                 vocab_size=len(input_word_index.word2idx),
                 embedding_dim=EMBEDDING_DIM,
                 enc_units=NUM_UNITS,
                 batch_size=BATCH_SIZE,
                 device=device):
        super().__init__()
        self.batch_size = batch_size
        self.enc_units = enc_units
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.embedding = nn.Embedding(self.vocab_size, self.embedding_dim)
        self.gru = nn.GRU(self.embedding_dim, self.enc_units,num_layers=2)
        self.device = device

    def forward(self, X, lengths=None, device=device):
        lengths = LongTensor([len(s) for s in X]) if lengths is None else lengths
        # x: batch_size, max_length

        # x: batch_size, max_length, embedding_dim
        X = self.embedding(X)

        # x transformed = max_len X batch_size X embedding_dim
        # x = x.permute(1,0,2)
        X = pack_padded_sequence(X, lengths)  # unpad

        # output: max_length, batch_size, enc_units
        # self.hidden: 1, batch_size, enc_units
        # gru returns hidden state of all timesteps as well as hidden state at last timestep
        output, self.hidden = self.gru(X)

        # pad the sequence to the max length in the batch
        output, _ = pad_packed_sequence(output)

        return output, self.hidden


# In[72]:


def sort_batch(X, y, lengths, descending_length=True):
    """ Sort batch function to be able to use with pad_packed_sequence """
    lengths, idx = lengths.sort(dim=0, descending=descending_length)  # this means
    X = X[idx]
    y = y[idx]
    return X.transpose(0, 1), y, lengths  # transpose (batch x seq) to (seq x batch)


# In[88]:


print('Training set pairs (source then target):...')
for rownum, (inp, targ) in enumerate(zip(input_tensors, target_tensors)):
    print()
    print(''.join([f"{target_word_index.idx2word[i]:<8s}" for i in targ]))
    print(''.join([f"{input_word_index.idx2word[i]:<8s}" for i in inp]))
    if rownum > 5:
        break


# ## Testing the Encoder
# Before proceeding with training, we should always try to test out model behavior
# such as the size of outputs just to make that things are going as expected.
# In PyTorch this can be done easily since everything comes in eager execution by default.

# ############################################################################################
# ### test Encoder & Decoder classes

# In[73]:

def show_example_encoder_shapes(
        dataset=dataset,
        vocab_inp_size=input_word_index.size,
        embedding_dim=EMBEDDING_DIM,
        enc_units=NUM_UNITS,
        batch_size=BATCH_SIZE):
    """ Created function to avoid poluting namespace and potentially corrupting trained model """
    encoder = Encoder(vocab_inp_size, embedding_dim=embedding_dim, enc_units=enc_units, batch_size=batch_size)
    encoder.to(device)

    # obtain one sample from the data iterator
    it = iter(dataset)
    inp_batch, out_batch, inp_batch_len = next(it)

    # sort the batch first to be able to use with pac_pack_sequence
    inp_batch_sorted, out_batch_sorted, lengths = sort_batch(X=inp_batch, y=out_batch, lengths=inp_batch_len)

    enc_output = encoder.forward(inp_batch_sorted.to(device), lengths, device=device)

    print('Encoder output tensor should be size (max_length, batch_size, num_enc_units):')
    print(f"encoder output hidden layer shape: {enc_output[0].size()}")
    print(f"encoder output hidden layer shape: {enc_output[1].size()}")
    print(inp_batch.size())
    print(out_batch.size())
    print(f'inp_batch_sorted.size(): {inp_batch_sorted.size()}')
    print(f'out_batch_sorted.size(): {out_batch_sorted.size()}')
    print(f'BATCH_SIZE: {batch_size}')

    return enc_output


show_example_encoder_shapes()

# ### Test Decoder
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

# ### test Encoder & Decoder classes
# ############################################################################################


class Decoder(nn.Module):
    def __init__(self, vocab_size, embedding_dim=EMBEDDING_DIM, dec_units=NUM_UNITS, enc_units=NUM_UNITS, batch_size=BATCH_SIZE):
        super(Decoder, self).__init__()
        self.batch_size = batch_size
        self.dec_units = dec_units
        self.enc_units = enc_units
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.embedding = nn.Embedding(self.vocab_size, self.embedding_dim)
        self.gru = nn.GRU(self.embedding_dim ,
                          self.dec_units,
                          num_layers=2)
        self.fc = nn.Linear(self.enc_units, self.vocab_size)

    def forward(self, X, hidden):
        X = self.embedding(X)
        X = X.unsqueeze(0)
        hidden, state = self.gru(X,hidden)
        hidden = self.fc(hidden)

        return hidden, state


# ## Testing the Decoder
# Similarily, try to test the decoder.

# In[75]:


def example_encoder_decoder():
    # obtain one sample from the data iterator
    it = iter(dataset)
    X, y, x_len = next(it)

    print("Input: ", X.shape)
    print("Output: ", y.shape)

    # sort the batch first to be able to use with pac_pack_sequence
    xs, ys, lengths = sort_batch(X=X, y=y, lengths=x_len)

    # TODO: Combine the encoder and decoder into one class (see Seq2Seq below & Translator by Winnie)
    encoder = Encoder(len(input_word_index.word2idx), embedding_dim=EMBEDDING_DIM, enc_units=NUM_UNITS, batch_size=BATCH_SIZE)
    encoder.to(device)

    enc_output, enc_hidden = encoder(xs.to(device), lengths=lengths, device=device)
    print("Encoder Output: ", enc_output.shape)  # batch_size X max_length X enc_units
    print("Encoder Hidden: ", enc_hidden.shape)  # batch_size X enc_units (corresponds to the last st

def example_encoder_decoder():
    # obtain one sample from the data iterator
    it = iter(dataset)
    X, y, x_len = next(it)

    print("Input: ", X.shape)
    print("Output: ", y.shape)

    # sort the batch first to be able to use with pac_pack_sequence
    xs, ys, lengths = sort_batch(X=X, y=y, lengths=x_len)

    # TODO: Combine the encoder and decoder into one class (see Seq2Seq below & Translator by Winnie)
    encoder = Encoder(len(input_word_index.word2idx), embedding_dim=EMBEDDING_DIM, enc_units=NUM_UNITS, batch_size=BATCH_SIZE)
    encoder.to(device)

    enc_output, enc_hidden = encoder(xs.to(device), lengths=lengths, device=device)
    print("Encoder Output: ", enc_output.shape)

    decoder = Decoder(
        target_word_index.size,
        embedding_dim=EMBEDDING_DIM,
        enc_units=NUM_UNITS,
        dec_units=NUM_UNITS,
        batch_size=BATCH_SIZE)
    decoder = decoder.to(device)


    dec_hidden = enc_hidden  # .squeeze(0)
    dec_input = torch.tensor([target_word_index.word2idx[SOS_TOKEN]] * BATCH_SIZE)
    print("Decoder Input: ", dec_input.shape)
    print("--------")

    for t in range(1, y.size(1)):
        # enc_hidden: 1, batch_size, enc_units
        # output: max_length, batch_size, enc_units
        predictions, dec_hidden = decoder(dec_input.to(device),
                                             dec_hidden.to(device))

        print("Prediction: ", predictions.shape)
        print("Decoder Hidden: ", dec_hidden.shape)

        # loss += loss_function(y[:, t].to(device), predictions.to(device))

        dec_input = y[:, t]
        print(dec_input.shape)
    return dict(predictions=predictions, decoder_hidden=dec_hidden, decoder_input=dec_input)

## Train End-to-End

criterion = nn.CrossEntropyLoss(ignore_index=target_word_index.get('<pad>'))


def loss_function(real, pred):
    """ Only consider non-zero inputs in the loss; mask needed """
    # mask = 1 - np.equal(real, 0) # assign 0 to all above 0 and 1 to all 0s
    # print(mask)
    mask = real.ge(1).type(FloatTensor)

    loss_ = criterion(pred, real) * mask
    return torch.mean(loss_)

encoder = Encoder(input_word_index.size, embedding_dim=EMBEDDING_DIM, enc_units=NUM_UNITS, batch_size=BATCH_SIZE)
decoder = Decoder(target_word_index.size, embedding_dim=EMBEDDING_DIM,
                  enc_units=NUM_UNITS, dec_units=NUM_UNITS, batch_size=BATCH_SIZE)

encoder.to(device)
decoder.to(device)

optimizer = optim.Adam(list(encoder.parameters()) + list(decoder.parameters()), lr=LEARNING_RATE)
for epoch in tqdm(range(NUM_EPOCHS)):
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
        dec_input = torch.tensor([target_word_index.word2idx[SOS_TOKEN]] * BATCH_SIZE)

        # run code below for every timestep in the ys batch
        for t in range(1, ys.size(1)):
            # predictions: [batch_size, vocab_size]
            predictions, dec_hidden = decoder(dec_input.to(device),
                                              dec_hidden.to(device))
            predictions = predictions.squeeze(0)
            loss += loss_function(ys[:, t].to(device), predictions.to(device))
            # loss += loss_
            dec_input = ys[:, t]

        batch_loss = (loss / int(ys.size(1)))
        total_loss += batch_loss

        optimizer.zero_grad()

        # Clip the gradients to 1
        torch.nn.utils.clip_grad_norm_(decoder.parameters(), 1)
        torch.nn.utils.clip_grad_norm_(encoder.parameters(), 1)

        loss.backward()

        # UPDATE MODEL PARAMETERS
        optimizer.step()

    # print('Epoch {} Loss {:.4f}'.format(batch, batch_loss.detach().item()))

    # TODO: Save checkpoint for model
    print(f"Epoch {(epoch+1):03d} Loss {total_loss/N_BATCH:.2f}  Time:{(time.time()-start):03.3f} s")


def convert_to_sentences(batch, vocab=target_word_index):
    sentences = []
    for s in batch:
        sentences.append(
            ' '.join([vocab[int(i.item())] for i in s]))
    return sentences

# In[ ]:


def predict_batch(dataset=dataset, num_batches=1):
    """ FIXME: only works for one batch (num_batches=1) """
    total_loss = 0
    for (batch_num, (inp, targ, inp_len)) in enumerate(dataset):
        if batch_num >= num_batches:
            break
        loss = 0

        # FIXME: don't sort
        Xs, ys, lengths = sort_batch(X=inp, y=targ, lengths=inp_len)
        enc_output, enc_hidden = encoder(Xs.to(device), lengths, device=device)
        dec_hidden = enc_hidden

        final_sentences = Variable(torch.zeros(BATCH_SIZE, ys.size(1)))
        # use teacher forcing - feeding the target as the next input (via dec_input)
        dec_input = torch.tensor([target_word_index.word2idx[SOS_TOKEN]]* BATCH_SIZE)
        final_sentences[:,0] = dec_input

        # run code below for every timestep in the ys for this batch
        for t in range(1, ys.size(1)):
            predictions, dec_hidden,  = decoder(dec_input.to(device),
                                                 dec_hidden.to(device),
                                                 )
            predictions = predictions.squeeze(0)
            final_sentences[:, t] = predictions.argmax(axis=1)

            loss += loss_function(ys[:, t].to(device), predictions.to(device))
            # loss += loss_
            dec_input = ys[:, t]

        batch_loss = (loss / int(ys.size(1)))
        total_loss += batch_loss

    total_loss = total_loss / batch_num
    target_sentences = convert_to_sentences(ys, vocab=target_word_index)
    translated_sentences = convert_to_sentences(final_sentences,vocab=target_word_index)
    input_sentences = convert_to_sentences(Xs.numpy().T, vocab=input_word_index)
    return dict(
        batch_loss=batch_loss,
        total_loss=total_loss,
        input_sentences=input_sentences,
        target_sentences=target_sentences,
        translated_sentences=translated_sentences)


print()
print('=' * 100)
predict_batch_results = predict_batch()
for count, (input_sent, target_sent,translation) in enumerate(zip(predict_batch_results['input_sentences'],predict_batch_results['target_sentences'],
                                                            predict_batch_results['translated_sentences'])):
    print(input_sent)
    print(target_sent)
    print(translation)
    print('-' * 100)
print('=' * 100)
print()
# In[52]:


# ##############################################################
# ##############################################################
# ##### NEEDS WORK...

for (inp, targ, inp_len) in dataset:
    break
print(inp)
print(targ)
print(inp_len)
# xs, ys, lens = sort_batch(inp, targ, inp_len)
# enc_output, enc_hidden = encoder(xs.to(device), lens, device=device)
# dec_hidden = enc_hidden


def detokenize_sentences(token_array, token_dictionary, method=None,remove_dummy=False):
    sentences = np.vectorize(token_dictionary.get)(token_array.cpu().numpy().astype(int))
    sentences.tolist()
    list_dummy_tokens = DUMMY_TOKENS

    reshaped_sentences = []

    for sentence in sentences:
        if remove_dummy:
            sentence_drop_tokens = [token for token in sentence if token not in list_dummy_tokens]
        else:
            sentence_drop_tokens = sentence
        if method == 'sentence':
            concat_sentence = ' '.join(sentence_drop_tokens)
        else:
            concat_sentence = sentence_drop_tokens
        reshaped_sentences.append(concat_sentence)

    return reshaped_sentences


def mask_3d(inputs, seq_len, mask_value=0.):
    batches = inputs.size()[0]
    assert batches == len(seq_len)
    max_idx = max(seq_len)
    for n, idx in enumerate(seq_len):
        if idx < max_idx.item():
            if len(inputs.size()) == 3:
                inputs[n, idx.int():, :] = mask_value
            else:
                assert len(inputs.size()) == 2, "The size of inputs must be 2 or 3, received {}".format(inputs.size())
                inputs[n, idx.int():] = mask_value
    return inputs


class Seq2Seq(nn.Module):
    """ Sequence to sequence module """

    # , config=None, vocab_inp_size=None, vocab_out_size=None):
    def __init__(self, encoder, decoder, input_word_index, target_word_index, device=device, debug=True, batch_size=BATCH_SIZE):
        super(Seq2Seq, self).__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.input_word_index = input_word_index
        self.target_word_index = target_word_index
        self.device = device
        self.gpu = str(self.device).strip().lower() != 'cpu'
        self.debug = debug
        self.batch_size = batch_size

        self.loss_fn = torch.nn.CrossEntropyLoss(ignore_index=0)

        if self.debug:
            print(f"self.device: {self.device}")
            print(f"self.gpu: {self.gpu}")
        self.vocab_inp_size = len(self.input_word_index.idx2word)
        self.vocab_out_size = len(self.target_word_index.idx2word)
        # self.batch_size = config.get("batch_size", 64)
        # self.gpu = config.get("gpu", False)
        # self.debug = config.get("debug", False)
        # self.training = False
        # self.device = torch.device("cuda" if self.gpu else "cpu")
        # self.target_max_length = 16

        # Loss Function

    def encode(self, X, lengths=None):
        """
        Given Input Sequence, Pass the Data to Encode

        Return:
        - Encoder Output
        - Encoder State
        """

        # Check to see if batch_size parameter is fixed or base on input batch
        if getattr(self, 'debug'):
            print('X')
            print(X)
            print('lengths')
            print(lengths)
        lengths = LongTensor([len(s) for s in X]) if lengths is None else lengths
        cur_batch_size = X.size()[1]
        if getattr(self, 'debug'):
            print(f"Encoder.cur_batch_size:{cur_batch_size} vs BATCH_SIZE:{BATCH_SIZE}")
        encoder_init_state = self.encoder.initialize_hidden_state()
        print('encoder_init_state.to(self.device)')
        print(encoder_init_state.to(self.device))
        lengths.to(self.device)
        if getattr(self, 'debug'):
            print(f"lengths:{lengths}")
            print(f"type(lengths):{type(lengths)}")
            print(f"type(lengths[0]):{type(lengths[0])}")
            print(f"lengths.shape:{lengths.shape}")
        # Encoder.forward(self, X, lengths):
        encoder_state, encoder_outputs = self.encoder.forward(
            X=X.to(self.device),
            lengths=lengths)

        return encoder_outputs, encoder_state

    def decode(self, encoder_outputs, encoder_hidden, targets, targets_lengths):
        """
        In the simplest seq2seq decoder we use only last output of the encoder.
        This last output is sometimes called the context vector as it encodes context from the entire sequence.
        This context vector is used as the initial hidden state of the decoder.

        At every step of decoding, the decoder is given an input token and hidden state.
        The initial input token is the SOS_TOKEN (start-of-string `<start>`, and the first hidden state is the context vector
        (the encoder’s last hidden state).

        Args:
            encoder_outputs: (B, T, H)
            encoder_hidden: (B, H)
            targets: (B, L)
            targets_lengths: (B)
            input_lengths: (B)
        Vars:
            decoder_input: (B)
            decoder_context: (B, H)
            hidden_state: (B, H)
            attention_weights: (B, T)
        Outputs:
            alignments: (L, T, B)
            logits: (B*L, V)
            labels: (B*L)
        """
        print("encoder_outputs.to(device)")
        encoder_outputs.to(device)
        print(encoder_outputs)
        print(encoder_outputs.size())
        batch_size = encoder_outputs.size()[1]

        max_length = targets.size()[1]
        decoder_input = torch.tensor([[self.target_word_index.word2idx[SOS_TOKEN]]] * batch_size)
        decoder_hidden = encoder_outputs

        logits = Variable(torch.ones(max_length, batch_size, self.decoder.vocab_size))
        final_sentences = Variable(torch.zeros(batch_size, max_length))

        if self.debug:
            print("decoder_input shape: {}".format(decoder_input.shape))
            print("decoder hidden shape:{}".format(decoder_hidden.shape))
            print("encoder output shape:{}".format(encoder_outputs.shape))
            print("targets.shap: {}".format(targets.shape))
            print("target_lengths: {}".format(targets_lengths))
            print("dummy sentences before inference:")
            print(final_sentences)

        decoder_input = decoder_input.to(device)
        decoder_hidden = decoder_hidden.to(device)
        logits = logits.to(device)
        final_sentences = final_sentences.to(device)

        for t in range(1, max_length):
            # The decoder accepts, at each time step t :
            # - an input, [B]
            # - a context, [B, H]
            # - an hidden state, [B, H]
            # - encoder outputs, [B, T, H]

            # The decoder outputs, at each time step t :
            # - an output, [B]
            # - a context, [B, H]
            # - an hidden state, [B, H]
            # - weights, [B, T]

            # enc_hidden: 1, batch_size, enc_units
            # output: max_length, batch_size, enc_units

            # Decoder.forward(self, x, hidden, enc_output)
            predictions, decoder_hidden_output, _ = self.decoder.forward(
                X=decoder_input.to(self.device),
                hidden=decoder_hidden.to(self.device),
                enc_output=encoder_outputs)
            print(predictions.shape, decoder_hidden_output.shape, _.shape)

            # Store Prediction at time step t
            logits[t] = predictions

            if self.training:
                decoder_input = targets[:, t].unsqueeze(1)
            else:
                decoder_input = torch.argmax(predictions, axis=1).unsqueeze(1)
                final_sentences[:, t] = decoder_input.squeeze(1)

                if self.debug:
                    print("final sentences:")
                    print(final_sentences)
        labels = targets.contiguous().view(-1)
        mask_value = 0

        # Masking the logits to prepare for eval
        logits = mask_3d(logits.transpose(1, 0), targets_lengths, mask_value)
        logits = logits.contiguous().view(-1, self.vocab_out_size)
        if self.debug:
            print("Logit dimension: {}".format(logits.shape))
            print("Label dimension: {}".format(labels.shape))
        # Return final state, labels
        return logits, labels.long(), final_sentences

    def step(self, batch, sorted=False):

        x, y, x_len, y_len = batch

        if not sorted:
            # sort the batch for pack_padded_seq in forward function
            x_sorted, y_sorted, x_len_sorted, y_len_sorted = sort_batch(X=x, y=y, lengths=x_len)
        else:
            x_sorted, y_sorted, x_len_sorted, y_len_sorted = x, y, x_len, y_len

        if self.debug:
            print("x_sorted: {}".format(x_sorted.shape))
            print("y_sorted: {}".format(y_sorted.shape))
            print("x_len_sorted: {}".format(x_len_sorted.shape))
            print("y_len_sorted: {}".format(y_len_sorted.shape))

        if self.gpu:
            x_sorted = x_sorted.cuda()
            y_sorted = y_sorted.cuda()
            x_len_sorted = x_len_sorted.cuda()
            y_len_sorted = y_len_sorted.cuda()

        encoder_out, encoder_state = self.encode(x_sorted, x_len_sorted)

        if self.debug:
            if encoder_out.size()[1] > 1:
                a = encoder_out[:, 0, :]
                b = encoder_out[:, 1, :]
                print("check equal tensor 0,1 == {}".format(torch.all(torch.eq(a, b))))

        logits, labels, final_sentences = self.decode(encoder_out, encoder_state, y_sorted, y_len_sorted)
        return logits, labels, final_sentences

    def loss(self, batch, sorted=False):
        logits, labels, final_sentences = self.step(batch, sorted=sorted)
        loss = self.loss_fn(logits, labels)
        return loss, logits, labels, final_sentences


# In[69]:

model = Seq2Seq(
    encoder=encoder,
    decoder=decoder,
    input_word_index=input_word_index,
    target_word_index=target_word_index)


class Translator():
    def __init__(self, model=None, input_word_index=None, target_word_index=None, debug=True):
        """ Initialize a translator with a model and word indexes for the two languages

        Input:
            model (nmt.seq2seq.Seq2Seq): pretrained encoder-decoder (seq2seq) model
            input_word_index (LanguageIndex): source (input) language vocabulary mapping to int IDs for each word
            target_word_index (LanguageIndex): target (output) language vocabulary mapping to int IDs for each word
        """
        super(Translator, self).__init__()
        self.model = model
        self.input_word_index = input_word_index
        self.target_word_index = target_word_index
        self.config = None
        self.max_length_inp = input_word_index.max_phrase_length
        self.max_length_tar = target_word_index.max_phrase_length
        self.debug = debug

    def corpus_translate(self,
                         sentences=(
                             "Ne alegro de que te guste.",
                             "Estare presente.",
                             "Tom es insensible.",
                             "No te desesperes!")):
        """ Translate a list of sentences (must be in the source language, e.g. Spanish)

        Input:
          sentences (list of str): raw sentences in the source language

        Output:
          pd.Dataframe with column for input (source sentence) and a column for the translated sentence
        """

        # Preprocess
        spanish_sentences = [preprocess_sentence(sent) for sent in sentences]

        # Look up the Spanish tokens from dictionary
        input_oov_token_int = self.input_word_index.word2idx[OOV_TOKEN]
        spanish_sentences = [[self.input_word_index.word2idx.get(
            s, input_oov_token_int) for s in es.split(' ')] for es in spanish_sentences]

        # Input for one sentence is shape (1xMAX_WORDS) so pad the sequence if the input shorter
        input_tensor = [
            pad_token_id_list(s, self.max_length_inp, self.input_word_index[PAD_TOKEN])
            for s in spanish_sentences]

        # Convert into tensors
        dummy_target_tensor = [self.target_word_index.word2idx[SOS_TOKEN]] * self.max_length_tar  # Dummy Target
        # dummy_target_length = len(dummy_target_tensor)
        # num_samples = len(input_tensor)

        inp_batch = torch.tensor(input_tensor)
        inp_lengths = torch.tensor([self.max_length_inp] * self.model.batch_size)

        if self.debug:
            print("inp_batch:")
            print(inp_batch)
            print("inp_lengths:")
            print(inp_lengths)

        # These are dummy tensors that will not be used in prediction
        dummy_targ_batch = torch.tensor([dummy_target_tensor] * self.model.batch_size)
        # targ_len_batch = torch.tensor([dummy_target_length] * num_samples)

        x_sorted, y_sorted, x_len_sorted = sort_batch(
            X=inp_batch, y=dummy_targ_batch, lengths=inp_lengths)
        if self.debug:
            print("inp_batch:")
            print(x_sorted)
            print("inp_len_batch:")
            print(x_len_sorted)
            print("=== Will pass to Seq2Seq ===")

        batch = [x_sorted, y_sorted, x_len_sorted, FloatTensor([len(s) for s in y_sorted])]

        _, _, _, final_sentences = self.model.loss(batch, sorted=True)

        if self.debug:
            print(final_sentences)

        # Convert sentences from idx to list of list of words
        decoded_input = detokenize_sentences(
            inp_batch,
            self.input_word_index,
            method=None)
        print('decoded input:')
        for s in decoded_input:
            print(s)
        decoded_pred = detokenize_sentences(
            final_sentences,
            self.target_word_index,
            method=None)
        print()
        print('decoded predictions:')
        for s in decoded_pred:
            print(s)
        print()
        df = pd.DataFrame({'SpanishInput': decoded_input,
                           'EnglishOutput': decoded_pred})

        return df

    def translate_sentence(self, input_sentence, display=False):
        """ Usage: for one-sentence translate and print output """

        assert isinstance(input_sentence, str)
        pred_df = self.corpus_translate([input_sentence] * self.model.batch_size)

        assert pred_df.shape[0] > 0

        translated_sentence = pred_df['EnglishOutput'][0]

        if display:
            print(' --Spanish Input : {} \n --English Output :{}'.format(input_sentence, translated_sentence))

        return translated_sentence


translator = Translator(
    model=model,
    input_word_index=input_word_index,
    target_word_index=input_word_index,
)
translator.translate_sentence('como estas usted?')


# ##### ^^^NEEDS WORK^^^
# ###########################################################################################
# ###########################################################################################
# ###########################################################################################


print('=' * 100)
print('===== Translations of Training Set ======')
for pair in zip(predict_batch_results['input_sentences'], predict_batch_results['predicted_sentences']):
    print(pair[0])
    print(pair[1])
    print()
print('============== (overfit?) ===============')
print('=' * 100)

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
