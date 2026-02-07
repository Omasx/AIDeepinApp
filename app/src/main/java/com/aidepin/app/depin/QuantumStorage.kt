package com.aidepin.app.depin

import android.content.Context
import android.util.Log
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File
import java.util.zip.GZIPInputStream
import java.util.zip.GZIPOutputStream

class QuantumStorage(private val context: Context) {
    
    companion object {
        private const val TAG = "QuantumStorage"
        private const val STORAGE_DIR = "quantum_storage"
    }
    
    data class StorageInfo(
        val fileId: String,
        val originalSize: Long,
        val compressedSize: Long,
        val compressionRatio: Float,
        val hash: String,
        val timestamp: Long
    )
    
    private val storageDir = File(context.filesDir, STORAGE_DIR)
    private val storageIndex = mutableMapOf<String, StorageInfo>()
    
    init {
        if (!storageDir.exists()) {
            storageDir.mkdirs()
        }
    }
    
    suspend fun storeData(fileId: String, data: ByteArray): StorageInfo =
        withContext(Dispatchers.IO) {
            try {
                Log.d(TAG, "تخزين البيانات: $fileId (${data.size} bytes)")
                
                val originalSize = data.size.toLong()
                
                // ضغط البيانات باستخدام GZIP
                val compressedData = compressData(data)
                val compressedSize = compressedData.size.toLong()
                
                // حساب نسبة الضغط
                val compressionRatio = (1 - (compressedSize.toFloat() / originalSize)) * 100
                
                // حفظ الملف المضغوط
                val file = File(storageDir, fileId)
                file.writeBytes(compressedData)
                
                // حساب Hash
                val hash = calculateHash(data)
                
                val info = StorageInfo(
                    fileId = fileId,
                    originalSize = originalSize,
                    compressedSize = compressedSize,
                    compressionRatio = compressionRatio,
                    hash = hash,
                    timestamp = System.currentTimeMillis()
                )
                
                storageIndex[fileId] = info
                
                Log.d(TAG, "✅ تم تخزين البيانات")
                Log.d(TAG, "الحجم الأصلي: $originalSize bytes")
                Log.d(TAG, "الحجم المضغوط: $compressedSize bytes")
                Log.d(TAG, "نسبة الضغط: $compressionRatio%")
                
                info
            } catch (e: Exception) {
                Log.e(TAG, "خطأ في تخزين البيانات: ${e.message}")
                throw e
            }
        }
    
    suspend fun retrieveData(fileId: String): ByteArray? = withContext(Dispatchers.IO) {
        try {
            Log.d(TAG, "استرجاع البيانات: $fileId")
            
            val file = File(storageDir, fileId)
            if (!file.exists()) {
                Log.w(TAG, "الملف غير موجود: $fileId")
                return@withContext null
            }
            
            val compressedData = file.readBytes()
            val decompressedData = decompressData(compressedData)
            
            Log.d(TAG, "✅ تم استرجاع البيانات")
            decompressedData
        } catch (e: Exception) {
            Log.e(TAG, "خطأ في استرجاع البيانات: ${e.message}")
            null
        }
    }
    
    suspend fun deleteData(fileId: String): Boolean = withContext(Dispatchers.IO) {
        try {
            Log.d(TAG, "حذف البيانات: $fileId")
            
            val file = File(storageDir, fileId)
            val deleted = file.delete()
            
            if (deleted) {
                storageIndex.remove(fileId)
                Log.d(TAG, "✅ تم حذف البيانات")
            }
            
            deleted
        } catch (e: Exception) {
            Log.e(TAG, "خطأ في حذف البيانات: ${e.message}")
            false
        }
    }
    
    suspend fun getStorageStats(): Map<String, Any> = withContext(Dispatchers.IO) {
        val totalOriginal = storageIndex.values.sumOf { it.originalSize }
        val totalCompressed = storageIndex.values.sumOf { it.compressedSize }
        val avgCompressionRatio = if (storageIndex.isNotEmpty()) {
            storageIndex.values.map { it.compressionRatio }.average()
        } else {
            0.0
        }
        
        mapOf(
            "total_files" to storageIndex.size,
            "total_original_size" to totalOriginal,
            "total_compressed_size" to totalCompressed,
            "average_compression_ratio" to avgCompressionRatio,
            "total_saved" to (totalOriginal - totalCompressed)
        )
    }
    
    private fun compressData(data: ByteArray): ByteArray {
        val outputStream = java.io.ByteArrayOutputStream()
        GZIPOutputStream(outputStream).use { gzip ->
            gzip.write(data)
        }
        return outputStream.toByteArray()
    }
    
    private fun decompressData(compressedData: ByteArray): ByteArray {
        val inputStream = java.io.ByteArrayInputStream(compressedData)
        val outputStream = java.io.ByteArrayOutputStream()
        GZIPInputStream(inputStream).use { gzip ->
            gzip.copyTo(outputStream)
        }
        return outputStream.toByteArray()
    }
    
    private fun calculateHash(data: ByteArray): String {
        val md = java.security.MessageDigest.getInstance("SHA-256")
        val hashBytes = md.digest(data)
        return hashBytes.joinToString("") { "%02x".format(it) }
    }
}
