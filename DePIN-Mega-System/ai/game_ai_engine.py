"""
🎮 Game AI Engine - محرك الألعاب الذكي
نظام ذكاء اصطناعي متقدم للعب الألعاب تلقائياً

يدعم:
- Fortnite, PUBG, Call of Duty, Valorant
- Computer Vision (رؤية الشاشة)
- Real-time Decision Making (اتخاذ القرارات)
- Mouse/Keyboard Control (التحكم بالفأرة والكيبورد)
- Strategy Planning (التخطيط الاستراتيجي)
"""

import asyncio
import numpy as np
from typing import Dict, List, Tuple, Optional
import cv2
from PIL import ImageGrab
import pyautogui
import time
from dataclasses import dataclass
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GameState(Enum):
    """حالات اللعبة"""
    LOADING = "loading"
    MENU = "menu"
    PLAYING = "playing"
    DEAD = "dead"
    VICTORY = "victory"
    PAUSED = "paused"


class ActionType(Enum):
    """أنواع الإجراءات"""
    MOVE_FORWARD = "move_forward"
    MOVE_BACKWARD = "move_backward"
    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"
    JUMP = "jump"
    CROUCH = "crouch"
    SHOOT = "shoot"
    AIM = "aim"
    RELOAD = "reload"
    SWITCH_WEAPON = "switch_weapon"
    USE_ABILITY = "use_ability"
    LOOK_UP = "look_up"
    LOOK_DOWN = "look_down"
    LOOK_LEFT = "look_left"
    LOOK_RIGHT = "look_right"


@dataclass
class GameAction:
    """إجراء في اللعبة"""
    action_type: ActionType
    duration: float = 0.1
    intensity: float = 1.0
    target: Optional[Tuple[int, int]] = None


@dataclass
class GameState:
    """حالة اللعبة الحالية"""
    player_health: float
    player_ammo: int
    player_position: Tuple[int, int]
    enemies_detected: List[Tuple[int, int, float]]  # (x, y, distance)
    items_visible: List[Tuple[int, int, str]]  # (x, y, item_type)
    minimap_data: np.ndarray
    screen_data: np.ndarray
    timestamp: float


class VisionSystem:
    """نظام الرؤية - Computer Vision"""
    
    def __init__(self):
        self.screen_width = 1920
        self.screen_height = 1080
        self.cascade_classifier = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
    
    async def capture_screen(self) -> np.ndarray:
        """التقط لقطة من الشاشة"""
        try:
            screenshot = ImageGrab.grab()
            frame = np.array(screenshot)
            return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        except Exception as e:
            logger.error(f"خطأ في التقاط الشاشة: {e}")
            return None
    
    async def detect_enemies(self, frame: np.ndarray) -> List[Tuple[int, int, float]]:
        """كشف الأعداء في الشاشة"""
        enemies = []
        
        # تحويل إلى HSV للكشف عن الألوان
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # نطاق اللون الأحمر (للأعداء)
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
        
        mask = cv2.inRange(hsv, lower_red, upper_red)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # حد أدنى للمساحة
                M = cv2.moments(contour)
                if M["m00"] > 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    distance = np.sqrt((cx - self.screen_width/2)**2 + (cy - self.screen_height/2)**2)
                    enemies.append((cx, cy, distance))
        
        return sorted(enemies, key=lambda x: x[2])  # ترتيب حسب المسافة
    
    async def detect_items(self, frame: np.ndarray) -> List[Tuple[int, int, str]]:
        """كشف الأغراض (أسلحة، ذخيرة، إلخ)"""
        items = []
        
        # كشف الأغراض بناءً على الألوان
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # نطاق اللون الأصفر (للأغراض)
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])
        
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:
                M = cv2.moments(contour)
                if M["m00"] > 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    items.append((cx, cy, "item"))
        
        return items
    
    async def read_health(self, frame: np.ndarray) -> float:
        """قراءة صحة اللاعب من الشاشة"""
        # البحث عن مؤشر الصحة (عادة في الزاوية السفلية اليمنى)
        roi = frame[-100:, -100:]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        # حساب النسبة المئوية للبكسلات البيضاء
        white_pixels = np.sum(thresh == 255)
        total_pixels = thresh.size
        health_percentage = (white_pixels / total_pixels) * 100
        
        return min(100, max(0, health_percentage))


