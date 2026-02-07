package com.aidepin.app.ai

import android.content.Context
import android.util.Log
import com.aidepin.app.models.Task
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject

class AIAgentManager(
    private val context: Context,
    private val llamaEngine: LlamaEngine
) {
    
    companion object {
        private const val TAG = "AIAgentManager"
    }
    
    private val apiKeys = mutableMapOf<String, String>()
    private val multiModelBridge = MultiModelBridge()
    
    fun setAPIKeys(keys: Map<String, String>) {
        apiKeys.clear()
        apiKeys.putAll(keys)
        multiModelBridge.initialize(keys)
    }
    
    suspend fun executeCommand(command: String): Task = withContext(Dispatchers.IO) {
        Log.d(TAG, "تنفيذ الأمر: $command")
        
        // المرحلة 1: تحليل الأمر باستخدام Llama المحلي
        val analysis = llamaEngine.generate(command)
        
        val task = parseAnalysis(analysis, command)
        
        // المرحلة 2: تنفيذ المهمة بالنموذج المناسب
        when (task.taskType) {
            "game" -> handleGameTask(task)
            "app" -> handleAppCreationTask(task)
            "query" -> handleQueryTask(task)
            "chat" -> handleChatTask(task)
            else -> task.copy(
                status = "unknown",
                response = "لم أفهم الأمر"
            )
        }
    }
    
    private fun parseAnalysis(analysis: String, originalCommand: String): Task {
        return try {
            // استخراج JSON من الرد
            val jsonStart = analysis.indexOf("{")
            val jsonEnd = analysis.lastIndexOf("}") + 1
            
            if (jsonStart != -1 && jsonEnd > jsonStart) {
                val jsonStr = analysis.substring(jsonStart, jsonEnd)
                val json = JSONObject(jsonStr)
                
                Task(
                    id = System.currentTimeMillis().toString(),
                    command = originalCommand,
                    taskType = json.getString("task_type"),
                    recommendedModel = json.getString("recommended_model"),
                    parameters = json.optJSONObject("parameters")?.toString() ?: "{}",
                    response = json.optString("response", ""),
                    status = "pending",
                    progress = 0
                )
            } else {
                // fallback - تحليل بسيط
                simpleAnalysis(originalCommand)
            }
        } catch (e: Exception) {
            Log.e(TAG, "خطأ في تحليل JSON: ${e.message}")
            simpleAnalysis(originalCommand)
        }
    }
    
    private fun simpleAnalysis(command: String): Task {
        val lowerCommand = command.lowercase()
        
        val taskType = when {
            "fortnite" in lowerCommand || "لعبة" in lowerCommand || "العب" in lowerCommand -> "game"
            "اصنع" in lowerCommand || "تطبيق" in lowerCommand || "موقع" in lowerCommand -> "app"
            "اقرأ" in lowerCommand || "شاشة" in lowerCommand -> "query"
            else -> "chat"
        }
        
        return Task(
            id = System.currentTimeMillis().toString(),
            command = command,
            taskType = taskType,
            recommendedModel = "local",
            parameters = "{}",
            response = "",
            status = "pending",
            progress = 0
        )
    }
    
    private suspend fun handleGameTask(task: Task): Task {
        // تشغيل اللعبة
        return task.copy(
            status = "processing",
            response = "جاري تحميل اللعبة من DePIN Network...",
            progress = 25
        )
    }
    
    private suspend fun handleAppCreationTask(task: Task): Task {
        // استخدام النموذج الخارجي لإنشاء الكود
        val model = task.recommendedModel
        
        return if (apiKeys.containsKey(model)) {
            val code = multiModelBridge.generateCode(
                model = model,
                apiKey = apiKeys[model]!!,
                prompt = task.command
            )
            
            task.copy(
                status = "completed",
                response = "✅ تم إنشاء التطبيق!",
                progress = 100,
                parameters = code
            )
        } else {
            task.copy(
                status = "error",
                response = "⚠️ مفتاح API غير متوفر للنموذج: $model"
            )
        }
    }
    
    private suspend fun handleQueryTask(task: Task): Task {
        // استعلام عادي
        val model = task.recommendedModel
        
        val response = if (model == "local") {
            llamaEngine.generate(task.command)
        } else if (apiKeys.containsKey(model)) {
            multiModelBridge.query(
                model = model,
                apiKey = apiKeys[model]!!,
                prompt = task.command
            )
        } else {
            "لا يوجد مفتاح API"
        }
        
        return task.copy(
            status = "completed",
            response = response,
            progress = 100
        )
    }
    
    private suspend fun handleChatTask(task: Task): Task {
        return handleQueryTask(task)
    }
}
