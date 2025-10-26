# 🧠 AI-Driven Blockchain-Backed Database Security System  

**Developer:** Yaswanth Vemulapalli  
**University:** Monroe University, King Graduate School  
**Course:** CS700 – Special Projects in Computer Science I  
**Instructor:** Dr. Noordeen Kateregga  
**Date:** August 2025  

---

## 📘 Project Overview

This project implements an **AI-Driven Blockchain-Backed Database Security System** that detects database intrusions in real time and creates immutable audit logs using blockchain.  
It integrates **Artificial Intelligence**, **Blockchain**, and **Database Security** into one unified platform with an admin dashboard.

### 🔒 Objectives
- Detect abnormal SQL queries using AI (Isolation Forest / Autoencoders)  
- Hash and store query logs on a blockchain (Hyperledger Fabric)  
- Provide a secure web dashboard for monitoring and alerts  
- Implement MFA, AES encryption, and JWT-based authentication  

---

## ⚙️ Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend** | React.js (Tailwind, Recharts) |
| **Backend** | Flask (Python) |
| **Database** | PostgreSQL + pgAudit |
| **Blockchain** | Hyperledger Fabric / Ganache |
| **AI/ML** | Scikit-learn, TensorFlow |
| **Authentication** | JWT, MFA, AES |
| **Deployment** | Docker & Docker Compose |

---

## 📂 Folder Structure

```
Prototype-Version-2/
│
├── backend/                # Flask REST API
│   ├── app.py
│   ├── models/
│   ├── routes/
│   ├── ai_module/
│   ├── blockchain_module/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/               # React.js Frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
│
├── blockchain_analyzer/    # Blockchain Log Handler
│   ├── main.py
│   └── Dockerfile
│
├── docker-compose.yml
├── AI_Blockchain_Security_System_Checklist.txt
├── Final_Project_Documentation_Yaswanth_Vemulapalli_Submit-08-02.pdf
└── README.md
```

---

## 🚀 Setup & Run

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/VemYaswanth/Prototype-Version-2.git
cd Prototype-Version-2
```

### 2️⃣ Build & Run Using Docker
```bash
docker compose up -d --build
```

### 3️⃣ Access the Application
- **Frontend:** http://localhost:3000  
- **Backend (API):** http://localhost:5000  

---

## 🔐 Key Features

✅ AI-powered anomaly detection  
✅ Blockchain-backed audit trail  
✅ Secure authentication (MFA + JWT + AES)  
✅ Real-time alert dashboard  
✅ Modular architecture with Docker  

---

## 📋 Development Checklist

*(from `AI_Blockchain_Security_System_Checklist.txt`)*

| Module | Highlights |
|--------|-------------|
| AI Module | Train Isolation Forest / Autoencoder for anomaly detection |
| Blockchain | Log cryptographic hashes on Hyperledger Fabric |
| Web App | React dashboard + Flask API |
| Security | MFA, JWT, AES encryption |
| Deployment | Dockerized setup |
| Compliance | GDPR / HIPAA standards |

---

## 🧩 Future Enhancements
- Transformer/LSTM anomaly models  
- SHAP/LIME explainability  
- SIEM integration (Splunk, ELK)  
- Cloud-native deployment via AWS/GCP  

---

## 💻 How to Push Files from Ubuntu to GitHub

### 🔹 **Option 1: Using HTTPS (simpler)**

#### Step 1: Initialize Git
```bash
cd ~/Prototype-Version-2
git init
git add .
git commit -m "Initial commit - AI Blockchain Security System"
```

#### Step 2: Link Remote Repository
```bash
git branch -M main
git remote add origin https://github.com/VemYaswanth/Prototype-Version-2.git
```

#### Step 3: Push to GitHub
```bash
git push -u origin main
```

> 💡 When prompted, use your **GitHub Personal Access Token (PAT)** instead of your password.

---

### 🔹 **Option 2: Using SSH (recommended for long-term use)**

#### Step 1: Generate SSH Key
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

#### Step 2: Copy Public Key
```bash
cat ~/.ssh/id_ed25519.pub
```

#### Step 3: Add SSH Key to GitHub  
- Go to **GitHub → Settings → SSH and GPG keys → New SSH Key**  
- Paste your copied key and click **Add SSH Key**

#### Step 4: Test Connection
```bash
ssh -T git@github.com
```

#### Step 5: Push Code via SSH
```bash
git remote remove origin
git remote add origin git@github.com:VemYaswanth/Prototype-Version-2.git
git add .
git commit -m "Updated project files"
git push -u origin main
```

---

### 🔹 **To Push New Changes**
```bash
git add .
git commit -m "Updated AI module / frontend UI"
git push
```

To pull new updates from GitHub:
```bash
git pull
```

---

## 🧾 License

This project is for **academic and research purposes**.  
All code and documentation © 2025 **Yaswanth Vemulapalli**.
