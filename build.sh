#!/bin/bash
# Compile for Linux/Windows/macOS
GOOS=linux GOARCH=amd64 go build -o agent_linux agent.go
GOOS=windows GOARCH=amd64 go build -o agent_win.exe agent.go
echo "Compilation complete."
