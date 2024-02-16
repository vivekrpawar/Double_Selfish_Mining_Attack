import sys, random, time
import node, simulator

n = len(sys.argv)
# If number of arguments is less then promt user to enter correct number of arguments.
if n != 6 :
    print("Invalid arguments!")
    print("Usage: simulatory.py <Number of peers> <Fraction of slow peers> <Fraction of slow cpu peers> <Mean of exponential distribution for interarrival time> <Simulation time>")
    exit()
else:
    if  not sys.argv[1].isdigit():
        print("Invalid argument!")
        print("Number of peers should be integer.")
        exit()
    if not sys.argv[2].replace('.','').isdigit() or float(sys.argv[1]) < 0 or float(sys.argv[2]) > 1:
        print(f'{sys.argv[2]} {isinstance(sys.argv[2], float)}')
        print("Invalid argument!")
        print("Fraction should be between 0 and 1")
        exit()
    if not sys.argv[3].replace('.','').isdigit() or float(sys.argv[3]) < 0 and float(sys.argv[2]) > 1:
        print(f'{sys.argv[3]} {isinstance(sys.argv[3], float)}')
        print("Invalid argument")
        print("Fraction should be between 0 and 1")
        exit()
    if not sys.argv[4].replace('.', '').isdigit():
        print("Mean of exponential distribution for Inter-arrival time should be numeric value")
        exit()
    if not sys.argv[5].isdigit() :
        print("Simulation time must be positive integer")
        exit()

def generate_unique_id():
    seed = random.random()
    random_number = random.randint(1000000, 9999999)
    timestamp = int(time.time() * 100)  
    unique_id = f"{timestamp:x}"
    return unique_id+str(random_number)



# Function to generate all peers of the node
def generate_nodes(number_of_peers, fract_of_slow, fract_of_slow_cpu, exp_dist_mean):

    # peers_dict will contain all the nodes created
    peers_dict = {}

    # Hashing power list will contain hashing power of all the nodes
    hashing_power_list = random.sample(range(1, 101), number_of_peers) 
    total_hashing_power = sum(hashing_power_list)
    hashing_power_list = [ i/total_hashing_power for i in hashing_power_list ] 

    # Neighbour dict will contains neighbours of each node 
    # Key: Node, value: list of neighbours
    neighbours_dict = {}
    all_nodes = {}

    # Create a slow_list and low_cpu to assign slow value to nodes
    is_slow = [False]*number_of_peers
    is_slow_cpu = [False]*number_of_peers

    # Set first some values in the list to true
    for i in range(int(fract_of_slow * n)):
        is_slow[i] = True
    for i in range(int(fract_of_slow_cpu * n)):
        is_slow_cpu[i] = True

    # Suffle the list to assign value randomly 
    random.shuffle(is_slow)
    random.shuffle(is_slow_cpu)

    # Create individual nodes
    for i in range(number_of_peers):
        node_id = generate_unique_id()
        all_nodes[node_id] = float('inf')
        coins = random.randint(1000, 100000)
        hashing_power = hashing_power_list[i]
        peers_dict['p'+str(i)] = node.Node(node_id, coins, hashing_power, is_slow[i], is_slow_cpu[i], exp_dist_mean)
        neighbours_dict['p'+str(i)] = []
    
    # Generate neighbours
    for i in peers_dict.keys():

        # Generate a random neighbours from the dictionary keys
        no_of_neighbours = random.randint(3, 6)
        neighbours = random.sample([neighbour for neighbour in peers_dict.keys() if neighbour != i], no_of_neighbours)
        
        for neighbour in neighbours:
            if peers_dict[i] not in neighbours_dict[neighbour] and len(neighbours_dict[neighbour]) < 6 and peers_dict[neighbour] not in neighbours_dict[i] and len(neighbours_dict[i]) < 6:
                
                # Get propagation delay between the two nodes
                propagation_delay = random.randint(10, 501)
                neighbours_dict[neighbour].append(peers_dict[i]) 
                neighbours_dict[i].append(peers_dict[neighbour])
                all_nodes[peers_dict[neighbour].node_id] = propagation_delay
                all_nodes[peers_dict[i].node_id] = propagation_delay


    # Add neighbours to each node        
    for i in peers_dict.keys():
        peers_dict[i].add_neighbours(neighbours_dict[i])
        peers_dict[i].add_allNodes(all_nodes)
    return peers_dict

number_of_peers = int(sys.argv[1]) 
fract_of_slow = float(sys.argv[2])
fract_of_slow_cpu = float(sys.argv[3])
mean_exp_dist = float(sys.argv[4])
simulation_time = int(sys.argv[5])
# Generate all nodes with respective peers
all_nodes = generate_nodes(number_of_peers, fract_of_slow, fract_of_slow_cpu, mean_exp_dist)

sim = simulator.simulator(number_of_peers, fract_of_slow, fract_of_slow_cpu, mean_exp_dist)
sim.run_simulator(simulation_time) 
sim.stop_simulator()
# threads = []
# all_peers = all_nodes.values()
# for peer in all_peers:
#     thread = threading.Thread(target=peer.master_routine)
#     thread.daemon = True
#     thread.start()
#     threads.append(thread)

# # Main thread continues executing without waiting for the background threads
# print("Main thread continues executing...")

# time.sleep(simulation_time)

# for peer in all_peers:
#     peer.stop_running()

# # Join the background threads to wait for them to finish before exiting the program
# for thread in threads:
#     thread.join()