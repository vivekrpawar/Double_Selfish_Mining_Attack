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

    def execute_event(self):
        self.node.receive_transaction(self.transaction, self.event_created_by) 


class BlockGenerate(Event):
    def __init__(self, event_created_by, node, node_id, created_at, run_at):
        super().__init__(event_created_by, node, node_id, event_type='BlockGenerate', timestamp=run_at)

    def __repr__(self):
        return f"B Gen: on={self.node_id}"

    def run(self):
        me = self.node

        for x in me.receivedStamps:
            if x > self.timestamp:
                return

        # Traverse the longest chain and find all transactions that've been spent
        longest_chain = me.longest_chain()
        longest_block = longest_chain[0]

        spent = set()

        for block in longest_chain:
            spent |= set(block.transactions.values())

        # Unspent = Seen - Spent
        unspent_txns = set(me.transaction_queue) - spent
        unspent_txns = {t.transaction_id: t for t in unspent_txns}

        # Only create a block if I have transactions to send
        if not unspent_txns:
            return

        # Generate a new block
        new_block = Block(
            block_id=me.block_id,
            created_by=me.node_id,
            mining_time=self.timestamp,
            prev_block_id=longest_block.block_id,
            length_of_chain=len(longest_block) + 1
        )
        new_block.transactions.update(unspent_txns)

        me.block_id += 1

        # Add the block to my chain
        me.blocks[new_block.block_id] = new_block
        
        me.coins += 50

        # Generate BlockReceive events for all my peers
        for peer_id in me.neighbours:
            # Except who created the thing!
            if peer_id != me.node_id:
                delay = random.uniform(0, 10)  # Adjust the range of delay as needed
                event = BlockReceive(
                    event_created_by=me.node_id,
                    node=me,
                    node_id=peer_id,
                    block=new_block,
                    created_at=self.timestamp,
                    run_at=self.timestamp + delay
                )
                me.event_queue.append(event)


class BlockReceive(Event):
    def __init__(self, event_created_by, node, node_id, block, created_at, run_at):
        super().__init__(event_created_by, node, node_id, event_type='BlockReceive', timestamp=run_at)

        # The block we've received
        self.block = block

    def __repr__(self):
        return f"B Rcv: on={self.node_id} | {repr(self.block)}"

    def run(self):
        # The node that this event is running on
        me = self.node

        # Check if this node has already seen this block before
        if self.block.block_id in me.blocks:
            return

        # Find previous block to the one that we've just received
        prev_block = me.blocks.get(self.block.prev_block_id)
        if prev_block is None:
            return

        # Add transactions in this block to my list of seen ones
        me.transaction_queue.extend(self.block.transactions)

        # Make a copy of the block to increase the length
        new_block = Block(
            block_id=self.block.block_id,
            created_by=self.block.created_by,
            mining_time=self.block.mining_time,
            prev_block_id=prev_block.block_id,
            length_of_chain=len(self.block) + 1
        )

        # Add the block to my chain
        me.blocks[new_block.block_id] = new_block
        me.receivedStamps.append(new_block.timestamp)

        # Generate BlockReceive events for all my peers
        for peer in me.neighbours:
            # Except for who created it
            if peer.node_id != self.block.created_by:
                delay = random.uniform(0, 10)  # Adjust the range of delay as needed
                event = BlockReceive(
                    event_created_by=me.node_id,
                    node=me,
                    node_id=peer_id,
                    block=new_block,
                    created_at=self.timestamp,
                    run_at=self.timestamp + delay
                )
                me.event_queue.append(event)

        # Create a new block generation event for me
        event = BlockGenerate(
            event_created_by=me.node_id,
            node=me,
            node_id=me.node_id,
            created_at=self.timestamp,
            run_at=self.timestamp + me.block_delay()  # You might need to define this method in your Node class
        )
        me.event_queue.append(event)          






