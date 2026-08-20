# 🏷️ Cerberus AI Dataset Structure & Labelling Guide

This guide details dataset structure, annotation classes, and augmentation strategies used for training the Cerberus AI model.

---

## 🏷️ Class Definitions (19 Classes)

| Class ID | Class Name | Category | Description |
| :---: | :--- | :--- | :--- |
| `0` | `Boots` | Compliant PPE | Industrial steel-toe boots |
| `1` | `Ear-Protection` | Compliant PPE | Hearing protection earmuffs / plugs |
| `2` | `Glass` | Compliant PPE | Protective safety eyewear |
| `3` | `Glove` | Compliant PPE | Industrial work gloves |
| `4` | `Hard_hat` | Compliant PPE | Industrial safety helmet |
| `5` | `Mask` | Compliant PPE | Respiratory face mask |
| `6` | `No-Boots` | Violation State | Bare/non-compliant footwear |
| `7` | `No-Ear-Protection`| Violation State | Missing ear protection in high-noise zone |
| `8` | `No-Glass` | Violation State | Missing eye protection |
| `9` | `No-Glove` | Violation State | Unprotected hands |
| `10` | `No-Helmet` | Violation State | Missing hard hat / safety helmet |
| `11` | `No-Mask` | Violation State | Missing respiratory mask |
| `12` | `No-Vest` | Violation State | Missing high-visibility vest |
| `13` | `Worker` | Core Subject | Person / worker full-body bounding box |
| `14` | `Vest` | Compliant PPE | High-vis reflective safety vest |
| `15` | `Circular_Saw` | Equipment Hazard | Handheld/bench circular saw |
| `16` | `Fire_Extinguisher`| Safety Asset | Emergency fire extinguisher |
| `17` | `Fire_prevention_Net`| Safety Asset | Work-at-height safety netting |
| `18` | `Welding_Equipment`| Hazard Asset | Arc / oxy-acetylene welding gear |

---

## 📁 YOLOv8/v11 Directory Layout

```
dataset/
├── data.yaml             # YOLO dataset configuration file
├── train/
│   ├── images/          # Training image files
│   └── labels/          # YOLO format text annotation files
├── valid/
│   ├── images/          # Validation image files
│   └── labels/          # Validation labels
└── test/
    ├── images/          # Test set images
    └── labels/          # Test set labels
```

---

## 💡 Augmentation Pipeline

- **Multi-Scale Mosaic:** Combines 4 images into a single training sample to improve small-object detection (`lanyard`, `hook`, `glasses`).
- **Color & CLAHE Enhancement:** Synthetic HSV jittering to simulate harsh outdoor sunlight, heavy shadows, and low-light indoor environments.
- **Hard Negative Mining:** Annotates un-worn equipment on site ground to eliminate false positives (e.g. helmets placed on tables).
