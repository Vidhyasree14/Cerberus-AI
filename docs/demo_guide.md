# 🎬 Cerberus AI Demonstration & Walkthrough Guide

Step-by-step instructions for launching and demonstrating the **Cerberus AI Platform** live or using recorded video clips.

---

## 1. Quick Launch

Launch the full-stack system using the automated launch script:
```cmd
start_fullstack.bat
```

This starts:
1. **Backend Server:** `http://localhost:8000` (FastAPI REST API & WebSockets).
2. **Control Room Dashboard:** `http://localhost:5173` (React executive dashboard).

---

## 2. Dashboard Tour

Navigate through the control room pages:

1. **Control Room Overview (`/`)** — Live pipeline throughput metrics, system FPS indicator, active violations, and 7-day compliance trend charts.
2. **Live Monitoring (`/live`)** — Multi-camera video wall with real-time bounding box overlays, worker tracking IDs, and focus stream selection.
3. **Incident Triage (`/violations`)** — Real-time violation inbox for reviewing unacknowledged, accepted, or declined safety alerts.
4. **Event History (`/events`)** — Searchable historical log of past breaches with image evidence and video clips.
5. **Worker Compliance (`/compliance`)** — Per-worker safety scorecards, shift history, and compliance metrics.
6. **Zone Rules (`/zones`)** — Per-zone PPE requirement toggles and temporal noise filter thresholds.
7. **Camera Manager (`/cameras`)** — Register, monitor, and configure RTSP feeds and webcam devices.
8. **Telemetry Reports (`/reports`)** — Export daily, weekly, and monthly compliance audit reports.
9. **Model Telemetry (`/model`)** — Real-time inference latency (P95), GPU temperature, and per-class precision/recall stats.

---

## 3. Command Line Inspection

To observe raw frame detection and rule processing directly in terminal:
```bash
python src/core/detector.py 0 work_at_height
```
This launches OpenCV capture on webcam index `0`, showing ByteTrack IDs and rule evaluation output in real time.
