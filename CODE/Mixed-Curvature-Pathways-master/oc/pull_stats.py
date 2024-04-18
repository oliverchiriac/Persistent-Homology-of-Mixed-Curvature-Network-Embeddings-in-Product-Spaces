import pandas as pd
import os
import re

def extract_stats(log_file):
    """
    Extract stats from the last few lines of a log file.
    
    Args:
    - log_file (str): Path to the log file.
    
    Returns:
    - Dictionary containing extracted stats.
    """
    stats = {}
    with open(log_file, 'r') as f:
        lines = f.readlines()
        # Extract stats from the last few lines of the log file
        for line in reversed(lines):
            # Match required patterns using regular expressions
            match_final_loss = re.search(r'final loss=(\d+\.\d+)', line)
            match_best_loss = re.search(r'best loss=(\d+\.\d+), distortion=(\d+\.\d+), map=(\d+\.\d+), wc_dist=(\d+\.\d+)', line)
            match_distortion = re.search(r'Distortion avg=(\d+\.\d+) wc=(\d+\.\d+) me=(\d+\.\d+) mc=(\d+\.\d+)', line)
            match_map = re.search(r'MAP = (\d+\.\d+)', line)
            
            # Update stats dictionary if matches are found
            if match_final_loss:
                stats['final_loss'] = float(match_final_loss.group(1))
            if match_best_loss:
                stats['best_loss'] = float(match_best_loss.group(1))
                stats['distortion'] = float(match_best_loss.group(2))
                stats['map'] = float(match_best_loss.group(3))
                stats['wc_dist'] = float(match_best_loss.group(4))
            if match_distortion:
                stats['avg_distortion'] = float(match_distortion.group(1))
                stats['wc'] = float(match_distortion.group(2))
                stats['me'] = float(match_distortion.group(3))
                stats['mc'] = float(match_distortion.group(4))
            if match_map:
                stats['MAP'] = float(match_map.group(1))
                
            # Break loop if all required stats are found
            if all(key in stats for key in ['final_loss', 'best_loss', 'distortion', 'map', 'wc_dist', 'avg_distortion', 'wc', 'me', 'mc']):
                break
    
    return stats

def extract_filename_data(filename):
    """
    Extract dataset name, number of nodes, and number of edges from the filename.
    
    Args:
    - filename (str): Name of the file.
    
    Returns:
    - Dictionary containing extracted data.
    """

    ## We need different patters for PPI vs CollgeMsg
    if 'PPI' in filename:
        pattern = r'dataset_data-(\w+)-cleaned-remapped-interactions_with_dates_(\d+)_nodes_(\d+)_edges_(\d+)_component_\d+\.edges-riemann_--batch-size-epochs_(\d+)-subsample_16-hyp_(\d+)-dim_(\d+)-euc_(\d+)-edim_(\d+)-sph_(\d+)-sdim_(\d+)_log'
    elif 'College' in filename:
        pattern = r'dataset_data-(\w+)-cleaned-remapped-CollegeMsg_(\d+)_nodes_(\d+)_edges_(\d+)_component_\d+\.edges-riemann_--batch-size-epochs_(\d+)-subsample_16-hyp_(\d+)-dim_(\d+)-euc_(\d+)-edim_(\d+)-sph_(\d+)-sdim_(\d+)_log'
    elif 'BITCOIN-ALPHA' in filename:
        pattern = r'dataset_data-(\w+-\w+)-cleaned-remapped-soc-sign-bitcoinalpha.e_(\d+)_nodes_(\d+)_edges_(\d+)_component_\d+\.edges-riemann_--batch-size-epochs_(\d+)-subsample_16-hyp_(\d+)-dim_(\d+)-euc_(\d+)-edim_(\d+)-sph_(\d+)-sdim_(\d+)_log'
    else:
        print(F'UNRECOGNIZED {filename=}')
        return {'dataset': None, 'time': None, 'nodes': None, 'edges': None, 'epochs': None, 'hyp': None, 'dim': None, 'euc': None, 'edim': None, 'sph': None, 'sdim': None}

    match = re.match(pattern, filename)
    if match:
        dataset = match.group(1)
        time = int(match.group(2))
        nodes = int(match.group(3))
        edges = int(match.group(4))
        epochs = int(match.group(5))
        hyp = int(match.group(6))
        dim = int(match.group(7))
        euc = int(match.group(8))
        edim = int(match.group(9))
        sph = int(match.group(10))
        sdim = int(match.group(11))
        return {'dataset': dataset, 'time': time, 'nodes': nodes, 'edges': edges, 'epochs': epochs, 'hyp': hyp, 'dim': dim, 'euc': euc, 'edim': edim, 'sph': sph, 'sdim': sdim}
    else:
        return {'dataset': None, 'time': None, 'nodes': None, 'edges': None, 'epochs': None, 'hyp': None, 'dim': None, 'euc': None, 'edim': None, 'sph': None, 'sdim': None}

def main(folder_path, csv_file, file_pattern):
    # Delete the existing CSV file if it exists
    if os.path.exists(csv_file):
        os.remove(csv_file)

    # Initialize an empty DataFrame or read existing CSV file
    df = pd.DataFrame()

    # Count the number of files processed
    num_files_processed = 0

    # Find log files matching the specified pattern
    for filename in os.listdir(folder_path):
        if re.match(file_pattern, filename):
            print(f"Processing file: {filename}")
            log_file = os.path.join(folder_path, filename)
            stats = extract_stats(log_file)
            stats['filename'] = filename  # Add filename to stats
            
            # Extract data from filename
            filename_data = extract_filename_data(filename)
            stats.update(filename_data)  # Add extracted data to stats
            
            df = pd.concat([pd.DataFrame(stats, index=[0]), df], ignore_index=True)  # Concatenate stats to DataFrame
            num_files_processed += 1

    # Reorder columns
    cols = ['filename', 'dataset', 'time', 'nodes', 'edges', 'epochs', 'hyp', 'dim', 'euc', 'edim', 'sph', 'sdim', 'MAP', 'avg_distortion', 'wc', 'me', 'mc', 'best_loss', 'distortion', 'map', 'wc_dist', 'final_loss']
    df = df[cols]
    
    # Sort DataFrame by dataset and nodes in descending order
    df = df.sort_values(by=['dataset', 'time'], ascending=[True, False])

    # Write DataFrame to CSV file
    df.to_csv(csv_file, index=False)

    # Print the number of files processed
    print(f"Number of files processed: {num_files_processed}")

def write_results(dataset_name, folder_with_logs='RESULTS_BAK', file_csv='stats.csv'):
    file_csv = f'{dataset_name}-{file_csv}'
    file_csv = os.path.join(folder_with_logs, file_csv)
    file_pattern = f'dataset_data-{dataset_name}-cleaned.*_log\.txt$'
    main(folder_with_logs, file_csv, file_pattern)
    print(f'{file_csv} written.')

if __name__ == "__main__":
    
    #write_results('BITCOIN-ALPHA', folder_with_logs='RESULTS-BITCOIN-ALPHA', file_csv='stats.csv' )
    # write_results('COLLEGE', folder_with_logs='RESULTS-COLLEGE', file_csv='stats.csv' )
    write_results('PPI', folder_with_logs='RESULTS-PPI', file_csv='stats.csv' )
