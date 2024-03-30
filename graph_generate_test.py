import matplotlib.pyplot as plt
import csv
import networkx as nx
import sys

def generate_graph(node_id, file_name):
    # Replace 'your_file.csv' with the actual path to your CSV file
    csv_file_path = './blockchain_tree_csv/blockchain_tree_'+str(node_id)+'.csv'

    # block and miner file 
    block_miner_file_path = 'miner_mappings.csv'
    # Lists to store data from CSV columns
    column1_data = []
    column2_data = []

    # Read data from CSV file
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        # Skip header row if it exists
        next(csv_reader, None)
        
        # Extract data from columns
        for row in csv_reader:
            column1_data.append(row[0])  # Keep as string
            column2_data.append(row[1])  # Keep as string
    
    # Read blocks and color parent mappings
    colors_dict = {}
    with open(block_miner_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        # Skip header if any
        next(csv_reader, None)
        # Extract data from columns
        for row in csv_reader:
            colors_dict[row[0]] = row[1]
        
    # Create a directed graph using NetworkX
    G = nx.DiGraph()

    # Map unique values to integer labels
    unique_values = list(set(column1_data + column2_data))
    unique_values.sort()
    node_colors = []
    # Map color to respective block depending on wheter it is from adversary of honest node.
    for i in unique_values: 
        if int(colors_dict[i]) == 0:
            node_colors.append('skyblue')
        elif int(colors_dict[i]) == 1:
            node_colors.append('red')
        else:
            node_colors.append('orange')
    label_mapping = {value: i + 1 for i, value in enumerate(unique_values)}

    # Add nodes and edges to the graph
    G.add_nodes_from(unique_values)
    for i in range(len(column1_data)):
        source = column1_data[i]
        target = column2_data[i]
        G.add_edge(source, target)

    # Draw the graph
    pos = nx.spring_layout(G)  # You can choose a different layout if needed
    nx.draw(G, pos, with_labels=True, arrowsize=2, node_size=80, node_color=node_colors, font_size=5, font_color='black', edge_color='gray', width=1)

    plt.title('Directed Graph with Integer Labels')

    # Save the graph
    output_file_name = str(file_name)+".png"
    plt.savefig(output_file_name)

if len(sys.argv) != 3:
    print("Invalid arguments!")
    print("Parameters should be <node_id> <output_file_name>")
    exit()

generate_graph(sys.argv[1], sys.argv[2])