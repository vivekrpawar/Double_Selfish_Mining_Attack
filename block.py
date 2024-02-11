class Block:
    def __init__(self, block_id, created_by, mining_time, prev_block_id, length_of_chain):
        self.block_id = block_id
        self.created_by = created_by
        self.mining_time = mining_time
        self.prev_block_id = prev_block_id
        self.transactions = []
        self.length_of_chain = length_of_chain  # Initialized to 1, as this is a new block

    def __str__(self):
        return f"Block ID: {self.block_id} is Created By: {self.created_by} in Mining time: {self.mining_time} which had previous block: {self.prev_block_id} \n" 

    def __len__(self):
        return self.length_of_chain