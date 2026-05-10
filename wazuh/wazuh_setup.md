# Wazuh SIEM — Setup Guide

## Overview
Wazuh is an open-source security monitoring platform
used for real-time threat detection in our demo.

## Phase 1: Installation via Docker

### 1. Install Docker
```bash
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl enable docker
sudo systemctl start docker
```

### 2. Clone Wazuh Docker
```bash
git clone https://github.com/wazuh/wazuh-docker.git
cd wazuh-docker/single-node
```

### 3. Generate certificates
```bash
docker compose -f generate-indexer-certs.yml run --rm generator
```

### 4. Start Wazuh
```bash
docker compose up -d
```

### 5. Verify
```bash
docker compose ps
```

---

## Phase 2: Access Dashboard

Open: https://localhost

Credentials:
- Username: admin
- Password: SecretPassword

---

## Phase 3: Generate Security Alert

### Simulate brute force attack
```bash
ssh wronguser@localhost
# Run 5 times quickly
```

---

## Phase 4: View Alerts

Navigate to Security Events in dashboard.

### Alerts Detected
| Rule | Description | Severity |
|---|---|---|
| 5712 | Brute force attack detected | Level 10 |
| 5710 | Login attempt — non-existent user | Level 10 |
| 2502 | User missed password multiple times | Level 10 |

---

## Results
- 1,134 security events monitored
- Brute force detected within seconds
- Critical Level 10 alerts generated

## Framework Mapping
- NIST CSF: Detect and Respond
- IEC 62443: Continuous security monitoring
