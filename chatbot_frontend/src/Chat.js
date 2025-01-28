import React, { useState, useEffect, useRef } from 'react';
import './Chat.css';

function Chat() {
  const [userMessage, setUserMessage] = useState('');
  const [messages, setMessages] = useState(() => {
    // Load messages from localStorage on initial render
    const cachedMessages = localStorage.getItem('chatMessages');
    return cachedMessages ? JSON.parse(cachedMessages) : [];
  });
  const [ws, setWs] = useState(null);
  const lastMessageRef = useRef(null);

  // Establish WebSocket connection
  useEffect(() => {
    const socket = new WebSocket('ws://127.0.0.1:8000/ws/messages/');

    socket.onmessage = (event) => {
      setMessages((prevMessages) => {
        const newMessages = [
          ...prevMessages,
          { role: 'bot', content: event.data },
        ];
        // Cache updated messages in localStorage
        localStorage.setItem('chatMessages', JSON.stringify(newMessages));
        return newMessages;
      });
    };

    socket.onopen = () => {
      console.log('WebSocket connection established');
    };

    socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    socket.onclose = () => {
      console.log('WebSocket connection closed');
    };

    setWs(socket);

    // Cleanup WebSocket connection when the component unmounts
    return () => socket.close();
  }, []);

  // Scroll to the last message whenever messages update
  useEffect(() => {
    if (lastMessageRef.current) {
      lastMessageRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const handleUserMessage = (e) => {
    setUserMessage(e.target.value);
  };

  const sendMessage = (e) => {
    e.preventDefault();

    if (ws) {
      // Send user message through WebSocket
      ws.send(userMessage);

      // Update the messages list with user message
      setMessages((prevMessages) => {
        const newMessages = [
          ...prevMessages,
          { role: 'user', content: userMessage },
        ];
        // Cache updated messages in localStorage
        localStorage.setItem('chatMessages', JSON.stringify(newMessages));
        return newMessages;
      });

      // Clear the input field after sending the message
      setUserMessage('');
    }
  };

  const clearChat = () => {
    setMessages([]);
    localStorage.removeItem('chatMessages'); // Clear cache
  };

  return (
    <div className="chat-container">
      <h2>Chat with AI</h2>
      <div className="messages">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={msg.role}
            ref={index === messages.length - 1 ? lastMessageRef : null}
          >
            <strong>{msg.role === 'user' ? 'You' : 'Bot'}:</strong> {msg.content}
          </div>
        ))}
      </div>
      <form onSubmit={sendMessage}>
        <input
          type="text"
          value={userMessage}
          onChange={handleUserMessage}
          placeholder="Type a message..."
          required
        />
        <button type="submit">Send</button>
      </form>
      <button onClick={clearChat} style={{ marginTop: '10px' }}>
        Clear Chat
      </button>
    </div>
  );
}

export default Chat;
