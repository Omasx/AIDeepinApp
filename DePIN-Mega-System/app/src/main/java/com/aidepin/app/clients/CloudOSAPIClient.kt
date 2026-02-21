package com.aidepin.app.clients

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.util.concurrent.TimeUnit

class CloudOSAPIClient {
    private val client = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(120, TimeUnit.SECONDS)
        .build()
    
    private var apiUrl = "http://localhost:8080"

    suspend fun createCloudVM(specs: JSONObject): JSONObject = withContext(Dispatchers.IO) {
        val request = Request.Builder()
            .url("$apiUrl/api/vm/create")
            .post(specs.toString().toRequestBody("application/json".toMediaType()))
            .build()
        val response = client.newCall(request).execute()
        JSONObject(response.body()?.string() ?: "{}")
    }

    suspend fun deployAllLLMs(): JSONObject = withContext(Dispatchers.IO) {
        val request = Request.Builder()
            .url("$apiUrl/api/llm/deploy-all")
            .post("{}".toRequestBody("application/json".toMediaType()))
            .build()
        val response = client.newCall(request).execute()
        JSONObject(response.body()?.string() ?: "{}")
    }

    suspend fun launchGame(name: String): JSONObject = withContext(Dispatchers.IO) {
        val data = JSONObject().put("name", name)
        val request = Request.Builder()
            .url("$apiUrl/api/games/launch")
            .post(data.toString().toRequestBody("application/json".toMediaType()))
            .build()
        val response = client.newCall(request).execute()
        JSONObject(response.body()?.string() ?: "{}")
    }
}
