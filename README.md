
A project by **Vignesh.M** and **Vijay.R.S**. This repository contains the implementation of a public blockchain protocol designed from the ground up with native post-quantum cryptographic primitives to ensure secure, end-to-end encrypted messaging.

## 📜 Table of Contents

- [The Problem](https://www.google.com/search?q=%23-the-problem)
- [Motivation](https://www.google.com/search?q=%23-motivation)
- [Key Features](https://www.google.com/search?q=%23-key-features)
- [Technical Architecture](https://www.google.com/search?q=%23%EF%B8%8F-technical-architecture)
  - [Core Cryptography](https://www.google.com/search?q=%23core-cryptography)
  - [Consensus: Delegated Proof of Luck (DPoL)](https://www.google.com/search?q=%23consensus-delegated-proof-of-luck-dpol)
- [System Architecture Diagram](https://www.google.com/search?q=%23-system-architecture-diagram)
- [Evaluation Plan](https://www.google.com/search?q=%23-evaluation-plan)
  - [Performance Metrics](https://www.google.com/search?q=%23performance-metrics)
  - [Security Analysis](https://www.google.com/search?q=%23security-analysis)
- [Getting Started](https://www.google.com/search?q=%23-getting-started)
  - [Running the Nodes](https://www.google.com/search?q=%23running-the-nodes)
  - [Sending a Transaction](https://www.google.com/search?q=%23sending-a-transaction)
- [References](https://www.google.com/search?q=%23-references)

## 🎯 The Problem

Current blockchain-based communication platforms depend on cryptographic algorithms like RSA and ECDSA, which are vulnerable to attacks from quantum computers. The development of quantum computing creates a significant risk of message theft, forgeries, and the loss of communication privacy.

There is an urgent need for a real-world, scalable, and user-friendly public blockchain protocol that ensures secure, end-to-end encrypted messaging in the post-quantum era.

## 🚀 Motivation

> Blockchain's promise of permanent security is on a collision course with the reality of quantum computing.

The cryptographic signatures (ECDSA) that protect major cryptocurrencies are vulnerable to quantum attacks like Shor's algorithm. This puts a large portion of the digital economy at risk, including an estimated **25% of all Bitcoin** in circulation.

The threat is immediate due to **"Harvest Now, Decrypt Later"** strategies, where adversaries store today's encrypted data to decrypt it in the future with quantum computers. In response, governments are setting urgent deadlines for migrating to Post-Quantum Cryptography (PQC), yet enterprise adoption remains dangerously low.

## ✨ Key Features

- **Quantum-Resistant by Design:** Uses NIST-standardized PQC primitives (`CRYSTALS-Kyber` and `CRYSTALS-Dilithium`) for all cryptographic operations.
- **Secure End-to-End Messaging:** Every message is treated as a fully encrypted and authenticated blockchain transaction.
- **Novel Consensus Mechanism:** Implements **Delegated Proof of Luck (DPoL)**, a fair and energy-efficient alternative to PoW and PoS.
- **Built with Python:** Developed in Python for its extensive cryptographic libraries and rapid prototyping capabilities.

## 🛠️ Technical Architecture

### Core Cryptography

To achieve quantum resistance, the architecture exclusively uses NIST-standardized cryptographic primitives from the **CRYSTALS (Cryptographic Suite for Algebraic Lattices)** suite. These lattice-based algorithms were chosen for their strong security guarantees and relatively compact key sizes.

- **Key Encapsulation:** `CRYSTALS-Kyber` is used for secure message encryption and delivery.
- **Digital Signatures:** `CRYSTALS-Dilithium` provides authenticity, integrity, and non-repudiation for all transactions.

### Consensus: Delegated Proof of Luck (DPoL)

The network uses a novel **Delegated Proof of Luck (DPoL)** consensus mechanism. This hybrid model avoids the high energy consumption of Proof of Work (PoW) and mitigates the centralization risk of Proof of Stake (PoS).

1.  **Delegation:** Token holders elect a small set of trusted delegates to run nodes and produce blocks, inspired by Delegated Proof of Stake (DPoS).
2.  **Luck-Based Selection:** For each block, a producer is chosen from the delegate pool via a cryptographically secure lottery using a **Verifiable Random Function (VRF)**. This "Proof of Luck" ensures fairness and prevents resource-based centralization.

## 📊 System Architecture Diagram

_(A block diagram illustrating the protocol's architecture would go here.)_

```
[ Placeholder for path/to/your/block_diagram.png ]
```

## 📈 Evaluation Plan

The protocol will be rigorously evaluated for both performance and security.

#### Performance Metrics

A prototype will be deployed in a simulated network to measure key metrics:

- **Transaction Throughput (TPS):** The rate at which transactions are successfully committed to the blockchain under a sustained load.
- **Transactional Latency:** The end-to-end time from transaction submission to final confirmation.
- **Space Overhead:** The on-chain data footprint of transactions and blocks, quantifying the "PQC tax" and its impact on long-term scalability.

#### Security Analysis

A theoretical analysis will be conducted to validate security claims:

- **Cryptographic Primitive Review:** Verify that `CRYSTALS-Kyber` and `CRYSTALS-Dilithium` are implemented according to NIST specifications.
- **Protocol-Level Threat Modeling:** Analyze the protocol and the DPoL consensus mechanism against known threats like Shor's and Grover's algorithms, as well as network-level attacks.

## 💻 Getting Started

Here is a sample walkthrough for running the nodes and submitting transactions.

### Running the Nodes

First, start each node in a separate terminal window using its configuration file.

**Terminal 1: Start Node 1**

```bash
# Activate your Python virtual environment
source venv/bin/activate

# Start the first node
python node.py config_node1.json
```

You will see output indicating the server is running and may see initial connection errors as it looks for peers.

**Terminal 2: Start Node 2**

```bash
# Activate your Python virtual environment
source venv/bin/activate

# Start the second node
python node.py config_node2.json
```

Once Node 2 starts, it will connect to Node 1, and you will see a `Connected to peer` message.

### Sending a Transaction

Use the `send_tx.py` script to create and broadcast a new transaction to the network.

```bash
# Activate your Python virtual environment
source venv/bin/activate

# Install dependencies if you haven't already
pip install requests

# Send a transaction from Alice to Bob
python send_tx.py Alice Bob "This is a quantum-resistant message!"
```

**Successful Output:**

```json
{
  "message": "Transaction submitted",
  "tx_hash": "6235747aeaf391c0d7fc3990dd5592b3be01c07cef5b000f12ea54ad62fb81c9"
}
```

## 📚 References

This project builds upon the foundational research in Post-Quantum Cryptography and blockchain consensus. Key papers and resources include:

1.  _Reviewing Crypto-Agility and Quantum Resistance in the Light of Agile Practices_
2.  _Post-Quantum Delegated Proof of Luck for Blockchain Consensus Algorithm_
3.  _Beyond ECDSA and RSA: Lattice-based digital signatures on constrained devices_
4.  _Study on Implementation of Shor's Factorization Algorithm on Quantum Computer_
5.  Fernandez, R. M. et al. (2023). _Post-quantum blockchains: A review on platforms, challenges and opportunities_.
6.  Ducas, L. et al. _CRYSTALS-Dilithium: A Lattice-Based Digital Signature Scheme_.
