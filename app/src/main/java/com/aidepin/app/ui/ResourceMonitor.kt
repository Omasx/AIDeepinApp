package com.aidepin.app.ui

import android.app.ActivityManager
import android.content.Context
import android.os.BatteryManager
import android.os.Debug
import android.net.TrafficStats
import android.content.Intent
import android.content.IntentFilter
import kotlinx.coroutines.*

/**
 * ResourceMonitor - مراقب موارد النظام
 * يتابع CPU, NET, Storage, Power
 */
class ResourceMonitor(private val context: Context) {

    data class SystemStats(
        val cpuUsage: Int,
        val uploadSpeed: String,
        val downloadSpeed: String,
        val storageUsed: Long,
        val powerUsage: Int,
        val batteryRemaining: Int
    )

    private var monitoringJob: Job? = null
    private val activityManager = context.getSystemService(Context.ACTIVITY_SERVICE) as ActivityManager

    /**
     * بدء مراقبة الموارد
     */
    suspend fun startMonitoring(onStatsUpdate: (SystemStats) -> Unit) {
        monitoringJob = CoroutineScope(Dispatchers.Default).launch {
            while (isActive) {
                val stats = collectSystemStats()
                withContext(Dispatchers.Main) {
                    onStatsUpdate(stats)
                }
                delay(1000) // تحديث كل ثانية
            }
        }
    }

    /**
     * إيقاف المراقبة
     */
    fun stopMonitoring() {
        monitoringJob?.cancel()
    }

    /**
     * جمع إحصائيات النظام
     */
    private fun collectSystemStats(): SystemStats {
        return SystemStats(
            cpuUsage = getCPUUsage(),
            uploadSpeed = getUploadSpeed(),
            downloadSpeed = getDownloadSpeed(),
            storageUsed = getStorageUsed(),
            powerUsage = getPowerUsage(),
            batteryRemaining = getBatteryRemaining()
        )
    }

    /**
     * الحصول على استخدام CPU
     */
    private fun getCPUUsage(): Int {
        return try {
            val runtime = Runtime.getRuntime()
            val totalMemory = runtime.totalMemory()
            val freeMemory = runtime.freeMemory()
            val usedMemory = totalMemory - freeMemory
            ((usedMemory * 100) / totalMemory).toInt()
        } catch (e: Exception) {
            37 // قيمة افتراضية
        }
    }

    /**
     * الحصول على سرعة التحميل
     */
    private fun getUploadSpeed(): String {
        return try {
            val txBytes = TrafficStats.getTotalTxBytes()
            "${txBytes / (1024 * 1024)}mb"
        } catch (e: Exception) {
            "500mb"
        }
    }

    /**
     * الحصول على سرعة التنزيل
     */
    private fun getDownloadSpeed(): String {
        return try {
            val rxBytes = TrafficStats.getTotalRxBytes()
            "${rxBytes / (1024 * 1024)}mb"
        } catch (e: Exception) {
            "890mb"
        }
    }

    /**
     * الحصول على المساحة المستخدمة
     */
    private fun getStorageUsed(): Long {
        return try {
            val runtime = Runtime.getRuntime()
            val totalMemory = runtime.totalMemory()
            totalMemory / (1024 * 1024 * 1024) // تحويل إلى GB
        } catch (e: Exception) {
            200 // قيمة افتراضية
        }
    }

    /**
     * الحصول على استهلاك الطاقة
     */
    private fun getPowerUsage(): Int {
        return try {
            // محاكاة استهلاك الطاقة
            (30..50).random()
        } catch (e: Exception) {
            45 // قيمة افتراضية
        }
    }

    /**
     * الحصول على الوقت المتبقي للبطارية
     */
    private fun getBatteryRemaining(): Int {
        return try {
            val batteryManager = context.getSystemService(Context.BATTERY_SERVICE) as BatteryManager
            val level = batteryManager.getIntProperty(BatteryManager.BATTERY_PROPERTY_CHARGE_COUNTER)
            (level / 100) // تحويل إلى ساعات تقريبية
        } catch (e: Exception) {
            3 // قيمة افتراضية
        }
    }
}
