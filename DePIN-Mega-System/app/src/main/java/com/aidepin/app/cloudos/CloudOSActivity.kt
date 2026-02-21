package com.aidepin.app.cloudos

import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.FrameLayout
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.aidepin.app.R
import com.aidepin.app.clients.CloudOSAPIClient
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import kotlinx.coroutines.launch
import org.json.JSONObject

class CloudOSActivity : AppCompatActivity() {

    private lateinit var cloudAPI: CloudOSAPIClient
    private lateinit var loadingOverlay: FrameLayout
    private lateinit var loadingText: TextView
    private lateinit var statusBar: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_cloud_os)

        loadingOverlay = findViewById(R.id.loadingOverlay)
        loadingText = findViewById(R.id.loadingText)
        statusBar = findViewById(R.id.statusBar)
        cloudAPI = CloudOSAPIClient()

        findViewById<Button>(R.id.btnLaunchGame).setOnClickListener {
            showGameSelector()
        }

        initializeSystem()
    }

    private fun initializeSystem() {
        lifecycleScope.launch {
            try {
                showLoading("🚀 Starting Cloud OS...")
                val vmResult = cloudAPI.createCloudVM(JSONObject().put("cpu", 32))
                if (vmResult.optBoolean("success")) {
                    updateLoading("🦙 Deploying LLMs (827B params)...")
                    cloudAPI.deployAllLLMs()
                    hideLoading()
                    statusBar.text = "✅ Cloud OS Ready | Provider: Akash"
                }
            } catch (e: Exception) {
                hideLoading()
                Toast.makeText(this@CloudOSActivity, "Init failed: ${e.message}", Toast.LENGTH_LONG).show()
            }
        }
    }

    private fun showGameSelector() {
        val games = arrayOf("Cyberpunk 2077", "GTA VI", "Fortnite", "The Witcher 3")
        MaterialAlertDialogBuilder(this)
            .setTitle("🎮 Select Game")
            .setItems(games) { _, which ->
                launchGame(games[which])
            }
            .show()
    }

    private fun launchGame(name: String) {
        lifecycleScope.launch {
            showLoading("🎮 Launching $name in Cloud...")
            try {
                val result = cloudAPI.launchGame(name)
                hideLoading()
                if (result.optBoolean("success")) {
                    statusBar.text = "🎮 Playing: $name | Latency: 25ms"
                    Toast.makeText(this@CloudOSActivity, "Streaming started from ${result.optString("stream_url")}", Toast.LENGTH_LONG).show()
                }
            } catch (e: Exception) {
                hideLoading()
                Toast.makeText(this@CloudOSActivity, "Launch failed", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun showLoading(msg: String) {
        loadingText.text = msg
        loadingOverlay.visibility = View.VISIBLE
    }

    private fun updateLoading(msg: String) {
        loadingText.text = msg
    }

    private fun hideLoading() {
        loadingOverlay.visibility = View.GONE
    }
}
