import asyncio
import json
import numpy as np
import cv2
import logging
from datetime import datetime
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from av import VideoFrame
import pyautogui
from .quantum_mirroring.input_speculation import InputSpeculator, QuantumMirrorStreamer, VolatileStorageManager

# إعداد logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AdvancedGamingServer")

class AdvancedGameCaptureTrack(VideoStreamTrack):
    def __init__(self, resolution=(1280, 720)):
        super().__init__()
        self.resolution = resolution
        self.streamer = QuantumMirrorStreamer()
        self.storage = VolatileStorageManager()
        self.frame_count = 0

    async def recv(self):
        pts, time_base = await self.next_timestamp()

        # التقاط الشاشة
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        frame = cv2.resize(frame, self.resolution)

        # تحويل إلى RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # ضغط LZ4 للإطار (Quantum Mirroring)
        compressed = self.streamer.compress_frame(frame_rgb.tobytes())

        # تخزين متقلب (Volatile Storage) - محاكاة لـ Zero-Storage
        self.storage.store_volatile(f"frame_{self.frame_count}", compressed)

        # استهلاك البيانات فوراً للبث
        data_to_send = self.storage.consume_volatile(f"frame_{self.frame_count}")
        decompressed = self.streamer.decompress_frame(data_to_send)

        # إعادة التشكيل
        final_frame = np.frombuffer(decompressed, dtype=np.uint8).reshape((self.resolution[1], self.resolution[0], 3))

        new_frame = VideoFrame.from_ndarray(final_frame, format="rgb24")
        new_frame.pts = pts
        new_frame.time_base = time_base

        self.frame_count += 1
        return new_frame

class AdvancedGamingServer:
    def __init__(self):
        self.pcs = set()
        self.speculator = InputSpeculator()

    async def handle_offer(self, request):
        params = await request.json()
        offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
        pc = RTCPeerConnection()
        self.pcs.add(pc)

        track = AdvancedGameCaptureTrack()
        pc.addTrack(track)

        @pc.on("datachannel")
        def on_datachannel(channel):
            @channel.on("message")
            def on_message(message):
                data = json.loads(message)
                if data["type"] == "input":
                    # تسجيل الإدخال للتنبؤ المستقبلي
                    self.speculator.record_input(data["x"], data["y"])

                    # التنبؤ بالحركة القادمة (Input Speculation) تقليل الـ Lag
                    predicted_x, predicted_y = self.speculator.predict_next_state()
                    logger.info(f"🔮 التنبؤ بالحركة القادمة: ({predicted_x}, {predicted_y})")

                    # تنفيذ الحركة الفعلية
                    pyautogui.moveTo(data["x"], data["y"])
                    if data.get("click"):
                        pyautogui.click()

        await pc.setRemoteDescription(offer)
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

        return web.json_response({
            "sdp": pc.localDescription.sdp,
            "type": pc.localDescription.type
        })

    def run(self, host="0.0.0.0", port=8080):
        app = web.Application()
        app.router.add_post("/offer", self.handle_offer)
        web.run_app(app, host=host, port=port)

if __name__ == "__main__":
    server = AdvancedGamingServer()
    server.run()
