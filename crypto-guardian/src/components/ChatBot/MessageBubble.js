import React from 'react';
import { FaUserCircle, FaVolumeUp } from 'react-icons/fa';
import styles from '../styles/Chatbot.module.css';
import botLogo from '../../assets/logo.svg';

const MessageBubble = ({ message, onSpeak }) => {
  const isUser = message.sender === 'user';
  
  const handleSpeak = () => {
    if (onSpeak) {
      onSpeak(message.text);
    }
  };

  return (
    <div className={`${styles.messageContainer} ${isUser ? styles.userMessage : styles.botMessage}`}>
      {!isUser && (
        <img
          src={botLogo}
          alt="Bot Logo"
          className={styles.botAvatar}
        />
      )}
      <div className={`${styles.messageBubble} ${isUser ? styles.userBubble : styles.botBubble}`}>
        {message.text}
        {!isUser && (
          <button 
            className={styles.speakButton} 
            onClick={handleSpeak}
            title="Listen to this message"
          >
            <FaVolumeUp />
          </button>
        )}
      </div>
      {isUser && <FaUserCircle size={40} className={styles.userAvatar} />}
    </div>
  );
};

export default MessageBubble;
