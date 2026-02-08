package com.aidepin.app.ai

class LlamaEngine(private val context: android.content.Context) {
    suspend fun initialize() {}
    suspend fun generateResponse(prompt: String): String {
        return "Llama response to: $prompt"
    }
}
