import React from "react";
import { projectData } from "../data/projectData";
import AnimatedItem from "../components/AnimatedItem";

export default function Idea() {
  return (
    <main className="relative pt-24 md:pt-32 px-4 overflow-hidden">
      {/* Background Decorations */}
      <div className="absolute inset-0 bg-gradient-to-br from-gray-900 via-gray-800 to-black z-0"></div>
      <div className="absolute top-20 left-10 w-72 h-72 bg-sky-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
      <div className="absolute bottom-10 right-10 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse delay-500"></div>

      <div className="relative z-10">
        {/* Abstract Section */}
        <AnimatedItem>
          <section
            id="abstract"
            className="py-16 md:py-20 text-center max-w-4xl mx-auto"
          >
            <h2 className="text-4xl font-extrabold text-white mb-6">
              Abstract
            </h2>
            <p className="text-lg md:text-xl text-gray-300 leading-relaxed">
              {projectData.abstract}
            </p>
          </section>
        </AnimatedItem>

        {/* Technical Approach Section */}
        <section
          id="tech"
          className="py-16 md:py-20 bg-white/5 backdrop-blur-md rounded-2xl shadow-lg mt-12"
        >
          <div className="container mx-auto px-4">
            <AnimatedItem>
              <h2 className="text-4xl font-extrabold text-white mb-12 text-center">
                Technical Approach
              </h2>
            </AnimatedItem>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
              {projectData.technicalApproach.map((item, index) => (
                <AnimatedItem
                  key={index}
                  delay={index * 150}
                  className={`${
                    index === 4 ? "md:col-span-2 lg:col-span-2" : ""
                  }`}
                >
                  <div className="h-full p-6 rounded-xl bg-white/10 backdrop-blur-lg border border-white/10 hover:shadow-2xl transform hover:-translate-y-2 transition-all duration-300">
                    <h3 className="text-xl font-bold text-sky-400 mb-3">
                      {item.title}
                    </h3>
                    <p className="text-gray-300 leading-relaxed">
                      {item.description}
                    </p>
                  </div>
                </AnimatedItem>
              ))}
            </div>
          </div>
        </section>

        {/* Future Sections Placeholder */}
        <section className="py-20 text-center text-gray-400">
          <p className="text-lg">
            More sections like <span className="text-sky-400">Impact</span>,{" "}
            <span className="text-sky-400">Challenges</span>, and{" "}
            <span className="text-sky-400">Future Scope</span> will be added
            here.
          </p>
        </section>
      </div>
    </main>
  );
}
