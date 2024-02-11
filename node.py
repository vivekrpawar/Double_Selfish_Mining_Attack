import networkx as nx 
import transaction
import numpy as np
import random, time, threading
import numpy.random as nprandom
from block import Block
import events

class Node:
    def __init__(self, node_id, coins ,hashing_power, is_slow, is_slow_cpu, exp_dist_mean, event_queue):
        # Data members
        self.node_id = node_id
        self.coins = coins
        self.is_slow = is_slow
        self.is_slow_cpu= is_slow_cpu
        self.hashing_power = hashing_power
        self.exp_dist_mean = exp_dist_mean 
        self.running = True
        self.neighbours = []    #list of nodes neighbours
        self.transaction_queue = []
        self.blocks = {     #dictionary of all blocks node has seen
            0: Block(block_id=0,created_by=self.node_id,mining_time=0,prev_block_id = -1, 
                    length_of_chain=0)
        }
        self.event_queue = event_queue
        self.Ttx = random.expovariate(1 / 60)  # Thik kar Assuming Ttx is set to 60 for example
        #self.time_of_arrival_list = []  
        self.receivedStamps=[]
        self.prev_block_id = 0 

    def __str__(self):
        return f"Node ID: {self.node_id}\nHashing Power: {self.hashing_power}\nIs Slow: {self.is_slow}\nIs slow CPU: {self.is_slow_cpu}\nCoins: {self.coins}\nNeighbours: {self.neighbours}\nAll Nodes: {self.all_nodes}\n"

    
    def generate_transaction(self):

        # Sample a transaction amount and a receiver uniformly at random
        transaction_amount = random.uniform(1, self.coins)  # Adjust the range as needed
        nodelistwithoutme = list(set(self.all_nodes.keys()) - set([self.node_id]))
        receiver_id = random.choice(nodelistwithoutme)  # Adjust the range as needed

        # adding and removing coins from ourselves and the receiver
        self.coins = self.coins - transaction_amount
        receiver_id.coins = receiver_id.coins + transaction_amount

        # Create the transaction and add it to the transaction queue
        transaction = transaction.Transaction(
            transaction_id = str(int(time.time()))+str(self.node_id),
            coins=transaction_amount,
            sender_id=self.node_id,
            receiver_id=receiver_id.node_id,
            timestamp = int(time.time())    
        )

        self.transaction_queue.append(transaction)

        # Schedule a TxnReceived event at each peer/neighbour, at the current time + network delay
        for neighbour in self.neighbours:
            delay = self.get_latency("transaction", neighbour.is_slow_cpu, neighbour.node_id)
            scheduled_timestamp = time.time() + delay  # Adjust the range as needed
            event = events.TxnReceived(
                event_created_by=self.node_id,
                node=neighbour,
                node_id=neighbour.node_id,
                timestamp=scheduled_timestamp
            )
            self.event_queue.append(event)

    def receive_transaction(self, transaction, event_created_by):
        # Check if the transaction has already been received
        if transaction.transaction_id not in [txn.transaction_id for txn in self.transaction_queue]:
            # Add the transaction to the received transactions
            self.transaction_queue.append(transaction)

            # Schedule a TxnReceived event at each neighbour with a randomly sampled delay
            for neighbour in self.neighbours:
                if (neighbour.node_id != event_created_by):
                    delay = self.get_latency("transaction", neighbour.is_slow_cpu, neighbour.node_id)
                    scheduled_timestamp = time.time() + delay  # Adjust the range as needed
                    event = events.TxnReceived(
                        event_created_by=self.node_id,
                        node=neighbour,
                        node_id=neighbour.node_id,
                        timestamp=scheduled_timestamp
                    )
                    self.event_queue.append(event)
    
    def generate_block(self):
        self.transaction_queue.sort()

        transctions_in_block = []
        spent_transaction = self.get_spent_transactions() 
        unspent_transactions = list(set(self.transaction_queue) - spent_transaction)
        for i in range(min(1000, len(unspent_transactions))):
            transctions_in_block.append(unspent_transactions[i])
        prev_longest_chain = self.get_longest_chain()
        mining_time = self.get_mining_time(prev_longest_chain)
        time.sleep(mining_time)
        curr_longest_chain = self.get_longest_chain()
        if(curr_longest_chain != prev_longest_chain):
            return
        # Create the coinbase transaction and add it to the transaction queue
        transaction = transaction.Transaction(
            transaction_id=str(int(time.time()))+str(self.node_id),
            coins=50,
            sender_id=0,
            receiver_id=self.node_id,
            timestamp = int(time.time())
        )
        transctions_in_block.add(0, transaction)
        block = block.Block(
            block_id = str(int(time.time()))+str(self.node_id),
            created_by = self.node_id,
            mining_time = mining_time,
            prev_block_id = self.prev_block_id,
            transactions = transctions_in_block,
            length_of_chain = prev_longest_chain+1,
            timestamp = int(time.time())
        )
        block[self.prev_block_id] = block
        self.prev_block_id = block.block_id

        for neighbour in self.neighbours:
            delay = self.get_latency("block", neighbour.is_slow_cpu, neighbour.node_id)
            scheduled_timestamp = time.time() + delay  # Adjust the range as needed
            event = events.BlockReceived(
                event_created_by=self.node_id,
                node=neighbour,
                node_id=neighbour.node_id,
                timestamp=scheduled_timestamp
            )
            self.event_queue.append(event)
        
    def received_block(self):
        

    def get_spent_transactions(self):
        curr_node = self.prev_node_id
        spent_transaction = {}
        while curr_node != 0:
            spent_transaction.update(self.blocks[curr_node])
            curr_node = self.block[curr_node].get_prev_block
        return spent_transaction

    def get_mining_time(self, prev_longest_chain):
        avg_interarrival_time = (self.last_block_time_stamp - self.fist_block_time_stamp)/prev_longest_chain
        hashing_power = 10 if (self.is_slow_cpu) else  1
        mining_time = nprandom.exponential(avg_interarrival_time/hashing_power)
        return mining_time
    
    def get_longest_chain(self):
        chain = []

        # Start with the genesis block
        longest_block = self.blocks[0]

        # Find the block ending with the longest chain
        for block in self.blocks.values():
            # Use block length and creation time to break ties in case of equal length
            if len(block) > len(longest_block) or (
            len(block) == len(longest_block) and block.timestamp < longest_block.timestamp):
                longest_block = block

        # Now find all the blocks in this chain
        current_block = longest_block

        # Do-While Loop!
        while True:
            chain.append(current_block)

            # Chain ends at Genesis block which has id 0
            if current_block.block_id == 0:
                break

            # Move backwards
            current_block = self.blocks[current_block.prev_block_id]

        return chain


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

    # Method to set the neighbours of current node
    def add_neighbours(self, neighbours):
        self.neighbours = neighbours 

    # Method to save all node_ids in the blockchain network into the current node
    def add_allNodes(self, all_nodes):
        self.all_nodes = all_nodes
    
    # Method to get message latency
    def get_latency(self, message_type, is_receiver_slow, neighbour_id):
        latency = 0
        message_size = 0
        if(message_type == 'transaction'):
            message_size += 8*10**3
        elif(message_type == 'block'):
            message_size += 8*10**6
        
        link_speed = 0
        if not self.is_slow and not is_receiver_slow:
            link_speed = 100*10**8
        else:
            link_speed = 5*10**8
        
        # Transmission delay
        latency += message_size/link_speed

        # Queing delay
        latency += nprandom.exponential(96*1e3/link_speed)

        # Propagation delay
        latency += self.all_node[neighbour_id]

        return latency
    # Mining routine

    
    # Routine to boadcast 
    

    





