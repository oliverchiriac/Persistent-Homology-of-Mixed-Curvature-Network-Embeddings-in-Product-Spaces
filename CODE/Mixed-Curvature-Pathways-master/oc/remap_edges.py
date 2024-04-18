import os
import csv


def convert_csv_to_edges(csv_file, output_file):
    id_mapping = {}
    edges = []

    with open(csv_file, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            id1 = row['id1']
            id2 = row['id2']
            if id1 != id2:  # Exclude edges where a node points to itself
                if id1 not in id_mapping:
                    id_mapping[id1] = len(id_mapping)
                if id2 not in id_mapping:
                    id_mapping[id2] = len(id_mapping)
                edges.append((id_mapping[id1], id_mapping[id2]))

    with open(output_file, 'w') as out_file:
        for edge in edges:
            out_file.write(f"{edge[0]} {edge[1]}\n")



def do_work(input_folder, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            csv_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, filename.replace('.csv', '.txt'))
            convert_csv_to_edges(csv_file, output_file)

if __name__ == "__main__":
    input_folder = 'data/PPI'
    output_folder = 'data/PPI2'
    do_work(input_folder, output_folder)

