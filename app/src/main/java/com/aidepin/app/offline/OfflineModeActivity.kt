package com.aidepin.app.offline

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.LinearLayout
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.card.MaterialCardView
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

/**
 * 🌐 نشاط وضع بدون إنترنت - Offline Mode Activity
 * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 * 
 * واجهة جميلة وأنيقة لوضع بدون إنترنت مع نظام اتصال ذكي بشبكات DePIN
 */

data class NetworkNode(
    val id: String,
    val name: String,
    val type: String, // depin, wifi, cellular, mesh
    val signalStrength: Int, // 0-100
    val latency: Int, // ms
    val distance: Double, // km
    val quality: String // excellent, good, fair, poor, offline
)

class OfflineModeActivity : AppCompatActivity() {
    
    private lateinit var scanButton: Button
    private lateinit var progressBar: ProgressBar
    private lateinit var networksRecyclerView: RecyclerView
    private lateinit var emptyStateContainer: LinearLayout
    private lateinit var statusTextView: TextView
    
    private val networksList = mutableListOf<NetworkNode>()
    private lateinit var networkAdapter: NetworkAdapter
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_offline_mode)
        
        initializeViews()
        setupRecyclerView()
        setupListeners()
    }
    
    private fun initializeViews() {
        scanButton = findViewById(R.id.scanButton)
        progressBar = findViewById(R.id.progressBar)
        networksRecyclerView = findViewById(R.id.networksRecyclerView)
        emptyStateContainer = findViewById(R.id.emptyStateContainer)
        statusTextView = findViewById(R.id.statusTextView)
    }
    
    private fun setupRecyclerView() {
        networkAdapter = NetworkAdapter(networksList) { network ->
            connectToNetwork(network)
        }
        networksRecyclerView.layoutManager = LinearLayoutManager(this)
        networksRecyclerView.adapter = networkAdapter
    }
    
    private fun setupListeners() {
        scanButton.setOnClickListener {
            scanNetworks()
        }
    }
    
    private fun scanNetworks() {
        scanButton.isEnabled = false
        progressBar.visibility = View.VISIBLE
        statusTextView.text = "جاري مسح الشبكات..."
        
        GlobalScope.launch(Dispatchers.Default) {
            // محاكاة مسح الشبكات
            Thread.sleep(2000)
            
            val mockNetworks = listOf(
                NetworkNode(
                    id = "depin-1",
                    name = "DePIN Hub - الرياض",
                    type = "depin",
                    signalStrength = 95,
                    latency = 15,
                    distance = 2.5,
                    quality = "excellent"
                ),
                NetworkNode(
                    id = "depin-2",
                    name = "DePIN Mesh - دبي",
                    type = "mesh",
                    signalStrength = 85,
                    latency = 25,
                    distance = 8.3,
                    quality = "good"
                ),
                NetworkNode(
                    id = "wifi-1",
                    name = "شبكة محلية",
                    type = "wifi",
                    signalStrength = 70,
                    latency = 35,
                    distance = 0.1,
                    quality = "fair"
                ),
                NetworkNode(
                    id = "cellular-1",
                    name = "شبكة الهاتف المحمول",
                    type = "cellular",
                    signalStrength = 60,
                    latency = 50,
                    distance = 0.0,
                    quality = "fair"
                )
            )
            
            withContext(Dispatchers.Main) {
                networksList.clear()
                networksList.addAll(mockNetworks)
                networkAdapter.notifyDataSetChanged()
                
                progressBar.visibility = View.GONE
                scanButton.isEnabled = true
                
                if (networksList.isEmpty()) {
                    emptyStateContainer.visibility = View.VISIBLE
                    statusTextView.text = "لم يتم العثور على شبكات متاحة"
                } else {
                    emptyStateContainer.visibility = View.GONE
                    statusTextView.text = "تم العثور على ${networksList.size} شبكات"
                }
            }
        }
    }
    
    private fun connectToNetwork(network: NetworkNode) {
        statusTextView.text = "جاري الاتصال بـ ${network.name}..."
        progressBar.visibility = View.VISIBLE
        
        GlobalScope.launch(Dispatchers.Default) {
            // محاكاة الاتصال
            Thread.sleep(1500)
            
            withContext(Dispatchers.Main) {
                progressBar.visibility = View.GONE
                statusTextView.text = "✅ متصل بـ ${network.name}"
                Toast.makeText(
                    this@OfflineModeActivity,
                    "تم الاتصال بنجاح بـ ${network.name}",
                    Toast.LENGTH_SHORT
                ).show()
                
                // إغلاق النشاط بعد ثانية
                Thread.sleep(1000)
                finish()
            }
        }
    }
}

