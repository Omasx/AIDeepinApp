package com.aidepin.app

import android.os.Bundle
import android.widget.Button
import android.widget.ImageButton
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.aidepin.app.services.AIAgentService
import com.aidepin.app.services.DePINNetworkService
import com.aidepin.app.ui.ResourceMonitor
import kotlinx.coroutines.launch

/**
 * MainActivity - الشاشة الرئيسية للتطبيق
 * تعرض الموارد والتصور ثلاثي الأبعاد والأزرار الرئيسية
 */
class MainActivity : AppCompatActivity() {

    private lateinit var aiAgentService: AIAgentService
    private lateinit var depinNetworkService: DePINNetworkService
    private lateinit var resourceMonitor: ResourceMonitor

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        initializeServices()
        setupUI()
        startMonitoring()
    }

    /**
     * تهيئة الخدمات
     */
    private fun initializeServices() {
        aiAgentService = AIAgentService(this)
        depinNetworkService = DePINNetworkService(this)
        resourceMonitor = ResourceMonitor(this)
    }

    /**
     * إعداد واجهة المستخدم
     */
    private fun setupUI() {
        // Settings Button
        findViewById<ImageButton>(R.id.settings_btn).setOnClickListener {
            openSettings()
        }

        // Navigation Buttons
        findViewById<Button>(R.id.btn_code).setOnClickListener {
            openCodeEditor()
        }

        findViewById<Button>(R.id.btn_data).setOnClickListener {
            openDataManager()
        }

        findViewById<Button>(R.id.btn_test).setOnClickListener {
            openTestRunner()
        }

        findViewById<Button>(R.id.btn_deploy).setOnClickListener {
            openDeployment()
        }

        // Task Scheduler Buttons
        findViewById<Button>(R.id.btn_schedule_task).setOnClickListener {
            showScheduleTaskDialog()
        }

        findViewById<Button>(R.id.btn_view_scheduled).setOnClickListener {
            viewScheduledTasks()
        }

        // AI Agent Button
        findViewById<ImageButton>(R.id.ai_agent_btn).setOnClickListener {
            activateAIAgent()
        }
    }

    /**
     * بدء مراقبة الموارد
     */
    private fun startMonitoring() {
        lifecycleScope.launch {
            resourceMonitor.startMonitoring { stats ->
                updateStatsDisplay(stats)
            }
        }
    }

    /**
     * تحديث عرض الإحصائيات
     */
    private fun updateStatsDisplay(stats: ResourceMonitor.SystemStats) {
        findViewById<TextView>(R.id.cpu_text).text = "CPU: ${stats.cpuUsage}%"
        findViewById<TextView>(R.id.net_text).text = "NET: ↑${stats.uploadSpeed} ↓${stats.downloadSpeed}"
        findViewById<TextView>(R.id.storage_text).text = "STOR: ${stats.storageUsed}GB Used"
        findViewById<TextView>(R.id.power_text).text = "PWR: ${stats.powerUsage}W (${stats.batteryRemaining}h rem)"
    }

    /**
     * فتح محرر الأكواد
     */
    private fun openCodeEditor() {
        // TODO: تطبيق محرر الأكواد
    }

    /**
     * فتح مدير البيانات
     */
    private fun openDataManager() {
        // TODO: تطبيق مدير البيانات
    }

    /**
     * فتح مشغل الاختبارات
     */
    private fun openTestRunner() {
        // TODO: تطبيق مشغل الاختبارات
    }

    /**
     * فتح النشر
     */
    private fun openDeployment() {
        // TODO: تطبيق النشر
    }

    /**
     * تفعيل وكيل AI
     */
    private fun activateAIAgent() {
        lifecycleScope.launch {
            aiAgentService.startAgent()
        }
    }

    /**
     * فتح الإعدادات
     */
    private fun openSettings() {
        // TODO: تطبيق الإعدادات
    }

    /**
     * عرض ديالوج جدولة مهمة
     */
    private fun showScheduleTaskDialog() {
        // TODO: تطبيق DatePickerDialog و TimePickerDialog
        // محاكاة إرسال مهمة مجدولة للسيرفر
        lifecycleScope.launch {
            aiAgentService.executeCommand("schedule_task: [Name: Audit, Time: 2026-02-08T10:00:00]")
        }
    }

    /**
     * عرض كافة المهام المجدولة
     */
    private fun viewScheduledTasks() {
        // TODO: عرض قائمة المهام في RecyclerView
    }

    override fun onDestroy() {
        super.onDestroy()
        resourceMonitor.stopMonitoring()
    }
}
