# ⚖️ Azure Lab 05: Auto-Scaling & Standard Load Balancer

Build an elastic, highly available web tier using Azure Standard Load Balancer and Virtual Machine Scale Sets (VMSS) running Ubuntu 24.04 and Nginx, validated via real-time CPU stress testing.

## 📖 Walkthrough Guide
Open [`index.html`](./index.html) in your browser for the full interactive deck.

## 🧪 Stress Test Command
```bash
sudo apt update && sudo apt install -y stress-ng
stress-ng --cpu $(nproc) --cpu-load 85 --timeout 300
```
