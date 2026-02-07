package com.aidepin.app.social

import android.content.Context
import android.util.Log
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class FriendManager(private val context: Context) {
    
    companion object {
        private const val TAG = "FriendManager"
    }
    
    data class Friend(
        val id: String,
        val name: String,
        val avatar: String,
        val status: String,  // online, offline, in_game
        val lastSeen: Long,
        val isFavorite: Boolean = false
    )
    
    private val friends = mutableMapOf<String, Friend>()
    private val friendRequests = mutableListOf<Friend>()
    
    suspend fun addFriend(friendId: String, name: String, avatar: String): Boolean =
        withContext(Dispatchers.IO) {
            try {
                Log.d(TAG, "إضافة صديق: $name ($friendId)")
                
                val friend = Friend(
                    id = friendId,
                    name = name,
                    avatar = avatar,
                    status = "offline",
                    lastSeen = System.currentTimeMillis()
                )
                
                friends[friendId] = friend
                
                Log.d(TAG, "✅ تم إضافة الصديق")
                true
            } catch (e: Exception) {
                Log.e(TAG, "خطأ في إضافة الصديق: ${e.message}")
                false
            }
        }
    
    suspend fun removeFriend(friendId: String): Boolean = withContext(Dispatchers.IO) {
        try {
            Log.d(TAG, "حذف الصديق: $friendId")
            
            friends.remove(friendId)
            
            Log.d(TAG, "✅ تم حذف الصديق")
            true
        } catch (e: Exception) {
            Log.e(TAG, "خطأ في حذف الصديق: ${e.message}")
            false
        }
    }
    
    suspend fun sendFriendRequest(friendId: String, name: String, avatar: String): Boolean =
        withContext(Dispatchers.IO) {
            try {
                Log.d(TAG, "إرسال طلب صداقة: $name")
                
                val friend = Friend(
                    id = friendId,
                    name = name,
                    avatar = avatar,
                    status = "offline",
                    lastSeen = System.currentTimeMillis()
                )
                
                friendRequests.add(friend)
                
                Log.d(TAG, "✅ تم إرسال طلب الصداقة")
                true
            } catch (e: Exception) {
                Log.e(TAG, "خطأ في إرسال الطلب: ${e.message}")
                false
            }
        }
    
    suspend fun acceptFriendRequest(friendId: String): Boolean = withContext(Dispatchers.IO) {
        try {
            Log.d(TAG, "قبول طلب صداقة: $friendId")
            
            val request = friendRequests.find { it.id == friendId }
            if (request != null) {
                friends[friendId] = request
                friendRequests.remove(request)
                Log.d(TAG, "✅ تم قبول الطلب")
                true
            } else {
                false
            }
        } catch (e: Exception) {
            Log.e(TAG, "خطأ في قبول الطلب: ${e.message}")
            false
        }
    }
    
    suspend fun rejectFriendRequest(friendId: String): Boolean = withContext(Dispatchers.IO) {
        try {
            Log.d(TAG, "رفض طلب صداقة: $friendId")
            
            val request = friendRequests.find { it.id == friendId }
            if (request != null) {
                friendRequests.remove(request)
                Log.d(TAG, "✅ تم رفض الطلب")
                true
            } else {
                false
            }
        } catch (e: Exception) {
            Log.e(TAG, "خطأ في رفض الطلب: ${e.message}")
            false
        }
    }
    
    suspend fun updateFriendStatus(friendId: String, status: String) = withContext(Dispatchers.IO) {
        friends[friendId]?.let { friend ->
            friends[friendId] = friend.copy(
                status = status,
                lastSeen = System.currentTimeMillis()
            )
            Log.d(TAG, "تم تحديث حالة الصديق: $status")
        }
    }
    
    suspend fun toggleFavorite(friendId: String): Boolean = withContext(Dispatchers.IO) {
        friends[friendId]?.let { friend ->
            friends[friendId] = friend.copy(isFavorite = !friend.isFavorite)
            Log.d(TAG, "تم تحديث حالة المفضلة")
            true
        } ?: false
    }
    
    fun getFriends(): List<Friend> {
        return friends.values.toList()
    }
    
    fun getFriendRequests(): List<Friend> {
        return friendRequests.toList()
    }
    
    fun getOnlineFriends(): List<Friend> {
        return friends.values.filter { it.status == "online" }
    }
    
    fun getFavoriteFriends(): List<Friend> {
        return friends.values.filter { it.isFavorite }
    }
}
