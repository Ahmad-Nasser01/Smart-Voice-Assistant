# 🎙️ Smart Voice & Text AI Assistant

🔗 **Live Demo:** [Click here to test the live application directly](https://smart-voice-assistant-yhyp.onrender.com)

A modern, secure, bilingual (Arabic/English) AI voice and text assistant built with **Flask (Python)**, integrated with the official **Cohere AI API**, featuring real-time conversation history and a sleek interactive user interface.

## 🚀 Features
- **Bilingual Support:** Full, high-accuracy support for both Arabic and English.
- **Chat History & Memory:** Maintains ongoing conversation context across turns.
- **Interactive UI:** Features a thinking indicator (`...`), audio controls, and an instant stop button (🛑).
- **Security First:** Strict separation of API keys using environment variables (`.env`) to prevent credential exposure.

---

## 📂 Project Structure
```text
Smart-Voice-Assistant/
├── app.py           # Flask backend server
├── index.html       # Frontend web interface
├── requirements.txt # Python dependencies
└── .env             # Environment variables (To be created by the user)
