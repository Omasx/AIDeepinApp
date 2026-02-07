/**
 * AI DePIN Cloud Platform - Frontend JavaScript
 */

// ============================================================================
// Global State
// ============================================================================

const state = {
    isLoggedIn: false,
    sessionToken: null,
    deviceId: generateDeviceId(),
    currentPage: 'dashboard',
    activeTasks: 0,
    storageUsed: 0,
    latency: 0,
    apiKeys: {
        openai: '',
        anthropic: '',
        google: '',
        deepseek: ''
    }
};

const API_BASE_URL = 'http://localhost:8080';

// ============================================================================
// Utility Functions
// ============================================================================

function generateDeviceId() {
    let deviceId = localStorage.getItem('deviceId');
    if (!deviceId) {
        deviceId = 'device_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('deviceId', deviceId);
    }
    return deviceId;
}

function showLoadingScreen(show = true) {
    const screen = document.getElementById('loading-screen');
    if (show) {
        screen.classList.remove('hidden');
    } else {
        screen.classList.add('hidden');
    }
}

function updateLoadingStatus(message) {
    document.getElementById('loading-status').textContent = message;
}

function showPage(pageName) {
    // إخفاء جميع الصفحات
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    // إظهار الصفحة المطلوبة
    const page = document.getElementById(pageName + '-page');
    if (page) {
        page.classList.add('active');
    }
    
    // تحديث الروابط النشطة
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.dataset.page === pageName) {
            link.classList.add('active');
        }
    });
    
    state.currentPage = pageName;
}

function addChatMessage(message, isBot = true) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isBot ? 'bot-message' : 'user-message'}`;
    
    const avatar = isBot ? '🤖' : '👤';
    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <p>${message}</p>
        </div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function addTerminalLine(text, isCommand = false) {
    const output = document.getElementById('terminal-output');
    const line = document.createElement('div');
    line.className = 'terminal-line';
    
    if (isCommand) {
        line.innerHTML = `
            <span class="terminal-prompt">ai-depin@cloud:~$</span>
            <span class="terminal-text">${text}</span>
        `;
    } else {
        line.innerHTML = `
            <span class="terminal-text">${text}</span>
        `;
    }
    
    output.appendChild(line);
    output.scrollTop = output.scrollHeight;
}

// ============================================================================
// API Functions
// ============================================================================

async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${state.sessionToken}`
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        showNotification('خطأ في الاتصال بالسيرفر', 'error');
        return null;
    }
}

async function login() {
    showLoadingScreen(true);
    updateLoadingStatus('جاري تسجيل الدخول...');
    
    try {
        const response = await apiCall('/connect', 'POST', {
            device_id: state.deviceId
        });
        
        if (response && response.success) {
            state.sessionToken = response.session_token;
            state.isLoggedIn = true;
            
            updateLoadingStatus('تحميل البيانات...');
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            showLoadingScreen(false);
            showPage('dashboard');
            updateUserStatus();
            loadSystemStats();
            
            showNotification('مرحباً! تم تسجيل الدخول بنجاح', 'success');
        } else {
            showNotification('فشل تسجيل الدخول', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showNotification('حدث خطأ أثناء تسجيل الدخول', 'error');
    }
}

async function syncApiKeys() {
    const keys = {
        openai: document.getElementById('openai-key').value,
        anthropic: document.getElementById('anthropic-key').value,
        google: document.getElementById('google-key').value,
        deepseek: document.getElementById('deepseek-key').value
    };
    
    // التحقق من وجود مفتاح واحد على الأقل
    if (!Object.values(keys).some(key => key.trim())) {
        showNotification('يرجى إدخال مفتاح واحد على الأقل', 'warning');
        return;
    }
    
    // عرض شريط التقدم
    const progressContainer = document.getElementById('sync-progress');
    progressContainer.classList.remove('hidden');
    
    // محاكاة المزامنة
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 30;
        if (progress > 100) progress = 100;
        
        document.getElementById('progress-fill').style.width = progress + '%';
        document.getElementById('sync-status').textContent = `جاري المزامنة... ${Math.floor(progress)}%`;
        
        if (progress === 100) {
            clearInterval(interval);
            setTimeout(() => {
                progressContainer.classList.add('hidden');
                showNotification('تمت مزامنة المفاتيح بنجاح!', 'success');
            }, 500);
        }
    }, 200);
    
    // إرسال المفاتيح للسيرفر
    try {
        await apiCall('/api/sync-keys', 'POST', keys);
        state.apiKeys = keys;
    } catch (error) {
        console.error('Sync error:', error);
    }
}

async function executeAgentCommand(command) {
    if (!command.trim()) return;
    
    // إضافة الأمر للدردشة
    addChatMessage(command, false);
    
    // مسح حقل الإدخال
    document.getElementById('chat-input').value = '';
    
    // إرسال الأمر للسيرفر
    try {
        const response = await apiCall('/api/agent/execute', 'POST', {
            command: command
        });
        
        if (response && response.success) {
            addChatMessage(`جاري تنفيذ: ${command}...`);
            
            // محاكاة الرد
            setTimeout(() => {
                addChatMessage(`تم تنفيذ الأمر بنجاح! ✅`);
            }, 1500);
        }
    } catch (error) {
        console.error('Command error:', error);
        addChatMessage('حدث خطأ في تنفيذ الأمر ❌');
    }
}

