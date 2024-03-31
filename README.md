# P2P Cryptocurrency Network Simulation

## Project Overview

This project simulates a Peer-to-Peer (P2P) Cryptocurrency Network, guided by Prof. Vinay Ribeiro for CS 765 at IIT Bombay.

## Requirements

- Python 3
- Pip Packages:
  - numpy
  - matplotlib
  - networkx

To install the required dependency run the following command:

```bash
$pip install -r requirements.txt
```
## Classes

### 1. Simulator
- Simulates each peer in the network.

### 2. Node
- Represents a peer in the P2P network.

### 3. Transaction
- Represents a transaction in the cryptocurrency network.

### 4. Block
- Represents a block in the blockchain.

### 5. Event
   - TxnGenerated
   - TxnReceived
   - BlockGenerate
   - BlockMined
   - BlockReceive

## Input Parameters

1. n: Number of peers in the network. 
2. Z1: Fraction of low CPU nodes.
3. Ttx: Mean of exponential distribution for transaction interarrival time.
4. Tk: Mean of exponential distribution for block generation time.
5. time: Simulation time.
6. C1: Hashing power of adversary 1
7. C2: Hashing power of adversary 2
(Here Z0 is set to 0.5 are mentined in the problem statement)
## Simulation Execution

To start the simulation, run the following command in the project folder:


$ python startsimulator.py [n] [Z1] [Ttx] [Tk] [time] [C1] [C2]
for e.g 
```bash
$python startsimulator.py 100 0.3 0.02 1 600 0.3 0.2
```

At the end of the simulation, for each peer, a Tree file at the node is created in the project folder and description about the simulation will be in experiment-desc.txt file
