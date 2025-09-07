import React from "react";

// Data that was previously in an external file
const projectData = {
  abstract:
    "Qubi is a next-generation blockchain system designed for the quantum era. It integrates a Quantum Resistant Communication System (QRCS) to ensure secure, scalable, and future-proof transactions against the looming threat of quantum attacks. By leveraging post-quantum cryptography (PQC) and a decentralized network, Qubi provides a robust platform for digital assets and communications, safeguarding data integrity and user privacy in a post-quantum world.",
  technicalApproach: [
    {
      title: "Post-Quantum Cryptography (PQC)",
      description:
        "Utilizing lattice-based cryptographic algorithms like CRYSTALS-Kyber for key exchange and CRYSTALS-Dilithium for digital signatures to protect against quantum computer attacks.",
    },
    {
      title: "Decentralized Network",
      description:
        "Building on a peer-to-peer network to ensure no single point of failure, enhancing censorship resistance and overall system resilience.",
    },
    {
      title: "Consensus Mechanism",
      description:
        "Implementing a hybrid Proof-of-Stake (PoS) and Proof-of-Work (PoW) consensus model to balance security, efficiency, and decentralization.",
    },
    {
      title: "Smart Contract Functionality",
      description:
        "Enabling the creation and execution of smart contracts on a quantum-resistant framework, opening up possibilities for secure decentralized applications (dApps).",
    },
    {
      title: "QRCS Integration",
      description:
        "The Quantum Resistant Communication System is the core of Qubi, ensuring that all data exchange, from transactions to messages, is encrypted with PQC standards.",
    },
     {
      title: "Scalability Solutions",
      description:
        "Incorporating layer-2 scaling solutions like sharding and state channels to improve transaction throughput and reduce network congestion.",
    },
  ],
  systemFlow: [
    {
      title: "1. User Initialization",
      description:
        "A new user generates a key pair using a PQC algorithm (e.g., CRYSTALS-Dilithium). The public key is used as their wallet address.",
    },
    {
      title: "2. Transaction Creation",
      description:
        "To send assets, a user creates a transaction, specifies the recipient's address and amount, and signs it with their private key.",
    },
    {
      title: "3. Secure Communication (QRCS)",
      description:
        "The signed transaction is broadcast to the network through the QRCS, which uses PQC for secure and authenticated channel establishment between nodes.",
    },
    {
      title: "4. Node Verification",
      description:
        "Network nodes receive the transaction, verify the digital signature using the sender's public key, and check for sufficient funds.",
    },
    {
      title: "5. Block Creation & Consensus",
      description:
        "Verified transactions are bundled into a block. Validators/Miners reach a consensus to add the new block to the blockchain.",
    },
    {
      title: "6. Ledger Update",
      description:
        "Once a block is added, the new state of the ledger is confirmed across the network, and the transaction is considered final.",
    },
  ],
};


// A simple component to handle delayed fade-in animations
const AnimatedItem = ({ delay = 0, children, className = '' }) => {
    return (
        <div 
            className={`animate-fade-in ${className}`} 
            style={{ animationDelay: `${delay}ms` }}
        >
            {children}
        </div>
    );
};


