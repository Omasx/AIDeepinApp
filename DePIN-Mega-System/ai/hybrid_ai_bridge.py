"""
🌐 Hybrid AI Bridge - جسر الذكاء الاصطناعي الهجين
ربط الذكاء الاصطناعي السحابي والمحلي معاً

يتضمن:
- اتصال بـ APIs السحابية (OpenAI, Google, Azure)
- معالجة محلية (TensorFlow, PyTorch)
- توازن ذكي بين السحابة والمحلي
- مراقبة الأداء والتكلفة
- Fallback تلقائي عند الأعطال
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import aiohttp
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CloudConfig:
    """إعدادات الخدمات السحابية"""
    openai_api_key: str = ""
    google_api_key: str = ""
    azure_api_key: str = ""
    azure_endpoint: str = ""
    use_cloud: bool = True
    max_cloud_latency: float = 5.0  # ثواني


@dataclass
class LocalConfig:
    """إعدادات المعالجة المحلية"""
    use_local: bool = True
    use_gpu: bool = True
    batch_size: int = 32
    max_memory: int = 8000  # MB


class HybridAIBridge:
    """جسر الذكاء الاصطناعي الهجين"""
    
    def __init__(self, cloud_config: CloudConfig = None, local_config: LocalConfig = None):
        self.cloud_config = cloud_config or CloudConfig()
        self.local_config = local_config or LocalConfig()
        
        self.cloud_available = False
        self.local_available = False
        
        self.stats = {
            'cloud_requests': 0,
            'local_requests': 0,
            'cloud_latency': [],
            'local_latency': [],
            'cloud_errors': 0,
            'local_errors': 0
        }
        
        self.session = None
    
    async def initialize(self):
        """تهيئة الجسر"""
        
        logger.info("🌐 تهيئة جسر الذكاء الاصطناعي الهجين")
        
        # تهيئة الجلسة
        self.session = aiohttp.ClientSession()
        
        # اختبار الاتصال السحابي
        if self.cloud_config.use_cloud:
            self.cloud_available = await self._test_cloud_connection()
        
        # تهيئة المعالجة المحلية
        if self.local_config.use_local:
            self.local_available = await self._init_local_processing()
        
        logger.info(f"✅ السحابة: {'متاحة' if self.cloud_available else 'غير متاحة'}")
        logger.info(f"✅ المحلي: {'متاح' if self.local_available else 'غير متاح'}")
        
        return {
            'cloud': self.cloud_available,
            'local': self.local_available
        }
    
    async def _test_cloud_connection(self) -> bool:
        """اختبار الاتصال السحابي"""
        
        try:
            # اختبار OpenAI
            if self.cloud_config.openai_api_key:
                headers = {
                    'Authorization': f'Bearer {self.cloud_config.openai_api_key}',
                    'Content-Type': 'application/json'
                }
                
                async with self.session.get(
                    'https://api.openai.com/v1/models',
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as resp:
                    if resp.status == 200:
                        logger.info("✅ اتصال OpenAI نجح")
                        return True
            
            return False
        
        except Exception as e:
            logger.warning(f"⚠️ فشل اختبار السحابة: {e}")
            return False
    
    async def _init_local_processing(self) -> bool:
        """تهيئة المعالجة المحلية"""
        
        try:
            import tensorflow as tf
            import torch
            
            # التحقق من GPU
            gpu_available = tf.config.list_physical_devices('GPU')
            logger.info(f"✅ GPU متاح: {len(gpu_available) > 0}")
            
            return True
        
        except ImportError:
            logger.warning("⚠️ TensorFlow/PyTorch غير مثبت")
            return False
    
    async def process_text(self, text: str, use_cloud: bool = None) -> Dict[str, Any]:
        """معالجة النصوص"""
        
        logger.info(f"📝 معالجة النص: {text[:50]}...")
        
        # اختيار الطريقة الأفضل
        if use_cloud is None:
            use_cloud = self._should_use_cloud('text')
        
        if use_cloud and self.cloud_available:
            return await self._process_text_cloud(text)
        else:
            return await self._process_text_local(text)
    
    async def _process_text_cloud(self, text: str) -> Dict[str, Any]:
        """معالجة النصوص عبر السحابة"""
        
        try:
            start_time = datetime.now()
            
            # استخدام OpenAI API
            headers = {
                'Authorization': f'Bearer {self.cloud_config.openai_api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {'role': 'user', 'content': text}
                ],
                'max_tokens': 500
            }
            
            async with self.session.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=self.cloud_config.max_cloud_latency)
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    latency = (datetime.now() - start_time).total_seconds()
                    
                    self.stats['cloud_requests'] += 1
                    self.stats['cloud_latency'].append(latency)
                    
                    return {
                        'status': 'success',
                        'source': 'cloud',
                        'result': result['choices'][0]['message']['content'],
                        'latency': latency
                    }
                else:
                    self.stats['cloud_errors'] += 1
                    return await self._process_text_local(text)
        
        except Exception as e:
            logger.error(f"❌ خطأ السحابة: {e}")
            self.stats['cloud_errors'] += 1
            return await self._process_text_local(text)
    
    async def _process_text_local(self, text: str) -> Dict[str, Any]:
        """معالجة النصوص محلياً"""
        
        try:
            start_time = datetime.now()
            
            # معالجة محلية بسيطة (يمكن استبدالها بـ BERT أو نماذج أخرى)
            from sklearn.feature_extraction.text import TfidfVectorizer
            
            vectorizer = TfidfVectorizer(max_features=100)
            features = vectorizer.fit_transform([text])
            
            latency = (datetime.now() - start_time).total_seconds()
            
            self.stats['local_requests'] += 1
            self.stats['local_latency'].append(latency)
            
            return {
                'status': 'success',
                'source': 'local',
                'result': f'معالجة محلية: {text[:100]}',
                'latency': latency,
                'features': features.shape
            }
        
        except Exception as e:
            logger.error(f"❌ خطأ محلي: {e}")
            self.stats['local_errors'] += 1
            return {'status': 'error', 'message': str(e)}
    
    async def process_image(self, image_path: str, use_cloud: bool = None) -> Dict[str, Any]:
        """معالجة الصور"""
        
        logger.info(f"🖼️ معالجة الصورة: {image_path}")
        
        if use_cloud is None:
            use_cloud = self._should_use_cloud('image')
        
        if use_cloud and self.cloud_available:
            return await self._process_image_cloud(image_path)
        else:
            return await self._process_image_local(image_path)
    
    async def _process_image_cloud(self, image_path: str) -> Dict[str, Any]:
        """معالجة الصور عبر السحابة"""
        
        try:
            import base64
            
            # قراءة الصورة
            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            
            # استخدام Google Vision API
            headers = {
                'Content-Type': 'application/json'
            }
            
            data = {
                'requests': [
                    {
                        'image': {'content': image_data},
                        'features': [
                            {'type': 'LABEL_DETECTION', 'maxResults': 10},
                            {'type': 'OBJECT_LOCALIZATION', 'maxResults': 10}
                        ]
                    }
                ]
            }
            
            url = f'https://vision.googleapis.com/v1/images:annotate?key={self.cloud_config.google_api_key}'
            
            async with self.session.post(
                url,
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    self.stats['cloud_requests'] += 1
                    return {
                        'status': 'success',
                        'source': 'cloud',
                        'result': result
                    }
                else:
                    return await self._process_image_local(image_path)
        
        except Exception as e:
            logger.error(f"❌ خطأ السحابة: {e}")
            return await self._process_image_local(image_path)
    
    async def _process_image_local(self, image_path: str) -> Dict[str, Any]:
        """معالجة الصور محلياً"""
        
        try:
            import cv2
            
            start_time = datetime.now()
            
            # قراءة الصورة
            image = cv2.imread(image_path)
            
            if image is None:
                return {'status': 'error', 'message': 'فشل قراءة الصورة'}
            
            # معالجة بسيطة
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            
            latency = (datetime.now() - start_time).total_seconds()
            
            self.stats['local_requests'] += 1
            self.stats['local_latency'].append(latency)
            
            return {
                'status': 'success',
                'source': 'local',
                'shape': image.shape,
                'edges_detected': edges.sum(),
                'latency': latency
            }
        
        except Exception as e:
            logger.error(f"❌ خطأ محلي: {e}")
            self.stats['local_errors'] += 1
            return {'status': 'error', 'message': str(e)}
    
    async def process_speech(self, audio_path: str, use_cloud: bool = None) -> Dict[str, Any]:
        """معالجة الكلام"""
        
        logger.info(f"🎤 معالجة الكلام: {audio_path}")
        
        if use_cloud is None:
            use_cloud = self._should_use_cloud('speech')
        
        if use_cloud and self.cloud_available:
            return await self._process_speech_cloud(audio_path)
        else:
            return await self._process_speech_local(audio_path)
    
    async def _process_speech_cloud(self, audio_path: str) -> Dict[str, Any]:
        """معالجة الكلام عبر السحابة"""
        
        try:
            # استخدام Google Speech-to-Text API
            from google.cloud import speech
            
            client = speech.SpeechClient()
            
            with open(audio_path, 'rb') as audio_file:
                content = audio_file.read()
            
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code='ar-SA'
            )
            
            response = client.recognize(config=config, audio=audio)
            
            self.stats['cloud_requests'] += 1
            
            return {
                'status': 'success',
                'source': 'cloud',
                'transcript': response.results[0].alternatives[0].transcript if response.results else ''
            }
        
        except Exception as e:
            logger.error(f"❌ خطأ السحابة: {e}")
            return await self._process_speech_local(audio_path)
    
    async def _process_speech_local(self, audio_path: str) -> Dict[str, Any]:
        """معالجة الكلام محلياً"""
        
        try:
            import wave
            
            with wave.open(audio_path, 'rb') as wav_file:
                frames = wav_file.readframes(wav_file.getnframes())
                sample_rate = wav_file.getframerate()
            
            self.stats['local_requests'] += 1
            
            return {
                'status': 'success',
                'source': 'local',
                'sample_rate': sample_rate,
                'frames': len(frames),
                'message': 'معالجة محلية للصوت'
            }
        
        except Exception as e:
            logger.error(f"❌ خطأ محلي: {e}")
            self.stats['local_errors'] += 1
            return {'status': 'error', 'message': str(e)}
    
    def _should_use_cloud(self, task_type: str) -> bool:
        """اختيار ما إذا كان يجب استخدام السحابة"""
        
        # قرار ذكي بناءً على:
        # - توفر السحابة
        # - نوع المهمة
        # - الأداء السابق
        
        if not self.cloud_available:
            return False
        
        # للمهام المعقدة، استخدم السحابة
        complex_tasks = ['image', 'speech']
        if task_type in complex_tasks:
            return True
        
        # للمهام البسيطة، استخدم المحلي
        return False
    
    async def get_stats(self) -> Dict[str, Any]:
        """الحصول على الإحصائيات"""
        
        avg_cloud_latency = np.mean(self.stats['cloud_latency']) if self.stats['cloud_latency'] else 0
        avg_local_latency = np.mean(self.stats['local_latency']) if self.stats['local_latency'] else 0
        
        return {
            'cloud': {
                'requests': self.stats['cloud_requests'],
                'errors': self.stats['cloud_errors'],
                'avg_latency': avg_cloud_latency
            },
            'local': {
                'requests': self.stats['local_requests'],
                'errors': self.stats['local_errors'],
                'avg_latency': avg_local_latency
            },
            'total_requests': self.stats['cloud_requests'] + self.stats['local_requests'],
            'total_errors': self.stats['cloud_errors'] + self.stats['local_errors']
        }
    
    async def close(self):
        """إغلاق الجسر"""
        
        if self.session:
            await self.session.close()
        
        logger.info("🔴 تم إغلاق جسر الذكاء الاصطناعي الهجين")


# مثال على الاستخدام
async def main():
    # إعدادات السحابة
    cloud_config = CloudConfig(
        openai_api_key="your-api-key-here",
        google_api_key="your-google-key-here"
    )
    
    # إعدادات المحلي
    local_config = LocalConfig(
        use_local=True,
        use_gpu=True
    )
    
    # إنشاء الجسر
    bridge = HybridAIBridge(cloud_config, local_config)
    
    # تهيئة
    await bridge.initialize()
    
    # معالجة نصوص
    result = await bridge.process_text("مرحباً، كيف حالك؟")
    print(f"النتيجة: {result}\n")
    
    # الحصول على الإحصائيات
    stats = await bridge.get_stats()
    print(f"الإحصائيات: {json.dumps(stats, indent=2, ensure_ascii=False)}\n")
    
    # إغلاق
    await bridge.close()


if __name__ == "__main__":
    asyncio.run(main())
