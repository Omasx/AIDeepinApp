// agent_panel.js - منطق الواجهة المتقدم
class AgentPanel {
    constructor() {
        this.serverUrl = 'http://localhost:8000';
        this.init();
    }

    init() {
        document.getElementById('send-command-btn').addEventListener('click', () => this.sendCommand());
        this.loadProjects();
    }

    async sendCommand() {
        const command = document.getElementById('command-input').value;
        const response = await fetch(`${this.serverUrl}/api/agent/execute`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ command, user_id: 'user_1' })
        });
        const result = await response.json();
        alert('تم البدء: ' + result.project_id);
        this.loadProjects();
    }

    async loadProjects() {
        const response = await fetch(`${this.serverUrl}/api/agent/projects`);
        const projects = await response.json();
        const grid = document.getElementById('projects-grid');
        grid.innerHTML = '';
        projects.forEach(p => {
            const card = document.createElement('div');
            card.className = 'project-card';
            card.innerHTML = `<h3>${p.command}</h3><p>الحالة: ${p.status}</p><p>التقدم: ${p.progress}%</p>`;
            grid.appendChild(card);
        });
    }
}

document.addEventListener('DOMContentLoaded', () => new AgentPanel());
