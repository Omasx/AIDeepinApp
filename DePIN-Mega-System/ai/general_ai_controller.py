"""
🤖 General AI Controller - متحكم ذكي عام
نظام ذكاء اصطناعي متقدم للتحكم في التطبيقات والأنظمة

يدعم:
- فهم الأوامر الطبيعية
- التحكم في التطبيقات
- تصفح الإنترنت
- كتابة الأكواد
- إدارة الملفات
- تنفيذ المهام المعقدة
"""

import asyncio
import json
import subprocess
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging
import re
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CommandType(Enum):
    """أنواع الأوامر"""
    OPEN_APP = "open_app"
    CLOSE_APP = "close_app"
    BROWSE_WEB = "browse_web"
    WRITE_CODE = "write_code"
    EXECUTE_CODE = "execute_code"
    MANAGE_FILES = "manage_files"
    SYSTEM_CONTROL = "system_control"
    PLAY_GAME = "play_game"
    SEARCH_INFO = "search_info"
    SEND_MESSAGE = "send_message"


@dataclass
class Command:
    """أمر للتنفيذ"""
    command_type: CommandType
    target: str
    parameters: Dict[str, Any]
    priority: int = 5
    timestamp: float = None


class NLPProcessor:
    """معالج اللغة الطبيعية"""
    
    def __init__(self):
        self.command_patterns = {
            r'افتح|open|launch': CommandType.OPEN_APP,
            r'أغلق|close|quit': CommandType.CLOSE_APP,
            r'ابحث|search|google': CommandType.SEARCH_INFO,
            r'اكتب|write|code': CommandType.WRITE_CODE,
            r'نفذ|execute|run': CommandType.EXECUTE_CODE,
            r'العب|play|game': CommandType.PLAY_GAME,
            r'أرسل|send|message': CommandType.SEND_MESSAGE,
        }
        
        self.app_aliases = {
            'فايرفوكس': 'firefox',
            'كروم': 'google-chrome',
            'فيجوال': 'code',
            'نوتباد': 'notepad',
            'فايل': 'explorer',
            'ترمينال': 'terminal',
            'بايثون': 'python',
            'جافا': 'java',
        }
    
    async def parse_command(self, user_input: str) -> Optional[Command]:
        """تحليل أمر من المستخدم"""
        
        user_input = user_input.lower().strip()
        
        # تحديد نوع الأمر
        command_type = None
        for pattern, cmd_type in self.command_patterns.items():
            if re.search(pattern, user_input):
                command_type = cmd_type
                break
        
        if not command_type:
            return None
        
        # استخراج الهدف
        target = self._extract_target(user_input, command_type)
        
        # استخراج المعاملات
        parameters = self._extract_parameters(user_input, command_type)
        
        return Command(
            command_type=command_type,
            target=target,
            parameters=parameters,
            timestamp=datetime.now().timestamp()
        )
    
    def _extract_target(self, text: str, command_type: CommandType) -> str:
        """استخراج الهدف من النص"""
        
        if command_type == CommandType.OPEN_APP:
            for alias, app_name in self.app_aliases.items():
                if alias in text:
                    return app_name
            # محاولة استخراج اسم التطبيق
            words = text.split()
            for word in words:
                if len(word) > 2:
                    return word
        
        elif command_type == CommandType.SEARCH_INFO:
            # استخراج كلمات البحث
            search_words = text.replace('ابحث', '').replace('search', '').strip()
            return search_words
        
        elif command_type == CommandType.PLAY_GAME:
            game_names = ['fortnite', 'pubg', 'valorant', 'minecraft', 'roblox']
            for game in game_names:
                if game in text:
                    return game
        
        return "unknown"
    
    def _extract_parameters(self, text: str, command_type: CommandType) -> Dict:
        """استخراج المعاملات من النص"""
        
        params = {}
        
        if command_type == CommandType.OPEN_APP:
            params['fullscreen'] = 'ملء' in text or 'fullscreen' in text
            params['admin'] = 'إداري' in text or 'admin' in text
        
        elif command_type == CommandType.WRITE_CODE:
            params['language'] = self._detect_language(text)
            params['filename'] = self._extract_filename(text)
        
        elif command_type == CommandType.PLAY_GAME:
            params['duration'] = self._extract_duration(text)
            params['difficulty'] = self._extract_difficulty(text)
        
        return params
    
    def _detect_language(self, text: str) -> str:
        """كشف لغة البرمجة"""
        languages = {
            'python': ['بايثون', 'python'],
            'javascript': ['جافا سكريبت', 'javascript'],
            'java': ['جافا', 'java'],
            'cpp': ['سي بلس', 'c++'],
            'csharp': ['سي شارب', 'c#'],
        }
        
        for lang, keywords in languages.items():
            for keyword in keywords:
                if keyword in text:
                    return lang
        
        return 'python'
    
    def _extract_filename(self, text: str) -> str:
        """استخراج اسم الملف"""
        # البحث عن أسماء الملفات
        match = re.search(r'(\w+\.\w+)', text)
        if match:
            return match.group(1)
        return 'output.txt'
    
    def _extract_duration(self, text: str) -> int:
        """استخراج المدة"""
        match = re.search(r'(\d+)\s*(ساعة|hour|دقيقة|minute|ثانية|second)', text)
        if match:
            duration = int(match.group(1))
            unit = match.group(2)
            
            if 'ساعة' in unit or 'hour' in unit:
                return duration * 3600
            elif 'دقيقة' in unit or 'minute' in unit:
                return duration * 60
            else:
                return duration
        
        return 3600  # ساعة واحدة افتراضياً
    
    def _extract_difficulty(self, text: str) -> str:
        """استخراج مستوى الصعوبة"""
        if 'سهل' in text or 'easy' in text:
            return 'easy'
        elif 'متوسط' in text or 'medium' in text:
            return 'medium'
        elif 'صعب' in text or 'hard' in text:
            return 'hard'
        else:
            return 'medium'


