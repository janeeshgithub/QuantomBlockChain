import React from "react";
import { projectData } from "../data/projectData";
import AnimatedItem from "../components/AnimatedItem";

export default function Flow() {
  return (
    <main className="relative pt-24 md:pt-32 px-4 overflow-hidden">
      {/* Animated Gradient Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-gray-900 via-gray-800 to-black z-0 animate-gradient-x"></div>
      {/* Extra Decorative Blobs & Particles */}
      <div className="absolute top-10 left-10 w-96 h-96 bg-sky-500 rounded-full mix-blend-multiply filter blur-3xl opacity-40 animate-pulse"></div>
      <div className="absolute bottom-10 right-10 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-40 animate-pulse delay-500"></div>
      <div className="absolute top-1/2 left-1/2 w-40 h-40 bg-pink-400 rounded-full mix-blend-multiply filter blur-2xl opacity-30 animate-pulse delay-700"></div>
      <div className="absolute top-1/3 right-1/4 w-24 h-24 bg-yellow-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse delay-1000"></div>
      <div className="absolute bottom-1/4 left-1/3 w-16 h-16 bg-green-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse delay-1200"></div>

      {/* Main Content */}
      <div className="relative z-10">
        <AnimatedItem>
          <section
            id="flow"
            className="min-h-screen py-16 md:py-20 animate-fade-in"
          >
            <div className="container mx-auto px-4">
              <h2 className="text-5xl font-extrabold text-sky-400 mb-16 text-center drop-shadow-xl">
                System Flow
              </h2>
              <div className="max-w-3xl mx-auto">
                <div className="relative">
                  {/* Vertical Line */}
                  <div className="absolute left-6 top-0 h-full w-1 bg-gradient-to-b from-sky-500/80 to-purple-500/80 rounded-full animate-pulse"></div>

                  {/* Steps */}
                  <div className="flex flex-col space-y-16">
                    {projectData.systemFlow.map((step, index) => (
                      <AnimatedItem key={index} delay={index * 200}>
                        <div className="relative pl-20 hover:scale-[1.04] transition-transform duration-300 animate-fade-in">
                          {/* Number Circle */}
                          <div className="absolute left-0 top-1 w-14 h-14 bg-gray-900 border-2 border-sky-400 rounded-full flex items-center justify-center text-2xl font-bold text-sky-400 shadow-2xl shadow-sky-500/30">
                            {index + 1}
                          </div>

                          {/* Step Content */}
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
