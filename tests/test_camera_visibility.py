import pytest
import asyncio
from src.core import sqlite_db, db, config
from src.api import server

@pytest.mark.asyncio
async def test_default_cameras_and_zones():
    # Verify default zones in SQLite
    zones = sqlite_db.get_zones_sql()
    zone_names = [z["name"] for z in zones]
    assert "General Plant Floor" in zone_names
    assert "Construction Site" in zone_names

    # Verify default cameras
    cameras = await db.get_cameras()
    cam_ids = [c["id"] for c in cameras]
    assert "CAM-01" in cam_ids
    assert "CAM-02" in cam_ids
    
    plant_cam = next(c for c in cameras if c["id"] == "CAM-01")
    assert plant_cam["zone_id"] == "General Plant Floor"
    assert "youtube.com" in plant_cam["source"] or "youtu.be" in plant_cam["source"]

    const_cam = next(c for c in cameras if c["id"] == "CAM-02")
    assert const_cam["zone_id"] == "Construction Site"
    assert "youtu" in const_cam["source"]

@pytest.mark.asyncio
async def test_local_camera_visibility_toggle():
    # 1. When show_main_webcam is True
    await server.update_settings_api({"show_main_webcam": True})
    res_on = await server.get_cameras_api()
    import json
    cams = json.loads(res_on.body.decode())
    cam_ids = [c["id"] for c in cams]
    assert any(c.get("type") == "webcam" or c.get("streamUrl") == "0" for c in cams)
    assert "CAM-01" in cam_ids
    assert "CAM-02" in cam_ids

    # 2. When show_main_webcam is False
    await server.update_settings_api({"show_main_webcam": False})
    res_off = await server.get_cameras_api()
    cams_hidden = json.loads(res_off.body.decode())
    cam_ids_hidden = [c["id"] for c in cams_hidden]
    assert not any(c.get("type") == "webcam" or c.get("streamUrl") == "0" for c in cams_hidden)
    assert "CAM-01" in cam_ids_hidden
    assert "CAM-02" in cam_ids_hidden
