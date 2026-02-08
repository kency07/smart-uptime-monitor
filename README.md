# smart-uptime-monitor
A lightweight yet professional website availability monitoring tool built with Python. It uses a **fast HTTP check first** and automatically falls back to a **real browser check (Playwright)** only when results are suspicious - reducing false positives while staying resource-efficient. 

---
## Table of Contents

- [Overview](#-overview)
- [Why This Project Matters](#-why-this-project-matters)
- [Features](#-features)
- [Architecture & Flow](#-architecture--flow)
- [Project Structure](#project-structure)
- [Installation & Setup](#-installation--setup)
- [Configuration](#️-configuration)
- [Running the Project](#️-running-the-project)
- [Email Alerts](#-email-alerts-optional)
- [Logging & Error Handling](#-logging---error-handling)
- [Status Tracking Strategy](#-status-tracking-strategy)
- [Use Cases](#-use-cases)
- [Design Philosophy](#-design-philosophy)
- [Limitations](#️-limitations-honest--professional)
- [Future Improvements](#-future-improvements)
- [Tech Stack](#-tech-stack)
- [License](#️-license)

---
## 📦 Overview

Traditional uptime monitors often mark sites **DOWN** due to temporary network issues, bot protection, or rate‑limiting. This project solves that by:

 1. Performing a **quick HTTP check** using `requests`
 2. Escalating to **Playwright browser verification** only when needed
 3. Confirming real downtime before sending alerts

This makes the monitor **accurate, explainable, and client‑ready**.

---

## 🧠 Why This Project Matters

- Demonstrates **real‑world monitoring logic**, not toy scripts
- Shows understanding of **false positives & verification layers**
- Suitable for **freelancing, SaaS demos, and portfolio projects**

---

## ✨ Features

- HTTP-first availability checks
- Automatic browser fallback using Playwright
- Retry logic for transient failures
- Status persistence to prevent alert spam
- Optional email notifications
- Structured logging
- Clean, modular architecture

---
## 🧩 Architecture & Flow

```
URL
│
▼
HTTP Check (requests)
│
├─ Status < 400 → UP (exit)
│
└─ Status ≥ 400 / Timeout
│
▼
Browser Check (Playwright)
│
├─ Page loads → UP
└─ Fails → DOWN (alert) 
```
---
## Project Structure
```
smart-uptime-monitor/
│
├── monitor/
│ ├── http_check.py      # Fast HTTP availability check
│ ├── browser_check.py   # Playwright verification
│ ├── state_manager.py   # Status persistence & change detection
│ ├── notifier.py        # Email alert handling
│ └── utils.py           # Shared helpers
│
├── data/
│ ├── state.json         # Stores the previous site status and time of check.
│ ├── config.json        # Runtime config (sites, interval)
│ └── alert.log          # Alert history
│
├── logging_config.py    # Central logging setup
├── main.py              # Entry point & orchestration
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```
---
## 🛠 Installation & Setup

### Clone the repository

Clone or download the project, then navigate into the folder:
```bash
git clone https://github.com/kency07/smart-uptime-monitor.git

cd smart-uptime-monitor
```
### Create and activate a virtual environment

```bash 
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```
### Requirements

- Python 3.10+
- Internet connection

### Install dependencies
```bash 
pip install -r requirements.txt
```
**Your requirements.txt should include**:
```
playwright>=1.40.0
python-dotenv>=1.0.0
```
---
## ⚙️ Configuration
### `data/config.json`
Runtime configuration file (sites, interval):
```
{"interval_second": 60,
"sites" : [
 "https://example.com",
 "https://google.com"
 ]
}

```
---
## 📧 Email Alerts (Optional)

Email notifications are disabled by default.

Enable Email Alerts

Create a .env file:
```
EMAIL_ENABLED=true
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_TO=receiver_email@gmail.com
EMAIL_INTERVAL_SECONDS=900
```
- Alerts trigger **only when status changes** (UP → DOWN or vice versa)
- Prevents repeated spam during prolonged outages
- SMTP-based (Gmail, Outlook, etc.)

⚠️ Never commit your `.env` file. It is intentionally excluded via `.gitignore`.

---
## ▶️ Running the Project
⚠️ Ensure Playwright browsers are installed:
```bash 
playwright install 
```
Start monitoring
```bash 
python main.py
```
Stop safely with:
Press <kbd>Ctrl</kbd> + <kbd>C</kbd>

The monitor will:

- Check all configured sites
- Verify failures using a browser
- Send alerts only on confirmed status changes
---
## 🧪 Logging & 🛡 Error Handling
Console output (real-time)

File logs: data/alerts.log
```
Example log:
[2026-02-07T21:57:18Z] INFO: you are online, now program will proceed
[2026-02-07T21:57:18Z] INFO: Uptime monitor started
[2026-02-07T21:57:18Z] INFO: [2026-02-07 21:57:18.049568+00:00] checking https://example.com
[2026-02-07T21:57:18Z] INFO: first time seeing this site https://example.com (UP)
[2026-02-07T21:57:18Z] INFO: [2026-02-07 21:57:18.447392+00:00] checking https://google.com
[2026-02-07T21:57:19Z] INFO: first time seeing this site https://google.com (UP)

[2026-02-07T21:57:34Z] INFO: [2026-02-07 21:57:34.239527+00:00] checking https://example.com
[2026-02-07T21:57:34Z] INFO: No status change for https://example.com (UP)
[2026-02-07T21:57:34Z] INFO: [2026-02-07 21:57:34.466809+00:00] checking https://google.com
[2026-02-07T21:57:35Z] INFO: No status change for https://google.com (UP)
[2026-02-07T21:57:41Z] INFO: Monitor stopped by user
```
- Centralized logging via `logging_config.py`
- Network errors, retries, and browser failures are logged
- Alert history stored in `data/alert.log`

Handled gracefully without stopping monitoring:
 - Missing or corrupted state.json
 - Network connectivity issues
 - Email credential issues

---
## 🔄 Status Tracking Strategy

Each site stores:

 - Last known status
 - Last check timestamp
 - Last status change time

This ensures:

 - No duplicate alerts
 - Clear history of uptime changes

---
## 📌 Use Cases

- Personal website monitoring
- Freelance client uptime checks
- Portfolio demonstration of monitoring systems
- Learning real‑world Python automation

---

## 🧠 Design Philosophy

- Verify before alarming
- Fast path first, resource-heavy tools last
- Readable > clever
- Production-style structure even for small tools

---
## ⚠️ Limitations (Honest & Professional)

- Not a replacement for enterprise tools like Pingdom
- Playwright is resource-heavy (used only on failure)
- Email alerts may require SMTP configuration

## 🔮 Future Improvements

- Async checks/concurrent checks
- Telegram / Slack alerts
- Dashboard (Flask)
- Docker support

---
## 🛠 Tech Stack
| Tool | Purpose |
|-----|--------|
| **Python** | Core application logic |
| **Playwright** | Check JavaScript-rendered pages |
| **Logging** | Traceability, error tracking, and execution history |
| **JSON** | Persistent site & status storage  |
| **Environment Variables** | Secure configuration (email credentials) |
---
## ⚖️ License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
## Contact

Maintainer: @kency07 (GitHub)
Project: Smart Uptime Monitor

---
