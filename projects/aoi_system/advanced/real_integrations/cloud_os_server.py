# cloud_os_server.py - الخادم الذي يعمل في Termux
from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import sys
import os

# إضافة المسار الحالي
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cloud_os_core import (
    CloudVMOrchestrator,
    MultiLLMCloudEngine,
    UniversalStoreManager,
    CloudGamingLauncher,
    AutonomousAgentSystem
)

app = Flask(__name__)
CORS(app)

# المكونات العالمية
vm_orchestrator = CloudVMOrchestrator()
llm_engine = None
store_manager = None
gaming_launcher = None

@app.route('/api/vm/create', methods=['POST'])
def create_vm():
    specs = request.json
    loop = asyncio.new_event_loop()
    vm = loop.run_until_complete(vm_orchestrator.create_cloud_vm(specs))
    return jsonify({
        "success": True,
        "vm_id": vm.vm_id,
        "ip_address": vm.ip_address,
        "vnc_port": vm.vnc_port,
        "ssh_port": vm.ssh_port,
        "provider": vm.provider
    })

@app.route('/api/llm/deploy-all', methods=['POST'])
def deploy_llms():
    global llm_engine
    llm_engine = MultiLLMCloudEngine(vm_orchestrator)
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(llm_engine.deploy_all_llms())
    return jsonify(result)

@app.route('/api/stores/setup-all', methods=['POST'])
def setup_stores():
    global store_manager
    vm = list(vm_orchestrator.active_vms.values())[0]
    store_manager = UniversalStoreManager(vm)
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(store_manager.setup_all_stores())
    return jsonify(result)

@app.route('/api/games/launch', methods=['POST'])
def launch_game():
    global gaming_launcher
    data = request.json
    vm = list(vm_orchestrator.active_vms.values())[0]
    gaming_launcher = CloudGamingLauncher(vm)
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(gaming_launcher.launch_game(data['name']))
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