class DecisionMaker:
    """نظام اتخاذ القرارات"""
    
    def __init__(self):
        self.strategy = "aggressive"  # aggressive, defensive, balanced
        self.target_priority = []
    
    async def analyze_situation(self, game_state: GameState) -> str:
        """تحليل الموقف واتخاذ قرار"""
        
        # إذا كانت الصحة منخفضة جداً
        if game_state.player_health < 20:
            return "seek_cover"
        
        # إذا كان هناك أعداء قريبين جداً
        if game_state.enemies_detected and game_state.enemies_detected[0][2] < 50:
            return "engage_combat"
        
        # إذا كانت الذخيرة منخفضة
        if game_state.player_ammo < 10:
            return "seek_ammo"
        
        # إذا كانت هناك أغراض قريبة
        if game_state.items_visible:
            return "collect_items"
        
        # البحث عن أعداء
        if not game_state.enemies_detected:
            return "explore"
        
        # الاشتباك مع الأعداء
        return "hunt_enemies"
    
    async def plan_action(self, situation: str, game_state: GameState) -> GameAction:
        """التخطيط للإجراء التالي"""
        
        if situation == "seek_cover":
            # البحث عن غطاء
            return GameAction(ActionType.MOVE_LEFT, duration=1.0)
        
        elif situation == "engage_combat":
            # الاشتباك
            if game_state.enemies_detected:
                target_x, target_y, _ = game_state.enemies_detected[0]
                return GameAction(ActionType.AIM, target=(target_x, target_y))
        
        elif situation == "seek_ammo":
            # البحث عن ذخيرة
            return GameAction(ActionType.MOVE_FORWARD, duration=0.5)
        
        elif situation == "collect_items":
            # جمع الأغراض
            if game_state.items_visible:
                item_x, item_y, _ = game_state.items_visible[0]
                return GameAction(ActionType.MOVE_FORWARD, target=(item_x, item_y))
        
        elif situation == "explore":
            # الاستكشاف
            return GameAction(ActionType.MOVE_FORWARD, duration=0.3)
        
        else:  # hunt_enemies
            # صيد الأعداء
            if game_state.enemies_detected:
                target_x, target_y, _ = game_state.enemies_detected[0]
                return GameAction(ActionType.SHOOT, target=(target_x, target_y))
        
        return GameAction(ActionType.MOVE_FORWARD, duration=0.1)


class ControlSystem:
    """نظام التحكم - Mouse/Keyboard"""
    
    def __init__(self):
        self.key_map = {
            'W': 'w',  # للأمام
            'A': 'a',  # لليسار
            'S': 's',  # للخلف
            'D': 'd',  # لليمين
            'SPACE': 'space',  # القفز
            'CTRL': 'ctrl',  # الاستقرار
            'E': 'e',  # الاستخدام
            'R': 'r',  # إعادة التحميل
        }
    
    async def execute_action(self, action: GameAction):
        """تنفيذ إجراء"""
        
        try:
            if action.action_type == ActionType.MOVE_FORWARD:
                pyautogui.press('w')
                await asyncio.sleep(action.duration)
                pyautogui.keyUp('w')
            
            elif action.action_type == ActionType.MOVE_BACKWARD:
                pyautogui.press('s')
                await asyncio.sleep(action.duration)
                pyautogui.keyUp('s')
            
            elif action.action_type == ActionType.MOVE_LEFT:
                pyautogui.press('a')
                await asyncio.sleep(action.duration)
                pyautogui.keyUp('a')
            
            elif action.action_type == ActionType.MOVE_RIGHT:
                pyautogui.press('d')
                await asyncio.sleep(action.duration)
                pyautogui.keyUp('d')
            
            elif action.action_type == ActionType.JUMP:
                pyautogui.press('space')
                await asyncio.sleep(0.1)
            
            elif action.action_type == ActionType.SHOOT:
                pyautogui.click()
                await asyncio.sleep(0.05)
            
            elif action.action_type == ActionType.AIM:
                if action.target:
                    target_x, target_y = action.target
                    pyautogui.moveTo(target_x, target_y, duration=0.1)
                    pyautogui.mouseDown()
                    await asyncio.sleep(action.duration)
                    pyautogui.mouseUp()
            
            elif action.action_type == ActionType.RELOAD:
                pyautogui.press('r')
                await asyncio.sleep(1.5)
            
            elif action.action_type == ActionType.CROUCH:
                pyautogui.press('ctrl')
                await asyncio.sleep(action.duration)
                pyautogui.keyUp('ctrl')
        
        except Exception as e:
            logger.error(f"خطأ في تنفيذ الإجراء: {e}")


