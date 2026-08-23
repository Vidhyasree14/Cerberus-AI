# Cerberus AI Jetson Deployment

Follow these steps on a Jetson device from an SSH terminal.

## 1. Connect to the Jetson

Run this on your computer:

```bash
ssh <username>@<jetson-ip>
```

Replace `<username>` and `<jetson-ip>` with your Jetson login details.

## 2. Download the project

Run these commands on the Jetson:

```bash
sudo apt update
sudo apt install -y git

git clone https://github.com/Vidhyasree14/Cerberus-AI.git
cd ~/Cerberus-AI
```

If the project was already cloned, run only:

```bash
cd ~/Cerberus-AI
git pull origin main
```

## 3. Confirm the Jetson AI stack

JetPack provides CUDA and TensorRT. Torch and TorchVision must be the NVIDIA builds matching the installed JetPack version. Install those NVIDIA packages before running the project installer.

Check them with:

```bash
python3 -c "import torch; print('Torch:', torch.__version__); print('CUDA:', torch.cuda.is_available())"
python3 -c "import torchvision, tensorrt; print('TorchVision:', torchvision.__version__); print('TensorRT:', tensorrt.__version__)"
```

The first command must print `CUDA: True`. If either command fails, install the Torch/TorchVision packages provided for your JetPack release, then run the checks again.

## 4. Install the remaining dependencies

Run the installer from the cloned project directory:

```bash
cd ~/Cerberus-AI
chmod +x deploy/jetson/install.sh
./deploy/jetson/install.sh
```

Successful installation shows acknowledgements similar to:

```text
[OK] System packages installed
[OK] Torch CUDA is available
[OK] TorchVision and TensorRT are available
[OK] pip tools updated
[OK] Python dependencies installed and checked
[OK] Jetson environment configured to use models/best.engine
Node.js: v22.x.x
npm: 10.x.x
[OK] Node.js and npm installed
[OK] Frontend dependencies installed
[OK] TensorRT engine available at models/best.engine
[OK] Jetson runtime verification completed
=== Installation Completed Successfully ===
```

If a command fails, the script prints `[ERROR]` with the failing line and command, then stops.

The installer installs Jetson OpenCV, Python requirements, ONNX export packages, Node.js 22, frontend packages, and verifies the hardware stack. It creates `.env` when needed, sets `MODEL_PATH=models/best.engine`, and creates the device-specific TensorRT engine:

```text
models/best.pt -> models/best.engine
```

The TensorRT engine must be built on the target Jetson and should not be copied from another computer.

## 5. Start the backend

Keep SSH terminal 1 open:

```bash
cd ~/Cerberus-AI
python3 -m src.api.server
```

## 6. Start the frontend

Open a second terminal on your computer and connect again:

```bash
ssh <username>@<jetson-ip>
cd ~/Cerberus-AI/frontend
npm run dev
```

## 7. Open the dashboard

From a computer on the same private network, open:

```text
http://<jetson-ip>:5173
```

Find the Jetson IP with:

```bash
hostname -I
```

## Secure remote access

For a computer on another network, use a VPN such as Tailscale or WireGuard. Alternatively, create an SSH tunnel on the computer displaying the dashboard:

```bash
ssh -L 5173:127.0.0.1:5173 -L 8000:127.0.0.1:8000 <username>@<jetson-ip>
```

Then open:

```text
http://localhost:5173
```

Do not expose ports `5173` or `8000` directly to the public internet.
