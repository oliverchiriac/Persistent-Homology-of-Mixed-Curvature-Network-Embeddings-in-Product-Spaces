from math import ceil
import os
import models
import loader
import config
from metrics import get_metrics
import functools
import os
import sys
import os
import pandas as pd
import re
from keras.callbacks import History
import traceback

def log_to_file(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract parameters passed to the run() method
        dataset = kwargs.get('dataset')
        filename = kwargs.get('filename')
        
        # Generate log file path based on dataset and filename
        log_filename = f"{os.path.splitext(os.path.basename(filename))[0]}.log"
        log_file_path = os.path.join(folder_path, log_filename)
        
        # Check if a custom log filename is provided
        custom_log_file = kwargs.pop('stdout', None)
        
        # Initialize flag to indicate if an exception occurred
        exception_occurred = False
        
        # Open the log file for writing
        with open(log_file_path, 'w') as log_file:
            # Redirect stdout to both the log file and console
            stdout = sys.stdout
            sys.stdout = Tee(log_file, stdout) if custom_log_file is None else log_file
            func(*args, **kwargs)
            # try:
            #     # Call the run function with stdout parameter set to the original stdout
            #     func(*args, **kwargs)
            # except Exception as e:
            #     exception_occurred = True
            #     print(f"An error occurred while running for file {filename}: {e}", file=sys.stderr)
            #     traceback.print_stack()

            # finally:
            #     # Restore original stdout after function execution
            #     sys.stdout = stdout
        
        # Delete the log file if an exception occurred
        if exception_occurred and os.path.exists(log_file_path):
            os.remove(log_file_path)
                
    return wrapper

# Helper class to write to both file and console
class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)

    def flush(self):
        for f in self.files:
            f.flush()

@log_to_file
def run(**kwargs):
    # load graph
    print(f'# load graph')
    graph_nx, dump_folder = loader.load_dataset(kwargs['dataset'], kwargs['filename'])

    # initialize tNodeEmbed
    task = kwargs['task']
    test_size = kwargs['test_size']
    print(f'# initialize tNodeEmbed for dataset={kwargs["dataset"]}, {test_size=}')
#    tnodeembed = models.tNodeEmbed(graph_nx, task=task, dump_folder=dump_folder, test_size=test_size, **kwargs['n2vargs'])
    tnodeembed = models.tNodeEmbed(graph_nx, task=task, dump_folder=dump_folder, test_size=test_size, align=False, **kwargs['n2vargs']) ## changed 04/24


    # load dataset
    print(f'# load dataset')
    X, y = tnodeembed.get_dataset(train_skip=kwargs['train_skip'])

    # fit
    print(f'# fit')
    keras_args = kwargs['keras_args']
    batch_size = keras_args.pop('batch_size', 32)
    steps_per_epoch = ceil(len(X['train']) / batch_size)
    # tNodeEmbed
    print(f'# tNodeEmbed {steps_per_epoch=}')
    generator = loader.dataset_generator(X['train'], y['train'], tnodeembed.graph_nx, tnodeembed.train_time_steps, batch_size=batch_size)
    history_tNodeEmbed = History()
    tnodeembed.fit_generator(generator, steps_per_epoch, callbacks=[history_tNodeEmbed], **keras_args)
    tNodeEmbed_final_loss = history_tNodeEmbed.history['loss'][-1]
    tNodeEmbed_final_accuracy = history_tNodeEmbed.history['accuracy'][-1]

    # node2vec
    print(f'# node2vec')
    static_model = models.StaticModel(task=task)
    generator = loader.dataset_generator(X['train'], y['train'], tnodeembed.graph_nx, [max(tnodeembed.train_time_steps)], batch_size=batch_size)
    history_node2vec = History()
    static_model.fit_generator(generator, steps_per_epoch, callbacks=[history_node2vec], **keras_args)
    node2vec_final_loss = history_node2vec.history['loss'][-1]
    node2vec_final_accuracy = history_node2vec.history['accuracy'][-1]


    # predict
    steps = ceil(len(X['test']) / batch_size)
    print(f'# predict: {steps=}')
    print(f'# predict: tnodeembed_metrics')
    generator = loader.dataset_generator(X['test'], y['test'], tnodeembed.graph_nx, tnodeembed.train_time_steps, batch_size=batch_size, shuffle=False)
    tnodeembed_metrics = get_metrics(y['test'], tnodeembed.predict_generator(generator, steps))
    print(f'# predict: node2vec_metrics')
    generator = loader.dataset_generator(X['test'], y['test'], tnodeembed.graph_nx, [max(tnodeembed.train_time_steps)], batch_size=batch_size, shuffle=False)
    node2vec_metrics = get_metrics(y['test'], static_model.predict_generator(generator, steps))


    print(f'tnodeembed: {tnodeembed_metrics} {tNodeEmbed_final_loss=} {tNodeEmbed_final_accuracy=} ')
    print(f'node2vec: {node2vec_metrics} {node2vec_final_loss=} {node2vec_final_accuracy=} ')


