import sys, random, time 
import networkx as nx
import node # Import node class to create network 

# Command line arguments
n = len(sys.argv)

# Create a sample graph using NetworkX
G = nx.Graph()


# If number of arguments is less then promt user to enter correct number of arguments.
if n != 6 :
    print("Invalid arguments!")
    print("Usage: simulatory.py <Number of peers> <Fraction of slow peers> <Fraction of fast peers> <Mean of exponential distribution for interarrival time> <Simulation time>")
    exit()
else:
    if  not isinstance(sys.argv[1], int):
        print("Invalid argument!")
        print("Number of peers should be integer.")
        exit()
    if not isinstance(sys.argv[2], float) and sys.argv[1] >= 0 and sys.argv[1] <= 1:
        print("Invalid argument!")
        print("Fraction should be between 0 and 1")
        exit()
    if not isinstance(sys.argv[3], float) and sys.argv[2] >= 0 and sys.argv[2] <= 1:
        print("Invalid argument")
        print("Fraction should be between 0 and 1")
        exit()
    if not isinstance(sys.argv[4], float):
        print("Inter-arrival time should be numeric value")
        exit()
    if not isinstance(sys.argv[5], int):
        print("Simulation time must be integer")

def generate_unique_id():
    timestamp = int(time.time() * 1000)  
    unique_id = f"{timestamp:x}"
    return unique_id

# Function to generate all peers of the node
def generate_nodes(number_of_peers):
    peers_dict =[] 
    hashing_power_list = random.sample(range(1, 101), number_of_peers)
    total_hashing_power = sum(hashing_power_list)
    hashing_power_list = [ i/total_hashing_power for i in hashing_power_list ]
    print(f'hashing_power_list {hashing_power_list}')
    print("-----------------------------------------------------------------------------------------------")
    #self, node_id, coins ,hashing_power, is_slow, is_high_cpu
    neighbours_dict = {}
    for i in range(number_of_peers):
        node_id = generate_unique_id()
        coins = random.randint(1000, 100000)
        hashing_power = hashing_power_list[i]
        is_slow = random.choice([True, False])
        is_high_cpu = random.choice([True, False])
        peers_dict['p'+str(i)] = node.Node(node_id, coins, hashing_power, is_slow, is_high_cpu)
        neighbours_dict['p'+str(i)] = []
    print("----------------------------------------------------------------------------------------------")
    print(f'peers dict {peers_dict}')
    # Generate neighbours
    for i in peers_dict.keys():
        # Generate a random neighbours from the dictionary keys
        no_of_neighbours = random.randint(3, 7)
        neighbours = random.sample([neighbour for neighbour in peers_dict.keys() if neighbour != i], no_of_neighbours)
        for neighbour in neighbours:
            neighbours_dict[neighbour].append(peers_dict[i])
            neighbours_dict[i].append(peers_dict[neighbour])

            G.add_edge(neighbour.node_id, peers_dict[i].node_id)
            G.add_edge(peers_dict[i].node_id, neighbour.node_id)

    print("-----------------------------------------------------------------------------------------------")
    # Add neighbours to each node        
    for i in peers_dict.keys():
        peers_dict[i].add_neighbours(neighbours_dict[i])
        print(i)
        print(peers_dict[i])
    return peers_dict

max_number_of_peers = 30
# Generate random number of peers
number_of_peers = random.randint(6, max_number_of_peers)

generate_nodes(number_of_peers)


if is_connected(G):
        print("The graph is connected. OK")
else:
    print("The graph is not connected. Recreating...")
    #recreate_graph(nodes)