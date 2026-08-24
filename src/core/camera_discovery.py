# Author: Vidhyasree M
"""
Cross-Platform Camera Hardware Discovery and Inspection Engine.
Automatically detects, enumerates, and configures cameras across:
  - Linux environments (Native V4L2 USB webcams & sysfs device name resolution)
  - NVIDIA Jetson platforms (Orin, Xavier, Nano – USB webcams & CSI ribbon cameras via GStreamer)
  - Windows environments (DirectShow, Media Foundation)
  - Containerized / Virtualized environments (Docker, WSL2)
"""

from __future__ import annotations

import os
import sys
import glob
import logging
import platform
from typing import Any, List, Dict

import cv2

log = logging.getLogger(__name__)


# ── Environment & Hardware Detectors ──────────────────────────────────────────

def is_linux() -> bool:
    """Return True if running on a Linux kernel (including Jetson & WSL)."""
    return sys.platform.startswith("linux")


def is_windows() -> bool:
    """Return True if running on Windows."""
    return sys.platform.startswith("win") or os.name == "nt"


def is_jetson() -> bool:
    """
    Return True if running on an NVIDIA Jetson hardware platform (Orin, Xavier, TX2, Nano).
    """
    if not is_linux():
        return False

    # Check 1: Tegra release file
    if os.path.exists("/etc/nv_tegra_release"):
        return True

    # Check 2: Tegra SoC family in sysfs / proc
    soc_family_path = "/sys/devices/soc0/family"
    if os.path.exists(soc_family_path):
        try:
            with open(soc_family_path, "r") as f:
                if "tegra" in f.read().lower():
                    return True
        except Exception:
            pass

    # Check 3: NVIDIA host control node & aarch64 architecture
    if platform.machine() in ("aarch64", "arm64") and (
        os.path.exists("/dev/nvhost-ctrl") or os.path.exists("/dev/nvmap")
    ):
        return True

    return False


def is_wsl() -> bool:
    """Return True if running inside Windows Subsystem for Linux (WSL)."""
    if not is_linux():
        return False
    return (
        os.path.exists("/proc/sys/fs/binfmt_misc/WSLInterop")
        or "microsoft" in platform.release().lower()
        or "wsl" in platform.release().lower()
    )


def is_docker() -> bool:
    """Return True if running inside a Docker container."""
    return os.path.exists("/.dockerenv") or os.path.isfile("/run/.containerenv")


def get_environment_info() -> Dict[str, Any]:
    """Return system environment, hardware architecture, and camera subsystem info."""
    return {
        "platform": sys.platform,
        "machine": platform.machine(),
        "is_linux": is_linux(),
        "is_windows": is_windows(),
        "is_jetson": is_jetson(),
        "is_wsl": is_wsl(),
        "is_docker": is_docker(),
        "opencv_version": cv2.__version__,
        "has_v4l2": hasattr(cv2, "CAP_V4L2"),
        "has_gstreamer": hasattr(cv2, "CAP_GSTREAMER"),
        "has_dshow": hasattr(cv2, "CAP_DSHOW"),
        "has_msmf": hasattr(cv2, "CAP_MSMF"),
    }


# ── Jetson CSI GStreamer Pipeline Generator ───────────────────────────────────

def get_jetson_csi_pipeline(
    sensor_id: int = 0,
    capture_width: int = 1280,
    capture_height: int = 720,
    framerate: int = 30,
    flip_method: int = 0,
) -> str:
    """
    Generate optimized NVIDIA Jetson hardware-accelerated CSI camera GStreamer pipeline string.
    Uses nvarguscamerasrc with hardware ISP for zero-copy frame ingestion.
    """
    return (
        f"nvarguscamerasrc sensor-id={sensor_id} ! "
        f"video/x-raw(memory:NVMM), width={capture_width}, height={capture_height}, "
        f"format=NV12, framerate={framerate}/1 ! "
        f"nvvidconv flip-method={flip_method} ! "
        f"video/x-raw, width={capture_width}, height={capture_height}, format=BGRx ! "
        f"videoconvert ! "
        f"video/x-raw, format=BGR ! "
        f"appsink drop=1"
    )


