# 🖥️ Azure Lab 02: Linux Virtual Machine & SSH Administration

Deploy an Ubuntu 24.04 LTS Linux Virtual Machine on Azure, configure Network Security Group rules, and host an active Nginx web server.

## 📖 Walkthrough Guide
Open [`index.html`](./index.html) in your browser for the interactive step-by-step guide.

## 🛠️ Key CLI Commands
```bash
az vm create \
  --resource-group rg-linux-vm-lab \
  --name vm-linux-web \
  --image Ubuntu2404 \
  --size Standard_B1s \
  --location westus2 \
  --admin-username azureuser \
  --generate-ssh-keys
```