class GameAIEngine:
    """محرك الألعاب الذكي الرئيسي"""
    
    def __init__(self):
        self.vision = VisionSystem()
        self.decision_maker = DecisionMaker()
        self.control = ControlSystem()
        self.is_running = False
        self.stats = {
            'kills': 0,
            'deaths': 0,
            'items_collected': 0,
            'games_played': 0,
            'wins': 0
        }
    
    async def start_game(self):
        """بدء اللعبة"""
        self.is_running = True
        logger.info("🎮 بدء محرك الألعاب الذكي")
        
        while self.is_running:
            try:
                # التقط الشاشة
                frame = await self.vision.capture_screen()
                if frame is None:
                    continue
                
                # كشف الأعداء والأغراض
                enemies = await self.vision.detect_enemies(frame)
                items = await self.vision.detect_items(frame)
                health = await self.vision.read_health(frame)
                
                # إنشاء حالة اللعبة
                game_state = GameState(
                    player_health=health,
                    player_ammo=100,  # سيتم قراءتها من الشاشة لاحقاً
                    player_position=(960, 540),  # مركز الشاشة
                    enemies_detected=enemies,
                    items_visible=items,
                    minimap_data=np.zeros((100, 100)),
                    screen_data=frame,
                    timestamp=time.time()
                )
                
                # تحليل الموقف
                situation = await self.decision_maker.analyze_situation(game_state)
                logger.info(f"📊 الموقف: {situation}")
                
                # التخطيط للإجراء
                action = await self.decision_maker.plan_action(situation, game_state)
                
                # تنفيذ الإجراء
                await self.control.execute_action(action)
                
                await asyncio.sleep(0.1)  # تأخير صغير
            
            except Exception as e:
                logger.error(f"خطأ في حلقة اللعبة: {e}")
                await asyncio.sleep(1)
    
    async def stop_game(self):
        """إيقاف اللعبة"""
        self.is_running = False
        logger.info("🛑 إيقاف محرك الألعاب الذكي")
    
    def get_stats(self) -> Dict:
        """الحصول على الإحصائيات"""
        return self.stats
    
    async def submit_task(self, task: Dict) -> Dict:
        """تقديم مهمة للمحرك"""
        
        if task.get('type') == 'play_game':
            game_name = task.get('game', 'fortnite')
            duration = task.get('duration', 3600)
            
            logger.info(f"🎮 تشغيل {game_name} لمدة {duration} ثانية")
            
            try:
                await asyncio.wait_for(self.start_game(), timeout=duration)
            except asyncio.TimeoutError:
                await self.stop_game()
            
            return {
                'status': 'completed',
                'game': game_name,
                'stats': self.stats
            }
        
        return {'status': 'error', 'message': 'مهمة غير معروفة'}


# مثال على الاستخدام
async def main():
    engine = GameAIEngine()
    
    # تشغيل لعبة Fortnite
    result = await engine.submit_task({
        'type': 'play_game',
        'game': 'fortnite',
        'duration': 600  # 10 دقائق
    })
    
    print(f"النتيجة: {result}")


if __name__ == "__main__":
    asyncio.run(main())
