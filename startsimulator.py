import sys, random, time
import node
import simulator

n = len(sys.argv)
# If number of arguments is less then promt user to enter correct number of arguments.
if n != 6 :
    print("Invalid arguments!")
    print("Usage: simulatory.py <Number of peers> <Fraction of slow peers> <Fraction of slow cpu peers> <Mean of exponential distribution for interarrival time> <Simulation time>")
    exit()
else:
    if  not sys.argv[1].isdigit():
        print("Invalid argument!")
        print("Number of peers should be integer.")
        exit()
    if not sys.argv[2].replace('.','').isdigit() or float(sys.argv[1]) < 0 or float(sys.argv[2]) > 1:
        print(f'{sys.argv[2]} {isinstance(sys.argv[2], float)}')
        print("Invalid argument!")
        print("Fraction should be between 0 and 1")
        exit()
    if not sys.argv[3].replace('.','').isdigit() or float(sys.argv[3]) < 0 and float(sys.argv[2]) > 1:
        print(f'{sys.argv[3]} {isinstance(sys.argv[3], float)}')
        print("Invalid argument")
        print("Fraction should be between 0 and 1")
        exit()
    if not sys.argv[4].replace('.', '').isdigit():
        print("Mean of exponential distribution for Inter-arrival time should be numeric value")
        exit()
    if not sys.argv[5].isdigit() :
        print("Simulation time must be positive integer")
        exit()

def generate_unique_id():
    seed = random.random()
    random_number = random.randint(1000000, 9999999)
    timestamp = int(time.time() * 100)  
    unique_id = f"{timestamp:x}"
    return unique_id+str(random_number)




number_of_peers = int(sys.argv[1]) 
fract_of_slow = float(sys.argv[2])
fract_of_low_cpu = float(sys.argv[3])
mean_exp_dist = float(sys.argv[4])
simulation_time = int(sys.argv[5])

# Generate all nodes with respective peers

# all_nodes = generate_nodes(number_of_peers, fract_of_slow, fract_of_low_cpu, mean_exp_dist)

sim = simulator.simulator(number_of_peers, fract_of_slow, fract_of_low_cpu, mean_exp_dist)
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