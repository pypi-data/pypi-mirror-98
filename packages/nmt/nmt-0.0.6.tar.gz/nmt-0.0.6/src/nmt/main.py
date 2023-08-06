import argparse
from datetime import datetime
import json
import os
import copy
from pathlib import Path
import pickle
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
import torch

from nmt.models.seq2seq import Seq2Seq
from nmt.utils.load_raw_data import load_raw_text_file, convert_tensor
from nmt.utils.data_generator import TranslationDataset, LanguageIndex
from nmt.training import train, evaluate
from nmt.utils.postprocess import create_scorer
from nmt.inference import Translator

DEFAULT_EPOCHS = 10
DEFAULT_BATCH_SIZE = 64
DEFAULT_NUM_EXAMPLES = 30000

# Define Default Data Path
NMT_DIR = Path(os.path.realpath(__file__)).expanduser().resolve().parent
SRC_DIR = Path(NMT_DIR).parent
BASE_DIR = Path(SRC_DIR).parent
DATA_DIR = Path(BASE_DIR, 'data')
SPANISH_PATH = str(Path(DATA_DIR, 'spa.txt'))
CHECKPOINT_DIR = str(Path(DATA_DIR, 'checkpoints'))
METRICS_DIR = str(Path(DATA_DIR, 'experiments'))


DEFAULT_CONFIG = {
    "decoder": "RNN",
    "encoder": "RNN",
    "vocab": {
        "pad_token": 0,
        "start_token": 1,
        "end_token": 2,
        "oov_token": 3
    },
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
    "val_batch_size": 256,
    "sampling_prob": 0.0,
    "embedding_dim": 256,
    "attention_score": "general",
    "attention_mlp_pre": False,
    "learning_rate": 0.00001,
    "metrics": "BLEU",
    "gpu": False,
    "loss": "cross_entropy",
    "val_acc_threshold": 35,
    "val_loss_threshold": 7,
    "disable_progress_bar": False,
    "debug": False
}

default_kwargs = dict(
    epochs=DEFAULT_EPOCHS,
    batch_size=DEFAULT_BATCH_SIZE,
    num_examples=DEFAULT_NUM_EXAMPLES,
    device='cpu',
    data_path=SPANISH_PATH,
    checkpoint_dir=CHECKPOINT_DIR,
    metrics_dir=METRICS_DIR,
    debug=False)


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`FLAGS`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="args for training neural machine translation")
    parser.add_argument('--epochs', default=DEFAULT_EPOCHS, type=int)
    parser.add_argument('--batch_size', default=DEFAULT_BATCH_SIZE, type=int)
    parser.add_argument('--num_examples', default=DEFAULT_NUM_EXAMPLES, type=int)
    parser.add_argument('--data_path', default=SPANISH_PATH, type=Path)
    parser.add_argument('--checkpoint_dir', default=CHECKPOINT_DIR, type=Path)
    parser.add_argument('--metrics_dir', default=METRICS_DIR, type=Path)
    parser.add_argument('--debug', type=bool)
    FLAGS, _ = parser.parse_known_args(args)
    args_dict = vars(FLAGS)

    return args_dict


