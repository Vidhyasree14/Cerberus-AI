# 📖 Cerberus AI Operational User Guide

Welcome to the **Cerberus AI Platform** operational manual for safety officers and control room operators.

---

## 🖥️ Dashboard Navigation

### 1. Live Control Room (`/live`)
- **Multi-Camera Grid:** Displays active camera streams with bounding boxes and worker tracking tags (`Worker-101`).
- **Focus Stream Mode:** Click any stream thumbnail or use `/api/stream/focus` to focus rendering on a single camera at full frame rate.

### 2. Incident Verification & Triage (`/violations`)
- Review alerts under **Unacknowledged**, **Accepted**, or **Declined** tabs.
- **Confirm Incident:** Marks the violation as verified for executive reporting and telemetry.
- **Decline (False Alarm):** Removes false alerts from active tracking.

### 3. Event Search & History (`/events`)
- Search historical safety violations filtered by **Zone**, **Camera**, **Worker ID**, or **Date Range**.
- Preview full-resolution JPEG evidence snapshots and recorded MP4 clips.

### 4. Zone Rules Configuration (`/zones`)
- Select any safety zone (`work_at_height`, `construction`, `general_plant`) to configure required PPE items:
  - `helmet` (Hard Hat)
  - `vest` (High-Vis Vest)
  - `boots` (Safety Boots)
  - `safety_belt` (Safety Harness)
  - `hook` (Anchor Hook)
- Adjust temporal debounce thresholds ($\ge 8/10$ frame validation window).

### 5. Camera Management (`/cameras`)
- Add local USB webcams (`0`, `1`), RTSP network feeds, or progressive video URLs.
- Monitor active FPS, processing latency, and connection status.
