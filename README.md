# NetSpectre 🛡️
### Smart Home IoT Network Security Monitor

> A real-time network security monitoring system built on Raspberry Pi for smart home environments. Detects connected devices, monitors network intrusions, and controls the firewall — all from a centralised web dashboard.

---

## 📸 Dashboard Preview

> NetSpectre Dashboard showing live device discovery, IDPS alerts, and firewall status connected to Firebase Realtime Database.

---

## 🔍 What is NetSpectre?

NetSpectre is a **final year project** developed for module **COM4901** at the Faculty of Computer Science and Engineering, **KIU (Kotelawala Defence University)**.

It turns a **Raspberry Pi 4** into a fully autonomous Smart Home IoT Network Security Monitor with three core capabilities:

| Feature | Tool Used | Description |
|---|---|---|
| 🖧 Host Discovery | Nmap | Scans all connected networks and profiles every device |
| 🚨 Intrusion Detection (IDPS) | Suricata | Monitors network traffic and detects suspicious activity |
| 🔥 Firewall Control | UFW | Remotely enable, disable, and manage firewall rules |

All data is stored in **Firebase Realtime Database** and displayed on the **NetSpectre web dashboard** — accessible from any device on the network.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────┐
│             RASPBERRY PI 4              │
│                                         │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │   Nmap   │ │ Suricata │ │   UFW   │ │
│  │  (Scan)  │ │  (IDPS)  │ │  (FW)   │ │
│  └────┬─────┘ └────┬─────┘ └────┬────┘ │
│       └────────────┼─────────────┘      │
│            ┌───────▼────────┐           │
│            │  Flask API     │           │
│            │  Port 5000     │           │
│            └───────┬────────┘           │
└────────────────────┼────────────────────┘
                     │
                     ▼
          ┌─────────────────────┐
          │ Firebase Realtime DB │
          └──────────┬──────────┘
                     │
                     ▼
          ┌─────────────────────┐
          │  NetSpectre Dashboard│
          │   (Any Browser)     │
          └─────────────────────┘
```

---

## 📁 Project Structure

```
Desktop/
├── discover.py                              ← Standalone network scanner
└── Monitoring_System/
    ├── apiEndPoint.py                       ← Main Flask API server (Port 5000)
    ├── credentials.json                     ← Firebase service account key
    ├── firebase_admin_manager.py            ← Firebase package checker
    ├── hostDiscovery/
    │   ├── network_scan.sh                  ← Nmap scan + Firebase upload
    │   └── feed_data.py                     ← Parse XML → upload hosts to Firebase
    ├── idps/
    │   ├── alerts.sh                        ← Run IDPS pipeline
    │   ├── extractAlerts.py                 ← Parse Suricata fast.log → XML
    │   ├── feed_data.py                     ← Upload alerts to Firebase
    │   ├── clearAlerts.sh                   ← Clear alerts from Firebase
    │   ├── Toggle_On/onIdps.sh              ← Start Suricata
    │   └── Toggle_Off/offIdps.sh            ← Stop Suricata
    └── firewall/
        ├── Rules_Upload/
        │   ├── fw_rules.sh                  ← Extract + upload UFW rules
        │   ├── extractRules.py              ← Parse UFW rules → XML
        │   └── feed_data.py                 ← Upload rules to Firebase
        ├── Toggle_On/onFW.sh               ← Enable UFW firewall
        └── Toggle_Off/offFW.sh             ← Disable UFW firewall
```

---

## ⚙️ Requirements

### Hardware
- Raspberry Pi 4 (2GB RAM or higher)
- MicroSD card (16GB or higher)
- Ethernet and/or WiFi connection

### Software
- Raspberry Pi OS (Debian Bookworm or later)
- Python 3.11+
- Nmap
- Suricata
- UFW
- Firebase project (Realtime Database)

---

## 🚀 Installation and Setup

### Step 1 — Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/NetSpectre.git
cd NetSpectre
```

