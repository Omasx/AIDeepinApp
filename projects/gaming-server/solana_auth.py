"""
solana_auth.py - نظام المصادقة والدفع مع Solana

هذا الملف يحتوي على:
1. التحقق من امتلاك NFT للوصول المجاني
2. إنشاء رموز جلسة مشفرة
3. تقدير التكاليف بناءً على استهلاك البيانات
4. معالجة المعاملات على Solana
"""

import hashlib
import time
import json
import logging
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class SolanaAuth:
    """
    نظام مصادقة قائم على Solana
    
    المميزات:
    - التحقق من امتلاك NFT للوصول
    - إنشاء رموز جلسة آمنة
    - تقدير التكاليف
    - إدارة الجلسات
    """
    
    def __init__(self, network: str = "devnet"):
        """
        تهيئة نظام المصادقة
        
        Args:
            network: شبكة Solana (devnet أو mainnet)
        """
        self.network = network
        self.endpoints = {
            "mainnet": "https://api.mainnet-beta.solana.com",
            "devnet": "https://api.devnet.solana.com",
            "testnet": "https://api.testnet.solana.com"
        }
        self.rpc_url = self.endpoints.get(network, self.endpoints["devnet"])
        self.sessions: Dict[str, dict] = {}
        self.nft_holders: set = set()
        
        logger.info(f"✅ تم تهيئة SolanaAuth على شبكة {network}")
        logger.info(f"📡 RPC URL: {self.rpc_url}")
    
    def verify_nft_access(self, wallet_address: str) -> bool:
        """
        التحقق من امتلاك NFT للوصول المجاني
        
        في الإنتاج، سيتم الاتصال بـ Solana RPC للتحقق الفعلي من NFTs
        حالياً نستخدم محاكاة بسيطة
        
        Args:
            wallet_address: عنوان المحفظة
            
        Returns:
            True إذا كان المستخدم لديه حق الوصول
        """
        try:
            # محاكاة: التحقق من قائمة المحافظ المعتمدة
            # في الإنتاج، سيتم الاستعلام من Solana blockchain
            
            # للاختبار، نقبل أي محفظة تبدأ بـ "valid_"
            if wallet_address.startswith("valid_") or len(wallet_address) == 44:
                self.nft_holders.add(wallet_address)
                logger.info(f"✅ المستخدم {wallet_address[:10]}... لديه حق الوصول")
                return True
            else:
                logger.warning(f"❌ المستخدم {wallet_address[:10]}... يحتاج NFT للوصول")
                return False
                
        except Exception as e:
            logger.error(f"⚠️ خطأ في التحقق: {e}")
            return False
    
    def create_session_token(self, wallet_address: str, duration_hours: int = 1) -> Dict:
        """
        إنشاء رمز جلسة مشفر
        
        المعادلة:
        token = SHA256(wallet_address + timestamp)
        
        Args:
            wallet_address: عنوان المحفظة
            duration_hours: مدة صلاحية الرمز بالساعات
            
        Returns:
            قاموس يحتوي على:
            - token: الرمز المشفر
            - wallet: عنوان المحفظة
            - expires: وقت انتهاء الصلاحية
            - created_at: وقت الإنشاء
        """
        timestamp = int(time.time())
        
        # إنشاء الرمز
        data = f"{wallet_address}:{timestamp}".encode()
        token = hashlib.sha256(data).hexdigest()
        
        # حساب وقت الانتهاء
        expires = timestamp + (duration_hours * 3600)
        
        session_data = {
            "token": token,
            "wallet": wallet_address,
            "created_at": timestamp,
            "expires": expires,
            "duration_hours": duration_hours,
            "is_active": True
        }
        
        # تخزين الجلسة
        self.sessions[token] = session_data
        
        logger.info(f"🎫 تم إنشاء رمز جلسة للمحفظة {wallet_address[:10]}...")
        logger.info(f"   صلاحية الرمز: {duration_hours} ساعة")
        
        return session_data
    
    def verify_session_token(self, token: str) -> Tuple[bool, Optional[str]]:
        """
        التحقق من صحة رمز الجلسة
        
        Args:
            token: الرمز المراد التحقق منه
            
        Returns:
            tuple: (is_valid, wallet_address)
        """
        if token not in self.sessions:
            logger.warning(f"❌ رمز غير معروف: {token[:20]}...")
            return False, None
        
        session = self.sessions[token]
        
        # التحقق من انتهاء الصلاحية
        if int(time.time()) > session["expires"]:
            logger.warning(f"⏰ رمز منتهي الصلاحية: {token[:20]}...")
            session["is_active"] = False
            return False, None
        
        if not session["is_active"]:
            logger.warning(f"❌ رمز غير نشط: {token[:20]}...")
            return False, None
        
        logger.info(f"✅ رمز صحيح للمحفظة {session['wallet'][:10]}...")
        return True, session["wallet"]
    
    def estimate_bandwidth_cost(self, gb_per_month: float, 
                               sol_price_usd: float = 100) -> Dict:
        """
        تقدير التكلفة بناءً على استهلاك البيانات
        
        المعادلة:
        cost_sol = bandwidth_gb × price_per_gb
        cost_usd = cost_sol × sol_price_usd
        
        Args:
            gb_per_month: استهلاك البيانات بـ GB
            sol_price_usd: سعر SOL بالدولار
            
        Returns:
            قاموس يحتوي على التكاليف
        """
        # السعر الأساسي: 0.001 SOL لكل GB
        price_per_gb_sol = 0.001
        
        # حساب التكلفة
        cost_sol = gb_per_month * price_per_gb_sol
        cost_usd = cost_sol * sol_price_usd
        
        # تقدير التكلفة اليومية والساعية
        daily_gb = gb_per_month / 30
        hourly_gb = daily_gb / 24
        
        cost_per_day_sol = daily_gb * price_per_gb_sol
        cost_per_hour_sol = hourly_gb * price_per_gb_sol
        
        result = {
            "bandwidth_gb_per_month": gb_per_month,
            "price_per_gb_sol": price_per_gb_sol,
            "cost_sol_per_month": round(cost_sol, 6),
            "cost_usd_per_month": round(cost_usd, 2),
            "cost_sol_per_day": round(cost_per_day_sol, 6),
            "cost_usd_per_day": round(cost_per_day_sol * sol_price_usd, 2),
            "cost_sol_per_hour": round(cost_per_hour_sol, 6),
            "cost_usd_per_hour": round(cost_per_hour_sol * sol_price_usd, 2),
            "sol_price_usd": sol_price_usd,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"💰 تقدير التكلفة:")
        logger.info(f"   • الاستهلاك: {gb_per_month} GB/شهر")
        logger.info(f"   • التكلفة: {cost_sol:.6f} SOL (${cost_usd:.2f})/شهر")
        logger.info(f"   • التكلفة الساعية: {cost_per_hour_sol:.6f} SOL (${cost_per_hour_sol * sol_price_usd:.4f})/ساعة")
        
        return result
    
    def calculate_session_cost(self, duration_minutes: float, 
                              bitrate_mbps: float = 2.76,
                              sol_price_usd: float = 100) -> Dict:
        """
        حساب تكلفة جلسة واحدة
        
        المعادلة:
        data_transferred_gb = (bitrate_mbps × duration_minutes × 60) / 8000
        cost = data_transferred_gb × price_per_gb
        
        Args:
            duration_minutes: مدة الجلسة بالدقائق
            bitrate_mbps: معدل البت بـ Mbps
            sol_price_usd: سعر SOL بالدولار
            
        Returns:
            قاموس يحتوي على تكلفة الجلسة
        """
        # حساب البيانات المنقولة
        # Mbps × seconds / 8 = MB
        # MB / 1024 = GB
        duration_seconds = duration_minutes * 60
        data_mb = (bitrate_mbps * duration_seconds) / 8
        data_gb = data_mb / 1024
        
        # حساب التكلفة
        price_per_gb_sol = 0.001
        cost_sol = data_gb * price_per_gb_sol
        cost_usd = cost_sol * sol_price_usd
        
        result = {
            "duration_minutes": duration_minutes,
            "duration_seconds": duration_seconds,
            "bitrate_mbps": bitrate_mbps,
            "data_transferred_gb": round(data_gb, 6),
            "data_transferred_mb": round(data_mb, 2),
            "price_per_gb_sol": price_per_gb_sol,
            "cost_sol": round(cost_sol, 6),
            "cost_usd": round(cost_usd, 4),
            "sol_price_usd": sol_price_usd,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"💰 تكلفة الجلسة:")
        logger.info(f"   • المدة: {duration_minutes} دقيقة")
        logger.info(f"   • البيانات: {data_gb:.6f} GB ({data_mb:.2f} MB)")
        logger.info(f"   • التكلفة: {cost_sol:.6f} SOL (${cost_usd:.4f})")
        
        return result
    
    def get_session_info(self, token: str) -> Optional[Dict]:
        """الحصول على معلومات الجلسة"""
        if token in self.sessions:
            session = self.sessions[token]
            remaining_time = session["expires"] - int(time.time())
            return {
                **session,
                "remaining_seconds": max(0, remaining_time)
            }
        return None
    
    def revoke_session(self, token: str) -> bool:
        """إلغاء جلسة"""
        if token in self.sessions:
            self.sessions[token]["is_active"] = False
            logger.info(f"🔒 تم إلغاء الجلسة: {token[:20]}...")
            return True
        return False
    
    def get_stats(self) -> Dict:
        """الحصول على إحصائيات النظام"""
        active_sessions = sum(1 for s in self.sessions.values() if s["is_active"])
        
        return {
            "network": self.network,
            "total_sessions": len(self.sessions),
            "active_sessions": active_sessions,
            "nft_holders": len(self.nft_holders),
            "timestamp": datetime.now().isoformat()
        }


