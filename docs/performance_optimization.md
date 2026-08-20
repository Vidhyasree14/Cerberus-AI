# ⚡ Cerberus AI — Performance & Multi-Camera Optimization Report

## Executive Summary

This report documents the architectural optimizations implemented in **Cerberus AI** to resolve multi-camera streaming bottlenecks, eliminate GPU/I/O starvation, and achieve stable real-time inference across diverse hardware configurations.

---

## 📊 Benchmark Comparison

Performance measured on Windows 10, Python 3.10, PyTorch 2.5.1+cu121 (CUDA), Ultralytics YOLOv11, OpenCV 5.0, 8 CPU Cores.

### Per-Camera Frame Rate (Smoothness Metric)

| Camera Count | Legacy Pipeline (Fixed 640px, Shared Executor) | Optimized Pipeline (Adaptive Scaling + Isolated I/O) | Performance Gain |
| :---: | :---: | :---: | :---: |
| **1 Stream** | 24.3 FPS | **24.6 FPS** | Baseline (No overhead) |
| **2 Streams** | 13.9 FPS | **24.5 FPS** | **1.8× Increase** |
| **4 Streams** | 6.8 FPS | **19.0 FPS** | **2.8× Increase** |
| **8 Streams** | 3.3 FPS | **10.5 FPS** | **3.2× Increase** |

> **Aggregate Throughput:** Total system throughput scaled from ~27 FPS (saturated at 640px) to **84 FPS** across 8 concurrent streams due to dynamic resolution scaling (`640px` → `416px` → `320px` → `256px`).

---

## 🔍 Root Cause Analysis & Technical Solves

### 1. I/O & Model Inference Contention
* **Problem:** GPU model inference (`pipeline.process_frame`) shared the default thread executor with disk I/O, image compression, base64 encoding, and database operations. Slow disk or DB writes directly blocked model inference.
* **Fix:** Introduced isolated thread pools in `src/core/runtime.py`:
  - `get_infer_executor()` dedicated strictly to model processing.
  - `get_io_executor()` dedicated strictly to async disk, database, and snapshot generation.

### 2. Static Inference Resolution
* **Problem:** High resolution (`640px`) caused GPU saturation when scaling beyond 2 streams.
* **Fix:** Implemented an adaptive inference ladder in `src/core/runtime.py` (`recompute_adaptive()`). The engine automatically adjusts inference dimensions based on active camera count:
  - 1 Camera: `640px`
  - 2 Cameras: `416px`
  - 3–4 Cameras: `320px`
  - 5+ Cameras: `256px`

### 3. WebSocket Bandwidth & Client CPU Saturation
* **Problem:** Broadcasting full base64 JPEG frames for every camera to all connected browsers overloaded low-end client CPUs with 120+ JPEG decodes per second.
* **Fix:** Created a focused camera model (`POST /api/stream/focus`). The focused view receives full frame rate, while non-focused grid thumbnails are capped at ~15 FPS via `GRID_STREAM_INTERVAL`.

### 4. MQTT Client Compatibility Update
* **Problem:** Paho MQTT v1 client setup caused warnings and connection drops under Paho MQTT 2.x.
* **Fix:** Updated `src/core/publisher.py` to use `CallbackAPIVersion.VERSION2` with backwards fallback support.

---

## ⚙️ Configuration & Hardware Profiles

The system supports environmental overrides via standard environment variables:

| Environment Variable | Default Value | Description |
| :--- | :--- | :--- |
| `GRID_STREAM_INTERVAL` | `0.066` (~15 FPS) | Minimum interval (in seconds) between grid card frame broadcasts. |
| `MAX_INFER_WORKERS` | `0` (Auto) | Explicit cap for inference thread executor workers. |
| `PERFORMANCE_PROFILE` | `auto` | Set to `high_end` (forces 640px base) or `low_end` (forces 480px base + frame skipping). |

---

## 🧪 Verification & Test Suite

- **Unit & Integration Tests:** Passed `49/49` PyTest test cases without regressions.
- **Benchmark Scripts:**
  - `python scripts/real_bench.py` — Evaluates single vs multi-camera FPS.
  - `python scripts/multicam_bench.py` — Simulates N-camera workload throughput.
