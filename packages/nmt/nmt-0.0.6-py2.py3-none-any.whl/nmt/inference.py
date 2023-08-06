import os

import torch
import pandas as pd

from nmt.utils.load_pretrained_model import load_language_index, load_config, load_model
from nmt.utils.preprocess import preprocess_sentence, pad_sequences, sort_batch
from nmt.utils.postprocess import detokenize_sentences


class Translator():
    def __init__(self, model_dir=None, model_name=None):
        super(Translator, self).__init__()
        self.model_dir = model_dir
        self.model_name = model_name
        self.input_word_index = None
        self.target_word_index = None
        self.model = None
        self.config = None
        self.max_length_inp = 16
        self.sample_input_sentences = ['Ne alegro de que te guste.',
                                       'Estare presente.', 'Tom es insensible.', 'No te desesperes!']
        self.debug = False

    def load_live_model(self, model, input_word_index, target_word_index):
        self.model = model
        self.input_word_index = input_word_index
        self.target_word_index = target_word_index

    def load_all_pretrained_components(self, gpu_enabled=False, debug=False):

        inp_dict_path = os.path.join(self.model_dir, 'input_index.p')
        target_dict_path = os.path.join(self.model_dir, 'target_index.p')
        config_path = os.path.join(self.model_dir, 'model_config.json')
        model_path = os.path.join(self.model_dir, self.model_name)

        # Set word indices
        self.input_word_index = load_language_index(inp_dict_path)
        self.target_word_index = load_language_index(target_dict_path)

        vocab_inp_size = len(self.input_word_index.word2idx)
        vocab_tar_size = len(self.target_word_index.word2idx)

        config = load_config(config_path)

        # Set debug
        config['debug'] = debug
        self.debug = config['debug']

        # Set GPU capability for inferencing
        config['gpu'] = gpu_enabled

        # Set config
        self.config = config
        self.model, _ = load_model(model_path,
                                   config=config,
                                   vocab_inp_size=vocab_inp_size,
                                   vocab_tar_size=vocab_tar_size)

        print("model loaded: {}".format(bool(self.model)))

    def corpus_translate(self, list_of_spanish_sentences):
        """
        - INPUT: Spanish Sentence
        - OUTPUT: Pandas Dataframe with input column and translation column
        """

        # Preprocess
        spanish_sentences = [preprocess_sentence(sent) for sent in list_of_spanish_sentences]

        # Look up the Spanish tokens from dictionary
        spanish_sentences = [[self.input_word_index.word2idx.get(
            s, self.input_word_index.oov_token) for s in es.split(' ')] for es in spanish_sentences]

        # Input required a 1x16 input so pad the sequence if the input is less
        input_tensor = [pad_sequences(x, self.max_length_inp) for x in spanish_sentences]

        # Convert into tensors
        dummy_target_tensor = [5, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Dummy Target
        dummy_target_length = len(dummy_target_tensor)
        num_samples = len(input_tensor)

        inp_batch = torch.tensor(input_tensor)
        inp_len_batch = torch.tensor([self.max_length_inp] * num_samples)

        if self.debug:
            print("inp_batch:")
            print(inp_batch)
            print("inp_len_batch:")
            print(inp_len_batch)

        # These are dummy tensors that will not be used in prediction
        targ_batch = torch.tensor([dummy_target_tensor] * num_samples)
        targ_len_batch = torch.tensor([dummy_target_length] * num_samples)

        x_sorted, y_sorted, x_len_sorted, y_len_sorted = sort_batch(inp_batch, targ_batch, inp_len_batch, targ_len_batch)
        if self.debug:
            print("inp_batch:")
            print(x_sorted)
            print("inp_len_batch:")
            print(x_len_sorted)
            print("=== Will pass to Seq2Seq ===")

        batch = [x_sorted, y_sorted, x_len_sorted, y_len_sorted]

        _, _, _, final_sentences = self.model.loss(batch, sorted=True)

        if self.debug:
            print(final_sentences)

        # Convert sentences from idx to list of list of words
        decoded_input = detokenize_sentences(
            inp_batch,
            self.input_word_index.idx2word,
            output='sentence')

        decoded_pred = detokenize_sentences(
            final_sentences,
            self.target_word_index.idx2word,
            output='sentence')

        df = pd.DataFrame({'SpanishInput': decoded_input,
                           'EnglishOutput': decoded_pred})

        return df

    def sentence_translate(self, input_sentence, display=False):
        """ Usage: for one-sentence translate and print output """

        assert isinstance(input_sentence, str)
        pred_df = self.corpus_translate([input_sentence])

        assert pred_df.shape[0] > 0

        translated_sentence = pred_df['EnglishOutput'][0]

        if display:
            print(' --Spanish Input : {} \n --English Output :{}'.format(input_sentence, translated_sentence))

        return translated_sentence
