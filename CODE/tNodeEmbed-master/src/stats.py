import os
import pandas as pd
import re

def compile_stat(folder_path, extension='.log'):
    # Initialize lists to store extracted data
    auc_tnodeembed = []
    f1_micro_tnodeembed = []
    f1_macro_tnodeembed = []
    
    auc_node2vec = []
    f1_micro_node2vec = []
    f1_macro_node2vec = []
    
    # Regex pattern to match lines containing model metrics
    pattern = re.compile(r"(tnodeembed|node2vec): {'auc': (\d+\.\d+), 'f1_micro': (\d+\.\d+), 'f1_macro': (\d+\.\d+)}")
    
    # Iterate over files in folder_path
    for file_name in os.listdir(folder_path):
        if file_name.endswith(extension):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                for line in file:
                    match = pattern.search(line)
                    if match:
                        model, auc, f1_micro, f1_macro = match.groups()
                        if model == 'tnodeembed':
                            auc_tnodeembed.append(float(auc))
                            f1_micro_tnodeembed.append(float(f1_micro))
                            f1_macro_tnodeembed.append(float(f1_macro))
                        elif model == 'node2vec':
                            auc_node2vec.append(float(auc))
                            f1_micro_node2vec.append(float(f1_micro))
                            f1_macro_node2vec.append(float(f1_macro))
    
    # Create DataFrame from extracted data
    data = {
        'Model': ['tnodeembed', 'node2vec'],
        'AUC': [auc_tnodeembed, auc_node2vec],
        'F1_micro': [f1_micro_tnodeembed, f1_micro_node2vec],
        'F1_macro': [f1_macro_tnodeembed, f1_macro_node2vec]
    }
    df = pd.DataFrame(data)
    
    # Write DataFrame to CSV file
    output_file = os.path.join(folder_path, 'compiled_stats.csv')
    df.to_csv(output_file, index=False)


def main():
    folder_path = "data/COLLEGE"
    params_college = {...}  # Your parameters for experiments
    
    # Run experiments
    run_experiments(folder_path, params_college)
    
    # Compile statistics
    compile_stat(folder_path)

if __name__ == "__main__":
    main()
