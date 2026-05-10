# Node-RED — Setup Guide

## Overview
Node-RED is a flow-based programming tool used to build
our real-time industrial monitoring dashboard.

## Phase 1: Installation

### 1. Install Node.js
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs
node -v && npm -v
```

### 2. Install Node-RED
```bash
sudo npm install -g --unsafe-perm node-red
```

### 3. Start Node-RED
```bash
node-red
```

Open browser: http://localhost:1880

---

## Phase 2: Install Dashboard Plugin

1. Click hamburger menu → Manage Palette
2. Click Install tab
3. Search: node-red-dashboard
4. Click Install

---

## Phase 3: Flow Structure
[inject] → [function 1] → [mqtt out: factory/sensor]
↓
(Mosquitto Broker)
↓
[mqtt in] → [json] → [function 2] → [Temperature gauge]
→ [Temp Over Time chart]
→ [Pressure gauge]
→ [Device Status text]

## Function 1 — Sensor Data Generator
```javascript
msg.payload = JSON.stringify({
    device: "sensor-01",
    temperature: Math.floor(Math.random() * 40) + 20,
    pressure: Math.floor(Math.random() * 10) + 90,
    status: "normal",
    timestamp: new Date().toISOString()
});
return msg;
```

## Function 2 — Value Extractor
```javascript
msg.payload = msg.payload.temperature;
msg.topic = "Temperature";
return msg;
```

## MQTT Node Configuration
- Broker: localhost
- Port: 1883
- Username: mqttuser
- Password: mqtt1234
- Topic: factory/sensor

---

## Phase 4: View Dashboard

Open: http://localhost:1880/ui

Shows:
- Live temperature gauge
- Temperature chart over time
- Pressure gauge
- Device status

---

## Framework Mapping
- NIST CSF: Detect function
- IEC 62443: Conduit data management