# ── Linux V4L2 Device Name Resolution ─────────────────────────────────────────

def get_linux_v4l2_device_name(dev_node: str) -> str:
    """
    Read human-readable camera product name from sysfs for a given /dev/videoX node.
    Example: 'Logitech Webcam C920', 'Integrated Camera', 'USB 2.0 Camera'
    """
    try:
        base_name = os.path.basename(dev_node)  # 'video0'
        name_path = f"/sys/class/video4linux/{base_name}/name"
        if os.path.exists(name_path):
            with open(name_path, "r", encoding="utf-8", errors="ignore") as f:
                name = f.read().strip()
                if name:
                    return name
    except Exception as e:
        log.debug("Could not read sysfs camera name for %s: %s", dev_node, e)

    return f"Linux V4L2 Camera ({os.path.basename(dev_node)})"


# ── Camera Probing & Discovery Functions ─────────────────────────────────────

def get_platform_opencv_backends() -> List[int]:
    """Return prioritized OpenCV capture backends suited for the current runtime OS."""
    backends: List[int] = []

    if is_jetson():
        if hasattr(cv2, "CAP_GSTREAMER"):
            backends.append(cv2.CAP_GSTREAMER)
        if hasattr(cv2, "CAP_V4L2"):
            backends.append(cv2.CAP_V4L2)
        backends.append(cv2.CAP_ANY)
    elif is_linux():
        if hasattr(cv2, "CAP_V4L2"):
            backends.append(cv2.CAP_V4L2)
        if hasattr(cv2, "CAP_GSTREAMER"):
            backends.append(cv2.CAP_GSTREAMER)
        backends.append(cv2.CAP_ANY)
    elif is_windows():
        if hasattr(cv2, "CAP_DSHOW"):
            backends.append(cv2.CAP_DSHOW)
        if hasattr(cv2, "CAP_MSMF"):
            backends.append(cv2.CAP_MSMF)
        backends.append(cv2.CAP_ANY)
    else:
        backends.append(cv2.CAP_ANY)

    return backends


def probe_linux_cameras() -> List[Dict[str, Any]]:
    """
    Probe all Linux Video4Linux2 (/dev/video*) hardware camera devices.
    Inspects sysfs, tests frame capture, and filters out non-capture metadata sub-devices.
    """
    discovered: List[Dict[str, Any]] = []
    seen_indices: set[int] = set()

    # 1. Enumerate device nodes in /dev/video*
    v4l_devices = sorted(glob.glob("/dev/video[0-9]*"))
    device_targets: List[tuple[int, str]] = []

    for dev_path in v4l_devices:
        num_str = dev_path.replace("/dev/video", "")
        if num_str.isdigit():
            idx = int(num_str)
            device_targets.append((idx, dev_path))
            seen_indices.add(idx)

    # 2. Add fallback indices 0..3 if no /dev/video nodes found (e.g. non-standard paths or permissions)
    for i in range(4):
        if i not in seen_indices:
            device_targets.append((i, f"/dev/video{i}"))

    # Try backends: CAP_V4L2 first
    backends = []
    if hasattr(cv2, "CAP_V4L2"):
        backends.append(cv2.CAP_V4L2)
    backends.append(cv2.CAP_ANY)

    for idx, dev_path in device_targets:
        opened = False
        width, height = 640, 480
        dev_name = get_linux_v4l2_device_name(dev_path) if os.path.exists(dev_path) else f"Webcam (Index {idx})"

        for backend in backends:
            try:
                cap = cv2.VideoCapture(idx, backend)
                if cap and cap.isOpened():
                    # Test read a frame to ensure device is an actual image sensor (not metadata node)
                    ok, test_frame = cap.read()
                    if ok and test_frame is not None:
                        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 640)
                        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 480)
                        if w > 0 and h > 0:
                            width, height = w, h
                        opened = True
                        cap.release()
                        break
                    cap.release()
            except Exception:
                pass

        if opened:
            discovered.append({
                "id": str(idx),
                "name": f"{dev_name} ({width}x{height})",
                "source": str(idx),
                "device_path": dev_path,
                "resolution": f"{width}x{height}",
                "type": "webcam",
                "environment": "linux_v4l2",
                "is_active": False,
            })

    return discovered


