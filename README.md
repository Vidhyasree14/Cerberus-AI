# 🛡️ Cerberus AI — Real-Time Industrial PPE Compliance & Safety Intelligence Platform

[![GitHub](https://img.shields.io/badge/GitHub-Vidhyasree14%2FCerberus--AI-181717?style=flat&logo=github)](https://github.com/Vidhyasree14/Cerberus-AI)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat&logo=python)](https://www.python.org)
[![YOLOv11](https://img.shields.io/badge/Detection-YOLOv11-00FFFF.svg?style=flat)](https://ultralytics.com)
[![React](https://img.shields.io/badge/React%2019-61DAFB.svg?style=flat&logo=react)](https://react.dev)
[![SQLite](https://img.shields.io/badge/SQLite-WAL--Mode-003B57.svg?style=flat&logo=sqlite)](https://www.sqlite.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Cerberus AI** is an industrial computer-vision platform engineered for real-time Personal Protective Equipment (PPE) compliance monitoring and safety verification across plant floors, construction zones, work-at-height platforms, and hazardous environments.

Featuring a 5-stage inference & temporal validation pipeline, persistent worker tracking (ByteTrack), dynamic per-zone safety rules, and low-latency WebSocket streaming, **Cerberus AI** guarantees high precision without false alarms caused by noisy individual frames.

- **Project Owner & Creator:** Vidhyasree M
- **Official Repository:** [https://github.com/Vidhyasree14/Cerberus-AI](https://github.com/Vidhyasree14/Cerberus-AI)

---

## 📚 Technical Documentation Sitemap

Explore the comprehensive master documentation and specialized subsystem guides:

- 📖 **[Master Project Documentation (Complete Technical & Non-Technical Guide)](PROJECT_DOCUMENTATION.md)**

| Guide / Report | Focus Area | Description |
| :--- | :--- | :--- |
| 📖 [Complete Master Documentation](PROJECT_DOCUMENTATION.md) | Full Platform | Complete non-technical executive overview + deep technical engineering spec |
| 🏗️ [Architecture Documentation](docs/architecture.md) | System Design | 5-stage vision pipeline, data flow, & concurrency model |
| ⚡ [Performance & Multi-Cam Optimization](docs/performance_optimization.md) | Optimization | I/O thread isolation, dynamic resolution scaling, & benchmarks |
| 📡 [API Documentation](docs/api_documentation.md) | Integration | Full RESTful API endpoints & WebSocket payload specs |
| 📊 [Hardware Benchmark Report](docs/benchmark_report.md) | Benchmarks | Throughput, P95 latency, & thermal stats (Jetson / x86) |
| 🎯 [Accuracy Evaluation Report](docs/accuracy_report.md) | ML Metrics | 19-class precision, recall, mAP50, & environmental test stats |
| 🚀 [NVIDIA Jetson Setup Guide](docs/jetson_setup.md) | Deployment | JetPack 6.x installation, systemd service, & power modes |
| 🧰 [Jetson SSH Quick Deployment](deploy/jetson/README.md) | Deployment | Copy-paste SSH commands for installation and launch |
| ⚡ [TensorRT Acceleration Guide](docs/TENSORRT_GUIDE.md) | Edge Acceleration | FP16 & INT8 engine compilation & DeepStream setup |
| 🏷️ [Dataset & Labelling Guide](docs/dataset_guide.md) | Training Data | 19-class schema, augmentation, & YOLOv8 layout |
| 🎬 [Demonstration & Walkthrough](docs/demo_guide.md) | Live Demo | Step-by-step control room dashboard & terminal guide |
| 📖 [Operational User Guide](docs/user_guide.md) | User Operations | Operator manual for live triage, zone setup, & reports |
| 🖥️ [Frontend Dashboard Guide](frontend/README.md) | Web UI | React 19 + TanStack file-based routing frontend guide |
| 🎯 [Model Training Guide](training/README.md) | AI Model | Fine-tuning YOLOv11 on local GPU, Kaggle, or Colab |

---

## 🌟 Key Platform Features

- **⚡ Multi-Stream Parallel Vision Engine:** Reads and processes multiple camera feeds concurrently (Webcam, RTSP/TCP, HTTP progressives, local MP4 files, and YouTube Live streams).
- **🎯 Per-Zone Rule Engine:** Custom rules per zone (`general_plant`, `construction`, `work_at_height`). Require helmets, vests, boots, safety harnesses, and anchor hooks per zone.
- **🧠 5-Stage Compliance Pipeline:** Person tracking (ByteTrack) $\rightarrow$ Multi-class PPE detection $\rightarrow$ Spatial association $\rightarrow$ Rule evaluation $\rightarrow$ Temporal noise suppression.
- **⏳ Temporal Noise Suppression:** Mandates violation persistence across $\ge 8$ out of 10 consecutive frames with a 2-second dwell floor to prevent single-frame false alerts.
- **💾 High-Performance SQL Persistence:** SQLite database engine with Write-Ahead Logging (WAL) for zero-latency local operations and optional PostgreSQL integration.
- **📸 Automated Evidence Capture:** Saves annotated JPEG snapshots and short MP4 video clips asynchronously without blocking the live inference thread.
- **💻 Industrial Control Room UI:** Dark-mode dashboard built in React 19, TanStack Start/Router, Tailwind CSS v4, and Recharts, fed by live WebSockets.

---

## 🏗️ System Architecture Overview

```mermaid
flowchart LR
    A["Camera Feeds<br>(RTSP / Webcams)"] --> B["Threaded Grabber<br>(src/core/detector.py)"]
    B --> C["5-Stage Vision Engine<br>(src/core/vision_pipeline.py)"]
    C --> D["FastAPI Backend<br>(src/api/server.py)"]
    D --> E["SQLite / SQL Engine<br>(src/core/db.py)"]
    D --> F["WebSocket Telemetry<br>(/ws/live)"]
    F --> G["React Control Room UI<br>(frontend/)"]
```

---

## 🚀 Quick Start

### 1. Prerequisites
- **Python:** `3.10` or higher
- **Node.js:** `v22+` & `npm`
- **GPU (Optional):** NVIDIA GPU with CUDA 12.x for accelerated inference (CPU fallback included).

### 2. Fullstack One-Click Launch (Windows)
Run the bundled startup script:
```cmd
start_fullstack.bat
```
This automatically starts:
- **FastAPI Backend:** `http://localhost:8000` (API & WebSockets)
- **React Control Room:** `http://localhost:5173`

### 3. Fullstack Launch over Jetson SSH
The Windows batch file is not used on Jetson. Run these commands from the beginning:

```bash
ssh <username>@<jetson-ip>
sudo apt update
sudo apt install -y git
git clone https://github.com/Vidhyasree14/Cerberus-AI.git
cd ~/Cerberus-AI

# These must be installed from NVIDIA/JetPack for the device's JetPack version.
python3 -c "import torch; print(torch.cuda.is_available())"
python3 -c "import torchvision, tensorrt; print('Jetson AI packages OK')"

chmod +x deploy/jetson/install.sh
./deploy/jetson/install.sh
```

The installer installs the remaining system and Python packages, Node.js 22, frontend packages, ONNX dependencies, and the device-specific `models/best.engine` file.

Start the backend in SSH terminal 1:

```bash
cd ~/Cerberus-AI
python3 -m src.api.server
```

Open a second SSH terminal and start the React dashboard:

```bash
ssh <username>@<jetson-ip>
cd ~/Cerberus-AI/frontend
npm run dev
```

Open `http://<jetson-ip>:5173` in a browser from another computer on the same private network. For Jetson-specific dependency installation and TensorRT setup, see [NVIDIA Jetson Setup Guide](docs/jetson_setup.md).

### 4. Remote Access from Another System
For access from a different computer, the safest option is an SSH tunnel. Run this command on the computer that will display the dashboard while the backend and frontend remain running on the Jetson:

```bash
ssh -L 5173:127.0.0.1:5173 -L 8000:127.0.0.1:8000 <username>@<jetson-ip>
```

Then open the dashboard locally at:

```text
http://localhost:5173
```

If the other computer is on a different network, connect the systems through a VPN such as Tailscale or WireGuard first. Do not expose ports `5173` or `8000` directly to the public internet.

### 5. Manual Server Launch (CLI)

#### Backend Server
```bash
# Install dependencies
pip install -r requirements.txt

# Start entry point server
python app.py
```

#### Frontend Dashboard
```bash
cd frontend
npm install
npm run dev
```

---

## 🧪 Testing & Verification Suite

Run pytest to execute the complete test suite covering rule engine validation, worker tracking, temporal suppression, and database fallback:

```bash
pytest
```

To run a specific module test:
```bash
pytest tests/test_rule_engine.py
```

---

## 📜 License & Copyright
 
Released under the **MIT License** — see [LICENSE](LICENSE).  
Copyright (c) 2026 **Vidhyasree M**. Built for enterprise workplace safety monitoring in compliance with OSHA and ISO 45001 safety guidelines.
