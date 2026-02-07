package com.aidepin.app.gaming

import android.util.Log
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class ControllerMapper {
    
    companion object {
        private const val TAG = "ControllerMapper"
    }
    
    data class ControllerInput(
        val type: String,  // keyboard, mouse, gamepad
        val action: String,  // press, release, move
        val key: String,  // W, A, S, D, SPACE, etc
        val x: Float = 0f,
        val y: Float = 0f,
        val pressure: Float = 0f
    )
    
    private val keyboardMapping = mapOf(
        // Movement
        "W" to "forward",
        "A" to "left",
        "S" to "backward",
        "D" to "right",
        
        // Actions
        "SPACE" to "jump",
        "SHIFT" to "sprint",
        "CTRL" to "crouch",
        "E" to "interact",
        "F" to "reload",
        "Q" to "ability_1",
        "R" to "ability_2",
        
        // UI
        "ESC" to "menu",
        "TAB" to "inventory",
        "M" to "map"
    )
    
    suspend fun mapKeyboardInput(key: String, action: String): ControllerInput =
        withContext(Dispatchers.IO) {
            try {
                Log.d(TAG, "تعيين مفتاح: $key -> $action")
                
                val mappedAction = keyboardMapping[key] ?: key.lowercase()
                
                ControllerInput(
                    type = "keyboard",
                    action = action,
                    key = key
                )
            } catch (e: Exception) {
                Log.e(TAG, "خطأ في تعيين المفتاح: ${e.message}")
                ControllerInput(type = "keyboard", action = "error", key = key)
            }
        }
    
    suspend fun mapMouseInput(x: Float, y: Float, action: String): ControllerInput =
        withContext(Dispatchers.IO) {
            try {
                Log.d(TAG, "تعيين الماوس: ($x, $y) -> $action")
                
                ControllerInput(
                    type = "mouse",
                    action = action,
                    key = "mouse",
                    x = x,
                    y = y
                )
            } catch (e: Exception) {
                Log.e(TAG, "خطأ في تعيين الماوس: ${e.message}")
                ControllerInput(type = "mouse", action = "error", key = "mouse", x = x, y = y)
            }
        }
    
    suspend fun mapGamepadInput(
        button: String,
        action: String,
        pressure: Float = 1f
    ): ControllerInput = withContext(Dispatchers.IO) {
        try {
            Log.d(TAG, "تعيين الجيمباد: $button -> $action (pressure: $pressure)")
            
            ControllerInput(
                type = "gamepad",
                action = action,
                key = button,
                pressure = pressure
            )
        } catch (e: Exception) {
            Log.e(TAG, "خطأ في تعيين الجيمباد: ${e.message}")
            ControllerInput(type = "gamepad", action = "error", key = button)
        }
    }
    
    suspend fun sendInput(input: ControllerInput): Boolean = withContext(Dispatchers.IO) {
        try {
            Log.d(TAG, "إرسال مدخل: ${input.type} - ${input.key} - ${input.action}")
            
            // محاكاة إرسال المدخل إلى السيرفر
            // في التطبيق الحقيقي، سيتم إرسال هذا عبر WebRTC
            
            true
        } catch (e: Exception) {
            Log.e(TAG, "خطأ في إرسال المدخل: ${e.message}")
            false
        }
    }
    
    fun getKeyboardMapping(): Map<String, String> {
        return keyboardMapping
    }
}