def probe_jetson_cameras() -> List[Dict[str, Any]]:
    """
    Probe both NVIDIA Jetson On-Board CSI ribbon cameras (nvarguscamerasrc) and USB V4L2 cameras.
    """
    discovered: List[Dict[str, Any]] = []

    # 1. Test Jetson On-Board CSI Camera (Sensor ID 0 and 1)
    if hasattr(cv2, "CAP_GSTREAMER"):
        for sensor_id in (0, 1):
            try:
                pipeline = get_jetson_csi_pipeline(sensor_id=sensor_id, capture_width=1280, capture_height=720)
                cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
                if cap and cap.isOpened():
                    ok, frame = cap.read()
                    if ok and frame is not None:
                        discovered.append({
                            "id": f"CSI-{sensor_id}",
                            "name": f"NVIDIA Jetson CSI Camera (Sensor {sensor_id} - 1280x720)",
                            "source": pipeline,
                            "device_path": f"nvarguscamerasrc sensor-id={sensor_id}",
                            "resolution": "1280x720",
                            "type": "jetson_csi",
                            "environment": "jetson_csi",
                            "is_active": False,
                        })
                    cap.release()
            except Exception as e:
                log.debug("Jetson CSI probe exception for sensor %d: %s", sensor_id, e)

    # 2. Probe Jetson USB V4L2 webcams
    usb_cams = probe_linux_cameras()
    for cam in usb_cams:
        cam["environment"] = "jetson_usb"
        discovered.append(cam)

    return discovered


def probe_windows_cameras() -> List[Dict[str, Any]]:
    """
    Probe Windows camera devices using DirectShow (CAP_DSHOW) and Media Foundation (CAP_MSMF).
    """
    discovered: List[Dict[str, Any]] = []
    backends = []
    if hasattr(cv2, "CAP_DSHOW"):
        backends.append(cv2.CAP_DSHOW)
    if hasattr(cv2, "CAP_MSMF"):
        backends.append(cv2.CAP_MSMF)
    backends.append(cv2.CAP_ANY)

    for idx in range(6):
        for backend in backends:
            try:
                cap = cv2.VideoCapture(idx, backend)
                if cap and cap.isOpened():
                    ok, frame = cap.read()
                    if ok and frame is not None:
                        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 640)
                        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 480)
                        discovered.append({
                            "id": str(idx),
                            "name": f"Windows Camera (Index {idx} - {w}x{h})",
                            "source": str(idx),
                            "device_path": f"Index {idx}",
                            "resolution": f"{w}x{h}",
                            "type": "webcam",
                            "environment": "windows_dshow",
                            "is_active": False,
                        })
                        cap.release()
                        break
                    cap.release()
            except Exception:
                pass

    return discovered


def discover_connected_cameras() -> List[Dict[str, Any]]:
    """
    Main cross-platform camera hardware discovery entrypoint.
    Inspects host OS and discovers all connected webcams, Jetson CSI pipelines, and USB sensors.
    """
    if is_jetson():
        cams = probe_jetson_cameras()
    elif is_linux():
        cams = probe_linux_cameras()
    elif is_windows():
        cams = probe_windows_cameras()
    else:
        cams = []

    # If no physical devices responded, provide default index 0 entry with environment label
    if not cams:
        env_label = "Jetson USB/CSI" if is_jetson() else ("Linux V4L2" if is_linux() else "Windows")
        cams.append({
            "id": "0",
            "name": f"Default {env_label} Webcam (Index 0)",
            "source": "0",
            "device_path": "/dev/video0" if is_linux() else "Index 0",
            "resolution": "640x480",
            "type": "webcam",
            "environment": "default_fallback",
            "is_active": False,
        })

    return cams
