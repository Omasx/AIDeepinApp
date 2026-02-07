package com.aidepin.app.models

data class Task(
    val id: String,
    val command: String,
    val taskType: String,  // game, app, query, chat
    val recommendedModel: String,  // openai, claude, gemini, deepseek, local
    val parameters: String,  // JSON string
    val response: String,
    val status: String,  // pending, processing, completed, error
    val progress: Int  // 0-100
)
