
def is_connected(peers_dict):
    # utility functin to check whether the given graph is connected of not
    num_of_peers = len(peers_dict)
    queue = []
    vis = {}
    root = list(peers_dict.keys())[0]
    queue.append(root)
    vis[root] = True
    count = 1
    while len(queue) > 0:
        curr = queue[0]
        queue.pop(0) 
        for i in peers_dict[curr]:
            if i.node_id not in vis.keys():
                queue.append(i.node_id)
                count += 1
                vis[i.node_id] = True
    return count == num_of_peers


def print_graph(peers_dir):
    # utility function to print the graph
    print("The graph will get displyed here.")