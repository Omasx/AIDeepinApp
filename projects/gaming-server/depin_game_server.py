"""
depin_game_server.py - سيرفر البث الرئيسي لـ DePIN Gaming

هذا الملف يحتوي على السيرفر الرئيسي الذي يقوم بـ:
1. التقاط شاشة اللعبة
2. تطبيق ضغط QFT
3. بث الفيديو عبر WebRTC
4. استقبال الأوامر من الهاتف
5. إدارة الاتصالات المتعددة
"""

import asyncio
import json
import numpy as np
import cv2
import logging
from datetime import datetime
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaBlackhole
from av import VideoFrame
import pyautogui
from quantum_compression import QuantumInspiredCompressor
from typing import Dict, Set, Optional

# إعداد logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GameCaptureTrack(VideoStreamTrack):
    """
    مسار التقاط شاشة اللعبة وبثها مع ضغط كمي
    
    المسؤوليات:
    - التقاط شاشة اللعبة بشكل مستمر
    - تطبيق ضغط QFT
    - تحويل الإطارات إلى صيغة WebRTC
    """
    
    def __init__(self, resolution: tuple = (1280, 720), fps: int = 60):
        """
        تهيئة مسار التقاط الشاشة
        
        Args:
            resolution: دقة الفيديو (width, height)
            fps: عدد الإطارات في الثانية
        """
        super().__init__()
        self.resolution = resolution
        self.fps = fps
        self.compressor = QuantumInspiredCompressor(compression_ratio=0.1)
        self.frame_count = 0
        self.start_time = datetime.now()
        logger.info(f"✅ تم تهيئة GameCaptureTrack: {resolution[0]}x{resolution[1]}@{fps}fps")
    
    async def recv(self):
        """
        استقبال الإطار التالي (يتم استدعاؤه من قبل WebRTC)
        
        المراحل:
        1. الحصول على الطابع الزمني
        2. التقاط الشاشة
        3. تغيير الحجم
        4. تطبيق الضغط الكمي
        5. تحويل إلى صيغة RGB
        6. إرجاع الإطار
        """
        pts, time_base = await self.next_timestamp()
        
        try:
            # 1. التقاط الشاشة
            screenshot = pyautogui.screenshot()
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # 2. تغيير الحجم إلى الدقة المطلوبة
            frame = cv2.resize(frame, self.resolution)
            
            # 3. تطبيق الضغط الكمي كل 5 إطارات (لتوفير المعالجة)
            if self.frame_count % 5 == 0:
                frame = self.compressor.apply_qft_simulation(frame)
            
            # 4. تحويل إلى RGB للبث
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # 5. تحويل إلى VideoFrame
            new_frame = VideoFrame.from_ndarray(frame, format="rgb24")
            new_frame.pts = pts
            new_frame.time_base = time_base
            
            self.frame_count += 1
            
            # طباعة الإحصائيات كل 60 إطار
            if self.frame_count % 60 == 0:
                elapsed = (datetime.now() - self.start_time).total_seconds()
                actual_fps = self.frame_count / elapsed if elapsed > 0 else 0
                logger.info(f"📊 الإطار #{self.frame_count} | FPS: {actual_fps:.1f} | Compression: {self.compressor.compression_ratio:.2f}")
            
            return new_frame
            
        except Exception as e:
            logger.error(f"❌ خطأ في التقاط الشاشة: {e}")
            # إرجاع إطار أسود في حالة الخطأ
            black_frame = np.zeros((self.resolution[1], self.resolution[0], 3), dtype=np.uint8)
            new_frame = VideoFrame.from_ndarray(black_frame, format="rgb24")
            new_frame.pts = pts
            new_frame.time_base = time_base
            return new_frame


