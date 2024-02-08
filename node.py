import networkx as nx 
import numpy as np
import random, time, threading
import numpy.random as nprandom
from block import Block
class Node:

    def __init__(self, node_id, coins ,hashing_power, is_slow, is_slow_cpu, exp_dist_mean):
        self.node_id = node_id
        self.coins = coins
        self.is_slow = is_slow
        self.is_slow_cpu= is_slow_cpu
        self.hashing_power = hashing_power
        self.exp_dist_mean = exp_dist_mean 
        self.running = True
        #list of nodes neighbours
        self.neighbours = []

        #dictionary of all blocks node has seen
        self.blocks = {
            0: Block(block_id=0,created_by=self.node_id,mining_time=0,prev_block_id = -1, 
                    length_of_chain=0)
        }

        self.transaction_queue = []

        self.event_queue = []
        self.Ttx = random.expovariate(1 / 60)  # Thik kar Assuming Ttx is set to 60 for example
        self.time_of_arrival_list = []  

    def __str__(self):
        return f"Node ID: {self.node_id}\nHashing Power: {self.hashing_power}\nIs Slow: {self.is_slow}\nIs slow CPU: {self.is_slow_cpu}\nCoins: {self.coins}\nNeighbours: {self.neighbours}\nAll Nodes: {self.all_nodes}\n"

    def transaction_generator(self):
        while self.running:
            scale = 1/self.exp_dist_mean
            waiting_time = np.random.exponential(scale)
            time.sleep(waiting_time)
            print("Transaction generated...")

    def miner(self):
    # Call node up method  to start the node
        print("miner is mining.")
    
    def master_routine(self):
        # Master method where all the routines will be executed
        transaction_generator_routine = threading.Thread(target=self.transaction_generator)
        miner_routine = threading.Thread(target=self.miner)

        transaction_generator_routine.start()
        miner_routine.start()

        transaction_generator_routine.join()
        miner_routine.join()
        print()
        # Inside up node
    
    def stop_running(self):
        print(f'Node {self.node_id} is stopped!!')
        self.running = False

    # Method to set the neighbours of current node
    def add_neighbours(self, neighbours):
        self.neighbours = neighbours 

    # Method to save all node_ids in the blockchain network into the current node
    def add_allNodes(self, all_nodes):
        self.all_nodes = all_nodes
    

    # Method to get message latency
    def get_latency(self, message_type, is_sender_slow, is_receiver_slow, propagation_delay):
        latency = 0
        message_size = 0
        if(message_type == 'transaction'):
            message_size += 8*10**3
        elif(message_type == 'block'):
            message_size += 8*10**3
        
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
    # Mining routine

    
    # Routine to boadcast 
    
    # def is_connected(graph):
    #     return nx.is_connected(graph)

    





