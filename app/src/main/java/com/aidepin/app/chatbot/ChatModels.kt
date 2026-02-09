package com.aidepin.app.chatbot

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.aidepin.app.R

data class ChatMessage(val text: String, val isUser: Boolean, val timestamp: Long)

class MessagesAdapter(private val messages: List<ChatMessage>) : RecyclerView.Adapter<MessagesAdapter.ViewHolder>() {
    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val messageText: TextView = view.findViewById(android.R.id.text1)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(android.R.layout.simple_list_item_1, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val msg = messages[position]
        holder.messageText.text = if (msg.isUser) "You: ${msg.text}" else "Bot: ${msg.text}"
    }

    override fun getItemCount() = messages.size
}

data class ApprovalRequest(val type: String, val data: Any?, val response: com.aidepin.app.clients.ChatResponse)
