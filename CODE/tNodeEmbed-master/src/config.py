import platform
from os.path import join
from datetime import datetime
from utils.consts import TLP, NC

time_now = datetime.now().strftime('%y%m%d_%H%M%S')

def get_results_path(filename, experiment_name):
    return join(r"../results", f"{platform.node()}_{time_now}_{filename}_{experiment_name}")



params_bitcoin_alpha = {
    'dataset': 'BITCOIN-ALPHA',
    'task': TLP,  # TLP, NC
    'test_size': 0.2,
    'train_skip': 1,  # down sample the training set
    'n2vargs': {'workers': 10},
    'keras_args': {
        'batch_size': 64,
        'epochs': 20,
        'workers': 10
    }
}


params_college_nc = {
    'dataset': 'COLLEGE_NC',
    'task': NC,  # TLP, NC
    'test_size': 0.2,
    'train_skip': 100,  # down sample the training set
    'n2vargs': {'workers': 10},
    'keras_args': {
        'batch_size': 64,
        'epochs': 25,
        'workers': 10
    }
}

params_ppi_nc = {
    'dataset': 'PPI_NC',
    'task': NC,  # TLP, NC
    'test_size': 0.2,
    'train_skip': 100,  # down sample the training set
    'n2vargs': {'workers': 10},
    'keras_args': {
        'batch_size': 64,
        'epochs': 25,
        'workers': 10
    }
}

params_college = {
    'dataset': 'COLLEGE',
    'task': TLP,  # TLP, NC
    'test_size': 0.2,
    'train_skip': 1,  # down sample the training set
    'n2vargs': {'workers': 10},
    'keras_args': {
        'batch_size': 64,
        'epochs': 25,
        'workers': 10
    }
}

params_ppi = {
    'dataset': 'PPI',
    'task': TLP,  # TLP, NC
    'test_size': 0.2,
    'train_skip': 1,  # down sample the training set
    'n2vargs': {'workers': 10},
    'keras_args': {
        'batch_size': 64,
        'epochs': 25,
        'workers': 10
    }
}
