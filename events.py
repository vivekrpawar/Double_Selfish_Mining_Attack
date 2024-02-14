# 4 events TxnGenerated, TransactionReceive, BlockGenerate, BlockReceive
from block import Block
from transaction import trasactions
from simulator import simulator
from node import Node
import random
import numpy as np

class Event:
    def __init__(self, event_created_by ,node, node_id, timestamp):

        #node which is creating event
        self.event_created_by=event_created_by

        #node on which this event will happen
        self.node=node

        #node id on which this event will happen
        self.node_id = node_id 
        
        # Time at whcih this event will run 
        self.timestamp=timestamp

    def __lt__(self, other):
        return self.timestamp < other.timestamp

#1st event 
class TxnGenerated(Event):
    def __init__(self, event_created_by, node, node_id, timestamp): 
        super().__init__(event_created_by, node, node_id, timestamp)
        
    def __str__(self):
        return f"{self.node_id} has generated a Transaction \n"
        
    def execute_event(self):
        self.node.generate_transaction()

class TxnReceived(Event):
    def __init__(self, event_created_by, node, node_id, timestamp, transaction):
        super().__init__(event_created_by, node, node_id, timestamp=timestamp)
        self.transaction = transaction

    def __str__(self):
        return f"{self.node_id} has received a Transaction \n"
    
    def execute_event(self):
        self.node.receive_transaction(self.transaction, self.event_created_by) 


class BlockGenerate(Event):
    def __init__(self, event_created_by, node, node_id, timestamp): 
        super().__init__(event_created_by, node, node_id, timestamp)

    def __str__(self):
        return f"{self.node_id} is generating a Block \n"
    
    def __repr__(self):
        return f"B Gen: on={self.node_id}"

    def execute_event(self):
        self.node.generate_block()

class BlockMined(Event):
    def __init__(self, event_created_by, node, node_id, timestamp):
        super().__init__(event_created_by, node, node_id, timestamp)

    def __str__(self):
        return f"{self.node_id} has generated a Block \n"
    
    def __repr__(self):
        return f"B Rcv: on={self.node_id} | {repr(self.block)}"
    
    def execute_event(self):
        self.node.mined_block(self.block) 
        
class BlockReceive(Event):
    def __init__(self, event_created_by, node, node_id, timestamp, block): 
        super().__init__(event_created_by, node, node_id, timestamp)
        # The block we've received
        self.block = block

    def __str__(self):
        return f"{self.node_id} has received a Block \n"
    
    def __repr__(self):
        return f"B Rcv: on={self.node_id} | {repr(self.block)}"

    def execute_event(self):
        self.node.generate_block(self.block)         






