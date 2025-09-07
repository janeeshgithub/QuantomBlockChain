import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import HomePage from "./pages/Home";
import BlockchainsPage from "./pages/Block";
import Chat from "./pages/Chat";

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50 text-gray-900">
        <Navbar />
        {/* Add padding so content doesn't stick under the navbar */}
        <main>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/chat" element={<Chat />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
