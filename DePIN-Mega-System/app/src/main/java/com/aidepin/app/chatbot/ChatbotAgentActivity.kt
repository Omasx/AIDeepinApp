package com.aidepin.app.chatbot

import android.content.Context
import android.graphics.PixelFormat
import android.os.Build
import android.os.Bundle
import android.view.Gravity
import android.view.LayoutInflater
import android.view.MotionEvent
import android.view.View
import android.view.WindowManager
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.cardview.widget.CardView
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.aidepin.app.R
import com.aidepin.app.clients.*
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

class ChatbotAgentActivity : AppCompatActivity() {

    private lateinit var recyclerView: RecyclerView
    private lateinit var messageInput: EditText
    private lateinit var sendButton: ImageButton
    private lateinit var modeIndicator: TextView
    private lateinit var agentStatusCard: CardView
    private lateinit var typingIndicator: ProgressBar

    private var currentMode = "chat"
    private val messages = mutableListOf<ChatMessage>()
    private lateinit var adapter: MessagesAdapter
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_chatbot_agent)

        setupUI()
    }

    private fun setupUI() {
        recyclerView = findViewById(R.id.chatRecyclerView)
        messageInput = findViewById(R.id.messageInput)
        sendButton = findViewById(R.id.sendButton)
        modeIndicator = findViewById(R.id.modeIndicator)
        agentStatusCard = findViewById(R.id.agentStatusCard)
        typingIndicator = findViewById(R.id.typingIndicator)

        adapter = MessagesAdapter(messages)
        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerView.adapter = adapter
        
        sendButton.setOnClickListener {
            val text = messageInput.text.toString()
            if (text.isNotBlank()) {
                handleSendMessage(text)
            }
        }

        findViewById<Button>(R.id.btnAgentMode).setOnClickListener {
            showAgentActivationDialog()
        }

        findViewById<Button>(R.id.btnHyperResearch).setOnClickListener {
            showHyperResearchDialog()
        }

        findViewById<Button>(R.id.btnCybersecurity).setOnClickListener {
            showCybersecurityDialog()
        }
    }

    private fun handleSendMessage(text: String) {
        messages.add(ChatMessage(text, true, System.currentTimeMillis()))
        adapter.notifyItemInserted(messages.size - 1)
        recyclerView.scrollToPosition(messages.size - 1)
        messageInput.setText("")
        
        lifecycleScope.launch {
            typingIndicator.visibility = View.VISIBLE
            delay(1500)
            typingIndicator.visibility = View.GONE
            
            if (text.contains("وكيل") || text.contains("agent")) {
                showAgentActivationDialog()
            } else {
                addBotMessage("I'm processing your request: $text")
            }
        }
    }

    private fun addBotMessage(text: String) {
        messages.add(ChatMessage(text, false, System.currentTimeMillis()))
        adapter.notifyItemInserted(messages.size - 1)
        recyclerView.scrollToPosition(messages.size - 1)
    }

    private fun showAgentActivationDialog() {
        androidx.appcompat.app.AlertDialog.Builder(this)
            .setTitle("Activate Agent Mode")
            .setMessage("Do you allow the bot to act as an independent agent with full system permissions?")
            .setPositiveButton("Accept") { _, _ ->
                activateAgentMode()
            }
            .setNegativeButton("Decline", null)
            .show()
    }

    private fun activateAgentMode() {
        currentMode = "agent"
        modeIndicator.text = "🤖 Agent Mode"
        modeIndicator.setBackgroundColor(android.graphics.Color.parseColor("#FF9500"))
        agentStatusCard.visibility = View.VISIBLE
        addBotMessage("Agent Mode Activated! I am now an autonomous agent.")
    }

    private fun showHyperResearchDialog() {
        val view = layoutInflater.inflate(R.layout.dialog_hyper_research, null)
        androidx.appcompat.app.AlertDialog.Builder(this)
            .setTitle("🔍 Hyper Research")
            .setView(view)
            .setPositiveButton("Start") { _, _ ->
                val query = view.findViewById<EditText>(R.id.researchQuery).text.toString()
                addBotMessage("Starting hyper research for: $query")
                showFloatingMonitorWindow("🔍 Hyper Research", "Searching for '$query'...")
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    private fun showCybersecurityDialog() {
        val view = layoutInflater.inflate(R.layout.dialog_security_scan, null)
        androidx.appcompat.app.AlertDialog.Builder(this)
            .setTitle("🛡️ Cyber Security")
            .setView(view)
            .setPositiveButton("Scan") { _, _ ->
                val target = view.findViewById<EditText>(R.id.targetInput).text.toString()
                addBotMessage("Initializing security scan for: $target")
                showFloatingTerminalWindow()
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    // --- Floating Windows Logic ---

    private fun showFloatingMonitorWindow(title: String, status: String) {
        val wm = getSystemService(Context.WINDOW_SERVICE) as WindowManager
        val view = LayoutInflater.from(this).inflate(R.layout.floating_monitor_window, null)
        
        val type = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY else WindowManager.LayoutParams.TYPE_PHONE
        val params = WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            type,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
            PixelFormat.TRANSLUCENT
        )
        params.gravity = Gravity.TOP or Gravity.START
        params.x = 100
        params.y = 200

        view.findViewById<TextView>(R.id.titleText).text = title
        view.findViewById<TextView>(R.id.statusText).text = status
        
        view.findViewById<ImageButton>(R.id.btnClose).setOnClickListener {
            wm.removeView(view)
        }

        setupDraggable(view, params, wm)
        try {
            wm.addView(view, params)
        } catch (e: Exception) {
            Toast.makeText(this, "Permission Required for Floating Windows", Toast.LENGTH_LONG).show()
        }
    }

    private fun showFloatingTerminalWindow() {
        val wm = getSystemService(Context.WINDOW_SERVICE) as WindowManager
        val view = LayoutInflater.from(this).inflate(R.layout.floating_terminal_window, null)
        
        val type = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY else WindowManager.LayoutParams.TYPE_PHONE
        val params = WindowManager.LayoutParams(
            dpToPx(400), dpToPx(300),
            type,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
            PixelFormat.TRANSLUCENT
        )
        params.gravity = Gravity.CENTER

        view.findViewById<ImageButton>(R.id.btnCloseTerminal).setOnClickListener {
            wm.removeView(view)
        }

        setupDraggable(view, params, wm)
        try {
            wm.addView(view, params)
        } catch (e: Exception) {
            Toast.makeText(this, "Permission Required for Floating Windows", Toast.LENGTH_LONG).show()
        }
    }

    private fun setupDraggable(view: View, params: WindowManager.LayoutParams, wm: WindowManager) {
        val header = view.findViewById<View>(R.id.windowHeader) ?: view.findViewById<View>(R.id.terminalHeader)
        header.setOnTouchListener(object : View.OnTouchListener {
            private var initialX = 0
            private var initialY = 0
            private var initialTouchX = 0f
            private var initialTouchY = 0f

            override fun onTouch(v: View, event: MotionEvent): Boolean {
                when (event.action) {
                    MotionEvent.ACTION_DOWN -> {
                        initialX = params.x
                        initialY = params.y
                        initialTouchX = event.rawX
                        initialTouchY = event.rawY
                        return true
                    }
                    MotionEvent.ACTION_MOVE -> {
                        params.x = initialX + (event.rawX - initialTouchX).toInt()
                        params.y = initialY + (event.rawY - initialTouchY).toInt()
                        wm.updateViewLayout(view, params)
                        return true
                    }
                }
                return false
            }
        })
    }

    private fun dpToPx(dp: Int): Int {
        return (dp * resources.displayMetrics.density).toInt()
    }
}
