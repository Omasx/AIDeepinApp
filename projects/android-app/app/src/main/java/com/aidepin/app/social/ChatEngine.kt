package com.aidepin.app.social

import android.util.Log
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class ChatEngine {
    
    companion object {
        private const val TAG = "ChatEngine"
    }
    
    data class Message(
        val id: String,
        val senderId: String,
        val senderName: String,
        val content: String,
        val timestamp: Long,
        val isRead: Boolean = false
    )
    
    data class Conversation(
        val id: String,
        val participantId: String,
        val participantName: String,
        val lastMessage: String,
        val lastMessageTime: Long,
        val unreadCount: Int = 0
    )
    
    private val conversations = mutableMapOf<String, MutableList<Message>>()
    private val conversationsList = mutableMapOf<String, Conversation>()
    
    suspend fun sendMessage(
        conversationId: String,
        senderId: String,
        senderName: String,
        content: String
    ): Message = withContext(Dispatchers.IO) {
        try {
            Log.d(TAG, "إرسال رسالة: $content")
            
            val message = Message(
                id = System.currentTimeMillis().toString(),
                senderId = senderId,
                senderName = senderName,
                content = content,
                timestamp = System.currentTimeMillis()
            )
            
            // إضافة الرسالة إلى المحادثة
            conversations.getOrPut(conversationId) { mutableListOf() }.add(message)
            
            // تحديث آخر رسالة
            conversationsList[conversationId]?.let { conv ->
                conversationsList[conversationId] = conv.copy(
                    lastMessage = content,
                    lastMessageTime = message.timestamp
                )
            }
            
            Log.d(TAG, "✅ تم إرسال الرسالة")
            message
        } catch (e: Exception) {
            Log.e(TAG, "خطأ في إرسال الرسالة: ${e.message}")
            throw e
        }
    }
    
    suspend fun getMessages(conversationId: String): List<Message> = withContext(Dispatchers.IO) {
        try {
            Log.d(TAG, "جاري جلب الرسائل: $conversationId")
            
            val messages = conversations[conversationId] ?: emptyList()
            
            Log.d(TAG, "تم جلب ${messages.size} رسالة")
            messages
        } catch (e: Exception) {
            Log.e(TAG, "خطأ في جلب الرسائل: ${e.message}")
            emptyList()
        }
    }
    
    suspend fun createConversation(
        participantId: String,
        participantName: String
    ): Conversation = withContext(Dispatchers.IO) {
        try {
            Log.d(TAG, "إنشاء محادثة مع: $participantName")
            
            val conversationId = participantId
            
            val conversation = Conversation(
                id = conversationId,
                participantId = participantId,
                participantName = participantName,
                lastMessage = "",
                lastMessageTime = System.currentTimeMillis()
            )
            
            conversationsList[conversationId] = conversation
            conversations[conversationId] = mutableListOf()
            
            Log.d(TAG, "✅ تم إنشاء المحادثة")
            conversation
        } catch (e: Exception) {
            Log.e(TAG, "خطأ في إنشاء المحادثة: ${e.message}")
            throw e
        }
    }
    
    suspend fun markAsRead(conversationId: String): Boolean = withContext(Dispatchers.IO) {
        try {
            Log.d(TAG, "تحديد المحادثة كمقروءة: $conversationId")
            
            conversations[conversationId]?.forEach { message ->
                // تحديث حالة القراءة
            }
            
            conversationsList[conversationId]?.let { conv ->
                conversationsList[conversationId] = conv.copy(unreadCount = 0)
            }
            
            Log.d(TAG, "✅ تم تحديد المحادثة كمقروءة")
            true
        } catch (e: Exception) {
            Log.e(TAG, "خطأ: ${e.message}")
            false
        }
    }
    
    fun getConversations(): List<Conversation> {
        return conversationsList.values.toList()
    }
    
    fun getConversation(conversationId: String): Conversation? {
        return conversationsList[conversationId]
    }
}
