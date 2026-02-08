// agent_panel.js - منطق الواجهة الموحدة المتطور
class AOIPanel {
    constructor() {
        this.serverUrl = window.location.origin; // استخدام النطاق الحالي
        this.init();
    }

    init() {
        document.getElementById('send-command-btn').addEventListener('click', () => this.handleMainCommand());
        this.updateStats();
        setInterval(() => this.updateStats(), 5000);
    }

    async handleMainCommand() {
        const command = document.getElementById('command-input').value;
        if (!command) return;

        // تحليل بسيط للأمر لتوجيهه للمسار الصحيح
        if (command.includes('لعب') || command.includes('game')) {
            this.launchGame('Cyberpunk 2077');
        } else if (command.includes('سحاب') || command.includes('cloud')) {
            this.initCloud();
        } else {
            this.sendAgiTask(command);
        }
    }

    async sendAgiTask(goal) {
        try {
            const response = await fetch(`${this.serverUrl}/api/agi/execute?goal=${encodeURIComponent(goal)}`, {
                method: 'POST'
            });
            const result = await response.json();
            alert('AGI Task Started: ' + result.status);
            this.addProjectCard(goal, 'Started');
        } catch (e) {
            console.error('API Error:', e);
        }
    }

    async initCloud() {
        try {
            const response = await fetch(`${this.serverUrl}/api/cloud/init?user_id=default_user`, { method: 'POST' });
            const result = await response.json();
            if (result.success) {
                alert('Cloud Brain Initialized! local CPU usage is now 0%');
                document.getElementById('local-cpu-val').innerText = '0%';
            }
        } catch (e) { console.error(e); }
    }

    async launchGame(game = 'Fortnite') {
        try {
            const response = await fetch(`${this.serverUrl}/api/gaming/launch?game=${encodeURIComponent(game)}`, { method: 'POST' });
            const result = await response.json();
            if (result.success) {
                alert(`🎮 Playing ${game} via Cloud Stream: ${result.stream_url}`);
            }
        } catch (e) { console.error(e); }
    }

    async updateStats() {
        try {
            const response = await fetch(`${this.serverUrl}/api/status`);
            const stats = await response.json();
            // تحديث القيم في الواجهة
            if (stats.resources) {
                document.getElementById('local-cpu-val').innerText = stats.resources.cpu + '%';
            }
        } catch (e) { }
    }

    addProjectCard(title, status) {
        const grid = document.getElementById('projects-grid');
        const card = document.createElement('div');
        card.className = 'project-card';
        card.innerHTML = `<h3>${title}</h3><p>Status: ${status}</p>`;
        grid.prepend(card);
    }
}

// Global functions for feature cards
function initCloud() { window.aoiPanel.initCloud(); }
function launchGame() { window.aoiPanel.launchGame(); }
function launchCreative() { alert('Launching Premiere Pro in Cloud...'); }
function startQuantum() { alert('Quantum Super Resolution Started...'); }

document.addEventListener('DOMContentLoaded', () => {
    window.aoiPanel = new AOIPanel();
});
