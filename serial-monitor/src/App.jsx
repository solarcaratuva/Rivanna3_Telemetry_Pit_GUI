import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const interval = setInterval(() => {
      axios.get("http://localhost:5000/messages")
        .then(res => setMessages(res.data))
        .catch(err => console.error(err));
    }, 1000); // poll every second

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">XBee Radio Messages</h1>
      <div className="bg-gray-100 p-4 h-96 overflow-y-scroll border rounded">
        {messages.map((msg, idx) => (
          <div key={idx} className="text-sm">{msg}</div>
        ))}
      </div>
    </div>
  );
}

export default App;
