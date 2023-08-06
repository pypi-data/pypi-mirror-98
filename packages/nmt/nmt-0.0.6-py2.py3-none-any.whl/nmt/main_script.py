# -*- coding: utf-8 -*-
"""
Main module to run in console
"""

import argparse
import sys
import logging
import pickle
import torch
import json
import os
from pathlib import Path
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split

from torch.utils import data

from nmt.training import train, evaluate
from nmt.models.seq2seq import Seq2Seq
from nmt.utils.load_raw_data import load_raw_text_file, convert_tensor
from nmt.utils.postprocess import create_scorer
from nmt.utils.data_generator import TranslationDataset, LanguageIndex


_logger = logging.getLogger(__name__)


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`FLAGS`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="args for training neural machine translation")
    parser.add_argument('--config', type=Path)
    parser.add_argument('--epochs', default=20, type=int)
    parser.add_argument('--data_path', type=Path)
    parser.add_argument('--model_checkpoint_dir', type=Path)
    parser.add_argument('--metrics_dir', type=Path)
    parser.add_argument('--export_tag', type=str)
    FLAGS, _ = parser.parse_known_args(args)

    return FLAGS


def setup_logging(loglevel=logging.INFO):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    FLAGS = parse_args(args)
    setup_logging()
    _logger.debug("Script Begins here")

    config_path = FLAGS.config

    if not os.path.exists(config_path):
        raise FileNotFoundError

    if not os.path.exists(FLAGS.data_path):
        raise FileNotFoundError

    with open(config_path, "r") as f:
        config = json.load(f)

    _logger.debug("Config file loaded")

    # Create Checkpoint folder
    now = datetime.now()
    current_time = now.strftime("%Y%m%d%H%M")
    checkpoint_path = '{}/{}_epoch_{}_bz_{}'.format(
        FLAGS.model_checkpoint_dir, current_time, FLAGS.epochs, config['batch_size'])
    if not os.path.exists(checkpoint_path):
        os.makedirs(checkpoint_path)

    # Check GPU Availability
    config["gpu"] = torch.cuda.is_available()

    # Load Data
    df = load_raw_text_file(
        FLAGS.data_path, num_examples=config['num_examples'])

    # index language for Input and Output
    inp_index = LanguageIndex(phrases=df["es"].values)
    targ_index = LanguageIndex(df["eng"].values)
    vocab_inp_size = len(inp_index.word2idx)
    vocab_tar_size = len(targ_index.word2idx)

    # Convert Sentences into tokenized tensors
    input_tensor, target_tensor = convert_tensor(df, inp_index, targ_index)
    # Split to training and test set
    input_tensor_train, input_tensor_val, target_tensor_train, target_tensor_val = train_test_split(
        input_tensor, target_tensor, test_size=0.2)
    train_dataset = TranslationDataset(input_tensor_train, target_tensor_train)
    val_dataset = TranslationDataset(input_tensor_val, target_tensor_val)

    # Conver to DataLoader Object
    train_dataset = data.DataLoader(train_dataset,
                                    batch_size=config['batch_size'],
                                    drop_last=True,
                                    shuffle=True)

    eval_dataset = data.DataLoader(val_dataset,
                                   batch_size=config['val_batch_size'],
                                   drop_last=False,
                                   shuffle=True)
    _logger.debug("Train and Val dataset created")

    # Initialize model
    model = Seq2Seq(config, vocab_inp_size, vocab_tar_size)
    scorer = create_scorer(config['metrics'])

    if config['gpu']:
        model = model.cuda()

    # Optimizer
    optimizer = torch.optim.Adam(model.parameters(),
                                 lr=config.get("learning_rate", .001))

    for name, param in model.named_parameters():
        if 'bias' in name:
            torch.nn.init.constant_(param, 0.0)
        elif 'weight' in name:
            torch.nn.init.xavier_normal_(param)
    _logger.debug("Weight Initialized")

    _logger.debug("Training job began")

    # Train and Evaluate over epochs
    all_train_avg_loss = []
    all_eval_avg_loss = []
    all_eval_avg_acc = []

    val_acc_threshold = config['val_acc_threshold']
    best_val_acc = 0

    for epoch in range(FLAGS.epochs):
        run_state = (epoch, FLAGS.epochs)

        # Train needs to return model and optimizer, otherwise
        # the model keeps restarting from zero at every epoch
        model, optimizer, train_avg_loss = train(
            model,
            optimizer,
            train_dataset,
            run_state,
            config['debug'])
        all_train_avg_loss.append(train_avg_loss)

        # Return Val Set Loss and Accuracy
        eval_avg_loss, eval_acc = evaluate(
            model,
            eval_dataset,
            targ_index,
            scorer,
            config['debug'])

        all_eval_avg_loss.append(eval_avg_loss)
        all_eval_avg_acc.append(eval_acc)

        # Save Model Checkpoint if it is at current best
        if eval_acc > val_acc_threshold:
            checkpoint_dict = {
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': eval_avg_loss,
            }

            checkpoint_name = '{}/epoch_{:0.0f}_val_loss_{:0.3f}.pt'.format(
                checkpoint_path, epoch, eval_avg_loss)
            torch.save(checkpoint_dict, checkpoint_name)
            _logger.info("Epoch {} model exported".format(epoch))

        if eval_acc > best_val_acc:
            best_val_acc = eval_acc

    # Export Input and Output Dictionary
    inp_index_export_path = '{}/input_index.p'.format(checkpoint_path)
    tar_index_export_path = '{}/target_index.p'.format(checkpoint_path)

    with open(inp_index_export_path, 'wb') as handle:
        pickle.dump(inp_index, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open(tar_index_export_path, 'wb') as handle:
        pickle.dump(targ_index, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # Export Config
    config_export_path = '{}/model_config.json'.format(checkpoint_path)
    out_file = open(config_export_path, "w")
    json.dump(config, out_file, indent=4)

    # Export Model Learning Curve Info
    df = pd.DataFrame({
        'epoch': range(FLAGS.epochs),
        'train_loss': all_train_avg_loss,
        'eval_loss': all_eval_avg_loss,
        'eval_acc': all_eval_avg_acc
    })

    now = datetime.now()
    current_time = now.strftime("%Y%m%d%H%M%S")
    export_path = '{}/{}_{}_BLEU_{:0.3f}.csv'.format(
        FLAGS.metrics_dir, current_time, FLAGS.export_tag, best_val_acc)
    df.to_csv(export_path, index=False)

    _logger.info("Script ends here")


def run():
    """ Entry point for console_scripts """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
