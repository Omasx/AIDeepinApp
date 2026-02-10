package com.aidepin.app.depin

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.widget.SwitchCompat
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.aidepin.app.R
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

class DePINControlPanel : AppCompatActivity() {

    private lateinit var providersRecyclerView: RecyclerView
    private lateinit var creditsBalanceText: TextView
    private lateinit var contributionSwitch: SwitchCompat
    private val providersList = mutableListOf<ProviderInfo>()
    private lateinit var adapter: ProvidersAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_depin_control_panel)

        providersRecyclerView = findViewById(R.id.providersRecyclerView)
        creditsBalanceText = findViewById(R.id.creditsBalanceText)
        contributionSwitch = findViewById(R.id.contributionSwitch)

        adapter = ProvidersAdapter(providersList)
        providersRecyclerView.layoutManager = GridLayoutManager(this, 2)
        providersRecyclerView.adapter = adapter

        findViewById<Button>(R.id.btnStartContribution).setOnClickListener {
            contributionSwitch.isChecked = true
        }

        startRealtimeUpdates()
    }

    private fun startRealtimeUpdates() {
        lifecycleScope.launch {
            while (true) {
                // Simulate fetching data
                val mockCredits = (0..1000).random() / 10.0
                creditsBalanceText.text = "%.2f".format(mockCredits)

                if (providersList.isEmpty()) {
                    val names = listOf("Akash", "Render", "Golem", "iExec", "Bittensor", "Petals", "Filecoin", "Storj")
                    names.forEach {
                        providersList.add(ProviderInfo(it, true, (10..50).random().toFloat(), 95f))
                    }
                    adapter.notifyDataSetChanged()
                }

                delay(5000)
            }
        }
    }
}

data class ProviderInfo(val name: String, val available: Boolean, val latencyMs: Float, val health: Float)

class ProvidersAdapter(private val providers: List<ProviderInfo>) : RecyclerView.Adapter<ProvidersAdapter.ViewHolder>() {
    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val nameText: TextView = view.findViewById(android.R.id.text1)
        val statusText: TextView = view.findViewById(android.R.id.text2)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(android.R.layout.simple_list_item_2, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val p = providers[position]
        holder.nameText.text = p.name
        holder.statusText.text = "Latency: ${p.latencyMs.toInt()}ms | Health: ${p.health.toInt()}%"
        holder.statusText.setTextColor(android.graphics.Color.GREEN)
    }

    override fun getItemCount() = providers.size
}
