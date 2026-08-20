# 🎯 Cerberus AI — Model Training & Dataset Pipeline

This directory contains scripts and configuration for training, fine-tuning, and exporting the **Cerberus AI YOLOv11 PPE Detection Model**.

---

## 📂 Directory Layout

```
training/
├── train_model.py      # Core PyTorch/Ultralytics training script
├── dataset.yaml        # YOLOv8/v11 19-class dataset specification
├── kaggle_export/      # Standalone scripts for Kaggle GPU training
└── colab_export/       # Google Colab notebook & script export
```

---

## 🏷️ Dataset Class Schema (19 Classes)

The model detects 19 distinct industrial classes covering compliant PPE, violation states, and site machinery:

| Index | Class Name | Category | Index | Class Name | Category |
| :---: | :--- | :--- | :---: | :--- | :--- |
| `0` | `Boots` | Compliant PPE | `10` | `No-Helmet` | Violation State |
| `1` | `Ear-Protection` | Compliant PPE | `11` | `No-Mask` | Violation State |
| `2` | `Glass` | Compliant PPE | `12` | `No-Vest` | Violation State |
| `3` | `Glove` | Compliant PPE | `13` | `Worker` | Person Subject |
| `4` | `Hard_hat` | Compliant PPE | `14` | `Vest` | Compliant PPE |
| `5` | `Mask` | Compliant PPE | `15` | `Circular_Saw` | Equipment Hazard |
| `6` | `No-Boots` | Violation State | `16` | `Fire_Extinguisher` | Safety Equipment |
| `7` | `No-Ear-Protection` | Violation State | `17` | `Fire_prevention_Net` | Safety Net |
| `8` | `No-Glass` | Violation State | `18` | `Welding_Equipment` | Equipment Hazard |
| `9` | `No-Glove` | Violation State | | | |

---

## 🚀 Training Instructions

### 1. Local Training (GPU / CPU)
Run `train_model.py` to train on your local workstation:
```bash
python training/train_model.py --epochs 100 --imgsz 640 --batch 8
```

### 2. Kaggle GPU Training (Recommended)
1. Upload your dataset or attach `Construction PPE Detection Combined.yolov8`.
2. Execute `training/kaggle_export/kaggle_training.py` in a GPU cell.
3. Export the resulting `best.pt` and `best.onnx` files to `models/`.

---

## ⚡ Model Deployment Workflow

1. **Train Model:** Generate `best.pt` via Kaggle/Colab/Local PyTorch training.
2. **Export ONNX:** Run `python scripts/export_onnx.py --model models/best.pt`.
3. **Build TensorRT Engine:** Build device-optimized FP16 or INT8 engine on target Jetson hardware:
   ```bash
   python scripts/export_tensorrt.py --model models/best.pt
   ```