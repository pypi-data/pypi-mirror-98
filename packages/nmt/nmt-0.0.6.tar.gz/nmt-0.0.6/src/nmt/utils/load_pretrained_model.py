import torch
import pickle
import copy
import json

from nmt.models.seq2seq import Seq2Seq

DEFAULT_CONFIG = {
    "decoder": "RNN",
    "encoder": "RNN",
    "n_channels": 4,
    "encoder_hidden": 64,
    "encoder_layers": 1,
    "encoder_dropout": 0.0,
    "bidirectional_encoder": False,
    "decoder_hidden": 64,
    "decoder_layers": 1,
    "decoder_dropout": 0.1,
    "bidirectional_decoder": False,
    "n_classes": 7,
    "batch_size": 64,
    "sampling_prob": 0.0,
    "embedding_dim": 256,
    "attention_score": "general",
    "attention_mlp_pre": False,
    "learning_rate": 0.00001,
    "metrics": "BLEU",
    "gpu": False,
    "loss": "cross_entropy",
    "val_acc_threshold": 35,
    "debug": False
}

def load_model(checkpoint_binary_path, **kwargs):

    config = kwargs['config']
    vocab_inp_size = kwargs['vocab_inp_size']
    vocab_tar_size = kwargs['vocab_tar_size']

    # Initialize Model and Optimizer
    model = Seq2Seq(config, vocab_inp_size, vocab_tar_size)
    optimizer = torch.optim.Adam(model.parameters(),
                                 lr=config.get("learning_rate", .001))

    checkpoint = torch.load(checkpoint_binary_path)
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    epoch = checkpoint['epoch']
    loss = checkpoint['loss']

    model.eval()

    print("model for epoch {} with loss {:.3f} loaded".format(epoch, loss))

    return model, optimizer


def load_language_index(lang_idx_pickled):

    with open(lang_idx_pickled, 'rb') as handle:
        language_index = pickle.load(handle)

    return language_index


def load_config(config_path):
    config = copy.deepcopy(DEFAULT_CONFIG)
    try:
        config.update(json.load(open(config_path)))
    except (IOError, TypeError):
        print('loading default config')
        pass
    return config
