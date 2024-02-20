import matplotlib.pyplot as plt
import csv
import networkx as nx

# Replace 'your_file.csv' with the actual path to your CSV file
csv_file_path = './blockchain_tree_csv/blockchain_tree_27c704b4f61540147.csv'

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
    source = column1_data[i]
    target = column2_data[i]
    G.add_edge(source, target)

# Draw the graph
pos = nx.spring_layout(G)  # You can choose a different layout if needed
nx.draw(G, pos, with_labels=True, arrowsize=10, node_size=700, node_color='skyblue', font_size=8, font_color='black', font_weight='bold', edge_color='gray', width=1.5)

plt.title('Directed Graph with Integer Labels')

# Save the graph
plt.savefig('blockchain_graph_node1.png')