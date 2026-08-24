# Author: Vidhyasree M
"""
Export trained YOLO model to ONNX format.

The ONNX file is the portable intermediate that can later be converted to
a TensorRT engine on the target Jetson device (see docs/tensorrt_instructions.md).

Usage
-----
python export_onnx.py
python export_onnx.py --model ppe_training/custom_model/weights/best.pt
python  export_onnx.py --model best.pt --imgsz 1280 --dynamic
"""

from __future__ import annotations

import argparse
import logging
import os
import sys

import torch
_orig = torch.load
def _safe_load(f, *args, **kwargs):
    kwargs.setdefault("weights_only", False)
    return _orig(f, *args, **kwargs)
torch.load = _safe_load

from ultralytics import YOLO

log = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export YOLO model to ONNX for Jetson / TensorRT deployment")
    parser.add_argument(
        "--model",
        default="models/best.pt",
        help="Path to trained .pt weights",
    )
    parser.add_argument("--imgsz",   type=int, default=640,   help="Input image size (default: 640)")
    parser.add_argument("--batch",   type=int, default=1,     help="Batch size for ONNX export (default: 1)")
    parser.add_argument("--dynamic", action="store_true",     help="Dynamic axes (Note: fixed shape is faster on Jetson)")
    parser.add_argument("--half",    action="store_true",     help="Export with FP16 half-precision for Jetson GPU")
    parser.add_argument("--opset",   type=int, default=17,    help="ONNX opset version (default: 17 for TensorRT 8.x/10.x)")
    parser.add_argument("--simplify",action="store_true", default=True, help="Simplify ONNX graph with onnxslim")
    parser.add_argument("--device",  default="cpu",             help="Device to use for export (e.g. 0 for Jetson GPU or cpu)")
    return parser.parse_args()


def export(args: argparse.Namespace) -> str:
    if not os.path.exists(args.model):
        log.error("Model weights not found: %s", args.model)
        sys.exit(1)

    log.info("Loading model: %s", args.model)
    model = YOLO(args.model)

    log.info(
        "Exporting to ONNX (imgsz=%d, batch=%d, opset=%d, half=%s, dynamic=%s, simplify=%s, device=%s)",
        args.imgsz, args.batch, args.opset, args.half, args.dynamic, args.simplify, args.device,
    )

    path = model.export(
        format   = "onnx",
        imgsz    = args.imgsz,
        batch    = args.batch,
        dynamic  = args.dynamic,
        half     = args.half,
        opset    = args.opset,
        simplify = args.simplify,
        device   = args.device,
    )

    expected = args.model.replace(".pt", ".onnx")
    onnx_path = path if path else expected

    if os.path.exists(onnx_path):
        size_mb = os.path.getsize(onnx_path) / 1e6
        log.info("✅ ONNX export complete: %s (%.1f MB)", onnx_path, size_mb)
    else:
        log.warning("ONNX file not found at expected path: %s", onnx_path)

    return onnx_path


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
    )
    args = parse_args()
    out  = export(args)
    print(f"\n✅ ONNX model saved to: {out}")
    print("\nNext steps for NVIDIA Jetson / DeepStream:")
    print(f"  1. Copy {out} to your Jetson device (if exported on PC)")
    print(f"  2. Build TensorRT engine directly on Jetson:")
    print(f"     python scripts/export_tensorrt.py --model {args.model}")
    print(f"     # OR use trtexec:")
    print(f"     /usr/src/tensorrt/bin/trtexec --onnx={out} --saveEngine={out.replace('.onnx', '.engine')} --fp16")
    print(f"  3. Set MODEL_PATH={out.replace('.onnx', '.engine')} in .env")

