# Neural Machine Translation (NMT)

## Description

This is the Neural Machine Translation package for NLPIA 2nd Edition. Currently support Spanish-English Seq2Seq model using 1-layer GRU with Bag-of-Word accuracy

## Installation

If you just want to install nmt package from PyPI channel:

```console
$ pip install nmt==0.0.4
```

If you want to modify the source code to run experiments you'll need to install dependencis in an environment and then install the package in `--editable` mode.


### Environment

Dependencies:

- NLTK
- editdistance

Create a conda environment where you can install all the dependencies like pytorch, pandas, nltk, spacy, and scikit-learn.
Jupyter is also installed so developers can experiment in `jupyter console` (ipython) and Data Scientists can use `jupyter notebook`.

```console
$ conda update -y -n base -c defaults conda
$ conda create -y -n nmt 'python=3.7.9'
$ conda env update -n nmt -f environment.yml
$ conda activate nmt || source activate nmt
```

## Usage

### Train an NMT model

1. Activate conda env with the `nmt` package installed
2. `nmt --config ${model_hyperparameter_json} --epochs ${num_epoch} --data_path ${training_file} --model_checkpoint_dir ${export_path} --metrics_dir ${metrics_path}`

### Parameters

- Model Hyperparameter Json: Name of the config file (under the experiment subdirectory)
- Epoch: Number of Epoch
- Training Text File: Directory of the training corpus (.txt)
- Model Checkpoint Path: Directory to save model checkpoint
- Metric Directory: Directory to save learning curve and model metrics

## Roadmap
- [ ] 0. [Add badge for unittests](https://docs.gitlab.com/ee/user/project/badges.html) to README.md
- [ ] 0. Push release to pypi: `git tag -a 0.0.6 -m 'toy_problem.py works!' && python setup.py sdist bdist_wheel upload`
- [x] 1. Set up a simple decoder-encoder model using GRU cells, BLEU score as evaluation metrics
- [x] 2. Conduct hyperparameter search
- [x] 3. Add Attention Mechanism to Decoder-Encoder module
- [ ] 4. Incorporate transfer learning from BERT or other models


## Directory structure

Code Structure within source directory:
- experiments: submodule where hyperparameters are stored in json format and retrieved as config
- models: submodule where Decoder, Encoder, Seq2Seq models are stored
- utils: submodule where Word Dictionary and Data Preprocessing functions are found
- main_script.py: script to kick start model training
- training.py: script to walk through the whole training process



## Credits/References:

- [Benjamin Etienne's repo](https://github.com/b-etienne/Seq2seq-PyTorch/)
- [PyTorch's documentation on Seq2Seq](https://pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html)



