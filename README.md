# 🛡️ AI-Driven Blockchain-Backed Database Security System

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Backend-black?logo=flask)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)](https://react.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)](https://www.docker.com/)
[![Blockchain](https://img.shields.io/badge/Blockchain-Hyperledger%20Fabric-brightgreen?logo=hyperledger)](https://www.hyperledger.org/use/fabric)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📖 Overview

An **AI + Blockchain-powered Database Security System** that detects, alerts, and logs **suspicious SQL operations in real-time** while ensuring **tamper-proof auditability** via blockchain integration.

This prototype demonstrates a **multi-layered defense system** combining:
- AI-driven anomaly detection
- Blockchain-backed audit trails
- Real-time alert monitoring via a secure dashboard (Flask + React)

---

## 🧩 System Architecture

![Architecture Diagram](https://github.com/VemYaswanth/Prototype-Version-2/assets/architecture-diagram-placeholder.png)

**Core Components:**
1. **Frontend:** React.js dashboard for administrators and auditors  
2. **Backend:** Flask REST API (AI inference, alerts, and blockchain commits)  
3. **Database:** PostgreSQL with `pgAudit` for SQL traffic capture  
4. **Blockchain Layer:** Hyperledger Fabric / Ethereum (Ganache for dev)  
5. **AI Engine:** Isolation Forest / Autoencoder models for anomaly detection  
6. **Dockerized Deployment:** For reproducibility and isolation  

---

## 🚀 Features

| Module | Description |
|--------|--------------|
| **AI Anomaly Detection** | Learns query patterns and flags outliers in real-time |
| **Blockchain Audit Logging** | Creates an immutable audit trail of all flagged operations |
| **Role-Based Dashboard** | Admin, Auditor, and Viewer panels |
| **Multi-Factor Authentication (MFA)** | Protects access with extra authentication layer |
| **Secure APIs** | Encrypted JWT + HTTPS/TLS |
| **Visual Analytics** | Charts for alert frequency and model confidence |
| **Cloud Ready** | Deployable on AWS EC2, Azure, or GCP |

---

## 🧠 AI Detection Module

- Detects anomalies in SQL logs using **Isolation Forest / Autoencoder**
- Trains on past query logs to recognize normal vs. abnormal operations
- **Outputs:**  
  - `is_anomalous (True/False)`  
  - `anomaly_score (0–1)`  
  - `confidence (%)`
- Inference speed: **<2 seconds per query**
- Auto-retraining supported through feedback loop

---

## ⛓️ Blockchain Audit Layer

- Uses **SHA-256** to hash each log entry
- Records immutable transactions in Hyperledger Fabric
- Enables verifiable audit trails for compliance (GDPR, HIPAA)
- Asynchronous blockchain commits for low-latency performance

---

## 🗄️ Database Schema (Simplified)

| Table | Description |
|--------|--------------|
| `users` | Stores user credentials, MFA, and roles |
| `query_logs` | SQL operations with metadata (IP, timestamp, session) |
| `anomalies` | AI-detected anomalies with scores |
| `alerts` | Open/Resolved alerts with confidence values |
| `blockchain_logs` | Blockchain hashes of verified queries |
| `model_config` | AI model parameters and tuning history |

---

## 🖥️ Dashboard Overview

![UI Mockup](https://github.com/VemYaswanth/Prototype-Version-2/assets/dashboard-ui-placeholder.png)

**Pages:**
- 🔐 **Login** — MFA-secured access  
- 📊 **Dashboard** — Central hub showing all security metrics  
- 🚨 **Alerts View** — Displays anomalies with SQL context and severity  
- 🔗 **Blockchain Validation** — Verifies tamper-proof status  
- ⚙️ **System Settings** — Configure AI and blockchain integrations  

**Visualizations:**
- 📈 **Alert Frequency (weekly trend)**  
- 🧮 **Model Confidence Distribution**

---

## 🛡️ Security Architecture

| Layer | Mechanism |
|--------|------------|
| **Authentication** | MFA + JWT tokens |
| **Access Control** | Role-Based Access (RBAC) |
| **Data Encryption** | AES-256 for stored fields |
| **Transport Security** | HTTPS + TLS |
| **Privacy Compliance** | GDPR / HIPAA-ready design |
| **Blockchain Integrity** | Immutable SHA-256 hash chains |

---

## 🧰 Technology Stack

| Category | Tools |
|-----------|-------|
| **Frontend** | React.js, TailwindCSS, Recharts |
| **Backend** | Flask, Gunicorn, SQLAlchemy |
| **Database** | PostgreSQL + pgAudit |
| **Blockchain** | Hyperledger Fabric / Ganache |
| **AI/ML** | Scikit-learn, TensorFlow, PyCaret |
| **DevOps** | Docker, GitHub Actions, AWS EC2 |
| **Monitoring** | Grafana, ELK Stack |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/VemYaswanth/Prototype-Version-2.git
cd Prototype-Version-2

2️⃣ Build and Run Docker Containers

docker-compose up --build

3️⃣ Verify Database Initialization

docker exec -it postgres_db psql -U postgres -d securitydb -c "\dt"

4️⃣ Access the Frontend Dashboard

👉 http://localhost:3000


---

🧾 Development Checklist

Refer to AI_Blockchain_Security_System_Checklist.txt for:

✅ AI module and model setup

✅ Blockchain transaction logging

✅ Authentication and RBAC

✅ CI/CD and deployment configuration

✅ Monitoring and compliance checks



---

🧱 Folder Structure

Prototype-Version-2/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── models/
│   │   ├── utils/
│   │   └── __init__.py
│   ├── init_db.py
│   ├── run.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── docker-compose.yml
├── AI_Blockchain_Security_System_Checklist.txt
├── Final_Project_Documentation_Yaswanth_Vemulapalli_Submit-08-02.pdf
└── README.md


---

🔮 Future Enhancements

🔁 Transformer / LSTM anomaly detection

🧩 Explainability with SHAP / LIME

📡 SIEM integration (Splunk, Elastic)

⚡ Horizontal AI model scaling

📊 Real-time observability (Grafana / Kibana)

🌐 Multi-tenant, enterprise-ready deployment



---

📘 Documentation

📄 Final_Project_Documentation_Yaswanth_Vemulapalli_Submit-08-02.pdf

Includes:

DFDs (Context, Level 0, Level 1)

ER & Network Diagrams

Security Measures

Use Case and UI Screens

Risk Assessment & Future Recommendations



---

👨‍💻 Author

Yaswanth Vemulapalli
🎓 Master of Science – Computer Science, Monroe University
📧 yaswanthvemulapalli@gmail.com
🌐 GitHub: VemYaswanth


---

🪪 License

This project is licensed under the MIT License – see the LICENSE file for details.


---

> "Bridging AI intelligence with blockchain immutability to redefine data security."



---

### 🔧 Notes for You:
1. Replace the two image placeholders:
   - `assets/architecture-diagram-placeholder.png`
   - `assets/dashboard-ui-placeholder.png`
   with real screenshots from your project or from your documentation PDF.

2. You can create a `/assets` folder in your repo and upload images using GitHub’s “Upload files” feature.

3. If you want, I can also generate **those diagrams automatically** (architecture + dashboard visuals) from your documentation for a clean GitHub look.

Would you like me to **generate both diagrams** (architecture + dashboard) so you can upload them to your repo?Perfect 👍 Here’s the enhanced and GitHub-optimized README.md — with badges, visuals, professional structure, and clarity for recruiters, professors, and collaborators.
You can paste this directly into your repository root as README.md.


---

# 🛡️ AI-Driven Blockchain-Backed Database Security System

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Backend-black?logo=flask)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)](https://react.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)](https://www.docker.com/)
[![Blockchain](https://img.shields.io/badge/Blockchain-Hyperledger%20Fabric-brightgreen?logo=hyperledger)](https://www.hyperledger.org/use/fabric)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📖 Overview

An **AI + Blockchain-powered Database Security System** that detects, alerts, and logs **suspicious SQL operations in real-time** while ensuring **tamper-proof auditability** via blockchain integration.

This prototype demonstrates a **multi-layered defense system** combining:
- AI-driven anomaly detection
- Blockchain-backed audit trails
- Real-time alert monitoring via a secure dashboard (Flask + React)

---

## 🧩 System Architecture

![Architecture Diagram](https://github.com/VemYaswanth/Prototype-Version-2/assets/architecture-diagram-placeholder.png)

**Core Components:**
1. **Frontend:** React.js dashboard for administrators and auditors  
2. **Backend:** Flask REST API (AI inference, alerts, and blockchain commits)  
3. **Database:** PostgreSQL with `pgAudit` for SQL traffic capture  
4. **Blockchain Layer:** Hyperledger Fabric / Ethereum (Ganache for dev)  
5. **AI Engine:** Isolation Forest / Autoencoder models for anomaly detection  
6. **Dockerized Deployment:** For reproducibility and isolation  

---

## 🚀 Features

| Module | Description |
|--------|--------------|
| **AI Anomaly Detection** | Learns query patterns and flags outliers in real-time |
| **Blockchain Audit Logging** | Creates an immutable audit trail of all flagged operations |
| **Role-Based Dashboard** | Admin, Auditor, and Viewer panels |
| **Multi-Factor Authentication (MFA)** | Protects access with extra authentication layer |
| **Secure APIs** | Encrypted JWT + HTTPS/TLS |
| **Visual Analytics** | Charts for alert frequency and model confidence |
| **Cloud Ready** | Deployable on AWS EC2, Azure, or GCP |

---

## 🧠 AI Detection Module

- Detects anomalies in SQL logs using **Isolation Forest / Autoencoder**
- Trains on past query logs to recognize normal vs. abnormal operations
- **Outputs:**  
  - `is_anomalous (True/False)`  
  - `anomaly_score (0–1)`  
  - `confidence (%)`
- Inference speed: **<2 seconds per query**
- Auto-retraining supported through feedback loop

---

## ⛓️ Blockchain Audit Layer

- Uses **SHA-256** to hash each log entry
- Records immutable transactions in Hyperledger Fabric
- Enables verifiable audit trails for compliance (GDPR, HIPAA)
- Asynchronous blockchain commits for low-latency performance

---

## 🗄️ Database Schema (Simplified)

| Table | Description |
|--------|--------------|
| `users` | Stores user credentials, MFA, and roles |
| `query_logs` | SQL operations with metadata (IP, timestamp, session) |
| `anomalies` | AI-detected anomalies with scores |
| `alerts` | Open/Resolved alerts with confidence values |
| `blockchain_logs` | Blockchain hashes of verified queries |
| `model_config` | AI model parameters and tuning history |

---

## 🖥️ Dashboard Overview

![UI Mockup](https://github.com/VemYaswanth/Prototype-Version-2/assets/dashboard-ui-placeholder.png)

**Pages:**
- 🔐 **Login** — MFA-secured access  
- 📊 **Dashboard** — Central hub showing all security metrics  
- 🚨 **Alerts View** — Displays anomalies with SQL context and severity  
- 🔗 **Blockchain Validation** — Verifies tamper-proof status  
- ⚙️ **System Settings** — Configure AI and blockchain integrations  

**Visualizations:**
- 📈 **Alert Frequency (weekly trend)**  
- 🧮 **Model Confidence Distribution**

---

## 🛡️ Security Architecture

| Layer | Mechanism |
|--------|------------|
| **Authentication** | MFA + JWT tokens |
| **Access Control** | Role-Based Access (RBAC) |
| **Data Encryption** | AES-256 for stored fields |
| **Transport Security** | HTTPS + TLS |
| **Privacy Compliance** | GDPR / HIPAA-ready design |
| **Blockchain Integrity** | Immutable SHA-256 hash chains |

---

## 🧰 Technology Stack

| Category | Tools |
|-----------|-------|
| **Frontend** | React.js, TailwindCSS, Recharts |
| **Backend** | Flask, Gunicorn, SQLAlchemy |
| **Database** | PostgreSQL + pgAudit |
| **Blockchain** | Hyperledger Fabric / Ganache |
| **AI/ML** | Scikit-learn, TensorFlow, PyCaret |
| **DevOps** | Docker, GitHub Actions, AWS EC2 |
| **Monitoring** | Grafana, ELK Stack |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/VemYaswanth/Prototype-Version-2.git
cd Prototype-Version-2

2️⃣ Build and Run Docker Containers

docker-compose up --build

3️⃣ Verify Database Initialization

docker exec -it postgres_db psql -U postgres -d securitydb -c "\dt"

4️⃣ Access the Frontend Dashboard

👉 http://localhost:3000


---

🧾 Development Checklist

Refer to AI_Blockchain_Security_System_Checklist.txt for:

✅ AI module and model setup

✅ Blockchain transaction logging

✅ Authentication and RBAC

✅ CI/CD and deployment configuration

✅ Monitoring and compliance checks



---

🧱 Folder Structure

Prototype-Version-2/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── models/
│   │   ├── utils/
│   │   └── __init__.py
│   ├── init_db.py
│   ├── run.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── docker-compose.yml
├── AI_Blockchain_Security_System_Checklist.txt
├── Final_Project_Documentation_Yaswanth_Vemulapalli_Submit-08-02.pdf
└── README.md


---

🔮 Future Enhancements

🔁 Transformer / LSTM anomaly detection

🧩 Explainability with SHAP / LIME

📡 SIEM integration (Splunk, Elastic)

⚡ Horizontal AI model scaling

📊 Real-time observability (Grafana / Kibana)

🌐 Multi-tenant, enterprise-ready deployment



---

📘 Documentation

📄 Final_Project_Documentation_Yaswanth_Vemulapalli_Submit-08-02.pdf

Includes:

DFDs (Context, Level 0, Level 1)

ER & Network Diagrams

Security Measures

Use Case and UI Screens

Risk Assessment & Future Recommendations



---

👨‍💻 Author

Yaswanth Vemulapalli
🎓 Master of Science – Computer Science, Monroe University
📧 yaswanthvemulapalli@gmail.com
🌐 GitHub: VemYaswanth


---

🪪 License

This project is licensed under the MIT License – see the LICENSE file for details.


---

> "Bridging AI intelligence with blockchain immutability to redefine data security."



---

### 🔧 Notes for You:
1. Replace the two image placeholders:
   - `assets/architecture-diagram-placeholder.png`
   - `assets/dashboard-ui-placeholder.png`
   with real screenshots from your project or from your documentation PDF.

2. You can create a `/assets` folder in your repo and upload images using GitHub’s “Upload files” feature.

3. If you want, I can also generate **those diagrams automatically** (architecture + dashboard visuals) from your documentation for a clean GitHub look.

Would you like me to **generate both diagrams** (architecture + dashboard) so you can upload them to your repo?Perfect 👍 Here’s the enhanced and GitHub-optimized README.md — with badges, visuals, professional structure, and clarity for recruiters, professors, and collaborators.
You can paste this directly into your repository root as README.md.


---

# 🛡️ AI-Driven Blockchain-Backed Database Security System

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Backend-black?logo=flask)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)](https://react.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)](https://www.docker.com/)
[![Blockchain](https://img.shields.io/badge/Blockchain-Hyperledger%20Fabric-brightgreen?logo=hyperledger)](https://www.hyperledger.org/use/fabric)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📖 Overview

An **AI + Blockchain-powered Database Security System** that detects, alerts, and logs **suspicious SQL operations in real-time** while ensuring **tamper-proof auditability** via blockchain integration.

This prototype demonstrates a **multi-layered defense system** combining:
- AI-driven anomaly detection
- Blockchain-backed audit trails
- Real-time alert monitoring via a secure dashboard (Flask + React)

---

## 🧩 System Architecture

![Architecture Diagram](https://github.com/VemYaswanth/Prototype-Version-2/assets/architecture-diagram-placeholder.png)

**Core Components:**
1. **Frontend:** React.js dashboard for administrators and auditors  
2. **Backend:** Flask REST API (AI inference, alerts, and blockchain commits)  
3. **Database:** PostgreSQL with `pgAudit` for SQL traffic capture  
4. **Blockchain Layer:** Hyperledger Fabric / Ethereum (Ganache for dev)  
5. **AI Engine:** Isolation Forest / Autoencoder models for anomaly detection  
6. **Dockerized Deployment:** For reproducibility and isolation  

---

## 🚀 Features

| Module | Description |
|--------|--------------|
| **AI Anomaly Detection** | Learns query patterns and flags outliers in real-time |
| **Blockchain Audit Logging** | Creates an immutable audit trail of all flagged operations |
| **Role-Based Dashboard** | Admin, Auditor, and Viewer panels |
| **Multi-Factor Authentication (MFA)** | Protects access with extra authentication layer |
| **Secure APIs** | Encrypted JWT + HTTPS/TLS |
| **Visual Analytics** | Charts for alert frequency and model confidence |
| **Cloud Ready** | Deployable on AWS EC2, Azure, or GCP |

---

## 🧠 AI Detection Module

- Detects anomalies in SQL logs using **Isolation Forest / Autoencoder**
- Trains on past query logs to recognize normal vs. abnormal operations
- **Outputs:**  
  - `is_anomalous (True/False)`  
  - `anomaly_score (0–1)`  
  - `confidence (%)`
- Inference speed: **<2 seconds per query**
- Auto-retraining supported through feedback loop

---

## ⛓️ Blockchain Audit Layer

- Uses **SHA-256** to hash each log entry
- Records immutable transactions in Hyperledger Fabric
- Enables verifiable audit trails for compliance (GDPR, HIPAA)
- Asynchronous blockchain commits for low-latency performance

---

## 🗄️ Database Schema (Simplified)

| Table | Description |
|--------|--------------|
| `users` | Stores user credentials, MFA, and roles |
| `query_logs` | SQL operations with metadata (IP, timestamp, session) |
| `anomalies` | AI-detected anomalies with scores |
| `alerts` | Open/Resolved alerts with confidence values |
| `blockchain_logs` | Blockchain hashes of verified queries |
| `model_config` | AI model parameters and tuning history |

---

## 🖥️ Dashboard Overview

![UI Mockup](https://github.com/VemYaswanth/Prototype-Version-2/assets/dashboard-ui-placeholder.png)

**Pages:**
- 🔐 **Login** — MFA-secured access  
- 📊 **Dashboard** — Central hub showing all security metrics  
- 🚨 **Alerts View** — Displays anomalies with SQL context and severity  
- 🔗 **Blockchain Validation** — Verifies tamper-proof status  
- ⚙️ **System Settings** — Configure AI and blockchain integrations  

**Visualizations:**
- 📈 **Alert Frequency (weekly trend)**  
- 🧮 **Model Confidence Distribution**

---

## 🛡️ Security Architecture

| Layer | Mechanism |
|--------|------------|
| **Authentication** | MFA + JWT tokens |
| **Access Control** | Role-Based Access (RBAC) |
| **Data Encryption** | AES-256 for stored fields |
| **Transport Security** | HTTPS + TLS |
| **Privacy Compliance** | GDPR / HIPAA-ready design |
| **Blockchain Integrity** | Immutable SHA-256 hash chains |

---

## 🧰 Technology Stack

| Category | Tools |
|-----------|-------|
| **Frontend** | React.js, TailwindCSS, Recharts |
| **Backend** | Flask, Gunicorn, SQLAlchemy |
| **Database** | PostgreSQL + pgAudit |
| **Blockchain** | Hyperledger Fabric / Ganache |
| **AI/ML** | Scikit-learn, TensorFlow, PyCaret |
| **DevOps** | Docker, GitHub Actions, AWS EC2 |
| **Monitoring** | Grafana, ELK Stack |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/VemYaswanth/Prototype-Version-2.git
cd Prototype-Version-2

2️⃣ Build and Run Docker Containers

docker-compose up --build

3️⃣ Verify Database Initialization

docker exec -it postgres_db psql -U postgres -d securitydb -c "\dt"

4️⃣ Access the Frontend Dashboard

👉 http://localhost:3000


---

🧾 Development Checklist

Refer to AI_Blockchain_Security_System_Checklist.txt for:

✅ AI module and model setup

✅ Blockchain transaction logging

✅ Authentication and RBAC

✅ CI/CD and deployment configuration

✅ Monitoring and compliance checks



---

🧱 Folder Structure

Prototype-Version-2/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── models/
│   │   ├── utils/
│   │   └── __init__.py
│   ├── init_db.py
│   ├── run.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── docker-compose.yml
├── AI_Blockchain_Security_System_Checklist.txt
├── Final_Project_Documentation_Yaswanth_Vemulapalli_Submit-08-02.pdf
└── README.md


---

🔮 Future Enhancements

🔁 Transformer / LSTM anomaly detection

🧩 Explainability with SHAP / LIME

📡 SIEM integration (Splunk, Elastic)

⚡ Horizontal AI model scaling

📊 Real-time observability (Grafana / Kibana)

🌐 Multi-tenant, enterprise-ready deployment



---

📘 Documentation

📄 Final_Project_Documentation_Yaswanth_Vemulapalli_Submit-08-02.pdf

Includes:

DFDs (Context, Level 0, Level 1)

ER & Network Diagrams

Security Measures

Use Case and UI Screens

Risk Assessment & Future Recommendations



---

👨‍💻 Author

Yaswanth Vemulapalli
🎓 Master of Science – Computer Science, Monroe University
📧 yaswanthvemulapalli@gmail.com
🌐 GitHub: VemYaswanth


---

🪪 License

This project is licensed under the MIT License – see the LICENSE file for details.


---

> "Bridging AI intelligence with blockchain immutability to redefine data security."



---

### 🔧 Notes for You:
1. Replace the two image placeholders:
   - `assets/architecture-diagram-placeholder.png`
   - `assets/dashboard-ui-placeholder.png`
   with real screenshots from your project or from your documentation PDF.

2. You can create a `/assets` folder in your repo and upload images using GitHub’s “Upload files” feature.

3. If you want, I can also generate **those diagrams automatically** (architecture + dashboard visuals) from your documentation for a clean GitHub look.

Would you like me to **generate both diagrams** (architecture + dashboard) so you can upload them to your repo?
