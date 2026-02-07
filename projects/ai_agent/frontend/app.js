// app.js - منطق الواجهة الأمامية

const API_BASE_URL = 'http://localhost:8000/api';

// State Management
const state = {
    projects: [],
    tasks: [],
    nodes: [],
    currentPage: 'dashboard',
    stats: {
        activeProjects: 0,
        completedTasks: 0,
        activeNodes: 0,
        performance: 92
    }
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
    loadDashboard();
});

function initializeApp() {
    console.log('🚀 تهيئة التطبيق...');
    
    // تحميل البيانات الأولية
    loadStats();
    loadProjects();
    loadNodes();
}

function setupEventListeners() {
    // Navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            switchPage(item.dataset.page);
        });
    });
    
    // Command Input
    document.getElementById('send-command').addEventListener('click', sendCommand);
    document.getElementById('command-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && e.ctrlKey) {
            sendCommand();
        }
    });
    
    // Modal Close
    document.querySelector('.close').addEventListener('click', closeModal);
    
    // Filter Buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            filterTasks(btn.dataset.filter);
        });
    });
}

function switchPage(page) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    
    // Show selected page
    document.getElementById(page).classList.add('active');
    
    // Update navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.dataset.page === page) {
            item.classList.add('active');
        }
    });
    
    // Update page title
    const titles = {
        'dashboard': 'لوحة التحكم',
        'projects': 'المشاريع',
        'tasks': 'المهام',
        'nodes': 'العقد',
        'settings': 'الإعدادات'
    };
    
    document.getElementById('page-title').textContent = titles[page];
    state.currentPage = page;
}

async function sendCommand() {
    const commandInput = document.getElementById('command-input');
    const command = commandInput.value.trim();
    
    if (!command) {
        alert('الرجاء إدخال أمر');
        return;
    }
    
    console.log('📤 إرسال أمر:', command);
    
    try {
        const response = await fetch(`${API_BASE_URL}/agent/execute`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ command })
        });
        
        const data = await response.json();
        
        if (data.success) {
            console.log('✅ تم إرسال الأمر بنجاح');
            commandInput.value = '';
            
            // إضافة المشروع الجديد
            state.projects.unshift(data);
            renderProjects();
            
            // عرض رسالة نجاح
            showNotification('تم إنشاء المشروع بنجاح! 🎉', 'success');
        } else {
            showNotification('حدث خطأ: ' + data.error, 'error');
        }
    } catch (error) {
        console.error('❌ خطأ في إرسال الأمر:', error);
        showNotification('فشل الاتصال بالسيرفر', 'error');
    }
}

