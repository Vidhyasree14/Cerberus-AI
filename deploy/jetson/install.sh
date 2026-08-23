#!/usr/bin/env bash
# Author: Vidhyasree M
# Cerberus AI NVIDIA Jetson Automated Installation Script

set -Eeuo pipefail

trap 'echo "[ERROR] Setup failed at line $LINENO: $BASH_COMMAND" >&2' ERR

ok() {
    echo "[OK] $1"
}

echo "=== Cerberus AI Jetson Installation ==="

# 1. Update APT Package Index
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev python3-opencv build-essential libopencv-dev libopenblas-dev ffmpeg git curl
ok "System packages installed"

# 2. Confirm JetPack hardware packages before installing Ultralytics.
if ! python3 -c "import torch; assert torch.cuda.is_available()"; then
    echo "ERROR: Install JetPack-compatible NVIDIA torch with CUDA before running this script."
    exit 1
fi
ok "Torch CUDA is available"
if ! python3 -c "import torchvision, tensorrt"; then
    echo "ERROR: Install JetPack-compatible torchvision and TensorRT before running this script."
    exit 1
fi
ok "TorchVision and TensorRT are available"

# 3. Upgrade pip
python3 -m pip install --upgrade pip setuptools wheel
ok "pip tools updated"

# 4. Install Python packages. Jetson Torch/TorchVision must be installed from
# the NVIDIA wheel matching the device's JetPack version before this step.
# requirements.txt skips pip OpenCV on Jetson ARM64; apt provides it above.
python3 -m pip install -r requirements.txt
python3 -m pip check
ok "Python dependencies installed and checked"

# 5. Configure the Jetson model path explicitly.
if [ ! -f .env ]; then
    cp .env.jetson.example .env
fi
if grep -q '^MODEL_PATH=' .env; then
    sed -i 's|^MODEL_PATH=.*|MODEL_PATH=models/best.engine|' .env
else
    printf '\nMODEL_PATH=models/best.engine\n' >> .env
fi
ok "Jetson environment configured to use models/best.engine"

# 6. Install Node.js 22 with nvm for the current user
export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
if [ ! -s "$NVM_DIR/nvm.sh" ]; then
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
fi
source "$NVM_DIR/nvm.sh"
nvm install 22
nvm alias default 22
node_version="$(node --version)"
npm_version="$(npm --version)"
echo "Node.js: $node_version"
echo "npm: $npm_version"
ok "Node.js and npm installed"

# 7. Install frontend packages
cd frontend
npm install
cd ..
ok "Frontend dependencies installed"

# 8. Build a device-specific TensorRT engine from the repository model.
if [ ! -f models/best.pt ]; then
    echo "ERROR: models/best.pt was not found in the cloned repository."
    exit 1
fi
if [ ! -f models/best.engine ]; then
    python3 scripts/export_tensorrt.py --model models/best.pt --imgsz 640 --device 0
fi
if [ ! -f models/best.engine ]; then
    echo "ERROR: TensorRT engine export did not create models/best.engine."
    exit 1
fi
ok "TensorRT engine available at models/best.engine"

echo "Verifying Jetson hardware packages..."
python3 -c "import torch; print('Torch:', torch.__version__); print('CUDA:', torch.cuda.is_available())"
python3 -c "import torchvision; print('TorchVision:', torchvision.__version__)"
python3 -c "import tensorrt; print('TensorRT:', tensorrt.__version__)"
python3 -c "import cv2; print('OpenCV:', cv2.__version__)"
ok "Jetson runtime verification completed"

echo "=== Installation Completed Successfully ==="
echo "Start the backend in one terminal:"
echo "  python3 -m src.api.server"
echo "Start the frontend in another terminal:"
echo "  cd ~/Cerberus-AI/frontend && npm run dev"
