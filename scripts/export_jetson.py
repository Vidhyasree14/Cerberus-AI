#!/usr/bin/env python3
# Author: Vidhyasree M
"""
Jetson Performance Export Script

This script converts a trained YOLO PyTorch model (.pt) into a highly optimized
TensorRT Engine (.engine) for max performance on Jetson devices (Orin, Xavier, Nano).

Usage:
    python scripts/export_jetson.py --model models/yolo11n.pt --imgsz 640

Requirements:
    - Must be run on the target Jetson device (or a host with identical TensorRT versions).
    - Requires `pip install ultralytics tensorrt`.
"""

import argparse
import sys
import os

try:
    import torch
    _orig = torch.load
    def _safe_load(f, *args, **kwargs):
        kwargs.setdefault("weights_only", False)
        return _orig(f, *args, **kwargs)
    torch.load = _safe_load
except Exception:
    pass

try:
    from ultralytics import YOLO
except ImportError:
    print("Error: ultralytics is not installed. Run `pip install ultralytics`")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Export YOLO model to TensorRT for Jetson")
    parser.add_argument("--model", type=str, default="models/best.pt", help="Path to the PyTorch model (.pt)")
    parser.add_argument("--imgsz", type=int, default=640, help="Target image size (e.g. 640 or 416)")
    parser.add_argument("--workspace", type=int, default=4, help="Max workspace size in GB (default: 4)")
    parser.add_argument("--int8", action="store_true", help="Enable INT8 quantization (requires calibration)")
    parser.add_argument("--device", default="0", help="CUDA device index (default: 0)")
    args = parser.parse_args()

    if not os.path.exists(args.model):
        print(f"Error: Model not found at {args.model}")
        sys.exit(1)

    print(f"Loading PyTorch model: {args.model}")
    model = YOLO(args.model)

    precision = "INT8" if args.int8 else "FP16"
    print(f"\n--- Starting TensorRT Export for Jetson ---")
    print(f"Image Size: {args.imgsz}")
    print(f"Precision:  {precision}")
    print(f"Workspace:  {args.workspace} GB")
    print(f"Device:     {args.device}")
    
    try:
        exported_path = model.export(
            format="engine",
            imgsz=args.imgsz,
            half=not args.int8,
            int8=args.int8,
            dynamic=False,   # Fixed shapes deliver maximum FPS on Jetson
            workspace=args.workspace,
            device=args.device,
            simplify=True,
        )
        print(f"\n✅ Export successful! TensorRT engine saved to: {exported_path}")
        print("The EdgeVision pipeline will automatically detect and load this .engine file.")
    except Exception as e:
        print(f"\n❌ Export failed: {e}")
        print("Note: TensorRT engine compilation must be executed directly on the target NVIDIA Jetson device.")

if __name__ == "__main__":
    main()

