import networkx as nx
import random

from block import Block
class Node:
    def __init__(self, node_id, coins ,hashing_power, is_slow, is_high_cpu):
        self.node_id = node_id
        self.coins = coins
        self.is_slow = is_slow
        self.is_high_cpu= is_high_cpu
        self.hashing_power = hashing_power

        #list of nodes neighbours
        self.neighbours = []
        #dictionary of all blocks node has seen
        self.blocks = {
            0: Block(block_id=0,created_by=self.node_id,mining_time=0,prev_block_id=-1,
                    length_of_chain=0)
        }

        self.transaction_queue = []

        self.event_queue = []
        self.Ttx = random.expovariate(1 / 60)  # Assuming Ttx is set to 60 for example
        self.time_of_arrival_list = []

    def __str__(self):
        return f"Node ID: {self.node_id} Hashing Power: {self.hashing_power} Is Slow: {self.is_slow} Is high CPU: {self.is_high_cpu} Coins: {self.coins} \n"

    def add_neighbours(self, neighbours):
        self.neighbours.append(neighbours)

    def is_connected(graph):
        return nx.is_connected(graph)

    





if __name__ == "__main__":
    # Create a sample graph using NetworkX
    
    # Create nodes
    nodes = [Node(node_id=i, coins=random.randint(1, 10), hashing_power=random.random(),
                  is_slow=random.choice([True, False]), is_high_cpu=random.choice([True, False])) for i in range(10)]

    # Connect nodes randomly (adjust as needed)
    for nodes in Node:
        num_peers = random.randint(3, 6)
        for i in range(num_peers):
            peer = random.choice(nodes)
            while peer == nodes or peer in nodes.peers:
                peer = random.choice(nodes)
            nodes.add_peer(peer)
            G.add_edge(nodes.node_id, peer.node_id)
