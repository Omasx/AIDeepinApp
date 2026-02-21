package com.aidepin.app.clients

class CloudGamingClient(private val vm: Any?) {
    data class GameResult(val success: Boolean, val stream_url: String)
    suspend fun initialize() {}
    suspend fun launchGame(gameName: String, settings: Map<String, Any>): GameResult {
        return GameResult(true, "wss://cloud-gaming.depin/stream")
    }
}
