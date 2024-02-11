import sys, random, time, threading
import events
import numpy as np
import numpy.random as nprandom
import node # Import node class to create network 

class simulator():
    def __init__(self, number_of_peers, fract_of_slow, fract_of_low_cpu, exp_dist_mean):
        self.number_of_peers = number_of_peers
        self.fract_of_slow = fract_of_slow
        self.fract_of_low_cpu = self.fract_of_low_cpu
        self.exp_dist_mean = exp_dist_mean
        self.simulation_running = True
        self.event_queue = []
        self.all_nodes = self.generate_nodes(self.number_of_peers, self.fract_of_slow, self.fract_of_low_cpu, self.exp_dist_mean, self.event_queue)
    # Function to generate all peers of the node
    def generate_nodes(self, number_of_peers, fract_of_slow, fract_of_slow_cpu, exp_dist_mean, event_queue):

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
            node_id = self.generate_unique_id()
            all_nodes[node_id] = float('inf')
            coins = random.randint(1000, 100000)
            hashing_power = hashing_power_list[i]
            peers_dict['p'+str(i)] = node.Node(node_id, coins, hashing_power, is_slow[i], is_slow_cpu[i], exp_dist_mean, event_queue)
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

    def generate_unique_id(self):
        seed = random.random()
        random_number = random.randint(1000000, 9999999)
        timestamp = int(time.time() * 100)  
        unique_id = f"{timestamp:x}"
        return unique_id+str(random_number)

    def transaction_generator(self):
        trasanction_generated_node = self.all_nodes['p'+str(np.random(1, self.number_of_peers+1))]
        #self, event_created_by, node, node_id, timestamp
        while(self.simulation_running):
            current_time = int(time.time())
            event  = events.TxnGenerated(trasanction_generated_node.node_id, trasanction_generated_node, trasanction_generated_node.node_id, current_time)
            self.event_queue.append(event)
            scale = 1/self.exp_dist_mean
            waiting_time = np.random.exponential(scale)
            time.sleep(waiting_time)
    
    # Method to get message latency
    def get_latency(self, message_type, is_sender_slow, is_receiver_slow, propagation_delay):
        latency = 0
        message_size = 0
        if(message_type == 'transaction'):
            message_size += 8*10**3
        elif(message_type == 'block'):
            message_size += 8*10**6
        
        link_speed = 0
        if not is_sender_slow and not is_receiver_slow:
            link_speed = 100*10**8
        else:
            link_speed = 5*10**8
        
        # Transmission delay
        latency += message_size/link_speed

        # Queing delay
        latency += nprandom.exponential(96*1e3/link_speed)

        # Propagation delay
        latency += propagation_delay

        return latency