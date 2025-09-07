import React, { useState, useRef, useEffect } from "react";

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

const initialChats = {
  1: {
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
        text: "It's going great! Making good progress.",
        sender: "You",
        timestamp: "10:01 AM",
      },
    ],
  },
  2: {
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
        text: "Yeah, pretty volatile.",
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
      <div className="w-full max-w-3xl h-[80vh] bg-gray-800 rounded-2xl shadow-2xl flex flex-col">
        {/* If no active chat → Show Users List */}
        {!activeChat && (
          <div className="flex flex-col w-full p-6">
            <h1 className="text-3xl font-bold text-sky-400 mb-6 text-center">
              Users
            </h1>
            <div className="overflow-y-auto flex-grow space-y-4">
              {Object.entries(chats).map(([id, chat]) => {
                const lastMessage = chat.messages[chat.messages.length - 1];
                return (
                  <div
                    key={id}
                    onClick={() => setActiveChatId(id)}
                    className="flex items-center p-4 bg-gray-700 hover:bg-gray-600 rounded-xl cursor-pointer transition-all"
                  >
                    <img
                      src={chat.avatar}
                      alt={chat.name}
                      className="w-14 h-14 rounded-full mr-4"
                    />
                    <div className="flex flex-col">
                      <h2 className="font-semibold text-lg">{chat.name}</h2>
                      <p className="text-gray-400 text-sm truncate max-w-[200px]">
                        {lastMessage?.text}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* If active chat → Show Chat Window */}
        {activeChat && (
          <div className="flex flex-col flex-grow">
            {/* Header */}
            <header className="flex items-center p-4 bg-gray-800 border-b border-gray-700">
              <button
                onClick={() => setActiveChatId(null)}
                className="mr-4 text-sky-400 hover:text-sky-300 text-lg"
              >
                ← Back
              </button>
              <img
                src={activeChat.avatar}
                alt={activeChat.name}
                className="w-10 h-10 rounded-full mr-3"
              />
              <h2 className="font-semibold text-lg">{activeChat.name}</h2>
            </header>

            {/* Messages */}
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

            {/* Input */}
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
