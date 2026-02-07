package com.aidepin.app.ai

import android.content.Context
import android.util.Log
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File
import java.io.FileOutputStream

class LlamaEngine(private val context: Context) {
    
    companion object {
        private const val TAG = "LlamaEngine"
        
        // تحميل المكتبة الأصلية
        init {
            try {
                System.loadLibrary("llama-android")
            } catch (e: Exception) {
                Log.w(TAG, "تحذير: لم يتم تحميل مكتبة llama-android: ${e.message}")
            }
        }
    }
    
    private var modelPath: String? = null
    private var isModelLoaded = false
    private var contextPtr: Long = 0
    
    // External native functions
    private external fun nativeLoadModel(modelPath: String): Long
    private external fun nativeGenerate(
        contextPtr: Long, 
        prompt: String, 
        maxTokens: Int
    ): String
    private external fun nativeFreeModel(contextPtr: Long)
    
    suspend fun loadModel(modelName: String): Boolean = withContext(Dispatchers.IO) {
        try {
            Log.d(TAG, "جاري تحميل نموذج Llama: $modelName")
            
            // نسخ النموذج من assets إلى الذاكرة الداخلية
            val modelFile = File(context.filesDir, modelName)
            
            if (!modelFile.exists()) {
                try {
                    context.assets.open("models/$modelName").use { input ->
                        FileOutputStream(modelFile).use { output ->
                            input.copyTo(output)
                        }
                    }
                } catch (e: Exception) {
                    Log.w(TAG, "تحذير: لم يتم العثور على النموذج في assets: ${e.message}")
                }
            }
            
            modelPath = modelFile.absolutePath
            
            // تحميل النموذج
            contextPtr = nativeLoadModel(modelPath!!)
            
            if (contextPtr != 0L) {
                isModelLoaded = true
                Log.d(TAG, "✅ تم تحميل النموذج بنجاح")
                true
            } else {
                Log.e(TAG, "❌ فشل تحميل النموذج")
                false
            }
            
        } catch (e: Exception) {
            Log.e(TAG, "خطأ في تحميل النموذج: ${e.message}")
            false
        }
    }
    
    suspend fun generate(prompt: String, maxTokens: Int = 512): String = withContext(Dispatchers.IO) {
        if (!isModelLoaded) {
            return@withContext "❌ النموذج غير محمّل"
        }
        
        try {
            Log.d(TAG, "توليد نص لـ: $prompt")
            
            val systemPrompt = """
                أنت محرك ذكاء اصطناعي مدمج في تطبيق AI DePIN.
                وظيفتك هي تنسيق المهام بين نماذج AI الخارجية (OpenAI, Claude, Gemini).
                قم بتحليل طلب المستخدم وحدد:
                1. نوع المهمة (لعبة، تطبيق، استعلام)
                2. النموذج الأنسب للمهمة
                3. المعاملات المطلوبة
                
                أجب بصيغة JSON:
                {
                    "task_type": "game|app|query|chat",
                    "recommended_model": "openai|claude|gemini|local",
                    "parameters": {},
                    "response": "رد للمستخدم"
                }
            """.trimIndent()
            
            val fullPrompt = "$systemPrompt\n\nالمستخدم: $prompt\n\nالمساعد:"
            
            val response = nativeGenerate(contextPtr, fullPrompt, maxTokens)
            
            Log.d(TAG, "الرد: $response")
            response
            
        } catch (e: Exception) {
            Log.e(TAG, "خطأ في التوليد: ${e.message}")
            "حدث خطأ في معالجة الطلب"
        }
    }
    
    fun cleanup() {
        if (contextPtr != 0L) {
            try {
                nativeFreeModel(contextPtr)
            } catch (e: Exception) {
                Log.w(TAG, "تحذير: خطأ في تحرير النموذج: ${e.message}")
            }
            contextPtr = 0
            isModelLoaded = false
        }
    }
}
