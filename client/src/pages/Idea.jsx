import React from "react";
import { projectData } from "../data/projectData";
import AnimatedItem from "../components/AnimatedItem";

export default function Idea() {
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

      <div className="relative z-10">
        {/* Abstract Section */}
        <AnimatedItem>
          <section
            id="abstract"
            className="py-16 md:py-20 text-center max-w-4xl mx-auto animate-fade-in"
          >
            <h2 className="text-5xl font-extrabold text-sky-400 mb-8 drop-shadow-xl">
              Abstract
            </h2>
            <p className="text-2xl md:text-3xl text-gray-200 leading-relaxed font-light">
              {projectData.abstract}
            </p>
          </section>
        </AnimatedItem>

        {/* Technical Approach Section */}
        <section
          id="tech"
          className="py-16 md:py-20 bg-gradient-to-br from-sky-900/30 via-purple-900/20 to-black/40 backdrop-blur-md rounded-2xl shadow-2xl mt-16 animate-fade-in"
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
                  className={`$${
                    index === 4 ? "md:col-span-2 lg:col-span-2" : ""
                  } animate-fade-in`}
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

        {/* Future Sections Placeholder */}
        <section className="py-20 text-center text-gray-400 animate-fade-in">
          <p className="text-xl">
            More sections like <span className="text-sky-400">Impact</span>,{" "}
            <span className="text-purple-400">Challenges</span>, and{" "}
            <span className="text-pink-400">Future Scope</span> will be added
            here.
          </p>
        </section>
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
