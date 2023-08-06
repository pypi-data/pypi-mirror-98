"""This module loads data"""
import pandas as pd
from nmt.utils.preprocess import preprocess_sentence


# # TODO: these should be in a constants.py file
# PAD_TOKEN = '<pad>'
# OOV_TOKEN = '<oov>'

def load_raw_text_file(file_path, num_examples=None, clean=True):
    """
    Input: Path for raw data
    Output: Preprocessed Dataframe
    """
    lines = open(file_path, encoding='UTF-8').read().strip().split('\n')

    # creates lists containing each pair
    original_word_pairs = [[w for w in line.split('\t')] for line in lines]

    if num_examples:
        original_word_pairs = original_word_pairs[:num_examples]

    # Store data as a Pandas dataframe
    df = pd.DataFrame(original_word_pairs, columns=["eng", "es", 'info'])

    if clean:
        # Now we do the preprocessing using pandas and lambdas
        df["eng"] = df.eng.apply(lambda w: preprocess_sentence(w))
        df["es"] = df.es.apply(lambda w: preprocess_sentence(w))

    return df


def texts_to_tensors(texts, language_index):
    # Vectorize the input and target languages
    return [
        [language_index.word2idx[t] for t in s.split()]
        for s in texts
    ]


# FIXME:
# this implementation hard codd the names of languages,
# instead should be a function that processes a list of phrases to produce an index and a set of tensors
# function can be called twice, once for each language

# def convert_tensor(df, input_word_index, target_word_index, pad_token='<pad>'):
#     """ Convert sentences into tensors """

#     # Vectorize the input and target languages
#     input_tensors = texts_to_tensors(df['eng'], input_word_index)
#     target_tensors = texts_to_tensors(df['es'], target_word_index)

#     # calculate the max_length of input and output tensor
#     max_length_inp = max(len(t) for t in input_tensors)
#     max_length_tar = max(len(t) for t in target_tensors)

#     input_tensors = [pad_token_id_list(x, max_length_inp, input_word_index[pad_token]) for x in input_tensors]
#     target_tensors = [pad_token_id_list(x, max_length_tar, target_word_index[pad_token]) for x in target_tensors]

#     return input_tensors, target_tensors
