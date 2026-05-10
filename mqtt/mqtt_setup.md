# Mosquitto MQTT Broker — Setup Guide

## Overview
Mosquitto is an open-source MQTT broker used to enable 
secure communication between IoT devices in our 
Industry 4.0 demo setup.

## Phase 1: Installation

### 1. Update system
```bash
sudo apt update && sudo apt upgrade
```

### 2. Install Mosquitto
```bash
sudo apt install mosquitto mosquitto-clients
```

### 3. Enable and start service
```bash
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

### 4. Verify installation
```bash
mosquitto -v
```

---

## Phase 2: Configure Authentication

### 1. Create password file
```bash
sudo mosquitto_passwd -c /etc/mosquitto/passwd mqttuser
```
Enter password: mqtt1234

### 2. Edit configuration
```bash
sudo nano /etc/mosquitto/mosquitto.conf
```

Add these lines:

allow_anonymous false
password_file /etc/mosquitto/passwd
listener 1883 localhost

### 3. Restart broker
```bash
sudo systemctl restart mosquitto
```

---

## Phase 3: Configure TLS Encryption

### 1. Create certificates directory
```bash
sudo mkdir -p /etc/mosquitto/certs
cd /etc/mosquitto/certs
```

### 2. Generate CA certificate
```bash
sudo openssl genrsa -out ca.key 2048
sudo openssl req -new -x509 -days 365 \
-key ca.key -out ca.crt \
-subj "/CN=localhost"
```

### 3. Generate server certificate
```bash
sudo openssl genrsa -out server.key 2048
sudo openssl req -new -key server.key \
-out server.csr -subj "/CN=localhost"
sudo openssl x509 -req -days 365 \
-in server.csr -CA ca.crt \
-CAkey ca.key -CAcreateserial \
-out server.crt
```

### 4. Set permissions
```bash
sudo chown -R mosquitto:mosquitto /etc/mosquitto/certs/
sudo chmod 644 /etc/mosquitto/certs/ca.crt
sudo chmod 644 /etc/mosquitto/certs/server.crt
sudo chmod 600 /etc/mosquitto/certs/server.key
```

### 5. Update config for TLS
listener 8883
cafile /etc/mosquitto/certs/ca.crt
certfile /etc/mosquitto/certs/server.crt
keyfile /etc/mosquitto/certs/server.key
require_certificate false

### 6. Restart
```bash
sudo systemctl restart mosquitto
```

---

## Phase 4: Testing

### Test authentication
```bash
# Subscribe
mosquitto_sub -h localhost -p 1883 \
-u mqttuser -P mqtt1234 \
-t factory/sensor

# Publish
mosquitto_pub -h localhost -p 1883 \
-u mqttuser -P mqtt1234 \
-t factory/sensor \
-m '{"device":"sensor-01","temp":41,"pressure":99,"status":"normal"}'

# Test anonymous blocked
mosquitto_pub -h localhost -p 1883 \
-t factory/sensor -m "test"
```

---

## Security Features Implemented
- Username and password authentication
- Anonymous connections blocked
- TLS encryption configured on port 8883
- Self-signed SSL certificates generated

## Framework Mapping
- IEC 62443: Zone access control
- NIST CSF: Protect function
