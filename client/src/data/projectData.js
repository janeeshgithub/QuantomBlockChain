export const projectData = {
  heroSubtitle: "A Project Showcase",
  heroTitle: "A Quantum-Resistant Communication System Using Blockchain",
  heroDescription:
    "Securing the next generation of digital communication against quantum threats with a decentralized, end-to-end encrypted System.",
  abstract:
    "The project proposes a quantum-resistant communication System built on a public blockchain. It aims to provide secure, end-to-end encrypted messaging for the quantum era. The core concept treats every message as a fully authenticated and encrypted transaction. The System uses NIST-standardized Post-Quantum Cryptography (PQC) to protect against both classical and quantum threats, ensuring privacy and integrity on a scalable platform.",
  technicalApproach: [
    {
      title: "Language & Prototyping",
      description:
        "The prototype is developed in Python for its extensive cryptographic libraries and rapid development capabilities.",
    },
    {
      title: "Core Cryptography",
      description:
        "Built on the CRYSTALS (Cryptographic Suite for Algebraic Lattices) suite.",
    },
    {
      title: "Encryption",
      description:
        "Uses CRYSTALS-Kyber for secure key encapsulation and message delivery.",
    },
    {
      title: "Authentication",
      description:
        "Uses CRYSTALS-Dilithium for digital signatures to ensure authenticity, integrity, and non-repudiation.",
    },
    {
      title: "Consensus: Delegated Proof of Luck (DPoL)",
      description:
        "A novel hybrid model that avoids the high energy use of PoW and mitigates centralization risks of PoS. Block producers are chosen via a verifiable, luck-based lottery.",
    },
  ],
  systemFlow: [
    {
      title: "Sender",
      description: "Encrypts and signs a message, creating a transaction.",
    },
    {
      title: "Broadcast",
      description: "The transaction is sent to the network's transaction pool.",
    },
    {
      title: "Validation",
      description: "A Validator Node processes the transaction.",
    },
    {
      title: "Consensus",
      description: "The transaction is recorded on the distributed ledger.",
    },
    {
      title: "Receiver",
      description:
        "Retrieves the transaction and securely decrypts the message.",
    },
  ],
  impact: [
    {
      title: "Economic",
      description:
        "Protects cryptocurrencies and digital assets from quantum attacks. An estimated 25% of all Bitcoin is currently vulnerable.",
    },
    {
      title: "Social",
      description:
        'Preserves long-term privacy by defeating "Harvest Now, Decrypt Later" strategies.',
    },
    {
      title: "Strategic",
      description:
        "Provides a clear path for critical infrastructure to meet government mandates for migrating to PQC.",
    },
  ],
  challenges: [
    '<strong>Performance Cost ("PQC Tax"):</strong> Post-quantum algorithms come with performance overhead.',
    "<strong>Size Overhead:</strong> PQC signatures are significantly larger (~35x), increasing the on-chain data footprint.",
    "<strong>Throughput Reduction:</strong> Larger transaction sizes may reduce transactions per block by over 90%.",
    "<strong>Security Validation Risk:</strong> Validation must rely on theoretical analysis until large-scale quantum computers exist.",
  ],
  futureScope: [
    {
      title: "Scalability & Long-Term Vision",
      description:
        "The ultimate goal is to develop a fully functional, public quantum-resistant blockchain, with the DPoL consensus mechanism designed for high speed and scalability.",
    },
    {
      title: "Immediate Next Steps",
      list: [
        "<strong>Performance Evaluation:</strong> Deploy the prototype in a simulated network to measure TPS, latency, and data overhead.",
        "<strong>Security Analysis:</strong> Conduct a rigorous theoretical review and System-level threat modeling.",
      ],
    },
    {
      title: "Adoption Strategy",
      description:
        "Target enterprises and critical infrastructure sectors that are mandated to upgrade their security to PQC standards.",
    },
  ],
};
