# -*- coding: utf-8 -*-
import pytest  # noqa
import nmt
import numpy as np
import torch

# Utils Module Unit testing
from nmt.utils.data_generator import LanguageIndex
# from nmt.utils.load_raw_data import convert_tensor
from nmt.utils.postprocess import detokenize_sentences, count_bag_of_words, create_scorer

__author__ = "Man Wai Winnie Yeung and Hobson Lane"
__copyright__ = "Man Wai Winnie Yeung and Hobson Lane"
__license__ = "mit"


def test_package_import():
    assert bool(nmt)


def test_LanguageIndex():
    phrases = ['<start> i am a man <stop>	', '<start> weather is great <stop>	']
    test_language_index = LanguageIndex(phrases)
    assert isinstance(test_language_index.word2idx.get('<start>'), int)
    assert isinstance(test_language_index.idx2word[0], str)


# def test_convert_tensor():

#     target_phrases = ['<start> i am a man <stop>',
#                       '<start> my dog is cute <stop>']
#     input_phrases = ['<start> yo soy un hombre <stop>',
#                      '<start> mi perro es lindo <stop>']

#     inp_index = LanguageIndex(input_phrases)
#     targ_index = LanguageIndex(target_phrases)

#     df = pd.DataFrame({'eng': target_phrases,
#                        'es': input_phrases,
#                        'info': [1, 2]})

#     test_input_tensor, test_target_tensor = convert_tensor(df, inp_index, targ_index)

#     assert len(test_input_tensor) == 2
#     assert len(test_target_tensor) == 2


def test_create_scorer():
    scorer = create_scorer(method='BoW')
    assert bool(scorer)

    scorer = create_scorer(method='BLEU')
    assert bool(scorer)


def test_detokenize_sentences():
    sentences_array = np.array([[1, 4, 5, 2, 3], [1, 4, 5, 6, 2]])
    sentences_array = torch.tensor(sentences_array)

    token_dictionary = {1: '<start>',
                        2: '<stop>	',
                        3: '<pad>',
                        4: 'hi',
                        5: 'bye',
                        6: 'cool'}
    sentences = detokenize_sentences(sentences_array, token_dictionary, output='sentence')
    assert sentences[0] == 'hi bye'
    assert sentences[1] == 'hi bye cool'

def test_count_bag_of_words():

    targ_sentence = [['this', 'is', 'a', 'bird'],
                     ['I', 'love', 'Pho']]
    pred_sentence = [['this', 'is', 'a', 'sealion'],
                     ['I', 'love', 'Table', 'Tennis']]

    cum_accuracy = count_bag_of_words(targ_sentence, pred_sentence, output='sum')
    exp_accuracy = 0.75 + 2 / 3

    assert cum_accuracy == exp_accuracy
