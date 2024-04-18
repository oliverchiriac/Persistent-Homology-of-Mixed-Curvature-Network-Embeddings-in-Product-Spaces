import os
import networkx as nx
import pandas as pd

def create_component_files(graph, output_dir, original_filename, delimiter=' '):
    # Find all connected components in the graph
    connected_components = list(nx.connected_components(graph))
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get the number of nodes and edges in the original graph
    num_nodes = len(graph.nodes())
    num_edges = len(graph.edges())
    
    # Write edge files for each component
    for i, component in enumerate(connected_components):
        component_graph = graph.subgraph(component)
        
        # Relabel nodes of the component from 0 onwards
        component_graph = nx.convert_node_labels_to_integers(component_graph)
        
        component_num_nodes = len(component_graph.nodes())
        component_num_edges = len(component_graph.edges())
        
        # Output file name with original file name, number of nodes, and number of edges
        output_file = f"{original_filename}_nodes_{component_num_nodes}_edges_{component_num_edges}_component_{i}.edges"
        output_file = os.path.join(output_dir, output_file)
        
        with open(output_file, 'w') as f:
            for edge in component_graph.edges():
                f.write(f"{edge[0]}{delimiter}{edge[1]}\n")

def read_directed_graph_from_csv(file_path, from_column, to_column):
    df = pd.read_csv(file_path)
    graph = nx.from_pandas_edgelist(df, from_column, to_column, create_using=nx.DiGraph())
    return graph.to_undirected()

def main(input_file, from_column, to_column, delimiter=' '):
    # Output directory for component edge files
    output_directory = os.path.join(os.path.dirname(input_file), "component_edges")
    
    # Read directed graph from the input CSV file and convert to undirected
    graph = read_directed_graph_from_csv(input_file, from_column, to_column)
    
    # Remove duplicate edges
    graph.remove_edges_from(nx.selfloop_edges(graph))
    
    # Identify the largest connected component
    largest_component = max(nx.connected_components(graph), key=len)
    largest_component_graph = graph.subgraph(largest_component)
    
    # Create edge files for each component
    create_component_files(largest_component_graph, output_directory, os.path.splitext(os.path.basename(input_file))[0], delimiter)
    
    print("Edge files for each component have been created in:", output_directory)

if __name__ == "__main__":

       
    input_folder = r'data/BITCOIN-ALPHA/'
    column_from = 'id1'
    column_from = 'from'
    column_to = 'to'
    for filename in os.listdir(input_folder):
        if filename.endswith('.csv') and '_' in filename:
            csv_file = os.path.join(input_folder, filename)
            main(csv_file, column_from, column_to, ' ')            

    # input_folder = r'data/PPI/'
    # column_from = 'id1'
    # column_to = 'id2'
    # for filename in os.listdir(input_folder):
    #     if filename.endswith('.csv') and '_' in filename:
    #         csv_file = os.path.join(input_folder, filename)
    #         main(csv_file, column_from, column_to, ' ')

    # input_folder = r'data/COLLEGE/'
    # column_from = 'from'
    # column_to = 'to'
    # for filename in os.listdir(input_folder):
    #     if filename.endswith('.csv') and '_' in filename:
    #         csv_file = os.path.join(input_folder, filename)
    #         main(csv_file, column_from, column_to, ' ')
        
    # import sys
    # if len(sys.argv) != 2:
    #     print("Usage: python script.py input_file_name.csv")
    # else:
    #     main(sys.argv[1])


    # if len(sys.argv) != 2:
    #     print("Usage: python script.py input_file_name.edges")
    #     filename='data\COLLEGE\CollegeMsg_20040422.csv'
    # else:
    #     filename = sys.argv[1]
    # main(filename)
