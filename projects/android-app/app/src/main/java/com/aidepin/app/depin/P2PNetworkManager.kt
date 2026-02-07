package com.aidepin.app.depin

import android.content.Context
import android.util.Log
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class P2PNetworkManager(private val context: Context) {
    
    companion object {
        private const val TAG = "P2PNetworkManager"
    }
    
    data class Peer(
        val id: String,
        val address: String,
        val port: Int,
        val status: String,  // online, offline, connecting
        val latency: Int  // ms
    )
    
    private val peers = mutableMapOf<String, Peer>()
    private var isConnected = false
    
    suspend fun connectToPeer(peerId: String, address: String, port: Int): Boolean =
        withContext(Dispatchers.IO) {
            try {
                Log.d(TAG, "الاتصال بـ Peer: $peerId @ $address:$port")
                
                val peer = Peer(
                    id = peerId,
                    address = address,
                    port = port,
                    status = "connecting",
                    latency = 0
                )
                
                peers[peerId] = peer
                
                // محاكاة الاتصال
                Thread.sleep(500)
                
                peers[peerId] = peer.copy(status = "online", latency = 50)
                isConnected = true
                
                Log.d(TAG, "✅ تم الاتصال بـ Peer: $peerId")
                true
            } catch (e: Exception) {
                Log.e(TAG, "خطأ في الاتصال: ${e.message}")
                false
            }
        }
    
    suspend fun disconnectFromPeer(peerId: String): Boolean = withContext(Dispatchers.IO) {
        try {
            Log.d(TAG, "قطع الاتصال بـ Peer: $peerId")
            
            peers.remove(peerId)
            
            if (peers.isEmpty()) {
                isConnected = false
            }
            
            Log.d(TAG, "✅ تم قطع الاتصال")
            true
        } catch (e: Exception) {
            Log.e(TAG, "خطأ في قطع الاتصال: ${e.message}")
            false
        }
    }
    
    suspend fun broadcastMessage(message: String): Int = withContext(Dispatchers.IO) {
        try {
            Log.d(TAG, "بث الرسالة: $message")
            
            var count = 0
            for (peer in peers.values) {
                if (peer.status == "online") {
                    // محاكاة إرسال الرسالة
                    count++
                }
            }
            
            Log.d(TAG, "تم إرسال الرسالة إلى $count أقران")
            count
        } catch (e: Exception) {
            Log.e(TAG, "خطأ في البث: ${e.message}")
            0
        }
    }
    
    fun getPeers(): List<Peer> {
        return peers.values.toList()
    }
    
    fun getPeerStatus(peerId: String): String? {
        return peers[peerId]?.status
    }
    
    fun isConnected(): Boolean {
        return isConnected && peers.isNotEmpty()
    }
    
    suspend fun getNetworkStats(): Map<String, Any> = withContext(Dispatchers.IO) {
        mapOf(
            "total_peers" to peers.size,
            "online_peers" to peers.count { it.value.status == "online" },
            "average_latency" to (peers.values.map { it.latency }.average() as? Number ?: 0),
            "is_connected" to isConnected
        )
    }
}