class NetworkAdapter(
    private val networks: List<NetworkNode>,
    private val onNetworkClick: (NetworkNode) -> Unit
) : RecyclerView.Adapter<NetworkAdapter.NetworkViewHolder>() {
    
    inner class NetworkViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val networkCard: MaterialCardView = itemView.findViewById(R.id.networkCard)
        private val networkName: TextView = itemView.findViewById(R.id.networkName)
        private val networkType: TextView = itemView.findViewById(R.id.networkType)
        private val signalStrength: TextView = itemView.findViewById(R.id.signalStrength)
        private val latency: TextView = itemView.findViewById(R.id.latency)
        private val distance: TextView = itemView.findViewById(R.id.distance)
        private val qualityBadge: TextView = itemView.findViewById(R.id.qualityBadge)
        
        fun bind(network: NetworkNode) {
            networkName.text = network.name
            networkType.text = getNetworkTypeLabel(network.type)
            signalStrength.text = "📶 ${network.signalStrength}%"
            latency.text = "⚡ ${network.latency}ms"
            distance.text = "📍 ${network.distance} km"
            
            // تعيين لون الجودة
            val qualityColor = getQualityColor(network.quality)
            qualityBadge.text = getQualityLabel(network.quality)
            qualityBadge.setBackgroundColor(qualityColor)
            
            networkCard.setOnClickListener {
                onNetworkClick(network)
            }
        }
        
        private fun getNetworkTypeLabel(type: String): String {
            return when (type) {
                "depin" -> "🌐 DePIN"
                "mesh" -> "🕸️ Mesh"
                "wifi" -> "📡 WiFi"
                "cellular" -> "📱 Cellular"
                else -> "🔗 Unknown"
            }
        }
        
        private fun getQualityColor(quality: String): Int {
            return when (quality) {
                "excellent" -> 0xFF10B981.toInt()
                "good" -> 0xFF3B82F6.toInt()
                "fair" -> 0xFFF59E0B.toInt()
                "poor" -> 0xFFEF4444.toInt()
                else -> 0xFF9CA3AF.toInt()
            }
        }
        
        private fun getQualityLabel(quality: String): String {
            return when (quality) {
                "excellent" -> "ممتاز"
                "good" -> "جيد"
                "fair" -> "مقبول"
                "poor" -> "ضعيف"
                else -> "غير متصل"
            }
        }
    }
    
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): NetworkViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_network, parent, false)
        return NetworkViewHolder(view)
    }
    
    override fun onBindViewHolder(holder: NetworkViewHolder, position: Int) {
        holder.bind(networks[position])
    }
    
    override fun getItemCount(): Int = networks.size
}

/**
 * Fragment لوضع بدون إنترنت
 */
class OfflineModeFragment : Fragment() {
    
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_offline_mode, container, false)
    }
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        val scanButton: Button = view.findViewById(R.id.scanButton)
        scanButton.setOnClickListener {
            // فتح نشاط وضع بدون إنترنت
            startActivity(
                android.content.Intent(
                    requireContext(),
                    OfflineModeActivity::class.java
                )
            )
        }
    }
}
