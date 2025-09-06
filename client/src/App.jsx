import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Home, Blocks } from "lucide-react"; // icons
import HomePage from "./pages/Home";
import BlockchainsPage from "./pages/Block";
import Navbar from "./components/Navbar";
import Idea from "./pages/Idea";
import Flow from "./pages/Flow";
function App() {
  return (
    <>
      <Router>
        <Navbar />
        <div className="min-h-screen bg-gray-50 text-gray-900">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/blockchains" element={<BlockchainsPage />} />

            <Route path="/idea" element={<Idea />} />
            <Route path="/flow" element={<Flow />} />
          </Routes>
        </div>
      </Router>
    </>
  );
}

export default App;