# ============================================================================
# اختبار
# ============================================================================

if __name__ == "__main__":
    import logging
    
    # إعداد logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("\n" + "="*60)
    print("🔐 اختبار نظام المصادقة Solana")
    print("="*60 + "\n")
    
    # إنشاء نظام المصادقة
    auth = SolanaAuth(network="devnet")
    
    # اختبار محفظة تجريبية
    test_wallet = "valid_11111111111111111111111111111111"
    
    print("🔍 اختبار التحقق من NFT:")
    access = auth.verify_nft_access(test_wallet)
    print(f"   النتيجة: {'✅ لديه حق الوصول' if access else '❌ بدون حق الوصول'}\n")
    
    if access:
        # إنشاء رمز جلسة
        print("🎫 إنشاء رمز جلسة:")
        session = auth.create_session_token(test_wallet, duration_hours=1)
        print(f"   الرمز: {session['token'][:32]}...")
        print(f"   الصلاحية: {session['duration_hours']} ساعة\n")
        
        # التحقق من الرمز
        print("✔️ التحقق من الرمز:")
        is_valid, wallet = auth.verify_session_token(session['token'])
        print(f"   صحيح: {is_valid}")
        print(f"   المحفظة: {wallet}\n")
    
    # تقدير التكلفة
    print("💰 تقدير التكلفة:")
    cost_monthly = auth.estimate_bandwidth_cost(300)  # 300 GB
    print(f"   الاستهلاك: {cost_monthly['bandwidth_gb_per_month']} GB/شهر")
    print(f"   التكلفة: {cost_monthly['cost_sol_per_month']:.6f} SOL (${cost_monthly['cost_usd_per_month']:.2f})/شهر")
    print(f"   التكلفة الساعية: {cost_monthly['cost_sol_per_hour']:.6f} SOL\n")
    
    # حساب تكلفة جلسة واحدة
    print("💰 تكلفة جلسة واحدة:")
    session_cost = auth.calculate_session_cost(duration_minutes=60, bitrate_mbps=2.76)
    print(f"   المدة: {session_cost['duration_minutes']} دقيقة")
    print(f"   البيانات: {session_cost['data_transferred_gb']:.6f} GB")
    print(f"   التكلفة: {session_cost['cost_sol']:.6f} SOL (${session_cost['cost_usd']:.4f})\n")
    
    # الإحصائيات
    print("📈 الإحصائيات:")
    stats = auth.get_stats()
    for key, value in stats.items():
        print(f"   • {key}: {value}")
    
    print("\n" + "="*60)
    print("✅ اكتمل الاختبار بنجاح!")
    print("="*60 + "\n")
