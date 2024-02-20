import matplotlib.pyplot as plt
import csv
import networkx as nx

def is_connected(peers_dict):
    # utility functin to check whether the given graph is connected of not
    num_of_peers = len(peers_dict)
    queue = []
    vis = {}
    root = list(peers_dict.keys())[0]
    queue.append(root)
    vis[root] = True
    count = 1
    while len(queue) > 0:
        curr = queue[0]
        queue.pop(0) 
        for i in peers_dict[curr]:
            if i.node_id not in vis.keys():
                queue.append(i.node_id)
                count += 1
                vis[i.node_id] = True
    return count == num_of_peers


def print_graph(peers_dict):
    # utility function to print the graph
    print(peers_dict)

def generate_graph(file_path, node_id):
    # Replace 'your_file.csv' with the actual path to your CSV file
    csv_file_path = file_path
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

    # Create a directed graph using NetworkX
    G = nx.DiGraph()

    # Map unique values to integer labels
    unique_values = list(set(column1_data + column2_data))
    label_mapping = {value: i + 1 for i, value in enumerate(unique_values)}

    # Add nodes and edges to the graph
    for i in range(len(column1_data)):
        source = label_mapping[column1_data[i]]
        target = label_mapping[column2_data[i]]
        G.add_edge(source, target)

    # Draw the graph
    pos = nx.spring_layout(G)  # You can choose a different layout if needed
    nx.draw(G, pos, with_labels=True, arrowsize=10, node_size=700, node_color='skyblue', font_size=8, font_color='black', font_weight='bold', edge_color='gray', width=1.5)

    plt.title('Directed Graph with Integer Labels')

    # Save the graph
    plt.savefig('./blockchain_tree_graph/blockchain_graph'+node_id+'.png')