def run(**kwargs):

    cli_kwargs = parse_args(sys.argv[1:])

    # Initailize Default Config
    config = copy.deepcopy(DEFAULT_CONFIG)

    # Update Default Config with Default Kwargs (data paths)
    config.update(default_kwargs)

    # Update from command line
    config.update(cli_kwargs)

    # Override config from kwargs
    config.update(kwargs)

    # Confirm if gpu is available on the machine
    config['gpu'] = config['gpu'] and torch.cuda.is_available()

    # Variables needed to define models
    num_examples = config.get('num_examples')
    batch_size = config.get('batch_size')
    epochs = config.get('epochs')
    metrics_dir = config.get('metrics_dir')
    debug = config.get('debug')
    display = config.get('disable_progress_bar')
    data_path = config.get('data_path')
    checkpoint_dir = config.get('checkpoint_dir')

    # Create Checkpoint folder
    now = datetime.now()
    current_time = now.strftime("%Y%m%d%H%M")
    checkpoint_path = '{}/{}_epoch_{}_bz_{}'.format(
        str(checkpoint_dir), current_time, epochs, config['batch_size'])
    if not os.path.exists(checkpoint_path):
        os.makedirs(checkpoint_path)
        print("created directory: {}".format(checkpoint_path))

    if str(checkpoint_dir) == CHECKPOINT_DIR:
        print(("You have not assigned a checkpoint direcotry, your"
               " trained model will be saved in the default"
               " location: {}".format(CHECKPOINT_DIR)))
        print(("It is recommended to specify the export"
               " location like nmt --epochs 10"
               " --checkpoint_dir /home/usr/proj/models"))
    if str(metrics_dir) == METRICS_DIR:
        print(("You have not assigned a metrics direcotry, the statistics"
               " of your trained model will be saved in the default"
               " location: {}".format(METRICS_DIR)))
        print(("It is recommended to specify the export"
               " location like nmt --epochs 10"
               " --metrics_dir /home/usr/proj/metrics"))

    # Load Data
    df = load_raw_text_file(data_path, num_examples=num_examples)
    df_reference = load_raw_text_file(data_path, num_examples=num_examples,clean=False)

    # index language for Input and Output
    vocab_kwargs_dict = config['vocab']
    inp_index = LanguageIndex(phrases=df["es"].values, **vocab_kwargs_dict)
    targ_index = LanguageIndex(phrases=df["eng"].values, **vocab_kwargs_dict)
    vocab_inp_size = len(inp_index.word2idx)  # vocab_size
    vocab_tar_size = len(targ_index.word2idx)

    # Convert Sentences into tokenized tensors
    input_tensor, target_tensor = convert_tensor(df, inp_index, targ_index)

    # Split to training and test set
    input_tensor_train, input_tensor_val, target_tensor_train, target_tensor_val = train_test_split(
        input_tensor, target_tensor, test_size=0.2)
    train_dataset = TranslationDataset(input_tensor_train, target_tensor_train)
    val_dataset = TranslationDataset(input_tensor_val, target_tensor_val)

    # Conver to DataLoader Object
    train_dataset = torch.utils.data.DataLoader(train_dataset,
                                                batch_size=batch_size,
                                                drop_last=True,
                                                shuffle=True)

    eval_dataset = torch.utils.data.DataLoader(val_dataset,
                                               batch_size=batch_size,
                                               drop_last=False,
                                               shuffle=True)
    # Models
    model = Seq2Seq(config, vocab_inp_size, vocab_tar_size)
    scorer = create_scorer(config['metrics'])

    if config['gpu']:
        model = model.cuda()

    # Optimizer
    optimizer = torch.optim.Adam(model.parameters(), lr=config.get("learning_rate", .001))

    for name, param in model.named_parameters():
        if 'bias' in name:
            torch.nn.init.constant_(param, 0.0)
        elif 'weight' in name:
            torch.nn.init.xavier_normal_(param)
    print("Weight Initialized")

    all_train_avg_loss = []
    all_eval_avg_loss = []
    all_eval_avg_acc = []

    val_acc_threshold = config['val_acc_threshold']
    val_loss_threshold = config['val_loss_threshold']
    best_val_acc = 0

    all_translation = []

    for epoch in range(epochs):
        run_state = (epoch, epochs)

        # Train needs to return model and optimizer, otherwise the model keeps restarting from zero at every epoch
        model, optimizer, train_avg_loss = train(
            model,
            optimizer,
            train_dataset,
            run_state,
            debug,
            display)
        all_train_avg_loss.append(train_avg_loss)

        # Return Val Set Loss and Accuracy
        eval_avg_loss, eval_acc = evaluate(
            model,
            eval_dataset,
            targ_index,
            scorer,
            debug,
            display)

        all_eval_avg_loss.append(eval_avg_loss)
        all_eval_avg_acc.append(eval_acc)

        if eval_acc > val_acc_threshold and eval_avg_loss < val_loss_threshold:
            checkpoint_dict = {
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': eval_avg_loss,
            }
            checkpoint_name = '{}/epoch_{:0.0f}_val_loss_{:0.3f}.pt'.format(
                checkpoint_path, epoch, eval_avg_loss)
            torch.save(checkpoint_dict, checkpoint_name)
            print("Epoch {} model exported".format(epoch))

        if eval_acc > best_val_acc:
            best_val_acc = eval_acc

        if epoch % 5 == 0 or eval_acc > val_acc_threshold:
            ## Check sample prediction every 10 epochs
            current_translator = Translator()
            current_translator.load_live_model(model,inp_index,targ_index)

            ## Sample sentences from training data
            list_of_sampled_sentences = df_reference['es'].sample(n=6).tolist()
            df_sampled_translation = current_translator.corpus_translate(list_of_sampled_sentences)
            print("=========Randomly Sampled Translation for epoch {}".format(epoch))
            print(df_sampled_translation)

            df_sampled_translation.loc[:,'epoch'] = epoch
            all_translation.append(df_sampled_translation)

        """
        if eval_acc > 40:
            ## Check sample prediction every 10 epochs
            current_translator = Translator()
            current_translator.load_live_model(model,inp_index,targ_index)

            list_of_candidate_sentences = df_reference['es'].tolist()
            df_translation = current_translator.corpus_translate(list_of_candidate_sentences)
            all_translated_export_path =  '{}/epoch_{}_translation.csv'.format(checkpoint_path,epoch)
            df_translation.to_csv(all_translated_export_path)
        """


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
    learning_curve = pd.DataFrame({
        'epoch': range(epochs),
        'train_loss': all_train_avg_loss,
        'eval_loss': all_eval_avg_loss,
        'eval_acc': all_eval_avg_acc
    })

    now = datetime.now()
    current_time = now.strftime("%Y%m%d%H%M%S")
    export_path = '{}/{}_{:0.0f}_bz_{}_val_loss_{:0.3f}.csv'.format(
        metrics_dir, current_time, epochs, batch_size, eval_avg_loss)

    learning_curve.to_csv(export_path, index=False)

    # Export Translation
    all_translation_df = pd.concat(all_translation)
    translation_export_path = '{}/translation.csv'.format(checkpoint_path)
    all_translation_df.to_csv(translation_export_path,index=False)

    print("Script ends here")


    return model, learning_curve


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--epochs', default=DEFAULT_EPOCHS, type=int)
    parser.add_argument('--batch_size', default=DEFAULT_BATCH_SIZE, type=int)
    parser.add_argument('--num_examples', default=DEFAULT_NUM_EXAMPLES, type=int)
    parser.add_argument('--config_path', type=Path)
    parser.add_argument('--data_path', type=Path)
    parser.add_argument('--checkpoint_dir', type=Path)
    parser.add_argument('--metrics_dir', type=Path)
    parser.add_argument('--debug', type=bool)
    FLAGS, _ = parser.parse_known_args()
    args_dict = vars(FLAGS)
    print(args_dict)
    model, learning_curve = run(**args_dict)
    print(model)
    print(learning_curve.tail())