def get_filenames_in_folder(folder_path, extension=None, prefix=None, regex=None):
    """Get list of filenames in a folder based on specified criteria."""
    filenames = os.listdir(folder_path)
    filtered_filenames = []
    
    for filename in filenames:
        file_extension = os.path.splitext(filename)[1]
        
        if extension and file_extension != extension:
            continue
        if prefix and not filename.startswith(prefix):
            continue
        if regex and not re.match(regex, filename):
            continue
        filtered_filenames.append(filename)
    
    return filtered_filenames

def run_experiments(folder_path, params, extension=None, prefix=None, regex=None):
    filenames = get_filenames_in_folder(folder_path, extension, prefix, regex)
    
    for filename in filenames:
        params['filename'] = filename
        params['experiment_name'] = filename  # You can also update experiment_name if needed
        params['results_path'] = config.get_results_path(filename, params['experiment_name'])
        run(**params)
        print(f'FINISHED with {filename=}')


def compile_stat(folder_path, extension='.log'):
    # Initialize dictionary to store extracted data for each file
    data_dict = {}
    
    # Regex pattern to match lines containing model metrics
    pattern = re.compile(r"(tnodeembed|node2vec): {'auc': (\d+\.\d+), 'f1_micro': (\d+\.\d+), 'f1_macro': (\d+\.\d+)} .*final_loss=(\d+\.\d+) .*final_accuracy=(\d+\.\d+)")
    
    # Iterate over files in folder_path
    for file_name in os.listdir(folder_path):
        if file_name.endswith(extension):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                for line in file:
                    match = pattern.search(line)
                    if match:
                        model, auc, f1_micro, f1_macro, final_loss, final_accuracy = match.groups()
                        if file_name not in data_dict:
                            data_dict[file_name] = {}
                        data_dict[file_name][f"{model}-AUC"] = auc
                        data_dict[file_name][f"{model}-F1_micro"] = f1_micro
                        data_dict[file_name][f"{model}-F1_macro"] = f1_macro
                        data_dict[file_name][f"{model}-final_loss"] = final_loss
                        data_dict[file_name][f"{model}-final_accuracy"] = final_accuracy
    
    # Create DataFrame from extracted data
    df = pd.DataFrame.from_dict(data_dict, orient='index')
    df.index.name = 'Filename'
    
    # Reorder columns
    # column_order = ['tnodeembed-AUC', 'node2vec-AUC', 'tnodeembed-F1_micro', 'node2vec-F1_micro',
    #                 'tnodeembed-F1_macro', 'node2vec-F1_macro', 'tnodeembed-final_loss', 'node2vec-final_loss',
    #                 'tnodeembed-final_accuracy', 'node2vec-final_accuracy']
    # df = df[column_order]
    
    # Write DataFrame to CSV file
    dataset = folder_path.split('/')[-1]
    output_file = os.path.join(folder_path, f'tNodeEmbed_compiled_stats_{dataset}.csv')
    df.to_csv(output_file)

    return output_file, len(data_dict)




