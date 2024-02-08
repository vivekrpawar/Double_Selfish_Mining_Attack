# 4 events TxnGenerated, TransactionReceive, BlockGenerate, BlockReceive
from block import Block
from transaction import trasactions
import random

class Event:
    def __init__(self, event_created_by , node_id, event_type, timestamp):

        #node which is creating event
        self.event_created_by=event_created_by

        #node on which this event will happen
        self.node_id = node_id

        #Type of event to be executed
        self.event_type=event_type
        
        # Time at whcih this event will run 
        self.timestamp=timestamp

    def __sort__(self, other):
        return self.timestamp<other.timestamp
    

    


#1st event 
#revisit the logic
class TxnGenerated(Event):
    def __init__(self, event_created_by, node_id, event_type, timestamp):
        super().__init__(event_created_by, node_id, "TxnGenerated", timestamp)        

    def __str__(self):
        return f"{self.node_id} has geneated a Transaction \n"


    def generate_transaction(self):
        # Sample a transaction amount and a receiver uniformly at random
        transaction_amount = random.uniform(1, self.coins)  # Adjust the range as needed
        nodelistwithoutme = list(set(self.all_nodes.keys()) - set([self.node_id]))
        receiver_id = random.choice(nodelistwithoutme)#thik karo

        #receiver_id = random.choice(self.neighbours)#thik karo

        ##adding and removing coins from ourself and reciever
        self.coins = self.coins - transaction_amount
        receiver_id.coins = receiver_id.coins + transaction_amount

        # Sample a network delay using connection link speeds, transaction size, and queuing delay
        network_delay = random.uniform(0, 10)  # Adjust the range as needed#thik karo
        
        # Create the transaction and add it to the transaction queue
        transaction = trasactions(transaction_id=len(self.transaction_queue) + 1,
                                  coins=transaction_amount,
                                  sender_id=self.node_id,
                                  receiver_id=receiver_id)
        
        self.transaction_queue.append(transaction)

        event = Event(event_created_by=self.node_id, node_id=neighbour, event_type="TxnGenerated",timestamp=scheduled_timestamp)
        self.event_queue.append(event)

        # Schedule a txnRcv event at each peer/neighbour, at the current time + network delay
        for neighbour in self.neighbours:
            scheduled_timestamp = self.Ttx + network_delay
            event = Event(event_created_by=self.node_id, node_id=neighbour, event_type="TxnReceived",timestamp=scheduled_timestamp)
            neighbour.event_queue.append(event)#
        
        event = Event(event_created_by=self.node_id, node_id=neighbour, event_type="TxnReceived",timestamp=scheduled_timestamp)


#2nd event
class TxnReceived(Event):
    def __init__(self, event_created_by, node_id, event_type, timestamp):
        super().__init__(event_created_by, node_id,"TxnReceived" ,timestamp)
    
    def txn_received(self, transaction):
        # Check if the transaction has already been received
        if transaction.transaction_id not in [txn.transaction_id for txn in self.transaction_queue]:
            # Add the transaction to the received transactions
            self.transaction_queue.append(transaction)

            # Schedule a txnRcv event at each neighbour with a randomly sampled delay
            for neighbour in self.neighbours:
                delay = random.uniform(0, 10)  # Adjust the range of delay as needed
                scheduled_timestamp = self.Ttx + delay#thik karo
                event = Event(event_created_by=self.node_id, node_id=neighbour, event_type="TxnReceived", timestamp=scheduled_timestamp)
                self.event_queue.append(event)

#BlockMined should look into this code

class BlockMined(Event):
    def __init__(self, event_created_by, node_id, event_type, timestamp):
        super().__init__(event_created_by, node_id, "BlockMined", timestamp)
        
    def block_mined(self, mining_time):
        # Check if this is still the longest chain
        if self.is_longest_chain():
            # Add the newly mined block to the longest chain of the blockchain
            new_block = self.create_block(mining_time)
            self.blocks[new_block.block_id] = new_block

            # At each peer, schedule a blockRcv event with a randomly sampled delay
            for neighbour in self.neighbours:
                delay = random.uniform(0, 10)  # Adjust the range of delay as needed
                scheduled_timestamp = self.Ttx + delay
                event = Event(event_created_by=self.node_id, node_id=neighbour, event_type='blockRcv', timestamp=scheduled_timestamp)
                self.event_queue.append(event)

            # Remove the transaction added to the block from the transaction queue
            # (This part depends on your specific implementation of the transaction queue)
            # Assuming you have a method remove_transaction_from_queue(transaction) in Node class
            if new_block.block_id in self.blocks:
                transactions_in_block = self.get_transactions_from_block(new_block)
                for transaction in transactions_in_block:
                    self.remove_transaction_from_queue(transaction)

            # Continue mining
            self.continue_mining()

    def continue_mining(self):
        # Sample random subsets (select transactions with max mining reward) from the transaction pool
        # to form new blocks until a valid block is formed.
        # Sample mining time from an exponential distribution with mean T/hk and where I is the average interarrival time.
        mining_reward = self.calculate_mining_reward()
        selected_transactions = self.select_transactions_with_max_reward(mining_reward)
        new_block = self.form_block(selected_transactions)

        # Sample mining time from an exponential distribution
        mining_time = np.random.exponential(scale=1.0)  # Adjust the scale parameter as needed

        # Schedule a block-mined event with the mining time
        scheduled_timestamp = self.Ttx + mining_time
        event = Event(event_created_by=self.node_id, node_id=self.node_id, event_type='BlockMined', timestamp=scheduled_timestamp)
        self.event_queue.append(event)

    def is_longest_chain(self):
        # Implement your logic to check if this is still the longest chain
        # (This part depends on how you determine the longest chain)
        return True

    def create_block(self, mining_time):
        # Implement your logic to create a new block
        # (This part depends on your specific implementation)
        return Block(block_id=len(self.blocks) + 1,
                     created_by=self.node_id,
                     mining_time=mining_time,
                     prev_block_id=max(self.blocks.keys(), default=0),
                     length_of_chain=self.blocks[max(self.blocks.keys(), default=0)].length_of_chain + 1)

    def calculate_mining_reward(self):
        # Implement your logic to calculate the mining reward
        # (This part depends on your specific implementation)
        return 1.0  # Placeholder value, adjust as needed

    def select_transactions_with_max_reward(self, mining_reward):
        # Implement your logic to select transactions with max mining reward
        # (This part depends on your specific implementation)
        return []

    def form_block(self, selected_transactions):
        # Implement your logic to form a new block from selected transactions
        # (This part depends on your specific implementation)
        return Block(block_id=len(self.blocks) + 1,
                     created_by=self.node_id,
                     mining_time=0,  # Placeholder value, adjust as needed
                     prev_block_id=max(self.blocks.keys(), default=0),
                     length_of_chain=self.blocks[max(self.blocks.keys(), default=0)].length_of_chain + 1)

    def get_transactions_from_block(self, block):
        # Implement your logic to get transactions from a block
        # (This part depends on your specific implementation)
        return []

    def remove_transaction_from_queue(self, transaction):
        # Implement your logic to remove a transaction from the transaction queue
        # (This part depends on your specific implementation)
        pass




#BlockRecieved
                






