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
        {/* Background Gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-gray-900 via-gray-800 to-black z-0"></div>

        {/* Decorative Blobs */}
        <div className="absolute top-10 left-10 w-72 h-72 bg-sky-500 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse"></div>
        <div className="absolute bottom-10 right-10 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse delay-500"></div>

        {/* Hero Content */}
        <div className="relative z-10">
          <AnimatedItem delay={100}>
            <span className="text-sky-400 font-semibold text-lg md:text-xl tracking-wider">
              {projectData.heroSubtitle}
            </span>
          </AnimatedItem>
          <AnimatedItem delay={200}>
            <h1 className="text-4xl md:text-6xl font-black text-white my-4 leading-tight tracking-tight drop-shadow-lg">
              {projectData.heroTitle}
            </h1>
          </AnimatedItem>
          <AnimatedItem delay={300}>
            <p className="max-w-3xl mx-auto text-lg md:text-xl text-gray-300 leading-relaxed">
              {projectData.heroDescription}
            </p>
          </AnimatedItem>
          <AnimatedItem delay={400}>
            <div className="mt-8">
              <Link
                to="/idea"
                className="bg-sky-500 text-white font-bold py-3 px-8 rounded-full hover:bg-sky-600 transition-all duration-300 transform hover:scale-105 shadow-xl"
              >
                Learn More
              </Link>
            </div>
          </AnimatedItem>
        </div>

        {/* Gradient Overlay for depth */}
        <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-black opacity-50"></div>
      </section>
    </main>
  );
}
