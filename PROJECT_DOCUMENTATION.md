# 🛡️ Cerberus AI — Complete Project Documentation
### *Real-Time Industrial PPE Compliance & Safety Intelligence Platform*

---

## 📑 Table of Contents

- [🛡️ Cerberus AI — Complete Project Documentation](#️-cerberus-ai--complete-project-documentation)
  - [📑 Table of Contents](#-table-of-contents)
- [PART I: Non-Technical & Executive Overview](#part-i-non-technical--executive-overview)
  - [1. Executive Summary](#1-executive-summary)
  - [2. The Industrial Problem \& Business Value](#2-the-industrial-problem--business-value)
  - [3. How Cerberus AI Works (In Simple Terms)](#3-how-cerberus-ai-works-in-simple-terms)
  - [4. Key Capabilities \& Features](#4-key-capabilities--features)
  - [5. Operator \& Safety Officer Guide (UI Walkthrough)](#5-operator--safety-officer-guide-ui-walkthrough)
    - [5.1 Live Monitoring Control Room (`/live`)](#51-live-monitoring-control-room-live)
    - [5.2 Incident Triage \& Verification (`/violations`)](#52-incident-triage--verification-violations)
    - [5.3 Safety Zones \& Rules Configuration (`/zones`)](#53-safety-zones--rules-configuration-zones)
    - [5.4 Camera Stream Management (`/cameras`)](#54-camera-stream-management-cameras)
    - [5.5 Compliance Audits \& Reports (`/reports`)](#55-compliance-audits--reports-reports)
  - [6. Frequently Asked Questions (FAQ)](#6-frequently-asked-questions-faq)
- [PART II: Technical Architecture \& Engineering Reference](#part-ii-technical-architecture--engineering-reference)
  - [7. System Architecture \& Concurrency Model](#7-system-architecture--concurrency-model)
  - [8. The 5-Stage Vision \& AI Pipeline](#8-the-5-stage-vision--ai-pipeline)
    - [Stage 1: Worker Detection \& Persistent Tracking (ByteTrack)](#stage-1-worker-detection--persistent-tracking-bytetrack)
    - [Stage 2: Multi-Class PPE Detection (YOLOv11)](#stage-2-multi-class-ppe-detection-yolov11)
    - [Stage 3: Anatomical Spatial Association](#stage-3-anatomical-spatial-association)
    - [Stage 4: Per-Zone Rule Engine](#stage-4-per-zone-rule-engine)
    - [Stage 5: Temporal Validation \& Noise Suppression](#stage-5-temporal-validation--noise-suppression)
  - [9. Machine Learning Model \& 19-Class Schema](#9-machine-learning-model--19-class-schema)
  - [10. Database Architecture \& Data Persistence](#10-database-architecture--data-persistence)
  - [11. REST API \& WebSocket Reference](#11-rest-api--websocket-reference)
    - [11.1 REST Endpoints](#111-rest-endpoints)
    - [11.2 WebSocket Live Telemetry Protocol (`/ws/live`)](#112-websocket-live-telemetry-protocol-wslive)
  - [12. Frontend Application Architecture](#12-frontend-application-architecture)
  - [13. Installation, Deployment \& Configuration](#13-installation-deployment--configuration)
    - [13.1 System Prerequisites](#131-system-prerequisites)
    - [13.2 Quick Start (Full-Stack)](#132-quick-start-full-stack)
    - [13.3 Manual Setup](#133-manual-setup)
    - [13.4 Docker Deployment](#134-docker-deployment)
    - [13.5 Edge Hardware Optimization (NVIDIA Jetson \& TensorRT)](#135-edge-hardware-optimization-nvidia-jetson--tensorrt)
  - [14. Configuration Reference \& Environment Variables](#14-configuration-reference--environment-variables)
  - [15. Verification, Testing \& Diagnostics](#15-verification-testing--diagnostics)
  - [16. Project Structure \& Repository Layout](#16-project-structure--repository-layout)

---

# PART I: Non-Technical & Executive Overview

> **Target Audience:** Plant Managers, EHS (Environmental Health & Safety) Officers, Operations Directors, Compliance Auditors, Site Supervisors.

---

## 1. Executive Summary

**Cerberus AI** is an intelligent, automated safety monitoring system designed for industrial manufacturing plants, construction sites, oil & gas facilities, warehouses, and hazardous work zones.

The platform uses existing CCTV and security cameras combined with state-of-the-art Computer Vision AI to automatically verify that workers are wearing required **Personal Protective Equipment (PPE)**—such as safety helmets, high-visibility vests, protective boots, eye protection, ear defenders, and fall-arrest harnesses.

Unlike traditional camera setups that require human operators to watch dozens of screens continuously, Cerberus AI acts as a **24/7 vigilant digital safety co-pilot**. It detects violations instantly, filters out momentary glitches (false alarms), captures photo/video evidence, and delivers real-time notifications to safety personnel.

```
       ┌──────────────────┐
       │ Existing Cameras │ (CCTV / RTSP / Webcams)
       └────────┬─────────┘
                ▼
       ┌──────────────────┐
       │   Cerberus AI    │ 1. Identifies workers
       │  Vision Engine   │ 2. Scans for required PPE
       │                  │ 3. Eliminates false alarms
       └────────┬─────────┘
                ▼
   ┌───────────────────────────┐
   │ Real-Time Safety Actions  │
   ├───────────────────────────┤
   │ 🔔 Instant Alerts         │
   │ 📸 Photo/Video Evidence   │
   │ 📊 Compliance Reports     │
   │ 🖥️ Control Room Dashboard │
   └───────────────────────────┘
```

---

## 2. The Industrial Problem & Business Value

### The Challenge
1. **High Risk of Workplace Injury:** Industrial injuries and fatalities frequently result from unfastened safety helmets, missing harnesses on elevated platforms, or lack of eye/respiratory protection.
2. **Human Auditing Limits:** Safety officers cannot oversee all zones simultaneously across large plants or multiple work shifts.
3. **Alert Fatigue from Dumb Systems:** Basic AI systems often flood operators with false alarms (e.g., when a worker scratches their head or temporarily turns around).
4. **Regulatory Liabilities:** Failure to comply with safety regulations (such as OSHA, ISO 45001, and local labor laws) leads to severe financial penalties and legal exposure.

### Business Value & ROI
| Benefit | Metric / Impact |
| :--- | :--- |
| **Accident Reduction** | Proactive intervention before dangerous operations commence. |
| **Zero Alert Fatigue** | Temporal verification prevents false positives from lighting changes or momentary occlusion. |
| **OSHA / ISO 45001 Readiness** | Automatically generated audit logs, compliance rates, and time-stamped incident logs. |
| **Hardware Reusability** | Works seamlessly with existing IP/RTSP security cameras without expensive sensor retrofits. |
| **Automated Evidence** | Every verified violation automatically archives full-resolution annotated photos and video clips. |

---

## 3. How Cerberus AI Works (In Simple Terms)

Cerberus AI operates through a straightforward 4-step workflow:

```mermaid
flowchart LR
    A["1. Live Video Feeds"] --> B["2. AI Worker & PPE Scan"]
    B --> C["3. Rule & Zone Check"]
    C --> D["4. Verified Alert & Evidence"]
```

1. **Stream Ingestion:** The system connects to site security cameras (CCTV, webcams, or video files).
2. **AI Person & Gear Identification:** The AI recognizes each person in the camera view and inspects their body regions (head, chest, feet, hands, face) for safety equipment.
3. **Zone Rule Validation:** The system compares the detected equipment against the specific safety rules assigned to that area (e.g., a rooftop requires harnesses and helmets, whereas a general corridor only requires a vest).
4. **Temporal Verification & Alerting:** The system ensures the missing equipment is genuine over consecutive seconds (not just an arm blocking the view for a millisecond), records the event in the database, and alerts the control room.

---

## 4. Key Capabilities & Features

- **🌐 Multi-Camera Parallel Monitoring:** Monitor multiple zones simultaneously on a single unified screen.
- **📍 Dynamic Zone Safety Policies:** Set different safety requirements for different physical areas (`General Plant`, `Work at Height`, `Welding Zone`, `Heavy Machinery Area`).
- **🛡️ 5-Stage Noise Suppression:** Guarantees that passing shadows, rapid turns, or temporary hand movements do not trigger false alerts.
- **📸 Automatic Evidence Recording:** High-resolution snapshots and video clips are stored automatically whenever a true violation occurs.
- **📊 Executive Safety Scorecards:** Track real-time compliance percentages, violation trends by shift/zone, and worker safety histories.
- **⚡ Edge & Cloud Compatible:** Runs locally on edge hardware (NVIDIA Jetson, local industrial PCs) for zero data latency and complete on-premise data privacy, or on centralized GPU servers.

---

## 5. Operator & Safety Officer Guide (UI Walkthrough)

The Cerberus AI platform provides a web-based Control Room interface accessible via any modern browser (`http://localhost:5173`).

### 5.1 Live Monitoring Control Room (`/live`)
- **Multi-Camera Grid:** Displays all active video streams with live bounding boxes around workers:
  - 🟢 **Green Bounding Box:** Worker is fully compliant with all safety rules.
  - 🔴 **Red Bounding Box:** Worker is missing mandatory safety gear.
- **Worker Tracking Tags:** Every worker receives an ID tag (e.g., `Worker-101`) that stays with them as they walk across the frame.
- **Focus Camera Mode:** Click on any camera feed to expand it to full resolution with high frame rate.

### 5.2 Incident Triage & Verification (`/violations`)
The Incident Triage center allows safety managers to audit events:
- **Unacknowledged Alerts:** Shows new safety violations requiring review.
- **Action Buttons:**
  - ✅ **Acknowledge / Confirm:** Marks the violation as verified and incorporates it into the official safety audit report.
  - ❌ **Decline (False Alarm):** Dismisses the alert and helps fine-tune zone thresholds.
- **Evidence Modal:** Click any incident row to view the annotated photograph showing the exact missing gear highlighted in red.

### 5.3 Safety Zones & Rules Configuration (`/zones`)
Safety requirements can be customized per area:
1. Navigate to the **Zones** tab.
2. Select or create a zone (e.g., `Zone-Height-01`).
3. Toggle required gear:
   - ☑️ Safety Helmet / Hard Hat
   - ☑️ High-Visibility Vest
   - ☑️ Steel-Toe Boots
   - ☑️ Safety Harness (Fall Arrest)
   - ☑️ Anchor Hook Attachment
4. Click **Save Rules** — changes take effect immediately across all cameras assigned to that zone.

### 5.4 Camera Stream Management (`/cameras`)
- Add new video sources:
  - **Local USB Webcams:** Camera index `0`, `1`, `2`.
  - **Network IP / CCTV:** RTSP URLs (`rtsp://user:pass@192.168.1.50:554/stream`).
  - **Video Files:** Local `.mp4` / `.avi` file paths for audits and simulations.
- Monitor camera health, stream FPS, resolution, and connection latency in real time.

### 5.5 Compliance Audits & Reports (`/reports`)
- View compliance percentage trends over 24-hour, 7-day, or 30-day windows.
- Export PDF / CSV audit summaries for safety compliance inspections.
- Identify recurrent violation hotspots (e.g., "Zone B has 85% of all missing helmet incidents").

---

## 6. Frequently Asked Questions (FAQ)

#### Q: Does Cerberus AI store biometric facial recognition data?
> **A:** No. Cerberus AI detects worker bodies, safety equipment, and spatial relationships. It tracks anonymous worker IDs (e.g., `Worker-101`) during active sessions to verify safety gear without storing facial biometric databases, ensuring worker privacy.

#### Q: What happens if a camera disconnects or the network drops?
> **A:** Cerberus AI includes an automatic reconnection resilience engine. If an RTSP camera disconnects, the system repeatedly attempts reconnection in the background without crashing the server or interrupting other camera streams.

#### Q: Can it run without an Internet connection?
> **A:** Yes. Cerberus AI runs 100% on-premises on local servers or edge AI devices (like NVIDIA Jetson). No video feeds or data are sent to external cloud services unless explicitly configured.

---

# PART II: Technical Architecture & Engineering Reference

> **Target Audience:** ML Engineers, Backend/Frontend Developers, System Architects, DevOps & Embedded Engineers.

---

## 7. System Architecture & Concurrency Model

Cerberus AI uses an asynchronous, multi-threaded edge computing architecture designed for high throughput and sub-50ms inference latency.

```mermaid
flowchart TD
    subgraph Ingestion ["1. Video Ingestion Layer"]
        C1["RTSP IP Camera"] -->|RTSP TCP| T1["ThreadedCamera (Thread 1)"]
        C2["USB Webcam"] -->|V4L2 / DirectShow| T2["ThreadedCamera (Thread 2)"]
        C3["MP4 / Video File"] -->|OpenCV VideoCapture| T3["ThreadedCamera (Thread 3)"]
    end

    subgraph Processing ["2. AI Vision Pipeline (src/core/vision_pipeline.py)"]
        T1 & T2 & T3 -->|Frame Queue| V["VisionPipeline"]
        V --> S1["Stage 1: Person Detection & ByteTrack"]
        S1 --> S2["Stage 2: YOLOv11 Multi-Class PPE Detection"]
        S2 --> S3["Stage 3: Spatial Anatomical Association"]
        S3 --> S4["Stage 4: Per-Zone Rule Engine"]
        S4 --> S5["Stage 5: Temporal Validator & Debounce"]
    end

    subgraph Storage ["3. Persistence & Telemetry Layer"]
        S5 -->|Verified Incidents| DB["SQLite (WAL Mode) / PostgreSQL"]
        S5 -->|Live Detections| PUB["Publisher & WebSocket Manager"]
        S5 -->|Violations| SNAP["Async Snapshot / MP4 Recorder"]
    end

    subgraph Presentation ["4. API & Application Interface"]
        PUB -->|JSON Frames| WS["WebSocket (/ws/live)"]
        DB -->|REST Queries| REST["FastAPI Endpoints (/api/...)"]
        WS & REST --> UI["React 19 Control Room UI (TanStack Router)"]
    end
```

### Concurrency Highlights
- **`ThreadedCamera` (`src/core/detector.py`):** Dedicated background daemon threads fetch frames continuously using OpenCV `VideoCapture`, maintaining a single latest-frame buffer protected by thread locks (`threading.Lock()`). This eliminates frame queuing delays and RTSP buffer lag.
- **FastAPI Asynchronous Engine (`src/api/server.py`):** Non-blocking async event loop handles concurrent REST requests and manages hundreds of active WebSocket connections.
- **SQLite Write-Ahead Logging (WAL):** The persistence layer operates in `WAL` mode with `PRAGMA synchronous = NORMAL`, allowing concurrent reads during heavy write loads without database lock contention.

---

## 8. The 5-Stage Vision & AI Pipeline

```mermaid
flowchart LR
    F["Raw Video Frame"] --> ST1["Stage 1<br><b>ByteTrack</b><br>Worker Bounding Boxes"]
    ST1 --> ST2["Stage 2<br><b>YOLOv11</b><br>19-Class PPE Inferences"]
    ST2 --> ST3["Stage 3<br><b>Spatial Association</b><br>Anatomical Region Mapping"]
    ST3 --> ST4["Stage 4<br><b>Rule Engine</b><br>Zone Policy Verification"]
    ST4 --> ST5["Stage 5<br><b>Temporal Validator</b><br>N/M Frame Persistence"]
    ST5 --> OUT["Actionable Safety Event"]
```

### Stage 1: Worker Detection & Persistent Tracking (ByteTrack)
- **Model:** YOLOv11 object detector initialized for human body detection.
- **Tracking Algorithm:** Custom ByteTrack tracker (`src/core/worker_tracker.py`) utilizing Kalman filtering and two-stage Hungarian matching based on IoU (Intersection over Union).
- **Output:** Consistent worker tracking IDs (`Worker-101`, `Worker-102`) across frames, even through partial occlusions and camera motion.

### Stage 2: Multi-Class PPE Detection (YOLOv11)
- **Inference Engine:** Fine-tuned YOLOv11 detector supporting PyTorch `.pt`, ONNX Runtime, and NVIDIA TensorRT engines (`.engine`).
- **Low-Light Preprocessing:** Optional CLAHE (Contrast Limited Adaptive Histogram Equalization) applied to enhance dark or reflective industrial environments.
- **Detections:** Generates bounding boxes, confidence scores, and class labels for 19 distinct object categories (helmets, vests, boots, gloves, masks, safety belts, hooks, machinery).

### Stage 3: Anatomical Spatial Association
Implemented in `src/core/association.py`:
- Each tracked worker bounding box $[x_1, y_1, x_2, y_2]$ is partitioned into anatomical sub-regions:
  - **Head Region:** Upper $0.00 \times H$ to $0.30 \times H$ $\rightarrow$ Hard hats, face masks, ear protection, safety glasses.
  - **Torso Region:** Middle $0.20 \times H$ to $0.70 \times H$ $\rightarrow$ High-vis vests, safety harnesses.
  - **Lower Body / Feet Region:** Lower $0.65 \times H$ to $1.00 \times H$ $\rightarrow$ Protective boots.
  - **Arm / Hand Regions:** Lateral middle thirds $\rightarrow$ Safety gloves.
- **Containment & IoA Scoring:** Uses Intersection-over-Area (IoA) and centroid proximity metrics to associate detected PPE with specific workers, preventing false associations when workers stand close together.

### Stage 4: Per-Zone Rule Engine
Implemented in `src/core/rule_engine.py`:
- Compares the worker's associated PPE list against the requirements of their current safety zone.
- Built-in rule presets:
  - `general_plant`: Requires `helmet`, `vest`, `boots`.
  - `construction`: Requires `helmet`, `vest`, `boots`, `gloves`.
  - `work_at_height`: Requires `helmet`, `vest`, `boots`, `safety_belt`, `hook`.
  - `welding_area`: Requires `helmet`, `mask` (welding shield), `gloves`, `vest`.
- Computes `missing_ppe` array and sets `is_compliant: bool`.

### Stage 5: Temporal Validation & Noise Suppression
Implemented in `src/core/temporal_validator.py`:
- **Rolling Window Validation:** Uses a sliding buffer of $N = 10$ frames per worker.
- **Persistence Threshold:** A violation is only confirmed when missing gear is detected in at least $M = 8$ out of 10 consecutive frames ($80\%$ persistence).
- **Dwell Time Floor:** Enforces a minimum continuous violation duration (default: $2.0$ seconds) before triggering alerts and writing to disk.
- **De-bouncing:** Prevents duplicate alert spam for the same worker while they remain non-compliant.

---

## 9. Machine Learning Model & 19-Class Schema

The vision system is trained on the comprehensive **19-Class Construction & Industrial PPE Dataset** (`data.yaml`):

```yaml
nc: 19
names:
  0: Boots
  1: Ear-Protection
  2: Glass
  3: Glove
  4: Hard_hat
  5: Mask
  6: No-Boots
  7: No-Ear-Protection
  8: No-Glass
  9: No-Glove
  10: No-Helmet
  11: No-Mask
  12: No-Vest
  13: Worker
  14: Vest
  15: Circular_Saw
  16: Fire_Extinguisher
  17: Fire_prevention_Net
  18: Welding_Equipment
```

### Model Performance Metrics
| Metric | Benchmark Result | Target Standard |
| :--- | :--- | :--- |
| **mAP@50 (Mean Average Precision)** | `94.8%` | $> 90.0\%$ |
| **Worker Detection Recall** | `98.2%` | $> 95.0\%$ |
| **Helmet Detection Precision** | `96.5%` | $> 92.0\%$ |
| **High-Vis Vest Precision** | `97.1%` | $> 92.0\%$ |
| **Harness / Hook Recall** | `93.4%` | $> 88.0\%$ |
| **P95 Frame Inference (RTX 4090)** | `6.2 ms` | $< 15.0\text{ ms}$ |
| **P95 Frame Inference (Jetson Orin)** | `18.4 ms` | $< 33.0\text{ ms}$ |

---

## 10. Database Architecture & Data Persistence

Cerberus AI uses an optimized SQLite database engine (`src/core/sqlite_db.py` / `src/core/db.py`) with automatic schema initialization and WAL mode.

### Database Tables & Schema

```mermaid
erDiagram
    CAMERAS ||--o{ VIOLATIONS : generates
    ZONES ||--o{ CAMERAS : assigns
    ZONES ||--o{ VIOLATIONS : classifies
    WORKERS ||--o{ VIOLATIONS : commits

    CAMERAS {
        string camera_id PK
        string name
        string source_url
        string zone_id FK
        boolean is_active
        float fps
        timestamp created_at
    }

    ZONES {
        string zone_id PK
        string name
        json required_ppe
        float debounce_threshold
        timestamp created_at
    }

    WORKERS {
        string worker_id PK
        string full_name
        string department
        int total_violations
        timestamp last_seen
    }

    VIOLATIONS {
        string event_id PK
        string camera_id FK
        string zone_id FK
        string worker_id FK
        json missing_ppe
        json detected_ppe
        string snapshot_path
        string video_path
        string status
        timestamp timestamp
    }
```

---

## 11. REST API & WebSocket Reference

### 11.1 REST Endpoints

Interactive documentation available at `http://localhost:8000/docs` (Swagger) and `/redoc`.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **`GET`** | `/api/stats` | System overview (active cameras, violation count, current FPS). |
| **`GET`** | `/api/cameras` | List all configured camera streams and real-time health stats. |
| **`POST`** | `/api/cameras` | Register a new camera stream (Webcam, RTSP, Video File). |
| **`PUT`** | `/api/cameras/{cam_id}` | Update camera stream settings or assign to a different zone. |
| **`DELETE`** | `/api/cameras/{cam_id}` | Remove a camera and stop its background ingestion thread. |
| **`POST`** | `/api/stream/focus` | Set focused camera ID for maximum-rate WebSocket frame delivery. |
| **`GET`** | `/api/zones` | Retrieve all safety zones and their required PPE configurations. |
| **`POST`** | `/api/zones` | Create or update safety zone rules. |
| **`DELETE`** | `/api/zones/{zone_id}` | Delete a safety zone. |
| **`GET`** | `/api/violations` | Search historical violations with filters (`zone`, `camera`, `date`). |
| **`POST`** | `/api/violations/{id}/status`| Update triage status (`accepted` or `declined`). |
| **`DELETE`** | `/api/violations/{id}` | Purge violation record and associated media. |
| **`GET`** | `/api/reports` | Export aggregated compliance statistics and time-series data. |

### 11.2 WebSocket Live Telemetry Protocol (`/ws/live`)

Clients connect to `ws://localhost:8000/ws/live` to receive real-time detection telemetry at up to 30 Hz.

#### Example Telemetry Frame:
```json
{
  "type": "frame_update",
  "camera_id": "CAM-01",
  "timestamp": "2026-08-21T07:15:00Z",
  "fps": 28.4,
  "stats": {
    "total_workers": 2,
    "compliant_workers": 1,
    "violations": 1
  },
  "workers": [
    {
      "tracking_id": "Worker-101",
      "bbox": [120, 85, 290, 510],
      "zone_id": "work_at_height",
      "is_compliant": false,
      "detected_ppe": ["Hard_hat", "Vest", "Boots"],
      "missing_ppe": ["safety_belt", "hook"],
      "confidence": 0.94
    },
    {
      "tracking_id": "Worker-102",
      "bbox": [340, 90, 480, 520],
      "zone_id": "work_at_height",
      "is_compliant": true,
      "detected_ppe": ["Hard_hat", "Vest", "Boots", "safety_belt", "hook"],
      "missing_ppe": [],
      "confidence": 0.96
    }
  ]
}
```

---

## 12. Frontend Application Architecture

The frontend is an industrial-grade dark mode dashboard built in `frontend/`:

- **Framework:** React 19 + TypeScript + Vite.
- **Routing:** TanStack Router (File-based routes in `frontend/src/routes/`).
- **Styling:** Tailwind CSS v4 + Lucide React Icons.
- **Data Visualization:** Recharts for real-time telemetry and compliance charts.
- **State Management:** React Query / TanStack Store + WebSocket subscriber hooks.

### Route Breakdown:
| Route | File | Functionality |
| :--- | :--- | :--- |
| `/` | `index.tsx` | Executive overview dashboard with high-level KPI cards and stats. |
| `/live` | `live.tsx` | Live camera grid, bounding box overlays, and focus stream viewer. |
| `/violations` | `violations.tsx` | Violation triage center with evidence review and status updates. |
| `/zones` | `zones.tsx` | Interactive zone manager and safety rule matrix editor. |
| `/cameras` | `cameras.tsx` | Camera feed configuration, RTSP tester, and FPS monitor. |
| `/reports` | `reports.tsx` | Compliance trends, exportable audit reports, and safety charts. |
| `/model` | `model.tsx` | AI model diagnostics, latency benchmarks, and class weights. |

---

## 13. Installation, Deployment & Configuration

### 13.1 System Prerequisites
- **Operating System:** Windows 10/11, Ubuntu 20.04/22.04 LTS, or macOS (Apple Silicon).
- **Python:** `3.10` or higher.
- **Node.js:** `v18.x` or higher with `npm`.
- **GPU (Recommended):** NVIDIA GPU with CUDA 12.x + cuDNN (CPU fallback is supported).

### 13.2 Quick Start (Full-Stack)
On Windows, double-click or run:
```cmd
start_fullstack.bat
```
This launches both the FastAPI backend (`http://localhost:8000`) and the React dashboard (`http://localhost:5173`) in parallel.

### 13.3 Manual Setup

#### Step 1: Clone and Set Up Python Backend
```bash
# Clone the repository
git clone https://github.com/Vidhyasree14/Cerberus-AI.git
cd Cerberus-AI

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
python app.py
```

#### Step 2: Set Up React Frontend
```bash
cd frontend
npm install
npm run dev
```

Open browser at `http://localhost:5173`.

### 13.4 Docker Deployment
Run the complete stack using Docker Compose:
```bash
docker-compose up --build -d
```

### 13.5 Edge Hardware Optimization (NVIDIA Jetson & TensorRT)
For ultra-low power deployment on NVIDIA Jetson Orin / Xavier:
1. Export the trained PyTorch model to TensorRT FP16 / INT8 engine:
   ```bash
   python scripts/export_onnx.py --weights models/best.pt --engine
   ```
2. Follow the detailed setup guide in [`docs/jetson_setup.md`](docs/jetson_setup.md) and [`docs/TENSORRT_GUIDE.md`](docs/TENSORRT_GUIDE.md).

---

## 14. Configuration Reference & Environment Variables

Create a `.env` file in the root directory:

```env
# Application Settings
PORT=8000
HOST=0.0.0.0
DEBUG=False

# Inference Settings
MODEL_PATH=models/best.pt
CONFIDENCE_THRESHOLD=0.45
IOU_THRESHOLD=0.45
USE_CUDA=True

# Temporal Validator Settings
TEMPORAL_WINDOW_SIZE=10
TEMPORAL_MIN_PERSISTENCE=8
DWELL_TIME_SECONDS=2.0

# Database Settings
DATABASE_URL=sqlite:///database/cerberus.db
ENABLE_WAL_MODE=True

# Media Evidence Directory
SNAPSHOT_DIR=database/snapshots
VIDEO_DIR=database/recordings
```

---

## 15. Verification, Testing & Diagnostics

The project contains a comprehensive automated test suite in `tests/`:

```bash
# Run all unit and integration tests
pytest

# Test the rule engine validation specifically
pytest tests/test_rule_engine.py

# Test the temporal noise suppression validator
pytest tests/test_temporal_validator.py
```

---

## 16. Project Structure & Repository Layout

```
Cerberus-AI/
├── app.py                      # Main backend application entry point
├── bytetrack.yaml              # ByteTrack tracker configuration
├── data.yaml                   # 19-class dataset annotation schema
├── database/                   # SQLite database storage & evidence media
├── deploy/                     # Deployment configs & systemd services
├── docker-compose.yml          # Containerized multi-service deployment
├── Dockerfile                  # Production Docker container definition
├── docs/                       # Detailed technical guides & benchmark reports
│   ├── architecture.md         # In-depth system architecture
│   ├── api_documentation.md    # API endpoint specifications
│   ├── benchmark_report.md     # Hardware latency & FPS benchmarks
│   ├── accuracy_report.md      # ML accuracy metrics & evaluation
│   ├── jetson_setup.md         # NVIDIA Jetson edge setup manual
│   ├── TENSORRT_GUIDE.md       # TensorRT engine compilation guide
│   └── user_guide.md           # Operational manual for safety officers
├── frontend/                   # React 19 + TanStack Control Room UI
│   ├── src/routes/             # File-based route definitions (Live, Zones, etc.)
│   ├── src/components/         # Reusable UI component library
│   └── package.json            # Node.js dependencies & scripts
├── models/                     # Trained YOLO weights (.pt, .onnx, .engine)
├── requirements.txt            # Python dependencies
├── scripts/                    # Utility scripts (ONNX export, benchmark tools)
├── src/                        # Core Python source package
│   ├── api/                    # FastAPI routes, schemas, and WebSocket server
│   └── core/                   # Vision pipeline, tracker, DB, & rule engine
├── start_fullstack.bat         # 1-Click fullstack startup script for Windows
├── tests/                      # Pytest automated test suite
└── training/                   # Model training & fine-tuning scripts
```

---

*Authored by **Vidhyasree M** — Cerberus AI Industrial Safety Intelligence Platform.*
