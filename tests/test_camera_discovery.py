# Author: Vidhyasree M
import pytest
import os
import sys
from unittest.mock import patch, MagicMock

from src.core import camera_discovery
from src.api import server


def test_platform_environment_detectors():
    info = camera_discovery.get_environment_info()
    assert "platform" in info
    assert "is_linux" in info
    assert "is_windows" in info
    assert "is_jetson" in info
    assert "has_v4l2" in info


def test_jetson_csi_pipeline_generation():
    pipe = camera_discovery.get_jetson_csi_pipeline(sensor_id=0, capture_width=1280, capture_height=720, framerate=30)
    assert "nvarguscamerasrc sensor-id=0" in pipe
    assert "width=1280, height=720" in pipe
    assert "appsink" in pipe


def test_probe_jetson_cameras_mock():
    with patch("src.core.camera_discovery.is_jetson", return_value=True), \
         patch("src.core.camera_discovery.is_linux", return_value=True), \
         patch("cv2.VideoCapture") as mock_cap:
        
        # Mock successful open
        mock_instance = MagicMock()
        mock_instance.isOpened.return_value = True
        mock_instance.read.return_value = (True, MagicMock())
        mock_instance.get.side_effect = lambda prop: 1280 if prop == 3 else 720
        mock_cap.return_value = mock_instance

        cams = camera_discovery.probe_jetson_cameras()
        assert len(cams) >= 1
        assert any("jetson" in c.get("environment", "") for c in cams)


def test_probe_linux_cameras_mock():
    with patch("src.core.camera_discovery.is_linux", return_value=True), \
         patch("glob.glob", return_value=["/dev/video0", "/dev/video2"]), \
         patch("cv2.VideoCapture") as mock_cap:
        
        mock_instance = MagicMock()
        mock_instance.isOpened.return_value = True
        mock_instance.read.return_value = (True, MagicMock())
        mock_instance.get.side_effect = lambda prop: 1920 if prop == 3 else 1080
        mock_cap.return_value = mock_instance

        cams = camera_discovery.probe_linux_cameras()
        assert len(cams) >= 2
        assert cams[0]["id"] == "0"
        assert cams[1]["id"] == "2"
        assert cams[0]["environment"] == "linux_v4l2"


@pytest.mark.asyncio
async def test_api_devices_environment():
    res = await server.get_device_environment()
    import json
    data = json.loads(res.body.decode())
    assert "platform" in data
    assert "is_linux" in data
    assert "is_windows" in data


@pytest.mark.asyncio
async def test_api_devices_cameras():
    res = await server.list_physical_cameras()
    import json
    data = json.loads(res.body.decode())
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "source" in data[0]
