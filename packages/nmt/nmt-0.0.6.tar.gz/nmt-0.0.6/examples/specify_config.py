
""" This script demonstrates how to specify
more specific config beyond the ones
provided by the command line argument
"""

from nmt.main import run

CUSTOMIZED_CONFIG = {

    "gpu": True,
    "val_acc_threshold": 25,

    # You would want to specify these file path
    'checkpoint_dir': '/home/winnie/nmt/dev/export_model',
    'metrics_dir': '/home/winnie/nmt/dev/metrics',
    'epochs': 2
}

model, learning_curive = run(**CUSTOMIZED_CONFIG)
