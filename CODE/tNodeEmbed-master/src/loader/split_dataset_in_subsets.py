import os
from os.path import join, exists

from datetime import datetime
import networkx as nx
import pandas as pd



def filter_dataset_to_static(dataset_name):


    folder_path = join(r"data", dataset_name)

    if dataset_name == 'PPI':
        filename = "interactions_with_dates.csv"
        filepath = join(folder_path, filename)
        df = pd.read_csv(filepath, sep=',')
        cols = df.columns
        df = df[~pd.isnull(df['discovery date'])]
        df['time'] = df['discovery date'].map(lambda x: eval(x).year)

        grouped = df.groupby('time')
        # Creating smaller dataframes for each group
        smaller_dfs = [group for _, group in grouped]     
        for year, smaller_df in zip(grouped.groups.keys(), smaller_dfs):
            file = f"{filename[:-4]}_{year}.csv"  # Change the filename format as per your requirement
            path = join(folder_path,file)
            smaller_df.to_csv(path, index=False)
            print(f"Data for year {year} has been written to {path}")  
    elif dataset_name == 'COLLEGE':
        filename = 'CollegeMsg.txt'
        graph_path = join(folder_path, filename)
        df = pd.read_csv(graph_path, sep=' ', header=None, names=['from', 'to', 'timestamp'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df = df[~pd.isnull(df['timestamp'])]
        df['year_column'] = df['timestamp'].dt.year
        df['month_column'] = df['timestamp'].dt.month
        df['day_column'] = df['timestamp'].dt.day
        df['time'] = df['year_column'].astype(str) + df['month_column'].astype(str).str.zfill(2) + df['day_column'].astype(str).str.zfill(2)
        df['time'] = df['time'].astype(int)
        
        grouped = df.groupby('time')
        # Creating smaller dataframes for each group
        smaller_dfs = [group for _, group in grouped]     
        for year, smaller_df in zip(grouped.groups.keys(), smaller_dfs):
            file = f"{filename[:-4]}_{year}.csv"  # Change the filename format as per your requirement
            path = join(folder_path,file)
            smaller_df.to_csv(path, index=False)
            print(f"Data for year {year} has been written to {path}")  

    elif dataset_name == 'slashdot-threads':
        filename = 'out.slashdot-threads'
        graph_path = join(folder_path, filename)
        df = pd.read_csv(graph_path, sep=' ', header=None, names=['from', 'to', 'weigth', 'timestamp'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df = df[~pd.isnull(df['timestamp'])]
        df['year_column'] = df['timestamp'].dt.year
        df['month_column'] = df['timestamp'].dt.month
        df['day_column'] = df['timestamp'].dt.day
        # date_dict = {'year': graph_df['year_column'], 'month': graph_df['month_column'], 'day': graph_df['day_column']}
        # graph_df['time'] = pd.to_datetime(date_dict)
        df['time'] = df['year_column'].astype(int)
       
        grouped = df.groupby('time')
        # Creating smaller dataframes for each group
        smaller_dfs = [group for _, group in grouped]     
        for year, smaller_df in zip(grouped.groups.keys(), smaller_dfs):
            file = f"{filename}_{year}"  # Change the filename format as per your requirement
            path = join(folder_path,file)
            smaller_df.to_csv(path, index=False)
            print(f"Data for year {year} has been written to {path}")  

    elif dataset_name == 'BITCOIN-ALPHA':
        filename = 'soc-sign-bitcoinalpha.edges'


        graph_path = join(folder_path, filename)
        df = pd.read_csv(graph_path, sep=',', header=None, names=['from', 'to', 'timestamp'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df = df[~pd.isnull(df['timestamp'])]
        df['year_column'] = df['timestamp'].dt.year
        df['month_column'] = df['timestamp'].dt.month
        df['day_column'] = df['timestamp'].dt.day
        # df['time'] = df['year_column'].astype(str) + df['month_column'].astype(str).str.zfill(2) + df['day_column'].astype(str).str.zfill(2)
        df['time'] = df['year_column'].astype(str) + df['month_column'].astype(str).str.zfill(2) ## only month?
        df['time'] = df['time'].astype(int)
        
        grouped = df.groupby('time')
        # Creating smaller dataframes for each group
        smaller_dfs = [group for _, group in grouped]     
        for year, smaller_df in zip(grouped.groups.keys(), smaller_dfs):
            file = f"{filename[:-4]}_{year}.csv"  # Change the filename format as per your requirement
            path = join(folder_path,file)
            smaller_df.to_csv(path, index=False)
            print(f"Data for {year} has been written to {path}")  

    else:
        raise Exception('dataset not available')




if __name__ == '__main__':
     filter_dataset_to_static('BITCOIN-ALPHA')

