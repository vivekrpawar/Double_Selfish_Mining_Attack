import sys, random, time, threading
import events
import numpy as np
import numpy.random as nprandom
import node, block # Import node class to create network 
from priority_queue import PriorityQueue
import graph_utils 
class simulator():
    def __init__(self, number_of_peers, fract_of_slow, fract_of_low_cpu, exp_dist_mean, c1, c2):
        self.number_of_peers = number_of_peers
        self.fract_of_slow = fract_of_slow
        self.fract_of_low_cpu = fract_of_low_cpu
        self.exp_dist_mean = exp_dist_mean
        self.c1 = c1
        self.c2 = c2 
        self.simulation_running = True
        self.event_queue = PriorityQueue()
        self.all_nodes = self.generate_nodes(self.number_of_peers-2, self.fract_of_slow, self.fract_of_low_cpu, self.exp_dist_mean, self.event_queue)

    # Function to generate all peers of the node
    def generate_nodes(self, number_of_peers, fract_of_slow, fract_of_low_cpu, exp_dist_mean, event_queue):

        # peers_dict will contain all the nodes created
        peers_dict = {}

        # Hashing power list will contain hashing power of all the nodes
        remaining_hashing_power = 1-self.c1-self.c2
        hashing_power_list = random.sample(range(1, 101), number_of_peers) 
        total_hashing_power = sum(hashing_power_list)
        hashing_power_list = [ i*remaining_hashing_power/total_hashing_power for i in hashing_power_list ] 

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
            peers_dict['p'+str(i)] = node.Node(node_id, coins, hashing_power, is_slow[i], is_slow_cpu[i], exp_dist_mean, event_queue, genesis_block, False)
            neighbours_dict['p'+str(i)] = []
            node_graph[node_id] = []
        
        # Generate adversary node c1
        c1_id = self.generate_unique_id()
        c1_coins = random.randint(1000, 100000)
        peers_dict['p'+str(number_of_peers)] = node.Node(c1_id, c1_coins, self.c1, False, False, exp_dist_mean, event_queue, genesis_block, True)
        neighbours_dict['p'+str(number_of_peers)] = []
        node_graph[c1_id] = []

        # Generate adversary node c2
        c2_id = self.generate_unique_id()
        c2_coins = random.randint(1000, 100000)
        peers_dict['p'+str(number_of_peers+1)] = node.Node(c2_id, c2_coins, self.c2, False, False, exp_dist_mean, event_queue, genesis_block, True)
        neighbours_dict['p'+str(number_of_peers+1)] = []
        node_graph[c2_id] = []

        # Store adversary node id
        self.c1_id = c1_id
        self.c2_id = c2_id

        print("Anamoly 1 id: "+c1_id)
        print("Anamoly 2 id: ", c2_id)
        while (not graph_utils.is_connected(node_graph)):
            # Generate neighbours
            for i in peers_dict.keys():

                # Generate a random neighbours from the dictionary keys
                no_of_neighbours = random.randint(3, 6)
                neighbours = random.sample([neighbour for neighbour in peers_dict.keys() if neighbour != i], no_of_neighbours)
                
                for neighbour in neighbours:
                    if peers_dict[i] not in neighbours_dict[neighbour] and len(neighbours_dict[neighbour]) < 6 and peers_dict[neighbour] not in neighbours_dict[i] and len(neighbours_dict[i]) < 6:
                        
                        # Get propagation delay between the two nodes
                        propagation_delay = random.randint(10, 501)*0.001
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
        # print(f"Number of peers: {len(peers_dict)}") 
        # for p in peers_dict.keys():
        #     print(peers_dict[p].node_id)
        # graph_utils.print_graph(peers_dict)
        return peers_dict

    def generate_unique_id(self):
        seed = random.random()
        random_number = random.randint(1000000, 9999999)
        timestamp = int(time.time() * 100)  
        unique_id = f"{timestamp:x}"
        return unique_id+str(random_number)

    def transaction_generate(self): 
        # Generate new transaction  
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
        print("---------------------------------------Simulations Started----------------------------------------------")
        
        curr_time = time.time()
        start_time = curr_time
        prev_transaction_time = curr_time
        scale = 1/self.exp_dist_mean
        waiting_time = np.random.exponential(scale)
        simulation_started = False
        while(curr_time <= start_time+simulation_time):
            # Generate transaction arter interarival of waiting time 
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
            if not self.event_queue.is_empty() and self.event_queue.peek().timestamp <= time.time(): 
                # Pop the top event and execute
                event = self.event_queue.pop() 
                event.execute_event()
            curr_time = time.time() 
        print("Similation is stopped!")
        print("------------------------------------------------------------------------------------------------------")
        total_interarrival_time = 0
        longest_chain = []
        longest_honest_chain = []
        node_mapping, miner_mapping = self.get_block_mapping(self.peers_dict)
        self.save_miner_mappings(miner_mapping)
        for i in self.peers_dict.keys():
            # self.print_longest_chain(self.peers_dict[i])
            total_interarrival_time += self.peers_dict[i].avg_interarrival_time
            self.save_chain_tree(self.peers_dict[i], node_mapping)
            curr_longest_chain = self.get_longest_chain(self.peers_dict[i])
            if len(curr_longest_chain) > len(longest_chain):
                longest_chain = curr_longest_chain
                if(self.peers_dict[i].node_id != self.c1_id and self.peers_dict[i].node_id != self.c2_id):
                    longest_honest_chain = curr_longest_chain
            # print(f"Interarrival time:{self.peers_dict[i].avg_interarrival_time}")
        
        # Total number of block in the blockhonest blockchain
        lvc_length = len(longest_honest_chain)
        # This stored the number of blocks generated by adverasies in the honest chain
        adv1_gen_block_count = 0
        adv2_gen_block_count = 0
        # Check if the block generated by both the advesaries is present in honest chain or not and if present count the occurence of such blocks
        for block in longest_honest_chain:
            if block.created_by == self.c1_id:
                adv1_gen_block_count += 1
            elif block.created_by == self.c2_id:
                adv2_gen_block_count += 1
        total_adv1_gen_block_count = 0
        total_adv2_gen_block_count = 0
        total_block_count = 0
        with open('experiment-desc.txt', 'w') as file:
            file.write("Similation details\n")
            file.write(f'Number of nodes {self.number_of_peers}\nFraction of low cpu nodes {self.fract_of_low_cpu}\nFraction of slow nodes {self.fract_of_slow}\nExponential Dist. Mean (txn) {self.exp_dist_mean}\n')
            for i in self.peers_dict.keys():
                file.write('-------------------------------------------------------------------------------------------------\n')
                # Get count of total blocks generated by adverasy 1
                if self.peers_dict[i].node_id == self.c1_id:
                    total_adv1_gen_block_count = self.peers_dict[i].block_mined_count
                # Get count of total blocks generated by adverasy 2
                elif self.peers_dict[i].node_id == self.c2_id:
                    total_adv2_gen_block_count = self.peers_dict[i].block_mined_count
                # Total blocks generated by all the nodes
                total_block_count += self.peers_dict[i].block_mined_count

                # To check the fraction of blocks present in longe chain by respective nodes
                total_blocks_generated = self.peers_dict[i].generated_blocks
                longest_chain_ids = set()
                for b in longest_chain:
                    longest_chain_ids.add(b.created_by)
                block_included_in_chain = len(total_blocks_generated & longest_chain_ids)
                fract_of_block_in_chain = block_included_in_chain/len(longest_chain_ids)
                file.write(f'Node {i}\nHashing power: {self.peers_dict[i]}\nTotal blocks generated:{self.peers_dict[i].block_mined_count}\n')
                file.write(f"Fraction of blocks in longest chain by node {i} is :{fract_of_block_in_chain}\n")
            mpu_adv_1 = 0
            mpu_adv_2 = 0
            if(total_adv1_gen_block_count > 0):
                mpu_adv_1 = adv1_gen_block_count/total_adv1_gen_block_count
            if(total_adv2_gen_block_count > 0):
                mpu_adv_2 = adv2_gen_block_count/total_adv2_gen_block_count
            mpu_overall = 0
            if(total_block_count > 0):
                mpu_overall = lvc_length/total_block_count

            file.write('\n-----------------------------------------------------------------------------------------------\n')
            file.write(f'MPU(ADV1) {mpu_adv_1}\n')
            file.write(f'MPU(ADV2) {mpu_adv_2}\n')
            file.write(f'MPU(OVERALL) {mpu_overall}\n')

            file.write('-------------------------------------------------------------------------------------------------\n')
            file.write(f'blocks generated by adv1 in lvc: {adv1_gen_block_count}\n')
            file.write(f'Total number of blocks generated by adv1: {total_adv1_gen_block_count}\n')
            
            file.write(f'blocks generated by adv2 in lvc: {adv2_gen_block_count}\n')
            file.write(f'Total number of blocks generated by adv2: {total_adv2_gen_block_count}\n')
            

            file.write(f'lvc length: {lvc_length}\n')
            file.write(f'Total blocks generated at all: {total_block_count}\n')
    # Utility function to get the logest chain
    def get_longest_chain(self, node):
        longest_chain = []
        curr_block_id = node.prev_block_id
        while curr_block_id != -1:
            longest_chain.append(node.blocks[curr_block_id]) 
            curr_block_id = node.blocks[curr_block_id].prev_block_id
        return longest_chain

    # This function maps block id to some interpretable value 
    def get_block_mapping(self, peers_dict):
        count = 0
        node_mapping = {} # Dictionary to map a block to interpretable value
        miner_mapping = {} # Dictionary to map each block to its miner
        node_mapping[-1] = -1
        miner_mapping[-1] = 0
        for peer in peers_dict.keys():
            for i in peers_dict[peer].blocks.keys(): 
                if i not in node_mapping.keys():
                    node_mapping[i] = count 
                    if peers_dict[peer].blocks[i].created_by == self.c1_id:
                       miner_mapping[count] = 1
                    elif peers_dict[peer].blocks[i].created_by == self.c2_id:
                        miner_mapping[count] = 2
                    else:
                        miner_mapping[count] = 0
                    count += 1
        return node_mapping, miner_mapping

    def save_chain_tree(self, node, node_mapping):
        with open('./blockchain_tree_csv/blockchain_tree_'+node.node_id+'.csv', 'a') as file:
            for i in node.blocks.keys(): 
                file.write(f'{node_mapping[i]},{node_mapping[node.blocks[i].prev_block_id]}\n')

    # Function to save the block and miner mapping
    def save_miner_mappings(self, miner_mapping):
        with open('miner_mappings.csv', 'a') as file:
            for i in miner_mapping.keys():
                file.write(f'{i},{miner_mapping[i]}\n')