class ApplicationManager:
    """مدير التطبيقات"""
    
    def __init__(self):
        self.running_apps = {}
    
    async def open_app(self, app_name: str, parameters: Dict) -> Dict:
        """فتح تطبيق"""
        
        try:
            logger.info(f"📱 فتح التطبيق: {app_name}")
            
            cmd = [app_name]
            
            if parameters.get('fullscreen'):
                cmd.append('--fullscreen')
            
            process = subprocess.Popen(cmd)
            self.running_apps[app_name] = process
            
            return {
                'status': 'success',
                'app': app_name,
                'pid': process.pid
            }
        
        except Exception as e:
            logger.error(f"خطأ في فتح التطبيق: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    async def close_app(self, app_name: str) -> Dict:
        """إغلاق تطبيق"""
        
        try:
            if app_name in self.running_apps:
                process = self.running_apps[app_name]
                process.terminate()
                del self.running_apps[app_name]
                
                logger.info(f"✅ تم إغلاق: {app_name}")
                return {'status': 'success', 'app': app_name}
            
            return {'status': 'error', 'message': 'التطبيق غير مفتوح'}
        
        except Exception as e:
            logger.error(f"خطأ في إغلاق التطبيق: {e}")
            return {'status': 'error', 'message': str(e)}


class WebBrowser:
    """متصفح الويب الذكي"""
    
    async def search(self, query: str) -> Dict:
        """البحث على الإنترنت"""
        
        logger.info(f"🔍 البحث عن: {query}")
        
        try:
            # استخدام Google Search API
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            
            subprocess.Popen(['google-chrome', search_url])
            
            return {
                'status': 'success',
                'query': query,
                'url': search_url
            }
        
        except Exception as e:
            logger.error(f"خطأ في البحث: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def browse(self, url: str) -> Dict:
        """تصفح موقع ويب"""
        
        logger.info(f"🌐 تصفح: {url}")
        
        try:
            subprocess.Popen(['google-chrome', url])
            
            return {
                'status': 'success',
                'url': url
            }
        
        except Exception as e:
            logger.error(f"خطأ في التصفح: {e}")
            return {'status': 'error', 'message': str(e)}


class CodeExecutor:
    """منفذ الأكواد"""
    
    async def write_code(self, code: str, language: str, filename: str) -> Dict:
        """كتابة كود"""
        
        logger.info(f"📝 كتابة كود {language}")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(code)
            
            return {
                'status': 'success',
                'filename': filename,
                'lines': len(code.split('\n'))
            }
        
        except Exception as e:
            logger.error(f"خطأ في كتابة الكود: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def execute_code(self, filename: str, language: str) -> Dict:
        """تنفيذ كود"""
        
        logger.info(f"▶️ تنفيذ: {filename}")
        
        try:
            if language == 'python':
                result = subprocess.run(['python3', filename], capture_output=True, text=True)
            elif language == 'javascript':
                result = subprocess.run(['node', filename], capture_output=True, text=True)
            else:
                return {'status': 'error', 'message': 'لغة غير مدعومة'}
            
            return {
                'status': 'success',
                'output': result.stdout,
                'error': result.stderr
            }
        
        except Exception as e:
            logger.error(f"خطأ في تنفيذ الكود: {e}")
            return {'status': 'error', 'message': str(e)}


class FileManager:
    """مدير الملفات"""
    
    async def create_file(self, path: str, content: str) -> Dict:
        """إنشاء ملف"""
        
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"📄 تم إنشاء: {path}")
            return {'status': 'success', 'path': path}
        
        except Exception as e:
            logger.error(f"خطأ في إنشاء الملف: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def delete_file(self, path: str) -> Dict:
        """حذف ملف"""
        
        try:
            import os
            os.remove(path)
            
            logger.info(f"🗑️ تم حذف: {path}")
            return {'status': 'success', 'path': path}
        
        except Exception as e:
            logger.error(f"خطأ في حذف الملف: {e}")
            return {'status': 'error', 'message': str(e)}


class GeneralAIController:
    """متحكم ذكي عام"""
    
    def __init__(self):
        self.nlp = NLPProcessor()
        self.app_manager = ApplicationManager()
        self.browser = WebBrowser()
        self.code_executor = CodeExecutor()
        self.file_manager = FileManager()
        self.command_history = []
    
    async def process_command(self, user_input: str) -> Dict:
        """معالجة أمر من المستخدم"""
        
        logger.info(f"📥 أمر: {user_input}")
        
        # تحليل الأمر
        command = await self.nlp.parse_command(user_input)
        
        if not command:
            return {'status': 'error', 'message': 'لم أفهم الأمر'}
        
        # تسجيل الأمر
        self.command_history.append(command)
        
        # تنفيذ الأمر
        result = await self._execute_command(command)
        
        return result
    
    async def _execute_command(self, command: Command) -> Dict:
        """تنفيذ أمر"""
        
        if command.command_type == CommandType.OPEN_APP:
            return await self.app_manager.open_app(command.target, command.parameters)
        
        elif command.command_type == CommandType.CLOSE_APP:
            return await self.app_manager.close_app(command.target)
        
        elif command.command_type == CommandType.SEARCH_INFO:
            return await self.browser.search(command.target)
        
        elif command.command_type == CommandType.WRITE_CODE:
            # يتطلب كود إضافي
            return {'status': 'pending', 'message': 'جاهز لكتابة الكود'}
        
        elif command.command_type == CommandType.EXECUTE_CODE:
            return await self.code_executor.execute_code(
                command.target,
                command.parameters.get('language', 'python')
            )
        
        else:
            return {'status': 'error', 'message': 'نوع أمر غير مدعوم'}
    
    async def submit_task(self, task: Dict) -> Dict:
        """تقديم مهمة"""
        
        if task.get('type') == 'command':
            return await self.process_command(task.get('command', ''))
        
        elif task.get('type') == 'sequence':
            results = []
            for cmd in task.get('commands', []):
                result = await self.process_command(cmd)
                results.append(result)
            
            return {
                'status': 'completed',
                'results': results
            }
        
        return {'status': 'error', 'message': 'نوع مهمة غير معروف'}
    
    def get_history(self) -> List[Command]:
        """الحصول على سجل الأوامر"""
        return self.command_history


# مثال على الاستخدام
async def main():
    controller = GeneralAIController()
    
    # أمثلة على الأوامر
    commands = [
        "افتح فايرفوكس",
        "ابحث عن معلومات عن الذكاء الاصطناعي",
        "اكتب كود بايثون",
    ]
    
    for cmd in commands:
        result = await controller.process_command(cmd)
        print(f"النتيجة: {result}")
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
