package com.aidepin.app.services

import android.content.Context
import android.util.Log
import kotlinx.coroutines.*
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

/**
 * AIAgentService - خدمة الوكيل الذكي
 * تتعامل مع تنفيذ الأوامر والاتصال بالسيرفر
 */
class AIAgentService(private val context: Context) {

    companion object {
        private const val TAG = "AIAgentService"
        private const val API_BASE_URL = "http://localhost:8000/api/"
    }

    private val httpClient = OkHttpClient.Builder()
        .connectTimeout(30, java.util.concurrent.TimeUnit.SECONDS)
        .readTimeout(30, java.util.concurrent.TimeUnit.SECONDS)
        .build()

    private val retrofit = Retrofit.Builder()
        .baseUrl(API_BASE_URL)
        .client(httpClient)
        .addConverterFactory(GsonConverterFactory.create())
        .build()

    private val apiService = retrofit.create(AIAgentAPI::class.java)

    /**
     * بدء الوكيل الذكي (DeOS Kernel)
     */
    suspend fun startAgent() {
        try {
            Log.d(TAG, "🚀 تفعيل نظام DeOS المستقل...")

            // طلب تفعيل النواة من السيرفر
            val response = apiService.executeCommand(
                mapOf(
                    "command" to "start_deos_kernel",
                    "mode" to "autonomous_24_7"
                )
            )

            if (response.isSuccessful) {
                Log.d(TAG, "✅ نظام DeOS يعمل الآن في الخلفية")
            } else {
                Log.e(TAG, "❌ فشل تفعيل DeOS")
            }

            Log.d(TAG, "🤖 بدء الوكيل الذكي...")
            
            // الاتصال بالسيرفر
            val response = apiService.executeCommand(
                mapOf(
                    "command" to "أنشئ مشروع جديد",
                    "user_id" to "mobile_user"
                )
            )

            if (response.isSuccessful) {
                Log.d(TAG, "✅ تم تنفيذ الأمر بنجاح")
            } else {
                Log.e(TAG, "❌ فشل تنفيذ الأمر: ${response.errorBody()}")
            }
        } catch (e: Exception) {
            Log.e(TAG, "❌ خطأ: ${e.message}")
        }
    }

    /**
     * تنفيذ أمر مخصص
     */
    suspend fun executeCommand(command: String) {
        try {
            Log.d(TAG, "📤 تنفيذ أمر: $command")
            
            val response = apiService.executeCommand(
                mapOf(
                    "command" to command,
                    "user_id" to "mobile_user"
                )
            )

            if (response.isSuccessful) {
                Log.d(TAG, "✅ تم التنفيذ بنجاح")
            } else {
                Log.e(TAG, "❌ فشل التنفيذ")
            }
        } catch (e: Exception) {
            Log.e(TAG, "❌ خطأ: ${e.message}")
        }
    }

    /**
     * الحصول على حالة المشروع
     */
    suspend fun getProjectStatus(projectId: String) {
        try {
            Log.d(TAG, "📊 الحصول على حالة المشروع: $projectId")
            
            val response = apiService.getProjectStatus(projectId)

            if (response.isSuccessful) {
                Log.d(TAG, "✅ تم الحصول على الحالة")
            } else {
                Log.e(TAG, "❌ فشل الحصول على الحالة")
            }
        } catch (e: Exception) {
            Log.e(TAG, "❌ خطأ: ${e.message}")
        }
    }
}
