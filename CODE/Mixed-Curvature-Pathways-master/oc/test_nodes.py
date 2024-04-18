import networkx as nx

# # Function to read edges from a file
# def read_edges_from_file(file_path):
#     edges = []
#     with open(file_path, 'r') as file:
#         for i, line in enumerate(file, start=1):
#             edge = line.strip().split()
#             if edge[0] == edge[1]:  # Check if both nodes in the edge are the same
#                 print(f"Edge with the same node repeated in line {i}: {edge}")
#             else:
#                 edges.append((edge[0], edge[1]))
#     return edges

# # Read edges from the file
# file_path = 'data/PPI_txts/interactions_with_dates_2012.txt'  # Replace 'edges.txt' with the actual path to your file
# edges = read_edges_from_file(file_path)

# # Create a NetworkX graph from the edges
# G = nx.Graph()
# G.add_edges_from(edges)

# # Check if any node links to itself
# self_loop_nodes = [node for node in G.nodes() if node in G.neighbors(node)]

# if len(self_loop_nodes) > 0:
#     print("Nodes that link to themselves:", self_loop_nodes)
# else:
#     print("No nodes link to themselves.")


# Function to read edges from a file and write to a new file
def filter_and_write_edges(file_path, output_file_path):
    with open(file_path, 'r') as file:
        with open(output_file_path, 'w') as output_file:
            for i, line in enumerate(file, start=1):
                edge = line.strip().split()
                if edge[0] != edge[1]:  # Check if both nodes in the edge are not the same
                    output_file.write(line)

# Define file paths
input_file_path = 'data/PPI_txts/interactions_with_dates_2012.txt'  # Replace 'edges.txt' with the actual path to your input file
output_file_path = 'data/PPI_txts/interactions_with_dates_2012_clean.txt'  # Specify the path for the output file

# Filter edges and write to the output file
filter_and_write_edges(input_file_path, output_file_path)

print("Filtered edges written to:", output_file_path)

