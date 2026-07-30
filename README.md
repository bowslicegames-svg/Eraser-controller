# C2 Research Framework

A modular framework for studying agent-based network orchestration.

## Setup
1. Controller: Run python3 controller.py on your management server.
2. Build Agent: Run ./build.sh to compile the Go agent.
3. Deployment: Execute the resulting binary on the target node.

## Usage
- Registration: Agents automatically register via POST /register.
- Tasking: Send commands via POST /command to trigger agent tasks.
- Monitoring: The controller tracks active agent UUIDs in memory.

## Disclaimer
This tool is for educational purposes only. Use only in authorized, sandboxed environments.
