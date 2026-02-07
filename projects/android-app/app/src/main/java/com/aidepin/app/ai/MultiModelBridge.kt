package com.aidepin.app.ai

import android.util.Log
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException

class MultiModelBridge {
    
    companion object {
        private const val TAG = "MultiModelBridge"
    }
    
    private val client = OkHttpClient.Builder()
        .connectTimeout(60, java.util.concurrent.TimeUnit.SECONDS)
        .readTimeout(60, java.util.concurrent.TimeUnit.SECONDS)
        .build()
    
    private val apiEndpoints = mapOf(
        "openai" to "https://api.openai.com/v1/chat/completions",
        "anthropic" to "https://api.anthropic.com/v1/messages",
        "google" to "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
        "deepseek" to "https://api.deepseek.com/v1/chat/completions"
    )
    
    private val apiKeys = mutableMapOf<String, String>()
    
    fun initialize(keys: Map<String, String>) {
        apiKeys.clear()
        apiKeys.putAll(keys)
        Log.d(TAG, "تم تهيئة MultiModelBridge مع ${keys.size} مفاتيح API")
    }
    
    suspend fun generateCode(model: String, apiKey: String, prompt: String): String = 
        withContext(Dispatchers.IO) {
            try {
                Log.d(TAG, "توليد كود باستخدام: $model")
                
                val enhancedPrompt = """
                    أنت مهندس برمجيات متخصص. قم بكتابة كود عالي الجودة.
                    
                    الطلب: $prompt
                    
                    الكود:
                """.trimIndent()
                
                when (model) {
                    "openai" -> queryOpenAI(apiKey, enhancedPrompt)
                    "anthropic" -> queryAnthropic(apiKey, enhancedPrompt)
                    "google" -> queryGoogle(apiKey, enhancedPrompt)
                    "deepseek" -> queryDeepSeek(apiKey, enhancedPrompt)
                    else -> "❌ نموذج غير مدعوم: $model"
                }
            } catch (e: Exception) {
                Log.e(TAG, "خطأ في توليد الكود: ${e.message}")
                "❌ خطأ: ${e.message}"
            }
        }
    
    suspend fun query(model: String, apiKey: String, prompt: String): String = 
        withContext(Dispatchers.IO) {
            try {
                Log.d(TAG, "الاستعلام من: $model")
                
                when (model) {
                    "openai" -> queryOpenAI(apiKey, prompt)
                    "anthropic" -> queryAnthropic(apiKey, prompt)
                    "google" -> queryGoogle(apiKey, prompt)
                    "deepseek" -> queryDeepSeek(apiKey, prompt)
                    else -> "❌ نموذج غير مدعوم: $model"
                }
            } catch (e: Exception) {
                Log.e(TAG, "خطأ في الاستعلام: ${e.message}")
                "❌ خطأ: ${e.message}"
            }
        }
    
    private fun queryOpenAI(apiKey: String, prompt: String): String {
        try {
            val requestBody = JSONObject().apply {
                put("model", "gpt-4")
                put("messages", JSONArray().apply {
                    put(JSONObject().apply {
                        put("role", "user")
                        put("content", prompt)
                    })
                })
                put("temperature", 0.7)
                put("max_tokens", 2000)
            }.toString().toRequestBody("application/json".toMediaType())
            
            val request = Request.Builder()
                .url(apiEndpoints["openai"]!!)
                .header("Authorization", "Bearer $apiKey")
                .post(requestBody)
                .build()
            
            val response = client.newCall(request).execute()
            
            if (response.isSuccessful) {
                val json = JSONObject(response.body?.string() ?: "{}")
                val choices = json.optJSONArray("choices")
                if (choices != null && choices.length() > 0) {
                    val message = choices.getJSONObject(0).getJSONObject("message")
                    return message.getString("content")
                }
            }
            
            return "❌ خطأ من OpenAI: ${response.code}"
        } catch (e: Exception) {
            Log.e(TAG, "خطأ في OpenAI: ${e.message}")
            return "❌ خطأ: ${e.message}"
        }
    }
    
    private fun queryAnthropic(apiKey: String, prompt: String): String {
        try {
            val requestBody = JSONObject().apply {
                put("model", "claude-3-opus-20240229")
                put("max_tokens", 2000)
                put("messages", JSONArray().apply {
                    put(JSONObject().apply {
                        put("role", "user")
                        put("content", prompt)
                    })
                })
            }.toString().toRequestBody("application/json".toMediaType())
            
            val request = Request.Builder()
                .url(apiEndpoints["anthropic"]!!)
                .header("x-api-key", apiKey)
                .header("anthropic-version", "2023-06-01")
                .post(requestBody)
                .build()
            
            val response = client.newCall(request).execute()
            
            if (response.isSuccessful) {
                val json = JSONObject(response.body?.string() ?: "{}")
                val content = json.optJSONArray("content")
                if (content != null && content.length() > 0) {
                    return content.getJSONObject(0).getString("text")
                }
            }
            
            return "❌ خطأ من Anthropic: ${response.code}"
        } catch (e: Exception) {
            Log.e(TAG, "خطأ في Anthropic: ${e.message}")
            return "❌ خطأ: ${e.message}"
        }
    }
    
    private fun queryGoogle(apiKey: String, prompt: String): String {
        try {
            val requestBody = JSONObject().apply {
                put("contents", JSONArray().apply {
                    put(JSONObject().apply {
                        put("parts", JSONArray().apply {
                            put(JSONObject().apply {
                                put("text", prompt)
                            })
                        })
                    })
                })
            }.toString().toRequestBody("application/json".toMediaType())
            
            val url = "${apiEndpoints["google"]}?key=$apiKey"
            
            val request = Request.Builder()
                .url(url)
                .post(requestBody)
                .build()
            
            val response = client.newCall(request).execute()
            
            if (response.isSuccessful) {
                val json = JSONObject(response.body?.string() ?: "{}")
                val candidates = json.optJSONArray("candidates")
                if (candidates != null && candidates.length() > 0) {
                    val content = candidates.getJSONObject(0).getJSONArray("content")
                    if (content.length() > 0) {
                        return content.getJSONObject(0).getString("text")
                    }
                }
            }
            
            return "❌ خطأ من Google: ${response.code}"
        } catch (e: Exception) {
            Log.e(TAG, "خطأ في Google: ${e.message}")
            return "❌ خطأ: ${e.message}"
        }
    }
    
    private fun queryDeepSeek(apiKey: String, prompt: String): String {
        try {
            val requestBody = JSONObject().apply {
                put("model", "deepseek-chat")
                put("messages", JSONArray().apply {
                    put(JSONObject().apply {
                        put("role", "user")
                        put("content", prompt)
                    })
                })
                put("temperature", 0.7)
            }.toString().toRequestBody("application/json".toMediaType())
            
            val request = Request.Builder()
                .url(apiEndpoints["deepseek"]!!)
                .header("Authorization", "Bearer $apiKey")
                .post(requestBody)
                .build()
            
            val response = client.newCall(request).execute()
            
            if (response.isSuccessful) {
                val json = JSONObject(response.body?.string() ?: "{}")
                val choices = json.optJSONArray("choices")
                if (choices != null && choices.length() > 0) {
                    val message = choices.getJSONObject(0).getJSONObject("message")
                    return message.getString("content")
                }
            }
            
            return "❌ خطأ من DeepSeek: ${response.code}"
        } catch (e: Exception) {
            Log.e(TAG, "خطأ في DeepSeek: ${e.message}")
            return "❌ خطأ: ${e.message}"
        }
    }
}
