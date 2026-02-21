#!/usr/bin/env python3
"""
🚀 تشغيل نظام الذكاء الاصطناعي المتكامل الفعلي
Run the Integrated AI System

استخدام:
    python run_integrated_system.py
"""

import asyncio
import sys
import os

# إضافة المسار
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ai'))

from ai.integrated_ai_system import IntegratedAISystem, interactive_cli


async def main():
    """البرنامج الرئيسي"""
    
    print("\n" + "="*70)
    print("🚀 نظام الذكاء الاصطناعي المتكامل الفعلي")
    print("Integrated AI System v1.0")
    print("="*70 + "\n")
    
    # إنشاء النظام
    system = IntegratedAISystem()
    
    try:
        # تهيئة
        print("🔧 جاري التهيئة...")
        init_result = await system.initialize()
        
        if init_result.get('status') == 'error':
            print(f"❌ خطأ في التهيئة: {init_result.get('message')}")
            return
        
        print("✅ تم التهيئة بنجاح\n")
        
        # بدء النظام
        print("🟢 جاري البدء...")
        start_result = await system.start()
        print(f"✅ {start_result.get('status')}\n")
        
        # واجهة سطر الأوامر
        await interactive_cli(system)
    
    except KeyboardInterrupt:
        print("\n\n⏹️ تم الإيقاف بواسطة المستخدم")
        await system.stop()
    
    except Exception as e:
        print(f"\n❌ خطأ: {e}")
        await system.stop()
    
    finally:
        print("\n" + "="*70)
        print("👋 شكراً لاستخدام النظام!")
        print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