async function loadStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats`);
        const data = await response.json();
        
        if (data.success) {
            state.stats = data.stats;
            updateStatsDisplay();
        }
    } catch (error) {
        console.error('خطأ في تحميل الإحصائيات:', error);
    }
}

async function loadProjects() {
    try {
        const response = await fetch(`${API_BASE_URL}/projects`);
        const data = await response.json();
        
        if (data.success) {
            state.projects = data.projects;
            renderProjects();
        }
    } catch (error) {
        console.error('خطأ في تحميل المشاريع:', error);
    }
}

async function loadNodes() {
    try {
        const response = await fetch(`${API_BASE_URL}/nodes`);
        const data = await response.json();
        
        if (data.success) {
            state.nodes = data.nodes;
            renderNodes();
        }
    } catch (error) {
        console.error('خطأ في تحميل العقد:', error);
    }
}

function updateStatsDisplay() {
    document.getElementById('active-projects').textContent = state.stats.activeProjects;
    document.getElementById('completed-tasks').textContent = state.stats.completedTasks;
    document.getElementById('active-nodes').textContent = state.stats.activeNodes;
    document.getElementById('performance').textContent = state.stats.performance + '%';
}

function renderProjects() {
    const projectsList = document.getElementById('projects-list');
    const projectsTbody = document.getElementById('projects-tbody');
    
    if (projectsList) {
        projectsList.innerHTML = state.projects.slice(0, 6).map(project => `
            <div class="project-card" onclick="showProjectDetails('${project.id}')">
                <h4>${project.command}</h4>
                <p>${project.description || 'لا توجد وصف'}</p>
                <span class="project-status status-${project.status}">
                    ${getStatusLabel(project.status)}
                </span>
                <div style="margin-top: 10px; font-size: 12px; color: #666;">
                    ${project.progress}% مكتمل
                </div>
            </div>
        `).join('');
    }
    
    if (projectsTbody) {
        projectsTbody.innerHTML = state.projects.map(project => `
            <tr>
                <td>${project.command}</td>
                <td><span class="project-status status-${project.status}">${getStatusLabel(project.status)}</span></td>
                <td>
                    <div style="width: 100px; height: 8px; background: #e5e7eb; border-radius: 4px; overflow: hidden;">
                        <div style="width: ${project.progress}%; height: 100%; background: #6366f1;"></div>
                    </div>
                </td>
                <td>${new Date(project.started_at).toLocaleDateString('ar-SA')}</td>
                <td>
                    <button onclick="showProjectDetails('${project.id}')" style="background: none; border: none; cursor: pointer; color: #6366f1;">👁️</button>
                </td>
            </tr>
        `).join('');
    }
}

function renderNodes() {
    const nodesGrid = document.getElementById('nodes-grid');
    
    if (nodesGrid) {
        nodesGrid.innerHTML = state.nodes.map(node => `
            <div class="project-card">
                <h4>${node.id}</h4>
                <p>السعة: ${node.capacity} MB</p>
                <p>السرعة: ${node.speed} Mbps</p>
                <p>التأخير: ${node.latency} ms</p>
                <span class="project-status" style="background: #dcfce7; color: #166534;">
                    ${node.status === 'active' ? '🟢 نشط' : '🔴 غير نشط'}
                </span>
            </div>
        `).join('');
    }
}

function filterTasks(filter) {
    // محاكاة تصفية المهام
    console.log('تصفية المهام:', filter);
}

function getStatusLabel(status) {
    const labels = {
        'pending': '⏳ قيد الانتظار',
        'running': '⚙️ قيد التنفيذ',
        'completed': '✅ مكتملة',
        'failed': '❌ فشلت'
    };
    return labels[status] || status;
}

function showProjectDetails(projectId) {
    const project = state.projects.find(p => p.id === projectId);
    
    if (!project) return;
    
    const modal = document.getElementById('project-modal');
    const modalBody = document.getElementById('modal-body');
    
    modalBody.innerHTML = `
        <div style="margin-bottom: 20px;">
            <h3>${project.command}</h3>
            <p style="color: #666; margin-top: 10px;">${project.description || 'لا توجد وصف'}</p>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px;">
            <div>
                <strong>الحالة:</strong>
                <p>${getStatusLabel(project.status)}</p>
            </div>
            <div>
                <strong>التقدم:</strong>
                <p>${project.progress}%</p>
            </div>
            <div>
                <strong>عدد المهام:</strong>
                <p>${project.tasks_total}</p>
            </div>
            <div>
                <strong>المهام المكتملة:</strong>
                <p>${project.tasks_completed}</p>
            </div>
        </div>
        
        <div style="margin-bottom: 20px;">
            <strong>شريط التقدم:</strong>
            <div style="width: 100%; height: 20px; background: #e5e7eb; border-radius: 10px; overflow: hidden; margin-top: 10px;">
                <div style="width: ${project.progress}%; height: 100%; background: linear-gradient(90deg, #6366f1, #8b5cf6);"></div>
            </div>
        </div>
        
        <div style="background: #f8fafc; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <strong>التاريخ:</strong>
            <p>البدء: ${new Date(project.started_at).toLocaleString('ar-SA')}</p>
            <p>المتوقع: ${new Date(project.estimated_completion).toLocaleString('ar-SA')}</p>
        </div>
        
        ${project.errors && project.errors.length > 0 ? `
            <div style="background: #fef2f2; padding: 15px; border-radius: 8px; border-right: 4px solid #ef4444;">
                <strong>الأخطاء (${project.errors.length}):</strong>
                <ul style="margin-top: 10px; padding-right: 20px;">
                    ${project.errors.map(err => `<li>${err.error}</li>`).join('')}
                </ul>
            </div>
        ` : ''}
    `;
    
    modal.classList.add('show');
}

function closeModal() {
    document.getElementById('project-modal').classList.remove('show');
}

function loadDashboard() {
    // تحديث البيانات كل 5 ثواني
    setInterval(() => {
        loadStats();
        loadProjects();
        loadNodes();
    }, 5000);
}

function showNotification(message, type = 'info') {
    // محاكاة عرض إشعار
    console.log(`[${type.toUpperCase()}] ${message}`);
    
    // يمكن إضافة مكتبة إشعارات حقيقية هنا
    alert(message);
}
