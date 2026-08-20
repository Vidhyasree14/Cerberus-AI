# 🖥️ Cerberus AI Frontend — Executive Dashboard

The **Cerberus AI Control Room Frontend** is a modern, high-performance web dashboard built for real-time safety monitoring, incident triage, zone rule configuration, and analytics.

---

## 🛠️ Technology Stack

- **Framework:** React 19 + [TanStack Start](https://tanstack.com/start) / Router (File-based routing)
- **Styling:** Tailwind CSS v4 + Industrial Dark Theme Design System
- **Icons & Visuals:** Lucide React icons, Lucide SVG badges, custom hazard-stripe UI motifs
- **Data Visualization:** Recharts (Compliance trends, latency stats, violation breakdowns)
- **Data Fetching & State:** React Hooks + Real-time WebSocket Client (`WS /ws/live`)

---

## 📁 Directory Structure

```
frontend/
├── public/                 # Static assets, icons, and logos
├── src/
│   ├── components/        # Reusable UI components (Cards, Tables, Modals, Badges)
│   ├── hooks/             # Custom React hooks (WebSocket client, camera stream hook)
│   ├── lib/               # Utility functions, API helpers, formatters
│   ├── routes/            # TanStack file-based routes
│   │   ├── __root.tsx     # App shell & layout wrapper
│   │   ├── index.tsx      # Dashboard Overview (/)
│   │   ├── live.tsx       # Multi-camera live view (/live)
│   │   ├── violations.tsx # Incident triage & review (/violations)
│   │   ├── events.tsx     # Historical violation log (/events)
│   │   ├── compliance.tsx # Worker compliance tracking (/compliance)
│   │   ├── zones.tsx      # Zone rules & PPE assignment (/zones)
│   │   ├── cameras.tsx    # Camera manager & RTSP config (/cameras)
│   │   ├── reports.tsx    # Safety telemetry reports (/reports)
│   │   └── model.tsx      # AI model telemetry & FPS monitor (/model)
│   └── main.tsx           # React root entry point
├── package.json           # Frontend dependencies & build scripts
└── vite.config.ts         # Vite build & proxy configuration
```

---

## 🚀 Quick Start (Local Development)

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Launch Development Server
```bash
npm run dev
```
The application will open locally at `http://localhost:5173`.

### 3. Build for Production
```bash
npm run build
```

---

## 📡 Backend Integration & WebSockets

- **API Proxy:** Requests to `/api/*` are automatically proxied to the FastAPI backend running on `http://localhost:8000`.
- **WebSocket Feed:** The dashboard connects to `ws://localhost:8000/ws/live` to receive low-latency frame bounding boxes, active worker tracking telemetry, and instant violation alerts.