// src/components/Navbar.jsx
import React, { useState } from "react";
import { NavLink } from "react-router-dom";

const navLinks = [
  { name: "Home", path: "/" },
  { name: "Idea", path: "/idea" },
  { name: "Flow", path: "/flow" },
];

function Navbar() {
  // We don't need local state if we use NavLink's `isActive` property
  return (
    <nav className="fixed top-4 left-1/2 -translate-x-1/2 z-50">
      <div className="relative flex items-center space-x-2 bg-gray-900/50 backdrop-blur-sm p-2 rounded-full border border-white/10 shadow-lg">
        {navLinks.map((link) => (
          <NavLink
            key={link.name}
            to={link.path}
            // `isActive` is provided by NavLink
            className={({ isActive }) =>
              `relative px-4 py-2 text-sm font-medium transition-colors duration-300 rounded-full ` +
              (isActive ? "text-white" : "text-gray-400 hover:text-white")
            }
          >
            {({ isActive }) => (
              <>
                {link.name}
                {isActive && (
                  <motion.div
                    className="absolute inset-0 bg-sky-500/80 rounded-full -z-10"
                    layoutId="active-pill"
                    transition={{ type: "spring", stiffness: 300, damping: 30 }}
                  />
                )}
              </>
            )}
          </NavLink>
        ))}
      </div>
    </nav>
  );
}

// To make the sliding animation work, you need to wrap your routes in AnimatePresence
// and install framer-motion: npm install framer-motion
import { motion, AnimatePresence } from "framer-motion";

export default Navbar;