### Step 2 — Install required packages
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install nmap suricata ufw python3 python3-pip python3-venv -y
```

### Step 3 — Set up Python virtual environment
```bash
cd ~/Desktop/Monitoring_System
python3 -m venv myenv
source myenv/bin/activate
pip install firebase-admin
deactivate
```

### Step 4 — Configure Firebase
1. Go to [Firebase Console](https://console.firebase.google.com)
2. Create a new project
3. Enable **Realtime Database** in test mode
4. Go to **Project Settings → Service Accounts → Generate new private key**
5. Download the JSON file and save it as:
   ```
   ~/Desktop/Monitoring_System/credentials.json
   ```
6. Update the `databaseURL` in the following files with your Firebase URL:
   - `hostDiscovery/feed_data.py`
   - `idps/feed_data.py`
   - `firewall/Rules_Upload/feed_data.py`

### Step 5 — Make shell scripts executable
```bash
chmod +x ~/Desktop/Monitoring_System/hostDiscovery/network_scan.sh
chmod +x ~/Desktop/Monitoring_System/idps/alerts.sh
chmod +x ~/Desktop/Monitoring_System/idps/clearAlerts.sh
chmod +x ~/Desktop/Monitoring_System/idps/Toggle_On/onIdps.sh
chmod +x ~/Desktop/Monitoring_System/idps/Toggle_Off/offIdps.sh
chmod +x ~/Desktop/Monitoring_System/firewall/Rules_Upload/fw_rules.sh
chmod +x ~/Desktop/Monitoring_System/firewall/Toggle_On/onFW.sh
chmod +x ~/Desktop/Monitoring_System/firewall/Toggle_Off/offFW.sh
```

### Step 6 — Enable auto-start on boot (optional)
```bash
sudo systemctl enable apiEndPoint.service
sudo systemctl start apiEndPoint.service
```

---

## ▶️ Running the System

### Start the Flask API server
```bash
python3 ~/Desktop/Monitoring_System/apiEndPoint.py
```

### Run a network scan
```bash
curl -X POST http://localhost:5000/hostDiscovery
```

### Control via API endpoints

| Endpoint | Method | Action |
|---|---|---|
| `/hostDiscovery` | POST | Scan network and upload devices to Firebase |
| `/toggleFWon` | POST | Enable firewall |
| `/toggleFWoff` | POST | Disable firewall |
| `/updateRules` | POST | Upload firewall rules to Firebase |
| `/toggleIdpson` | POST | Start Suricata IDPS |
| `/toggleIdpsoff` | POST | Stop Suricata IDPS |
| `/updateAlerts` | POST | Upload IDPS alerts to Firebase |
| `/clearAlerts` | POST | Clear all alerts from Firebase |

---

## 🌐 NetSpectre Dashboard

Open `dashboard.html` in any browser on the same network as your Pi.

Update the following in the dashboard:
- **Firebase URL** — your Firebase Realtime Database URL
- **Pi IP Address** — your Raspberry Pi's IP (find with `hostname -I`)

The dashboard auto-refreshes every 30 seconds and shows:
- ✅ Total connected devices
- ✅ Firewall status (ON/OFF)
- ✅ IDPS status (ON/OFF)
- ✅ Active alert count
- ✅ Connected hosts with IP, MAC, OS, open ports, risk level
- ✅ IDPS alerts with classification, protocol, source/destination
- ✅ Firewall rules with allow/deny colour coding
- ✅ Remote control buttons for all features

---

## 🧪 Testing the System

### Generate test IDPS alerts
```bash
# Port scan your router to trigger Suricata
sudo nmap -sS YOUR_ROUTER_IP

# Then update alerts
curl -X POST http://localhost:5000/updateAlerts
```

### Test firewall blocking
```bash
# Block a device
sudo ufw deny from DEVICE_IP

# Upload rules to Firebase
curl -X POST http://localhost:5000/updateRules

# Unblock after demo
sudo ufw delete deny from DEVICE_IP
```

---

## 🔧 Troubleshooting

| Problem | Fix |
|---|---|
| Port 5000 already in use | `sudo fuser -k 5000/tcp` then restart |
| firebase_admin not found | `source myenv/bin/activate && pip install firebase-admin` |
| XML ParseError on scan | Delete old XML and re-run nmap scan |
| Suricata not running | `sudo systemctl start suricata` |
| No alerts in Firebase | Check `/var/log/suricata/fast.log` has data first |
| Dashboard can't reach Pi | Make sure laptop and Pi are on the same network |

---

## 🛠️ Technologies Used

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.11 | Main programming language |
| Flask | 3.x | REST API framework |
| Nmap | 7.93 | Network scanning |
| Suricata | 6.x | Intrusion detection |
| UFW | 0.36 | Firewall management |
| Firebase Admin SDK | 6.x | Cloud database client |
| Firebase Realtime DB | — | Cloud data storage |
| HTML/CSS/JavaScript | — | Web dashboard |

---

## 👨‍💻 Multi-Vendor IoT Device Testing

The system was tested against simulated multi-vendor IoT devices using Linux VMs:

| Vendor | Device | Test Focus |
|---|---|---|
| Hikvision | IP Security Camera | RTSP ports, camera service detection |
| Xiaomi | Smart Bulb | MQTT-based device detection |
| Suprema | Biometric Reader | Access control device profiling |
| Samsung | Smart TV | Multi-port consumer device detection |

---

## 📄 Academic Information

| Field | Details |
|---|---|
| Project Title | NetSpectre: Smart Home IoT Network Security Monitor |
| Module | COM4901 — Final Year Project |
| Institution | KIU — Kotelawala Defence University |
| Faculty | Computer Science and Engineering |
| Supervisor | [Supervisor Name] |
| Student | [Your Name] — [Your ID] |

---

## 📝 License

This project is developed for academic purposes at KIU. All rights reserved.

---

## ⭐ If you found this project helpful, please give it a star!
