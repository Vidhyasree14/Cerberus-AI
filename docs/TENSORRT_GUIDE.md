# ⚡ TensorRT & DeepStream Acceleration Guide

This guide covers building NVIDIA TensorRT engines for **Cerberus AI** to maximize throughput on NVIDIA GPUs and Jetson edge hardware.

---

## ⚙️ Compilation Steps

### Step 1: Export PyTorch Model to ONNX
Export PyTorch weights (`best.pt`) to ONNX:
```bash
python scripts/export_onnx.py --model models/best.pt --imgsz 640
```
Output: `models/best.onnx`

---

### Step 2: Compile FP16 TensorRT Engine
Build a half-precision (FP16) TensorRT engine:
```bash
python scripts/export_tensorrt.py \
    --model models/best.pt \
    --imgsz 640 \
    --device 0
```
Output: `models/best.engine`

---

### Step 3: Quantized INT8 Engine Compilation (Optional)
For ultra-high-throughput environments, INT8 quantization delivers up to $3\times$ speedup over FP32:

1. Place 200 calibration sample images into `datasets/calibration/images/`.
2. Execute INT8 calibration and engine generation:
   ```bash
   python scripts/export_tensorrt.py \
       --model models/best.pt \
       --imgsz 640 \
       --int8 \
       --calib_data datasets/calibration \
       --device 0
   ```

---

## 📊 Precision Comparison

| Mode | Precision | Latency Speedup | mAP Impact | Calibration Needed? |
| :--- | :--- | :---: | :---: | :---: |
| **FP32** | 32-bit Floating Point | $1.0\times$ (Baseline) | $0.0\%$ | No |
| **FP16** | 16-bit Floating Point | **$2.1\times$ Speedup** | $< 0.2\%$ | No |
| **INT8** | 8-bit Integer Quantized | **$3.5\times$ Speedup** | $\approx 1.2\%$ | Yes |
