# 🏗️ Cerberus AI System Architecture

The **Cerberus AI PPE Compliance Platform** is designed as an industrial-grade edge computing architecture. It processes concurrent multi-camera video streams through a 5-stage inference & temporal verification pipeline, serving telemetry to a React control room dashboard via FastAPI WebSockets.

---

## 📐 Architecture Overview

```mermaid
flowchart LR
    A["Camera Inputs<br>(Webcam / RTSP / Video)"] --> B["Threaded Frame Grabber<br>(src/core/detector.py)"]
    B --> C["Stage 1: Person Tracking<br>(ByteTrack ID Persistence)"]
    C --> D["Stage 2: PPE Detection<br>(YOLOv11 Multi-Class)"]
    D --> E["Stage 3: Spatial Association<br>(Body Region & BBox Mapping)"]
    E --> F["Stage 4: Per-Zone Rule Engine<br>(Configurable Safety Rules)"]
    F --> G["Stage 5: Temporal Validator<br>(Noise Suppression & Debounce)"]
    G --> H["Persistence Layer<br>(SQLite + PostgreSQL SQL Engine)"]
    H --> I["API & WebSocket Server<br>(FastAPI Async Core)"]
    I --> J["Executive Dashboard<br>(React + TanStack Start)"]
```

---

## 🧩 Core Pipeline Components

### 1. Threaded Camera Reader (`ThreadedCamera`)
- **Non-blocking Frame Grabber:** Separate daemon threads read camera frames independently into thread-safe buffers (`cap_lock`).
- **Resilience Loop:** Automatic reconnect logic handles dropped RTSP packets, TCP socket timeouts, and HTTP progressive stream resets without halting the main application.

### 2. Multi-Stage Vision Engine (`VisionPipeline` & `PPEDetector`)
- **Stage 1 — Worker Tracking:** Person detection using YOLOv11 combined with ByteTrack tracking to assign persistent tracking IDs (`Worker-101`, `Worker-102`).
- **Stage 2 — Multi-Class PPE Detection:** Detects helmets, safety vests, boots, harness belts, lanyards, and hooks. Incorporates optional CLAHE image enhancement for low-light industrial environments.
- **Stage 3 — Spatial Association:** Maps detected PPE items to the corresponding tracked worker bounding box using head/torso/foot anatomical region containment algorithms.
- **Stage 4 — Per-Zone Rule Engine:** Evaluates compliance against zone-specific required PPE rules (e.g., `work_at_height` requires helmet, vest, boots, harness, and connected hook).
- **Stage 5 — Temporal Noise Suppression:** Requires a violation to persist across $\ge 8$ out of 10 consecutive frames with a minimum 2-second dwell time before triggering an alert.

### 3. Asynchronous Data & Telemetry Engine
- **FastAPI Core (`src/api/server.py`):** Serves RESTful management routes and broadcasts real-time detection telemetry over `WS /ws/live`.
- **SQL Persistence:** High-performance storage using SQLite (WAL mode) for zero-latency local operations with optional PostgreSQL support.
