import React from "react";
import { projectData } from "../data/projectData";
import AnimatedItem from "../components/AnimatedItem";

export default function Flow() {
  return (
    <main className="relative pt-24 md:pt-32 px-4 overflow-hidden">
      {/* Background Gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-gray-900 via-gray-800 to-black z-0"></div>

      {/* Decorative Blobs */}
      <div className="absolute top-10 left-20 w-72 h-72 bg-sky-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
      <div className="absolute bottom-10 right-20 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse delay-500"></div>

      {/* Main Content */}
      <div className="relative z-10">
        <AnimatedItem>
          <section id="flow" className="min-h-screen py-16 md:py-20">
            <div className="container mx-auto px-4">
              <h2 className="text-4xl font-extrabold text-white mb-16 text-center">
                System Flow
              </h2>
              <div className="max-w-3xl mx-auto">
                <div className="relative">
                  {/* Vertical Line */}
                  <div className="absolute left-6 top-0 h-full w-1 bg-gradient-to-b from-sky-500/60 to-purple-500/60 rounded-full animate-pulse"></div>

                  {/* Steps */}
                  <div className="flex flex-col space-y-12">
                    {projectData.systemFlow.map((step, index) => (
                      <AnimatedItem key={index} delay={index * 200}>
                        <div className="relative pl-20 hover:scale-[1.02] transition-transform duration-300">
                          {/* Number Circle */}
                          <div className="absolute left-0 top-1 w-12 h-12 bg-gray-900 border-2 border-sky-500 rounded-full flex items-center justify-center text-xl font-bold text-sky-400 shadow-lg shadow-sky-500/30">
                            {index + 1}
                          </div>

                          {/* Step Content */}
                          <div className="bg-white/10 backdrop-blur-md p-5 rounded-xl border border-white/10 hover:shadow-2xl hover:shadow-sky-500/20 transition-all duration-300">
                            <h4 className="font-bold text-white text-lg mb-2">
                              {step.title}
                            </h4>
                            <p className="text-gray-300 leading-relaxed">
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
    </main>
  );
}
