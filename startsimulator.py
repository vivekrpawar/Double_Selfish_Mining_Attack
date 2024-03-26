import sys, random, time
import node
import simulator

n = len(sys.argv)
# If number of arguments is less then promt user to enter correct number of arguments. 
if n != 7 :
    print("Invalid arguments!")
    print("Usage: simulatory.py <Number of peers> <Fraction of low cpu peers> <Mean of exponential distribution for interarrival time> <Simulation time> <Hashing Power of adversary 1> <Hashing power of adversary 2>")
    exit()
else:
    if  not sys.argv[1].isdigit():
        print("Invalid argument!")
        print("Number of peers should be integer.")
        exit()
    if not sys.argv[2].replace('.','').isdigit() or (float(sys.argv[3]) < 0 and float(sys.argv[3])) > 1:
        print(f'{sys.argv[3]} {isinstance(sys.argv[3], float)}')
        print("Invalid argument")
        print("Fraction should be between 0 and 1")
        exit()
    if not sys.argv[3].replace('.', '').isdigit():
        print("Mean of exponential distribution for Inter-arrival time should be numeric value")
        exit()
    if not sys.argv[4].isdigit() :
        print("Simulation time must be positive integer")
        exit()
    if not sys.argv[5].replace('.','').isdigit() or (float(sys.argv[5]) < 0 and float(sys.argv[5])) > 1:
        print("Hashing power must be between 0 to 1")
        exit()
    if not sys.argv[6].replace('.','').isdigit() or (float(sys.argv[6]) < 0 and float(sys.argv[6])) > 1:
        print("Hashing power must be between 0 to 1")
        exit()

def generate_unique_id():
    seed = random.random()
    random_number = random.randint(1000000, 9999999)
    timestamp = int(time.time() * 100)  
    unique_id = f"{timestamp:x}"
    return unique_id+str(random_number)




number_of_peers = int(sys.argv[1]) 
fract_of_slow = 0.5
fract_of_low_cpu = float(sys.argv[2])
mean_exp_dist = float(sys.argv[3])
simulation_time = int(sys.argv[4])
c1 = float(sys.argv[5])
c2 = float(sys.argv[6])

# Generate all nodes with respective peers

# all_nodes = generate_nodes(number_of_peers, fract_of_slow, fract_of_low_cpu, mean_exp_dist)

sim = simulator.simulator(number_of_peers, fract_of_slow, fract_of_low_cpu, mean_exp_dist, c1, c2)
sim.run_simulator(simulation_time)
# time.sleep(simulation_time)
# sim.stop_simulator()

# threads = []
# all_peers = all_nodes.values()
# for peer in all_peers:
#     thread = threading.Thread(target=peer.master_routine)
#     thread.daemon = True
#     thread.start()
#     threads.append(thread)

# # Main thread continues executing without waiting for the background threads
# print("Main thread continues executing...")

# time.sleep(simulation_time)

# for peer in all_peers:
#     peer.stop_running()

# # Join the background threads to wait for them to finish before exiting the program
# for thread in threads:
#     thread.join()