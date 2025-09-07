import React, { useState, useRef, useEffect } from "react";

// --- SVG Icons ---
const SendIcon = ({ className }) => (
  <svg
    className={className}
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="currentColor"
  >
    <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
  </svg>
);

// --- Initial Data ---
const initialChats = {
  "1": {
    name: "Alice",
    avatar: "https://placehold.co/80x80/A0AEC0/FFFFFF?text=A",
    messages: [
      {
        id: 1,
        text: "Hey, how is the Qubi project going?",
        sender: "Alice",
        timestamp: "10:00 AM",
      },
      {
        id: 2,
        text: "It's going great! Making good progress on the quantum resistance layer.",
        sender: "You",
        timestamp: "10:01 AM",
      },
    ],
  },
  "2": {
    name: "Bob",
    avatar: "https://placehold.co/80x80/F6AD55/FFFFFF?text=B",
    messages: [
      {
        id: 1,
        text: "Did you see the latest market trends?",
        sender: "Bob",
        timestamp: "Yesterday",
      },
      {
        id: 2,
        text: "Yeah, pretty volatile. But our long-term vision is solid.",
        sender: "You",
        timestamp: "Yesterday",
      },
    ],
  },
};

const replies = [
  "That's interesting!",
  "Cool, thanks for the update.",
  "Got it.",
  "Let's discuss this further on the call.",
];

export default function ChatApp() {
  const [chats, setChats] = useState(initialChats);
  const [activeChatId, setActiveChatId] = useState(null);
  const [newMessage, setNewMessage] = useState("");
  const messageEndRef = useRef(null);

  const activeChat = activeChatId ? chats[activeChatId] : null;

  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [activeChat?.messages]);

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!newMessage.trim() || !activeChatId) return;

    const userMessage = {
      id: Date.now(),
      text: newMessage,
      sender: "You",
      timestamp: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    };

    setChats((prevChats) => ({
      ...prevChats,
      [activeChatId]: {
        ...prevChats[activeChatId],
        messages: [...prevChats[activeChatId].messages, userMessage],
      },
    }));
    setNewMessage("");

    setTimeout(() => {
      const replyMessage = {
        id: Date.now() + 1,
        text: replies[Math.floor(Math.random() * replies.length)],
        sender: activeChat.name,
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      };

      setChats((prevChats) => ({
        ...prevChats,
        [activeChatId]: {
          ...prevChats[activeChatId],
          messages: [...prevChats[activeChatId].messages, replyMessage],
        },
      }));
    }, 1000);
  };

  return (
    <div className="bg-gray-900 text-gray-100 h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-4xl h-[80vh] bg-gray-800 rounded-2xl shadow-2xl flex overflow-hidden">
        {/* Sidebar */}
        {!activeChat && (
          <div className="flex flex-col w-full p-6">
            <h1 className="text-3xl font-bold text-sky-400 mb-4 text-center">
              Chat Dashboard
            </h1>
            <div className="overflow-y-auto flex-grow">
              {Object.entries(chats).map(([id, chat]) => {
                const lastMessage = chat.messages[chat.messages.length - 1];
                return (
                  <div
                    key={id}
                    onClick={() => setActiveChatId(id)}
                    className="flex items-center p-4 rounded-xl hover:bg-gray-700 transition-all mb-3 cursor-pointer"
                  >
                    <img
                      src={chat.avatar}
                      alt={chat.name}
                      className="w-12 h-12 rounded-full mr-4"
                    />
                    <div>
                      <h2 className="font-semibold text-lg">{chat.name}</h2>
                      <p className="text-gray-400 truncate max-w-[200px]">
                        {lastMessage?.text}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Chat Window */}
        {activeChat && (
          <div className="flex flex-col w-full md:w-3/4 bg-gray-900 rounded-xl overflow-hidden">
            <header className="flex items-center p-4 border-b border-gray-700 bg-gray-800">
              <button
                onClick={() => setActiveChatId(null)}
                className="mr-4 text-sky-400 hover:text-sky-300"
              >
                ← Back
              </button>
              <img
                src={activeChat.avatar}
                alt={activeChat.name}
                className="w-10 h-10 rounded-full mr-4"
              />
              <h2 className="font-semibold text-lg">{activeChat.name}</h2>
            </header>

            <main className="flex-grow p-4 overflow-y-auto space-y-3">
              {activeChat.messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`flex ${
                    msg.sender === "You" ? "justify-end" : "justify-start"
                  }`}
                >
                  <div
                    className={`max-w-xs px-4 py-2 rounded-2xl shadow-md ${
                      msg.sender === "You"
                        ? "bg-gradient-to-br from-sky-500 to-purple-600 text-white"
                        : "bg-gray-700 text-gray-200"
                    }`}
                  >
                    {msg.text}
                    <div className="text-xs text-gray-300 mt-1">
                      {msg.timestamp}
                    </div>
                  </div>
                </div>
              ))}
              <div ref={messageEndRef} />
            </main>

            <footer className="p-4 bg-gray-800 border-t border-gray-700">
              <form onSubmit={handleSendMessage} className="flex space-x-3">
                <input
                  type="text"
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  placeholder="Type a message..."
                  className="flex-grow p-3 bg-gray-700 border border-gray-600 rounded-full focus:outline-none text-white"
                />
                <button
                  type="submit"
                  className="bg-gradient-to-br from-sky-500 to-purple-600 text-white rounded-full p-3 hover:opacity-90"
                >
                  <SendIcon className="w-6 h-6" />
                </button>
              </form>
            </footer>
          </div>
        )}
      </div>
    </div>
  );
}
