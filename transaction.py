#class transactions

class Transaction:
    def __init__(self, transaction_id, coins, sender_id, receiver_id, timestamp):
        self.transaction_id = transaction_id
        self.coins = coins
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.timestamp = timestamp

    def __str__(self):
        #Transaction format : IDx pays IDy C coins
        
        return f"{self.sender_id} pays {self.receiver_id}: {self.coins} Coins"
    
    def __lt__(self, other):
        return self.timestamp < other.timestamp

    
