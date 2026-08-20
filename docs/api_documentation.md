# 📡 Cerberus AI REST & WebSocket API Reference

The **Cerberus AI API** provides high-throughput management endpoints and low-latency WebSocket telemetry streams.

---

## 🚀 Live API Documentation

When the Cerberus AI backend server is running, live interactive documentation is accessible at:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## 📌 REST API Endpoint Summary

### 1. Safety Zones (`/api/zones`)
- `GET /api/zones` — List all registered safety zones and required PPE rules.
- `POST /api/zones` — Create or update a safety zone configuration.
- `DELETE /api/zones/{zone_id}` — Delete a safety zone.

### 2. Camera Management (`/api/cameras`)
- `GET /api/cameras` — Retrieve registered camera streams with real-time FPS and latency metrics.
- `POST /api/cameras` — Register a new camera stream (Webcam, RTSP, HTTP, or YouTube URL).
- `PUT /api/cameras/{cam_id}` — Update camera parameters.
- `DELETE /api/cameras/{cam_id}` — Remove a camera and terminate its background processing loop.
- `POST /api/stream/focus` — Set active focus camera for high-FPS WebSocket delivery.

### 3. Safety Violations & Evidence (`/api/violations`)
- `GET /api/violations` — Query violation records (supports filtering by camera, zone, worker, and date range).
- `POST /api/violations/{evt_id}/status` — Update violation state (`accepted` or `declined`).
- `DELETE /api/violations/{evt_id}` — Purge a specific violation evidence record.

### 4. Telemetry & Analytics (`/api/stats`, `/api/reports`)
- `GET /api/stats` — System overview metrics (active cameras, total violations, system FPS).
- `GET /api/reports` — Aggregated safety compliance telemetry (daily/weekly/monthly breakdowns).

---

## ⚡ WebSocket Telemetry (`WS /ws/live`)

The WebSocket endpoint streams live JSON frames containing worker tracking telemetry, bounding boxes, and compliance state:

```json
{
  "type": "frame_update",
  "camera_id": "CAM-01",
  "timestamp": "2026-08-18T09:50:00Z",
  "fps": 24.5,
  "workers": [
    {
      "tracking_id": "Worker-101",
      "bbox": [120, 80, 240, 480],
      "zone_id": "work_at_height",
      "detected_ppe": ["helmet", "vest", "boots"],
      "missing_ppe": ["safety_belt", "hook"],
      "is_compliant": false
    }
  ]
}
```
