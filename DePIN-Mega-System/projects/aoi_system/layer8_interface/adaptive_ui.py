# adaptive_ui.py - مدير الواجهة التكيفية (Adaptive UI Manager)
import logging
from enum import Enum
from typing import Dict, Any, List

logger = logging.getLogger("AOI-AdaptiveUI")

class UIMode(Enum):
    CONSOLE = "console"   # واجهة ألعاب مع وحدات تحكم
    FLOATING = "floating"  # نافذة عائمة مع شريط دائري
    DESKTOP = "desktop"   # بيئة سطح مكتب (Windows 11 مصغرة)
    MOBILE = "mobile"     # الواجهة الأصلية

class AdaptiveUIManager:
    """
    مدير الواجهة التكيفية.
    يقوم بتوجيه وتغيير شكل النظام بناءً على نوع المهمة أو التطبيق المفتوح.
    """
    
    def __init__(self):
        self.current_mode = UIMode.MOBILE
        self.layout_config = {}
        logger.info("🎨 Adaptive UI Manager initialized.")

    async def route_ui_by_task(self, task_type: str, app_info: Dict = None) -> Dict[str, Any]:
        """
        توجيه الواجهة تلقائياً (UI Routing Logic).
        """
        previous_mode = self.current_mode
        
        if task_type == "gaming" or (app_info and app_info.get("category") == "Gaming"):
            self.current_mode = UIMode.CONSOLE
        elif task_type == "productivity" or (app_info and app_info.get("platform") in ["Windows", "macOS"]):
            self.current_mode = UIMode.DESKTOP
        elif task_type == "ai_mission":
            self.current_mode = UIMode.FLOATING
        else:
            self.current_mode = UIMode.MOBILE

        if self.current_mode != previous_mode:
            logger.info(f"🔄 UI Transition: {previous_mode.value} -> {self.current_mode.value}")
            
        return self.get_mode_layout_specs()

    def get_mode_layout_specs(self) -> Dict[str, Any]:
        """
        الحصول على تفاصيل التصميم للوضع الحالي.
        """
        specs = {
            "mode": self.current_mode.value,
            "features": [],
            "gestures": {}
        }

        if self.current_mode == UIMode.CONSOLE:
            specs["features"] = ["virtual_joystick", "haptic_feedback", "3d_touch_triggers"]
            specs["gestures"] = {"bottom_swipe": "quick_controls"}
            
        elif self.current_mode == UIMode.FLOATING:
            specs["features"] = ["circular_toolbar", "translucency", "always_on_top"]
            specs["gestures"] = {
                "3_finger_drag": "move_window",
                "2_finger_pinch": "resize_window",
                "4_finger_tap": "quick_menu"
            }
            
        elif self.current_mode == UIMode.DESKTOP:
            specs["features"] = ["top_taskbar", "start_menu", "multi_window", "drag_and_drop"]
            specs["gestures"] = {"edge_swipe": "switch_apps"}

        return specs

    def set_custom_mode(self, mode_name: str):
        try:
            self.current_mode = UIMode(mode_name.lower())
            return True
        except ValueError:
            return False
