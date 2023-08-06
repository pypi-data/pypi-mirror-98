""" This script demonstrates how to run grid search """

from itertools import product
from nmt.main import run

def hyper_tune():

    learning_rate_list = [1e-4, 1e-5, 1e-6]
    batch_size_list = [8, 32, 64]
    embedding_dim_list = [64, 128, 256]

    args_dict = {
        'data_path': '/home/winnie/nmt/repo/machine-translation/data/spa.txt',
        'checkpoint_dir': '/home/winnie/nmt/dev/export_model',
        'metrics_dir': '/home/winnie/nmt/dev/metrics',
        'epochs': 2,
        'gpu': True
    }

    all_config = []
    all_best_val_loss = []

    for lr, bz, embed in product(learning_rate_list, batch_size_list, embedding_dim_list):
        model, learning_curve = run(batch_size=bz,
                                    learning_rate=lr,
                                    embedding_dim=embed,
                                    **args_dict)

        best_val_loss = learning_curve['eval_loss'].min()

        all_config.append((lr, bz, embed))
        all_best_val_loss.append(best_val_loss)

    min_idx = all_best_val_loss.index(min(all_best_val_loss))
    print("best config = {}".format(all_config[min_idx]))
    print("best val loss = {:.3f}".format(all_best_val_loss[min_idx]))


if __name__ == "__main__":
    hyper_tune()
