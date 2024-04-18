import os, re
from os.path import join, exists

from datetime import datetime
import networkx as nx
import pandas as pd



def load_dataset(dataset_name, filename):
    '''
    This function is responsible of receiving the dataset name and access the right folder, read and create the graph.
    Args:
        dataset_name: str - the name of the graph dataset

    Returns:
        graph_nx: networkx - graph of the dataset with all needed attributes
        folder_path: str - the path to the dataset folder, in order to dump files in it
    '''

    if str(filename).endswith('.edges'):
        folder_path = join(r"data", dataset_name, 'cleaned-remapped')
    else:
        folder_path = join(r"data", dataset_name)

    dump_folder = join(folder_path, 'dump')
    print(f'Processing Static file: {filename=}')
    

    if dataset_name == 'BITCOIN-ALPHA':
        folder_path = join(r"data", dataset_name)
        graph_path = join(folder_path, filename)
        dump_folder = join(folder_path, 'dump')

        if re.search(r'.*_[0-9]{4}.*', filename):
            if str(filename).endswith('.edges'):
                graph_df = pd.read_csv(graph_path, sep=' ', header=None, names=['from', 'to'])
                graph_df['time'] = int(re.findall(r'\d+', filename)[0])
            else:
                graph_df = pd.read_csv(graph_path)
        else:
            graph_df = pd.read_csv(graph_path, sep=',', header=None, names=['from', 'to', 'label', 'timestamp'])
            graph_df['timestamp'] = pd.to_datetime(graph_df['timestamp'], unit='s')
            graph_df = graph_df[~pd.isnull(graph_df['timestamp'])]
            graph_df['year_column'] = graph_df['timestamp'].dt.year
            graph_df['month_column'] = graph_df['timestamp'].dt.month
            graph_df['day_column'] = graph_df['timestamp'].dt.day
            graph_df['time'] = graph_df['year_column'].astype(str) + graph_df['month_column'].astype(str).str.zfill(2)
            graph_df['time'] = graph_df['time'].astype(int)
            # graph_df.rename({'id1': 'from', 'id2': 'to'}, axis='columns', inplace=True)
        graph_nx = nx.from_pandas_edgelist(graph_df, 'from', 'to', edge_attr=['time'], create_using=nx.Graph())

    elif dataset_name == 'PPI':
        graph_path = join(folder_path, filename)
        if re.search(r'.*_[0-9]{4}.*', filename):
            if str(filename).endswith('.edges'):
                graph_df = pd.read_csv(graph_path, sep=' ', header=None, names=['from', 'to'])
                graph_df['time'] = int(re.findall(r'\d+', filename)[0])
            else:
                # graph_df = pd.read_csv(graph_path)
                graph_df = pd.read_csv(graph_path, sep=',', usecols=['id1', 'id2', 'discovery date'])
                graph_df = graph_df[~pd.isnull(graph_df['discovery date'])]
                graph_df['time'] = graph_df['discovery date'].map(lambda x: eval(x).year)
                graph_df.rename({'id1': 'from', 'id2': 'to'}, axis='columns', inplace=True)
        else:
            graph_df = pd.read_csv(graph_path, sep=',', usecols=['id1', 'id2', 'discovery date'])
            graph_df = graph_df[~pd.isnull(graph_df['discovery date'])]
            graph_df['time'] = graph_df['discovery date'].map(lambda x: eval(x).year)
            graph_df.rename({'id1': 'from', 'id2': 'to'}, axis='columns', inplace=True)
        graph_nx = nx.from_pandas_edgelist(graph_df, 'from', 'to', edge_attr=['time'], create_using=nx.Graph())
    elif dataset_name == 'PPI_NC':
        graph_path = join(folder_path, filename)
        if re.search(r'.*_[0-9]{4}.*', filename):
            if str(filename).endswith('.edges'):
                graph_df = pd.read_csv(graph_path, sep=' ', header=None, names=['from', 'to'])
                graph_df['time'] = int(re.findall(r'\d+', filename)[0])
            else:
                # graph_df = pd.read_csv(graph_path)
                graph_df = pd.read_csv(graph_path, sep=',', usecols=['id1', 'id2', 'discovery date'])
                graph_df = graph_df[~pd.isnull(graph_df['discovery date'])]
                graph_df['time'] = graph_df['discovery date'].map(lambda x: eval(x).year)
                graph_df.rename({'id1': 'from', 'id2': 'to'}, axis='columns', inplace=True)
        else:
            graph_df = pd.read_csv(graph_path, sep=',', usecols=['id1', 'id2', 'discovery date'])
            graph_df = graph_df[~pd.isnull(graph_df['discovery date'])]
            graph_df['time'] = graph_df['discovery date'].map(lambda x: eval(x).year)
            graph_df.rename({'id1': 'from', 'id2': 'to'}, axis='columns', inplace=True)
        graph_nx = nx.from_pandas_edgelist(graph_df, 'from', 'to', edge_attr=['time'], create_using=nx.Graph())
        # Assign labels based on node degree (connected edges)
        for node in graph_nx.nodes():
            degree = graph_nx.degree[node]
            graph_nx.nodes[node]['label'] = degree
            
    elif dataset_name == 'COLLEGE':
        graph_path = join(folder_path, filename)
        if re.search(r'.*_[0-9]{4}.*', filename):
            if str(filename).endswith('.edges'):
                graph_df = pd.read_csv(graph_path, sep=' ', header=None, names=['from', 'to'])
                graph_df['time'] = int(re.findall(r'\d+', filename)[0])
            else:
                graph_df = pd.read_csv(graph_path)
        else:
            graph_df = pd.read_csv(graph_path, sep=' ', header=None, names=['from', 'to', 'timestamp'])
            graph_df['timestamp'] = pd.to_datetime(graph_df['timestamp'], unit='s')
            graph_df = graph_df[~pd.isnull(graph_df['timestamp'])]
            graph_df['year_column'] = graph_df['timestamp'].dt.year
            graph_df['month_column'] = graph_df['timestamp'].dt.month
            graph_df['day_column'] = graph_df['timestamp'].dt.day
            # date_dict = {'year': graph_df['year_column'], 'month': graph_df['month_column'], 'day': graph_df['day_column']}
            # graph_df['time'] = pd.to_datetime(date_dict)
            graph_df['time'] = graph_df['year_column'].astype(str) + graph_df['month_column'].astype(str).str.zfill(2) + graph_df['day_column'].astype(str).str.zfill(2)
            graph_df['time'] = graph_df['time'].astype(int)
            graph_df.rename({'id1': 'from', 'id2': 'to'}, axis='columns', inplace=True)
        graph_nx = nx.from_pandas_edgelist(graph_df, 'from', 'to', edge_attr=['time'], create_using=nx.Graph())
    elif dataset_name == 'COLLEGE_NC':
        graph_path = join(folder_path, filename)
        if re.search(r'.*_[0-9]{4}.*', filename):
            if str(filename).endswith('.edges'):
                graph_df = pd.read_csv(graph_path, sep=' ', header=None, names=['from', 'to'])
                graph_df['time'] = int(re.findall(r'\d+', filename)[0])
            else:
                graph_df = pd.read_csv(graph_path)
        else:
            graph_df = pd.read_csv(graph_path, sep=' ', header=None, names=['from', 'to', 'timestamp'])
            graph_df['timestamp'] = pd.to_datetime(graph_df['timestamp'], unit='s')
            graph_df = graph_df[~pd.isnull(graph_df['timestamp'])]
            graph_df['year_column'] = graph_df['timestamp'].dt.year
            graph_df['month_column'] = graph_df['timestamp'].dt.month
            graph_df['day_column'] = graph_df['timestamp'].dt.day
            # date_dict = {'year': graph_df['year_column'], 'month': graph_df['month_column'], 'day': graph_df['day_column']}
            # graph_df['time'] = pd.to_datetime(date_dict)
            graph_df['time'] = graph_df['year_column'].astype(str) + graph_df['month_column'].astype(str).str.zfill(2) + graph_df['day_column'].astype(str).str.zfill(2)
            graph_df['time'] = graph_df['time'].astype(int)
            graph_df['label'] = graph_df['time'].astype(str)
            graph_df.rename({'id1': 'from', 'id2': 'to'}, axis='columns', inplace=True)
        graph_nx = nx.from_pandas_edgelist(graph_df, 'from', 'to', edge_attr=['time'], create_using=nx.Graph())
        # Assign labels based on node degree (connected edges)
        for node in graph_nx.nodes():
            degree = graph_nx.degree[node]
            graph_nx.nodes[node]['label'] = degree
            

    elif dataset_name == 'slashdot-threads':
        # filename = 'out.slashdot-threads'
        graph_path = join(folder_path, filename)
        graph_df = pd.read_csv(graph_path, sep=' ', header=None, names=['from', 'to', 'weigth', 'timestamp'])
        graph_df['timestamp'] = pd.to_datetime(graph_df['timestamp'], unit='s')
        graph_df = graph_df[~pd.isnull(graph_df['timestamp'])]
        graph_df['year_column'] = graph_df['timestamp'].dt.year
        graph_df['month_column'] = graph_df['timestamp'].dt.month
        graph_df['day_column'] = graph_df['timestamp'].dt.day
        # date_dict = {'year': graph_df['year_column'], 'month': graph_df['month_column'], 'day': graph_df['day_column']}
        # graph_df['time'] = pd.to_datetime(date_dict)
        graph_df['time'] = graph_df['year_column'].astype(int)
        graph_df.rename({'id1': 'from', 'id2': 'to'}, axis='columns', inplace=True)
        graph_nx = nx.from_pandas_edgelist(graph_df, 'from', 'to', edge_attr=['time'], create_using=nx.Graph())

    else:
        raise Exception('dataset not available')

    if not exists(dump_folder):
        os.mkdir(dump_folder)

    return graph_nx, dump_folder

def df2graph(graph_df, source, target, time, create_using=nx.Graph()):
    return nx.from_pandas_edgelist(graph_df, source, target, edge_attr=[time], create_using=create_using)

