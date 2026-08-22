#!/usr/bin/env bash
# ==============================================================================
# EdgeVision - NVIDIA Jetson One-Click Deployment & Run Script
# ==============================================================================

set -e

echo "========================================================"
echo "🚀 Initializing EdgeVision PPE Compliance Platform on Jetson"
echo "========================================================"

# 1. Performance Optimization (Max power and lock GPU/CPU clocks)
if command -v nvpmodel &> /dev/null; then
    echo "[1/4] Setting Jetson power mode to MAXN..."
    sudo nvpmodel -m 0 || true
fi

if command -v jetson_clocks &> /dev/null; then
    echo "[2/4] Locking Jetson GPU/CPU clocks for max inference speed..."
    sudo jetson_clocks || true
fi

# 2. Configuration Setup
if [ ! -f .env ]; then
    echo "[3/4] Creating .env from .env.jetson.example..."
    cp .env.jetson.example .env
fi

# 3. Model Engine Verification / Compilation
mkdir -p models
if [ ! -f models/best.engine ]; then
    if [ -f models/best.pt ]; then
        echo "[3/4] Compiling TensorRT FP16 Engine for Jetson hardware..."
        python3 scripts/export_jetson.py --model models/best.pt --imgsz 640 --workspace 4
    else
        echo "[WARNING] models/best.pt not found. Please place your model weights in models/"
    fi
else
    echo "[3/4] Found pre-compiled TensorRT engine at models/best.engine"
fi

# 4. Launch EdgeVision Server
echo "[4/4] Starting EdgeVision Server on port 8000..."
echo "--------------------------------------------------------"
echo "🌐 Access the Dashboard at: http://$(hostname -I | awk '{print $1}'):8000"
echo "--------------------------------------------------------"

python3 app.py
