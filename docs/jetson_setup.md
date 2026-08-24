# 🚀 NVIDIA Jetson Deployment Guide

Guide for deploying **Cerberus AI** on NVIDIA Jetson Orin / AGX Xavier devices running JetPack 6.x.

---

## 📋 System Requirements

| Component | Minimum Specification | Recommended |
| :--- | :--- | :--- |
| **Target Hardware** | NVIDIA Jetson Orin Nano (8GB) | NVIDIA Jetson AGX Orin |
| **OS / JetPack** | JetPack 6.0 (L4T R36) | JetPack 6.1+ |
| **CUDA / TensorRT** | CUDA 12.2 / TensorRT 10.x | CUDA 12.2+ / TensorRT 10.x |
| **Python** | Python 3.10 | Python 3.10 |

---

## 🛠️ Step-by-Step Installation

### Step 1: Install System Dependencies
```bash
sudo apt update
sudo apt install -y git
```

### Step 2: Download the Repository
```bash
git clone https://github.com/Vidhyasree14/Cerberus-AI.git
cd ~/Cerberus-AI
```

### Step 3: Install Dependencies with the Jetson Script
Install JetPack-compatible Torch, TorchVision, and TensorRT before running the script. It installs the system packages, Python requirements, Node.js 22, and frontend packages, then verifies the hardware stack.

```bash
chmod +x deploy/jetson/install.sh
./deploy/jetson/install.sh
```

### Step 4: Build TensorRT Engine on Jetson
Build the device-optimized TensorRT engine directly on the Jetson device:
```bash
python3 scripts/export_tensorrt.py --model models/best.pt --imgsz 640 --device 0
```
This compiles `models/best.engine`.

### Step 5: Configure Systemd Service
Copy the service configuration file to run EdgeVision automatically on boot:
```bash
sudo cp scripts/edgevision.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable edgevision
sudo systemctl start edgevision
```

Verify service status:
```bash
sudo systemctl status edgevision
```

### Step 6: Power & Performance Optimization
Lock Jetson clocks for maximum throughput:
```bash
sudo nvpmodel -m 0      # Max power mode (MAXN)
sudo jetson_clocks      # Lock CPU/GPU frequencies
```

---

## 📷 Linux & Jetson Camera Verification (Webcam / USB / CSI)

### 1. Check Video Device Nodes
```bash
ls -l /dev/video*
```
Make sure your user account has access to the video devices:
```bash
sudo usermod -aG video $USER
```

### 2. Verify with `v4l-utils`
```bash
sudo apt install -y v4l-utils
v4l2-ctl --list-devices
```

### 3. Supported Camera Formats
- **USB Webcams**: Source index `0`, `1`, or `/dev/video0` (uses V4L2 backend).
- **Jetson CSI Ribbon Cameras**: GStreamer pipeline string, e.g.:
  ```
  nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=30/1 ! nvvidconv ! video/x-raw, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink
  ```
- **RTSP IP Streams**: `rtsp://<ip>:<port>/stream`