// Main App Component
export default function Home() {
  return (
    <main className="relative min-h-screen font-sans text-white bg-gray-900 overflow-x-hidden">
        {/* Shared Animated Background */}
        <div className="absolute inset-0 bg-gradient-to-br from-gray-900 via-gray-800 to-black z-0 animate-gradient-x"></div>
        <div className="absolute top-10 left-10 w-96 h-96 bg-sky-500 rounded-full mix-blend-screen filter blur-3xl opacity-20 animate-pulse"></div>
        <div className="absolute bottom-10 right-10 w-96 h-96 bg-purple-500 rounded-full mix-blend-screen filter blur-3xl opacity-20 animate-pulse delay-500"></div>
        
        {/* Hero Section */}
        <section
            id="hero"
            className="relative min-h-screen flex items-center justify-center text-center pt-20 px-4 overflow-hidden"
        >
            <div className="absolute top-0 left-0 w-[30vw] h-[30vw] bg-sky-500 rounded-full mix-blend-multiply filter blur-3xl opacity-50 animate-pulse"></div>
            <div className="absolute bottom-0 right-0 w-[32vw] h-[32vw] bg-purple-600 rounded-full mix-blend-multiply filter blur-3xl opacity-50 animate-pulse delay-500"></div>
            <div className="absolute top-1/2 left-1/2 w-40 h-40 bg-pink-400 rounded-full mix-blend-multiply filter blur-2xl opacity-30 animate-pulse delay-700"></div>
            
            <div className="relative z-10 flex flex-col items-center justify-center w-full">
                <AnimatedItem delay={100}>
                    <span className="text-sky-400 font-semibold text-lg md:text-2xl tracking-wider drop-shadow-xl">
                        Welcome to <span className="text-purple-400">Qubi</span>
                    </span>
                </AnimatedItem>
                <AnimatedItem delay={200}>
                    <h1 className="text-6xl md:text-8xl font-black text-white my-8 leading-tight tracking-tight drop-shadow-2xl">
                        Quantum<br className="hidden md:inline" />
                        Resistant<br className="hidden md:inline" />
                        Blockchain
                    </h1>
                </AnimatedItem>
                <AnimatedItem delay={300}>
                    <p className="max-w-3xl mx-auto text-2xl md:text-3xl text-gray-200 leading-relaxed">
                        Qubi is the next-generation blockchain System for the quantum era.
                        <br />
                        Powered by <span className="text-sky-400 font-bold">QRCS</span> (
                        <span className="text-purple-400 font-bold">Quantum Resistant Communication System</span>
                        ), Qubi ensures secure, scalable, and future-proof transactions.
                    </p>
                </AnimatedItem>
                <AnimatedItem delay={400}>
                    <div className="mt-12">
                        <a
                            href="#idea"
                            className="bg-gradient-to-r from-sky-500 via-purple-500 to-pink-500 text-white font-bold py-4 px-14 rounded-full hover:bg-sky-600 transition-all duration-300 transform hover:scale-110 shadow-2xl text-2xl border-2 border-white/10 inline-block"
                        >
                            Learn More About Qubi
                        </a>
                    </div>
                </AnimatedItem>
            </div>
            <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-black opacity-70"></div>
        </section>

        {/* Idea Section */}
        <div id="idea" className="relative z-10 pt-24 md:pt-12 px-4">
            <AnimatedItem>
                <section
                    id="abstract"
                    className="py-16 md:py-20 text-center max-w-4xl mx-auto"
                >
                    <h2 className="text-5xl font-extrabold text-sky-400 mb-8 drop-shadow-xl">
                        Abstract
                    </h2>
                    <p className="text-2xl md:text-3xl text-gray-200 leading-relaxed font-light">
                        {projectData.abstract}
                    </p>
                </section>
            </AnimatedItem>

            <section
                id="tech"
                className="py-16 md:py-20 bg-gradient-to-br from-sky-900/30 via-purple-900/20 to-black/40 backdrop-blur-md rounded-2xl shadow-2xl mt-16"
            >
                <div className="container mx-auto px-4">
                    <AnimatedItem>
                        <h2 className="text-4xl font-extrabold text-white mb-12 text-center drop-shadow-xl">
                            Technical Approach
                        </h2>
                    </AnimatedItem>
                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-10 max-w-6xl mx-auto">
                        {projectData.technicalApproach.map((item, index) => (
                            <AnimatedItem
                                key={index}
                                delay={index * 150}
                                className={`${index === 4 ? "md:col-span-2 lg:col-span-1" : ""} ${index === 5 ? "md:col-span-2 lg:col-span-2" : ""}`}
                            >
                                <div className="h-full p-8 rounded-2xl bg-white/10 backdrop-blur-lg border border-sky-400/20 hover:shadow-2xl hover:shadow-sky-500/30 transform hover:-translate-y-2 transition-all duration-300">
                                    <h3 className="text-2xl font-bold text-sky-400 mb-4 drop-shadow">
                                        {item.title}
                                    </h3>
                                    <p className="text-gray-200 leading-relaxed text-lg">
                                        {item.description}
                                    </p>
                                </div>
                            </AnimatedItem>
                        ))}
                    </div>
                </div>
            </section>
        </div>
        
        {/* Flow Section */}
        <div className="relative z-10 pt-24 md:pt-32 px-4 pb-24">
            <AnimatedItem>
                <section
                    id="flow"
                    className="py-16 md:py-20"
                >
                    <div className="container mx-auto px-4">
                        <h2 className="text-5xl font-extrabold text-sky-400 mb-16 text-center drop-shadow-xl">
                            System Flow
                        </h2>
                        <div className="max-w-3xl mx-auto">
                            <div className="relative">
                                <div className="absolute left-6 top-0 h-full w-1 bg-gradient-to-b from-sky-500/80 to-purple-500/80 rounded-full animate-pulse"></div>
                                <div className="flex flex-col space-y-16">
                                    {projectData.systemFlow.map((step, index) => (
                                        <AnimatedItem key={index} delay={index * 200}>
                                            <div className="relative pl-20 hover:scale-[1.04] transition-transform duration-300">
                                                <div className="absolute left-0 top-1 w-14 h-14 bg-gray-900 border-2 border-sky-400 rounded-full flex items-center justify-center text-2xl font-bold text-sky-400 shadow-2xl shadow-sky-500/30">
                                                    {index + 1}
                                                </div>
                                                <div className="bg-white/10 backdrop-blur-lg p-7 rounded-2xl border border-sky-400/20 hover:shadow-2xl hover:shadow-sky-500/30 transition-all duration-300">
                                                    <h4 className="font-bold text-white text-xl mb-3 drop-shadow">
                                                        {step.title}
                                                    </h4>
                                                    <p className="text-gray-200 leading-relaxed text-lg">
                                                        {step.description}
                                                    </p>
                                                </div>
                                            </div>
                                        </AnimatedItem>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </AnimatedItem>
        </div>

      {/* Global Styles */}
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
        html {
            scroll-behavior: smooth;
        }
        body {
            font-family: 'Inter', sans-serif;
        }
        @keyframes gradient-x {
          0%, 100% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
        }
        .animate-gradient-x {
          background-size: 200% 200%;
          animation: gradient-x 10s ease infinite;
        }
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in {
          animation: fade-in 1s ease-out forwards;
          opacity: 0;
        }
      `}</style>
    </main>
  );
}

