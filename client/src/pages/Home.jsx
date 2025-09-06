import React from "react";
import { Link } from "react-router-dom";
import { projectData } from "../data/projectData";
import AnimatedItem from "../components/AnimatedItem";

export default function Home() {
  return (
    <main>
      <section
        id="hero"
        className="relative min-h-screen flex items-center justify-center text-center pt-20 px-4 overflow-hidden"
      >
        {/* Animated Gradient Background */}
        <div className="absolute inset-0 bg-gradient-to-br from-gray-900 via-gray-800 to-black z-0 animate-gradient-x"></div>

        {/* Extra Decorative Blobs & Particles */}
        <div className="absolute top-0 left-0 w-[30vw] h-[30vw] bg-sky-500 rounded-full mix-blend-multiply filter blur-3xl opacity-50 animate-pulse"></div>
        <div className="absolute bottom-0 right-0 w-[32vw] h-[32vw] bg-purple-600 rounded-full mix-blend-multiply filter blur-3xl opacity-50 animate-pulse delay-500"></div>
        <div className="absolute top-1/2 left-1/2 w-40 h-40 bg-pink-400 rounded-full mix-blend-multiply filter blur-2xl opacity-30 animate-pulse delay-700"></div>
        <div className="absolute top-1/3 right-1/4 w-24 h-24 bg-yellow-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse delay-1000"></div>
        <div className="absolute bottom-1/4 left-1/3 w-16 h-16 bg-green-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse delay-1200"></div>

        {/* Hero Content */}
        <div className="relative z-10 flex flex-col items-center justify-center w-full">
          <AnimatedItem delay={100}>
            <span className="text-sky-400 font-semibold text-lg md:text-2xl tracking-wider drop-shadow-xl animate-fade-in">
              Welcome to <span className="text-purple-400">Qubi</span>
            </span>
          </AnimatedItem>
          <AnimatedItem delay={200}>
            <h1 className="text-6xl md:text-8xl font-black text-white my-8 leading-tight tracking-tight drop-shadow-2xl animate-fade-in">
              Quantum
              <br className="hidden md:inline" />
              Resistant
              <br className="hidden md:inline" />
              Blockchain
            </h1>
          </AnimatedItem>
          <AnimatedItem delay={300}>
            <p className="max-w-3xl mx-auto text-2xl md:text-3xl text-gray-200 leading-relaxed animate-fade-in">
              Qubi is the next-generation blockchain System for the quantum era.
              <br />
              Powered by <span className="text-sky-400 font-bold">QRCS</span> (
              <span className="text-purple-400 font-bold">
                Quantum Resistant Communication System
              </span>
              ), Qubi ensures secure, scalable, and future-proof transactions
              against quantum attacks.
            </p>
          </AnimatedItem>
          <AnimatedItem delay={350}>
            <div className="mt-8 flex flex-col items-center gap-4 animate-fade-in">
              <span className="inline-block bg-black/70 text-sky-300 px-6 py-3 rounded-full font-mono text-lg shadow-2xl border border-sky-500/30">
                Introducing <span className="text-purple-400">QRCP</span>:
                Quantum Resistant Communication System
              </span>
              <span className="inline-block text-gray-400 text-lg max-w-xl">
                Experience the future of decentralized security and privacy.
                <br />
                Qubi leverages post-quantum cryptography to protect your assets
                and data from tomorrow's threats.
              </span>
            </div>
          </AnimatedItem>
          <AnimatedItem delay={400}>
            <div className="mt-12 animate-fade-in">
              <Link
                to="/idea"
                className="bg-gradient-to-r from-sky-500 via-purple-500 to-pink-500 text-white font-bold py-4 px-14 rounded-full hover:bg-sky-600 transition-all duration-300 transform hover:scale-110 shadow-2xl text-2xl border-2 border-white/10"
              >
                Learn More About Qubi
              </Link>
            </div>
          </AnimatedItem>
        </div>

        {/* Gradient Overlay for depth */}
        <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-black opacity-70"></div>
      </section>
      {/* Custom CSS for extra animation */}
      <style>{`
        @keyframes gradient-x {
          0%, 100% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
        }
        .animate-gradient-x {
          background-size: 200% 200%;
          animation: gradient-x 8s ease-in-out infinite;
        }
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in {
          animation: fade-in 1.2s cubic-bezier(0.4,0,0.2,1) both;
        }
      `}</style>
    </main>
  );
}
