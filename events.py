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
    

    