async function executeTerminalCommand(command) {
    if (!command.trim()) return;
    
    // إضافة الأمر للترمينال
    addTerminalLine(command, true);
    
    // مسح حقل الإدخال
    document.getElementById('terminal-input').value = '';
    
    // إرسال الأمر للسيرفر
    try {
        const response = await apiCall('/api/terminal/execute', 'POST', {
            command: command
        });
        
        if (response && response.success) {
            // إضافة النتيجة
            response.output.split('\n').forEach(line => {
                if (line.trim()) {
                    addTerminalLine(line);
                }
            });
        } else {
            addTerminalLine(`خطأ: ${response.error}`, false);
        }
    } catch (error) {
        console.error('Terminal error:', error);
        addTerminalLine('خطأ في تنفيذ الأمر', false);
    }
}

async function loadSystemStats() {
    try {
        const response = await apiCall('/stats');
        
        if (response) {
            // تحديث الإحصائيات
            document.getElementById('storage-used').textContent = 
                response.storage?.cache_size_mb + ' MB' || '0 MB';
            document.getElementById('active-tasks').textContent = 
                response.active_sessions || '0';
            document.getElementById('latency').textContent = 
                Math.random() * 50 + ' ms';
            
            // تحديث معلومات النظام
            const systemInfo = `
                النماذج المتاحة: ${response.ai_models?.length || 0}
                الجلسات النشطة: ${response.active_sessions || 0}
                التكلفة الإجمالية: ${response.total_cost || '0 USD'}
            `;
            document.getElementById('system-info').textContent = systemInfo;
        }
    } catch (error) {
        console.error('Stats error:', error);
    }
}

function updateUserStatus() {
    const userStatus = document.getElementById('user-status');
    if (state.isLoggedIn) {
        userStatus.textContent = `متصل - ${state.deviceId.substring(0, 10)}...`;
    } else {
        userStatus.textContent = 'غير متصل';
    }
}

function showNotification(message, type = 'info') {
    console.log(`[${type.toUpperCase()}] ${message}`);
    // يمكن إضافة نظام إشعارات بصري هنا
}

// ============================================================================
// Event Listeners
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    // تهيئة معرف الجهاز
    document.getElementById('device-id').value = state.deviceId;
    
    // زر تسجيل الدخول
    document.getElementById('login-btn').addEventListener('click', login);
    
    // أزرار الملاحة
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            showPage(link.dataset.page);
        });
    });
    
    // زر تسجيل الخروج
    document.getElementById('logout-btn').addEventListener('click', () => {
        state.isLoggedIn = false;
        state.sessionToken = null;
        showPage('login');
        showNotification('تم تسجيل الخروج');
    });
    
    // مزامنة المفاتيح
    document.getElementById('sync-keys-btn').addEventListener('click', syncApiKeys);
    
    // إرسال رسالة الدردشة
    document.getElementById('send-btn').addEventListener('click', () => {
        const input = document.getElementById('chat-input');
        executeAgentCommand(input.value);
    });
    
    document.getElementById('chat-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            executeAgentCommand(e.target.value);
        }
    });
    
    // الأوامر السريعة
    document.querySelectorAll('.quick-cmd').forEach(btn => {
        btn.addEventListener('click', () => {
            executeAgentCommand(btn.dataset.cmd);
        });
    });
    
    // تنفيذ أمر الترمينال
    document.getElementById('terminal-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            executeTerminalCommand(e.target.value);
        }
    });
    
    // مسح الترمينال
    document.getElementById('clear-terminal').addEventListener('click', () => {
        document.getElementById('terminal-output').innerHTML = '';
        addTerminalLine('تم مسح الترمينال');
    });
    
    // الوضع الليلي
    document.getElementById('dark-mode').addEventListener('change', (e) => {
        if (e.target.checked) {
            document.documentElement.style.filter = 'invert(0)';
        } else {
            document.documentElement.style.filter = 'invert(1)';
        }
    });
    
    // إعادة التعيين
    document.getElementById('reset-btn').addEventListener('click', () => {
        if (confirm('هل أنت متأكد من رغبتك في إعادة تعيين جميع البيانات؟')) {
            localStorage.clear();
            location.reload();
        }
    });
    
    // إخفاء شاشة التحميل بعد التهيئة
    setTimeout(() => {
        showLoadingScreen(false);
    }, 2000);
});

// تحديث الإحصائيات كل 5 ثوان
setInterval(() => {
    if (state.isLoggedIn) {
        loadSystemStats();
    }
}, 5000);

// ============================================================================
// WebSocket Connection (Optional)
// ============================================================================

let ws = null;

function connectWebSocket() {
    if (!state.isLoggedIn) return;
    
    ws = new WebSocket(`ws://localhost:8080/ws`);
    
    ws.onopen = () => {
        console.log('WebSocket متصل');
        addChatMessage('تم الاتصال بالسيرفر بنجاح! 🟢');
    };
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.type === 'agent_response') {
            addChatMessage(data.message);
        } else if (data.type === 'notification') {
            showNotification(data.message, data.level);
        } else if (data.type === 'task_update') {
            console.log('تحديث المهمة:', data.task);
        }
    };
    
    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };
    
    ws.onclose = () => {
        console.log('WebSocket مغلق');
        // محاولة إعادة الاتصال بعد 3 ثوان
        setTimeout(connectWebSocket, 3000);
    };
}

// الاتصال بـ WebSocket عند تسجيل الدخول
document.addEventListener('login-success', connectWebSocket);
