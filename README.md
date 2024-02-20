# P2P Cryptocurrency Network Simulation

## Project Overview

This project simulates a Peer-to-Peer (P2P) Cryptocurrency Network, guided by Prof. Vinay Ribeiro for CS 765 at IIT Bombay.

## Requirements

- Python 3
- Pip Packages:
  - numpy
  - matplotlib
  - networkx

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
2. Z0: Fraction of slow nodes.
3. Z1: Fraction of low CPU nodes.
4. Ttx: Mean of exponential distribution for interarrival time.
5. time: Simulation time.

## Simulation Execution

To start the simulation, run the following command in the project folder:


$ python startsimulator.py [n] [Z0] [Z1] [Ttx] [time]
for e.g 
```bash
$python startsimulator.py 10 0.2 0.2 0.3 60
```

At the end of the simulation, for each peer, a Tree file at the node is created in the project folder