class DePINGameServer:
    """
    سيرفر الألعاب اللامركزي الرئيسي
    
    المسؤوليات:
    - إدارة الاتصالات WebRTC المتعددة
    - معالجة طلبات الاتصال من العملاء
    - استقبال الأوامر من الهاتف
    - توفير إحصائيات الأداء
    """
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8080):
        """
        تهيئة السيرفر
        
        Args:
            host: عنوان الاستماع
            port: منفذ الاستماع
        """
        self.host = host
        self.port = port
        self.pcs: Set[RTCPeerConnection] = set()
        self.compressor = QuantumInspiredCompressor()
        self.input_queue = asyncio.Queue()
        logger.info(f"✅ تم تهيئة DePINGameServer على {host}:{port}")
    
    async def handle_offer(self, request: web.Request) -> web.Response:
        """
        معالجة طلب الاتصال من الهاتف
        
        المراحل:
        1. استقبال عرض الاتصال (Offer)
        2. إنشاء اتصال WebRTC جديد
        3. إضافة مسار البث
        4. إضافة قناة البيانات للأوامر
        5. إرسال الإجابة (Answer)
        
        Args:
            request: طلب HTTP
            
        Returns:
            استجابة JSON تحتوي على الإجابة
        """
        try:
            params = await request.json()
            offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
            
            # إنشاء اتصال WebRTC جديد
            pc = RTCPeerConnection()
            self.pcs.add(pc)
            
            logger.info(f"🔗 اتصال جديد من {request.remote} | إجمالي الاتصالات: {len(self.pcs)}")
            
            # إضافة مسار البث
            game_track = GameCaptureTrack(resolution=(1280, 720), fps=60)
            pc.addTrack(game_track)
            
            # معالجة قناة البيانات للأوامر
            @pc.on("datachannel")
            def on_datachannel(channel):
                logger.info(f"📡 قناة بيانات جديدة: {channel.label}")
                
                @channel.on("message")
                def on_message(message):
                    try:
                        input_data = json.loads(message)
                        self.handle_input(input_data)
                    except json.JSONDecodeError:
                        logger.error(f"❌ خطأ في فك تشفير الرسالة: {message}")
            
            # معالجة إغلاق الاتصال
            @pc.on("connectionstatechange")
            async def on_connectionstatechange():
                logger.info(f"🔌 حالة الاتصال: {pc.connectionState}")
                if pc.connectionState == "failed":
                    await pc.close()
                    self.pcs.discard(pc)
                    logger.info(f"❌ تم إغلاق الاتصال | الاتصالات المتبقية: {len(self.pcs)}")
            
            # تعيين الوصف البعيد
            await pc.setRemoteDescription(offer)
            
            # إنشاء الإجابة
            answer = await pc.createAnswer()
            await pc.setLocalDescription(answer)
            
            # إرسال الإجابة
            return web.Response(
                content_type="application/json",
                text=json.dumps({
                    "sdp": pc.localDescription.sdp,
                    "type": pc.localDescription.type
                })
            )
            
        except Exception as e:
            logger.error(f"❌ خطأ في معالجة العرض: {e}")
            return web.Response(status=400, text=json.dumps({"error": str(e)}))
    
    def handle_input(self, input_data: dict):
        """
        معالجة الأوامر من الهاتف
        
        أنواع الأوامر المدعومة:
        - key: ضغط مفتاح على لوحة المفاتيح
        - mouse: نقرة الماوس
        
        Args:
            input_data: بيانات الأمر
        """
        try:
            if input_data["type"] == "key":
                key = input_data.get("key")
                if key:
                    pyautogui.press(key)
                    logger.debug(f"⌨️ ضغط المفتاح: {key}")
            
            elif input_data["type"] == "mouse":
                x = input_data.get("x", 0)
                y = input_data.get("y", 0)
                pyautogui.click(x, y)
                logger.debug(f"🖱️ نقرة الماوس: ({x}, {y})")
            
            elif input_data["type"] == "drag":
                x1, y1 = input_data.get("x1", 0), input_data.get("y1", 0)
                x2, y2 = input_data.get("x2", 0), input_data.get("y2", 0)
                pyautogui.drag(x2 - x1, y2 - y1, duration=0.1)
                logger.debug(f"🖱️ سحب الماوس: ({x1}, {y1}) -> ({x2}, {y2})")
            
        except Exception as e:
            logger.error(f"❌ خطأ في معالجة الأمر: {e}")
    
    async def stats(self, request: web.Request) -> web.Response:
        """
        إحصائيات الأداء
        
        Returns:
            JSON يحتوي على:
            - عدد الاتصالات النشطة
            - معدل البت المتوقع
            - نسبة الضغط
            - إحصائيات الإطارات
        """
        stats = {
            "active_connections": len(self.pcs),
            "bitrate_720p_mbps": self.compressor.calculate_bitrate((1280, 720), 60),
            "bitrate_1080p_mbps": self.compressor.calculate_bitrate((1920, 1080), 60),
            "compression_ratio": self.compressor.compression_ratio,
            "frames_processed": self.compressor.frame_count,
            "timestamp": datetime.now().isoformat()
        }
        return web.json_response(stats)
    
    async def health(self, request: web.Request) -> web.Response:
        """فحص صحة السيرفر"""
        return web.json_response({
            "status": "healthy",
            "active_connections": len(self.pcs),
            "timestamp": datetime.now().isoformat()
        })
    
    def run(self):
        """تشغيل السيرفر"""
        app = web.Application()
        app.router.add_post("/offer", self.handle_offer)
        app.router.add_get("/stats", self.stats)
        app.router.add_get("/health", self.health)
        
        print("\n" + "="*60)
        print("🚀 DePIN Gaming Server")
        print("="*60)
        print(f"📡 السيرفر يعمل على http://{self.host}:{self.port}")
        print(f"📊 Bitrate المتوقع (720p@60fps): {self.compressor.calculate_bitrate((1280,720), 60):.2f} Mbps")
        print(f"📊 Bitrate المتوقع (1080p@60fps): {self.compressor.calculate_bitrate((1920,1080), 60):.2f} Mbps")
        print("="*60)
        print("\n📍 النقاط النهائية المتاحة:")
        print(f"  • POST /offer - استقبال عروض الاتصال WebRTC")
        print(f"  • GET /stats - إحصائيات الأداء")
        print(f"  • GET /health - فحص صحة السيرفر")
        print("\n" + "="*60 + "\n")
        
        web.run_app(app, host=self.host, port=self.port)


# ============================================================================
# نقطة الدخول الرئيسية
# ============================================================================

if __name__ == "__main__":
    server = DePINGameServer(host="0.0.0.0", port=8080)
    server.run()
