import React from "react";
import { NavLink } from "react-router-dom";
import { motion } from "framer-motion";
import { Home, MessageSquare, Blocks } from "lucide-react";

const navLinks = [
  { name: "Home", path: "/", icon: Home },
  { name: "Chat", path: "/chat", icon: MessageSquare },
];

function Navbar() {
  return (
    <nav className="fixed top-0 right-0 z-50 w-full bg-transparent border-b border-white/10">
      <div className="flex justify-end items-center gap-6 px-8 py-4">
        {navLinks.map((link) => {
          const Icon = link.icon;
          return (
            <NavLink
              key={link.name}
              to={link.path}
              className={({ isActive }) =>
                `relative flex items-center gap-2 px-3 py-2 text-sm font-medium transition-colors duration-300 ` +
                (isActive ? "text-white" : "text-gray-300 hover:text-white")
              }
            >
              {({ isActive }) => (
                <>
                  <Icon size={16} />
                  <span>{link.name}</span>
                  {isActive && (
                    <motion.div
                      layoutId="active-underline"
                      className="absolute bottom-0 left-0 w-full h-[2px] bg-sky-500"
                      transition={{
                        type: "spring",
                        stiffness: 300,
                        damping: 25,
                      }}
                    />
                  )}
                </>
              )}
            </NavLink>
          );
        })}
      </div>
    </nav>
  );
}

export default Navbar;
