# 🎤 SpeakSmart — AI Interview Coach

An AI-powered mock interview platform that helps users practice interviews using real-time speech analysis, intelligent feedback, and performance analytics.

SpeakSmart simulates realistic interview sessions and evaluates communication skills such as fluency, grammar, and answer accuracy using AI and NLP techniques.

---

# 🚀 Features

## 🎯 AI Mock Interview Simulation

* Practice HR and technical interview questions
* Role-based interview categories
* Multi-level difficulty support

## 🎤 Voice Recording & Analysis

* Real-time audio recording
* Speech duration analysis
* RMS audio feature extraction
* Pause & filler detection

## 🤖 AI-Powered Feedback

* Fluency evaluation
* Grammar analysis
* Accuracy scoring
* Personalized improvement suggestions

## 📊 Analytics Dashboard

* Performance tracking
* Skill progress visualization
* Interview score analytics
* Weak skill identification

## 🔐 Authentication System

* User registration & login
* Local session handling
* Protected pages

## 🎨 Modern SaaS UI

* Glassmorphism design
* Responsive layouts
* Animated microphone recording
* Premium dark theme

---

# 🧠 Tech Stack

## Frontend

* HTML5
* CSS3
* JavaScript (ES6 Modules)

## Backend

* FastAPI
* Python

## AI / NLP

* Groq API
* Whisper Speech-to-Text
* NLP-based scoring system

## Audio Processing

* Librosa
* NumPy
* SoundFile

## Database

* SQLite (Current)
* PostgreSQL (Planned)

---

# 🏗️ System Architecture

```text
Frontend (HTML/CSS/JS)
        ↓
FastAPI Backend
        ↓
AI Services & NLP Analysis
        ↓
Database Storage
```

---

# 📁 Project Structure

```text
SpeakSmart-AI-Interview-Coach/
│
├── backend/
│   ├── ai/
│   ├── routes/
│   ├── services/
│   ├── main.py
│   └── db.py
│
├── frontend/
│   ├── js/
│   ├── styles.css
│   ├── responsive.css
│   ├── index.html
│   ├── home.html
│   ├── practice.html
│   └── analytics.html
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/SpeakSmart-AI-Interview-Coach.git

cd SpeakSmart-AI-Interview-Coach
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\\Scripts\\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Backend

```bash
uvicorn backend.main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

---

# ▶️ Run Frontend

Open second terminal:

```bash
cd frontend

python -m http.server 5500
```

Frontend runs at:

```text
http://127.0.0.1:5500/index.html
```

---

# 📸 Screenshots

## 🏠 Home Page

(Add Screenshot Here)

## 🎤 Interview Practice

(Add Screenshot Here)

## 📊 Analytics Dashboard

(Add Screenshot Here)

---

# 🔮 Future Improvements

* PostgreSQL integration
* Cloud deployment
* AI adaptive interviews
* Emotion & confidence detection
* Real-time transcription
* JWT refresh authentication
* Advanced LLM evaluation pipeline

---

# 🌟 Why This Project?

SpeakSmart was designed to simulate realistic interview preparation using AI-powered speech analysis and feedback systems.

The project combines:

* Full Stack Development
* AI Integration
* Audio Processing
* NLP Techniques
* Analytics Dashboards
* SaaS UI Design

into one complete platform.

---

# 👨‍💻 Author

Developed by Prasanna Lakshmi Satti

Aspiring AI/ML Engineer passionate about:

* Generative AI
* Full Stack Development
* Intelligent Systems
* AI-Powered Applications

---

# ⭐ If You Like This Project

Give this repository a star ⭐ on GitHub!
