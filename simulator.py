import sys, random, time, threading
import events
import numpy as np
import numpy.random as nprandom
import node, block # Import node class to create network 
from priority_queue import PriorityQueue
import graph_utils
class simulator():
    def __init__(self, number_of_peers, fract_of_slow, fract_of_low_cpu, exp_dist_mean):
        self.number_of_peers = number_of_peers
        self.fract_of_slow = fract_of_slow
        self.fract_of_low_cpu = fract_of_low_cpu
        self.exp_dist_mean = exp_dist_mean
        self.simulation_running = True
        self.event_queue = PriorityQueue()
        self.all_nodes = self.generate_nodes(self.number_of_peers, self.fract_of_slow, self.fract_of_low_cpu, self.exp_dist_mean, self.event_queue)
    # Function to generate all peers of the node
    def generate_nodes(self, number_of_peers, fract_of_slow, fract_of_low_cpu, exp_dist_mean, event_queue):

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
        for i in range(int(fract_of_slow * number_of_peers)):
            is_slow[i] = True
        for i in range(int(fract_of_low_cpu * number_of_peers)):
            is_slow_cpu[i] = True

        # Suffle the list to assign value randomly 
        random.shuffle(is_slow)
        random.shuffle(is_slow_cpu)

        # Create individual nodes
        node_graph = {}

        # Create a genisis block
        genesis_block =  block.Block(
                block_id=0,
                created_by=0,
                mining_time=0,
                prev_block_id = -1,
                transactions=[],
                length_of_chain=1,
                timestamp=time.time()
                )
        for i in range(number_of_peers):
            node_id = self.generate_unique_id()
            all_nodes[node_id] = float('inf')
            coins = random.randint(1000, 100000)
            hashing_power = hashing_power_list[i]
            peers_dict['p'+str(i)] = node.Node(node_id, coins, hashing_power, is_slow[i], is_slow_cpu[i], exp_dist_mean, event_queue, genesis_block)
            neighbours_dict['p'+str(i)] = []
            node_graph[node_id] = []
        
        while (not graph_utils.is_connected(node_graph)):
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
                node_graph[peers_dict[i].node_id] = neighbours_dict[i]
        # print(peers_dict)
        self.peers_dict = peers_dict
        return peers_dict

    def generate_unique_id(self):
        seed = random.random()
        random_number = random.randint(1000000, 9999999)
        timestamp = int(time.time() * 100)  
        unique_id = f"{timestamp:x}"
        return unique_id+str(random_number)

    def transaction_generate(self): 
        # Generate new transaction 
        # print(self.all_nodes)
        print("Generating transactions!")
        trasanction_generated_node = self.all_nodes['p'+str(random.randint(0, self.number_of_peers-1))]
        current_time = time.time()
        event  = events.TxnGenerated(trasanction_generated_node.node_id, trasanction_generated_node, trasanction_generated_node.node_id, current_time)
        self.event_queue.push(event, event.timestamp) 
    
    def block_generator(self):
        # Schedule block generated event on all the node at start of simulation
        for i in self.all_nodes.keys():
            block_generator_node = self.all_nodes[i]
            current_time = time.time()
            #self, event_created_by, node, node_id, created_at, run_at
            event  = events.BlockGenerate(block_generator_node.node_id, block_generator_node, block_generator_node.node_id, current_time)
            self.event_queue.push(event, event.timestamp)
    
    def run_simulator(self, simulation_time):
        # Run the simulator while simulation is running
        print("running simulator")
        curr_time = time.time()
        start_time = curr_time
        prev_transaction_time = curr_time
        scale = 1/self.exp_dist_mean
        waiting_time = np.random.exponential(scale)
        simulation_started = False
        while(curr_time <= start_time+simulation_time):
            # Generate transaction arter interarival of waiting time
            print(f"{prev_transaction_time + waiting_time } {curr_time}")
            if prev_transaction_time + waiting_time <= curr_time:
                # Generate transaction after waiting for some time
                self.transaction_generate()
                # Wait for the waiting time before generating next transaction
                prev_transaction_time = curr_time
                scale = 1/self.exp_dist_mean
                waiting_time = np.random.exponential(scale)
                # Start generationg block after generating first transaction
                if not simulation_started:
                    self.block_generator() 
                    simulation_started = True
            # Check if there is any event in event queue
            # If the queue is empty then weight for the event
            print(f'event_queue:\n {len(self.event_queue)} {not self.event_queue.is_empty()}')
            if not self.event_queue.is_empty() and self.event_queue.peek().timestamp <= time.time(): 
                # Pop the top event and execute
                event = self.event_queue.pop()
                print(f"Executing events! {event}")
                event.execute_event()
            curr_time = time.time()
            time.sleep(0.1)
        print("Similation is stopped!")
        print("------------------------------------------------------------------------------------------------------")
        for i in self.peers_dict.keys():
            self.print_longest_chain(self.peers_dict[i])
    
    def print_longest_chain(self, node):
        curr_block_id = node.prev_block_id
        print(f'longest chain length: {len(node.blocks[curr_block_id])} top block: {curr_block_id} total number of blocks: {len(node.blocks)}')
        while curr_block_id != 0:
            print(curr_block_id)
            curr_block_id = node.blocks[curr_block_id].prev_block_id
        print(curr_block_id)




