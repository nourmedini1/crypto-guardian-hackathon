import React, { useState, useRef, useEffect } from 'react';
import { Button, Form, InputGroup, Offcanvas } from 'react-bootstrap';
import axios from 'axios';
import styles from './styles/Chatbot.module.css';
import MessageBubble from './ChatBot/MessageBubble';
import logo from '../assets/logo.svg';

const Chatbot = () => {
  const [show, setShow] = useState(false);
  const [context, setContext] = useState('');
  const [message, setMessage] = useState('');
  const [conversation, setConversation] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const recognitionRef = useRef(null);

  useEffect(() => {
    if ('webkitSpeechRecognition' in window) {
      recognitionRef.current = new window.webkitSpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = 'en-US';

      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setMessage(transcript);
      };

      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
      };
    }
  }, []);

  const speak = (text) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'en-US';
      utterance.rate = 1;
      utterance.pitch = 1;
  
      const voices = window.speechSynthesis.getVoices();
      utterance.voice = 
        voices.find(voice => voice.name.includes('Google UK English Female')) || 
        voices.find(voice => voice.name.includes('Google US English')) ||
        voices.find(voice => voice.lang.startsWith('en')) || 
        voices[0];
  
      window.speechSynthesis.speak(utterance);
    } else {
      alert('Your browser does not support speech synthesis.');
    }
  };
  
  const handleShow = () => setShow(!show);

  const sendMessage = async () => {
    if (!message.trim() || isLoading) return;
  
    setIsLoading(true);
    setConversation((prev) => [...prev, { sender: 'user', text: message }]);
    const userMessage = message;
    setMessage('');
  
    try {
      const response = await axios.post("http://20.199.80.240:5010/chat", {
        user_question: userMessage,
        context: context
      });
  
      const botResponse = response.data.chatbot_response;
      setContext(response.data.context);
      setConversation((prev) => [...prev, { sender: 'bot', text: botResponse }]);
  
    } catch (error) {
      console.error('Error communicating with chatbot:', error);
      const errorMessage = 'Sorry, I am unable to respond at the moment. Please try again later.';
      setConversation((prev) => [...prev, { sender: 'bot', text: errorMessage }]);
  

    } finally {
      setIsLoading(false);
    }
  };
  

  return (
    <>
      <Button onClick={handleShow} className={styles.chatButton}>
        <img src={logo} alt="Chat" className={styles.chatbotLogo} />
      </Button>

      <Offcanvas show={show} onHide={handleShow} placement="end" className={styles.chatOffcanvas}>
        <Offcanvas.Header closeButton className={styles.chatHeader}>
          <div className={styles.titleContainer}>
            <img src={logo} alt="CryptoGuardian Logo" className={styles.headerLogo} />
            <span>CryptoGuardian AI</span>
          </div>
        </Offcanvas.Header>
        <Offcanvas.Body className={styles.chatBody}>
          <div className={styles.conversationContainer}>
            {conversation.map((msg, index) => (
              <MessageBubble key={index} message={msg} onSpeak={speak} />
            ))}
          </div>
          <div className={styles.inputContainer}>
            <InputGroup>
              <Form.Control
                placeholder="Type your message..."
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              />

              <Button
                variant="primary"
                onClick={sendMessage}
                disabled={isLoading}
                title="Send message"
              >
                {isLoading ? '...' : 'Send'}
              </Button>
            </InputGroup>
          </div>
        </Offcanvas.Body>
      </Offcanvas>
    </>
  );
};

export default Chatbot;
