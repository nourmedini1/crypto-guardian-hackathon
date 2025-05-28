# 🛡 Crypto Guardian – AI-Powered Crypto Scam Detection Platform

**🏆 Awarded 3rd Place at the AI Odyssey Hackathon by GDG SUP'COM**
<p align="center">
  <img src="./crypto-guardian/src/assets/logo.png" alt="Crypto Guardian Logo" width="200"/>
</p>

Crypto Guardian is a full-stack AI-powered platform designed to detect cryptocurrency scams in real time, provide market insights, and assist users with a voice-enabled intelligent assistant. The project combines real-time sentiment analysis, scam pattern detection, predictive modeling, and conversational AI to improve safety and trust in the crypto ecosystem.

[🎥 Watch Demo Video](https://youtu.be/yYzrvi1w0bI)

---

## Problem Statement

The cryptocurrency space is heavily targeted by scams such as pump-and-dump schemes, rug pulls, and misinformation campaigns, especially on platforms like Telegram. These tactics often go unnoticed until after major financial losses occur.

**Objective:**  
Build a comprehensive AI assistant capable of detecting scams, analyzing sentiment, predicting price trends, and answering user questions using reliable crypto knowledge—delivered in real time via web and Telegram.

---

##  Solution Overview

Crypto Guardian combines several intelligent components to form an integrated assistant that addresses multiple facets of crypto security.

### ✳ Key Features

- **LLM-Based Sentiment Analysis**  
  Analyzes message streams in Telegram groups to detect sentiment shifts indicative of pump-and-dump schemes. Uses prompt-engineered large language models (LLMs) for nuanced emotion and manipulation detection.

- **RAG Chatbot (Retrieval-Augmented Generation)**  
  Provides context-grounded answers to user questions by retrieving relevant information from a curated crypto knowledge base and generating responses using an LLM.

- **Telegram Bot Integration**  
  Allows users to interact with the assistant directly via Telegram. It not only answers questions but also sends scam alerts when manipulation or suspicious group activity is detected.

- **Voice-Enabled Web Assistant**  
  Enables users to talk with the assistant using Speech-to-Text (STT) and receive spoken replies through Text-to-Speech (TTS), improving accessibility and ease of use.

- **Ethereum Price Prediction**  
  Forecasts ETH prices using an LSTM-based time series prediction model. Helps users understand market trends over a 7-day horizon.

- **Rug Pull Detection System**  
  Scans and analyzes token behavior using smart contract metadata and liquidity movement patterns to identify potential rug pulls. Flags suspicious tokens exhibiting signs of exit scams or sudden fund drainage.

---

##  System Architecture

- **Frontend**: Built with React for an interactive web UI displaying live crypto data and supporting chatbot interaction.
- **Backend**: Python-based services using FastAPI for model inference, sentiment analysis, and RAG logic.
- **AI Layer**: LLMs for sentiment analysis and chatbot logic, LSTM for price forecasting.
- **Bots**: Telegram integration via Telethon and Telegram Bot API for real-time user interaction and alerting.
- **Voice Interface**: Web Speech API enables seamless spoken input and output.

---

## 🔧 Technologies Used

| Layer             | Tools & Technologies                                |
|------------------|------------------------------------------------------|
| Frontend          | React, JavaScript, SCSS                             |
| Voice Interaction | Web Speech API                                      |
| Backend           | Python, FastAPI                                     |
| Bots              | Telethon, Telegram Bot API                          |
| AI & NLP          | LLMs, Prompt Engineering, RAG, LSTM                 |
| Blockchain Data   | Smart contract analysis, token metadata, price APIs |
| Deployment        | Microsoft Azure Virtual Machines                    |

---

## Project Outcomes

- Delivered a fully functional AI crypto assistant in under 7 days.
- Detected and alerted real-time pump-and-dump activity in monitored Telegram groups.
- Flagged potentially fraudulent tokens through rug pull detection logic.
- Enabled voice-based user interaction via web interface.
- Supported question-answering through a reliable RAG chatbot.
- Earned 3rd place at the AI Odyssey Hackathon for innovation and impact.

---