if __name__ == '__main__':

    ###########################
    ###########################
    ##### PPI  - whole set
    ###########################
    ###########################
    # full dataset (all days)
    folder_path = "data/PPI"  # Update this with your folder path
    extension = ""  # Example extension
    prefix = "interactions_with_dates.csv"  # Example prefix
    regex = None  # Example regex
    #regex = r'.*_[0-9]{4}.*' # _ followed by a year
    run_experiments(folder_path, config.params_ppi, extension, prefix, regex)



    ###########################
    ###########################
    ##### COLLEGE - whole set
    ###########################
    ###########################
    # full dataset (all days)
    # folder_path = "data/COLLEGE"  # Update this with your folder path
    # extension = ".txt"  # Example extension
    # prefix = "CollegeMsg"  # Example prefix
    # regex = None  # Example regex
    # #regex = r'.*_[0-9]{4}.*' # _ followed by a year
    # run_experiments(folder_path, config.params_college, extension, prefix, regex)

    ###########################
    ###########################
    ##### BITCOIN ALPHA - whole set
    ###########################
    ###########################
    # full dataset (all days)
    # folder_path = "data/BITCOIN-ALPHA"  # Update this with your folder path
    # extension = ".edges"  # Example extension
    # prefix = "soc-sign-bitcoinalpha"  # Example prefix
    # regex = None  # Example regex
    # #regex = r'.*_[0-9]{4}.*' # _ followed by a year
    # run_experiments(folder_path, config.params_bitcoin_alpha, extension, prefix, regex)



















    ## static dataset (after Oli picked 12 days)
    ## TEMPORAL DATA THAT IS NOT CLEANED UP
    # ##
    # folder_path = "data/BITCOIN-ALPHA"  # Update this with your folder path
    # extension = ".csv"  # Example extension
    # prefix = "soc-sign-bitcoinalpha"  # Example prefix
    # regex = None  # Example regex
    # regex = r'.*_[0-9]{4}.*' # _ followed by a year
    # run_experiments(folder_path, config.params_bitcoin_alpha, extension, prefix, regex)
    # output_file, num_files_processed = compile_stat(folder_path)
    # print(f"Compiled statistics saved to: {output_file}")
    # print(f"Number of files processed: {num_files_processed}")



    ###########################
    ###########################
    ##### NC work
    ###########################
    ###########################

    ###########################
    ############# NC work - CollegeMSG
    ###########################

    ## COLLEGE - full dataset (all days)
    # folder_path = "data/COLLEGE_NC"  # Update this with your folder path
    # extension = ""  # Example extension
    # prefix = "CollegeMsg.txt"  # Example prefix
    # regex = None  # Example regex
    # #regex = r'.*_[0-9]{4}.*' # _ followed by a year
    # run_experiments(folder_path, config.params_college_nc, extension, prefix, regex)

    ## COLLEGE - one day at a time .csv files
    ## TEMPORAL DATA THAT IS NOT CLEANED UP
    # folder_path = "data/COLLEGE_NC"  # Update this with your folder path
    # extension = ".csv"  # Example extension
    # prefix = "CollegeMsg"  # Example prefix
    # # regex = None  # Example regex
    # regex = r'.*_[0-9]{4}.*' # _ followed by a year
    # run_experiments(folder_path, config.params_college_nc, extension, prefix, regex)

    ## TEMPORAL DATA cleaned and remapped
    # folder_path = "data/COLLEGE_NC/cleaned-remapped"  # Update this with your folder path
    # extension = ".edges"  # Example extension
    # prefix = "CollegeMsg"  # Example prefix
    # # regex = None  # Example regex
    # regex = r'.*_[0-9]{4}.*' # _ followed by a year
    # run_experiments(folder_path, config.params_college_nc, extension, prefix, regex)


    ###########################
    ############# NC work - PPI
    ###########################
    ## PPI - full dataset (all years) 
    # folder_path = "data/PPI_NC"  # Update this with your folder path
    # extension = ""  # Example extension
    # prefix = "interactions_with_dates.csv"  # Example prefix
    # regex = None  # Example regex
    # #regex = r'.*_[0-9]{4}.*' # _ followed by a year
    # run_experiments(folder_path, config.params_ppi_nc, extension, prefix, regex)

    ## COLLEGE - one day at a time .csv files
    ## TEMPORAL DATA THAT IS NOT CLEANED UP
    # folder_path = "data/PPI_NC"  # Update this with your folder path
    # extension = ".csv"  # Example extension
    # prefix = "interactions_with_dates_"  # Example prefix
    # # regex = None  # Example regex
    # regex = r'.*_[0-9]{4}.*' # _ followed by a year
    # run_experiments(folder_path, config.params_ppi_nc, extension, prefix, regex)
    ## TEMPORAL DATA THAT WAS CLEANED UP
    # folder_path = "data/PPI_NC/cleaned-remapped"  # Update this with your folder path
    # extension = ".edges"  # Example extension
    # prefix = "interactions_with_dates_"  # Example prefix
    # # regex = None  # Example regex
    # regex = r'.*_[0-9]{4}.*' # _ followed by a year
    # run_experiments(folder_path, config.params_ppi_nc, extension, prefix, regex)




    ###########################
    ###########################
    ##### TLP work
    ###########################
    ###########################
    ## 
    ## TEMPORAL DATA THAT IS NOT CLEANED UP
    ##
    # folder_path = "data/COLLEGE"  # Update this with your folder path
    # extension = ".csv"  # Example extension
    # prefix = "CollegeMsg"  # Example prefix
    # # regex = None  # Example regex
    # regex = r'.*_[0-9]{4}.*' # _ followed by a year
    # run_experiments(folder_path, config.params_college, extension, prefix, regex)
    # output_file, num_files_processed = compile_stat(folder_path)
    # print(f"Compiled statistics saved to: {output_file}")
    # print(f"Number of files processed: {num_files_processed}")

    ## 
    ## TEMPORAL DATA THAT WAS CLEANED UP
    ##
    # folder_path = "data/COLLEGE/cleaned-remapped"  # Update this with your folder path
    # extension = ".edges"  # Example extension
    # prefix = "CollegeMsg_"  # Example prefix
    # # regex = None  # Example regex
    # regex = r'.*_[0-9]{4}.*' # _ followed by a year

    # run_experiments(folder_path, config.params_college, extension, prefix, regex)


    # 
    # TEMPORAL DATA THAT IS NOT CLEANED UP
    #
    # folder_path = "data/PPI"  # Update this with your folder path
    # extension = ".csv"  # Example extension
    # prefix = "interactions_with_dates_"  # Example prefix
    # # regex = None  # Example regex
    # regex = r'.*_[0-9]{4}.*' # _ followed by a year
    # run_experiments(folder_path, config.params_ppi, extension, prefix, regex)
    # # Compile statistics
    # output_file, num_files_processed = compile_stat(folder_path)
    # print(f"Compiled statistics saved to: {output_file}")
    # print(f"Number of files processed: {num_files_processed}")

    # 
    # TEMPORAL DATA THAT WAS CLEANED UP
    #
    # folder_path = "data/PPI/cleaned-remapped"  # Update this with your folder path
    # extension = ".edges"  # Example extension
    # prefix = "interactions_with_dates_"  # Example prefix
    # # regex = None  # Example regex
    # regex = r'.*_[0-9]{4}.*' # _ followed by a year

    # run_experiments(folder_path, config.params_ppi, extension, prefix, regex)



    # # Compile statistics
    output_file, num_files_processed = compile_stat(folder_path)
    print(f"Compiled statistics saved to: {output_file}")
    print(f"Number of files processed: {num_files_processed}")



