# VM Deployment Guide

This directory contains the necessary files for deploying the Dummy application on a VM using Ansible.

## Deployment Architecture

The deployment architecture consists of:

1. **Application VM** - Runs the Flask application as a systemd service
2. **Ansible Control VM** - Dedicated VM for managing deployments with Ansible
3. **Monitoring Stack** - Prometheus and Grafana running locally or on a separate host

## Setup Instructions

### 1. Create the Application VM

Create a VM using the cloud-init file:

```bash
# Example with a cloud provider that supports cloud-init
# Replace with your preferred VM creation method
orb create ubuntu app-vm -c cloud-init/app-vm-cloud-init.yml
```

Note the IP address of the VM after creation.

### 2. Create the Ansible Control VM

Create a VM for Ansible using the cloud-init file:

```bash
orb create ubuntu ansible-vm -c cloud-init/ansible-vm-cloud-init.yml
```

Note the IP address of this VM as well.

### 3. Configure the Ansible Control VM

1. SSH into the Ansible control VM using the default password:

```bash
ssh ansible@<ANSIBLE_VM_IP>
# Password: ansible123
```

2. Copy the monitoring system files to the Ansible control VM:

```bash
# From your local machine
scp -r /path/to/monitoring-system/* ansible@<ANSIBLE_VM_IP>:~/monitoring-system/
# Password: ansible123
```

3. Update the Ansible inventory file with the Application VM's IP address:

```bash
# On the Ansible control VM
sed -i 's/APP_VM_IP/<APP_VM_IP>/g' ~/monitoring-system/vm-deployment/ansible/inventory.ini
```

### 4. Update Configuration Files

On the Ansible control VM, update the inventory file with the application VM's IP:

```bash
# Replace APP_VM_IP with the actual IP address
sed -i 's/APP_VM_IP/<ACTUAL_APP_VM_IP>/g' ~/monitoring-system/vm-deployment/ansible/inventory.ini
```

### 5. Deploy the Application

From the Ansible control VM, run the deployment playbook:

```bash
cd ~/monitoring-system/vm-deployment/ansible
ansible-playbook -i inventory.ini deploy_app.yml
```

### 6. Configure Prometheus

On your local machine or monitoring host, update the Prometheus configuration:

```bash
# Replace APP_VM_IP with the actual IP address
sed -i 's/APP_VM_IP/<ACTUAL_APP_VM_IP>/g' /path/to/monitoring-system/prometheus/prometheus.yml
```

### 7. Start the Monitoring Stack

Start Prometheus and Grafana:

```bash
cd /path/to/monitoring-system
docker-compose up -d
```

## Access Information

- **Flask Application**: http://<APP_VM_IP>:5000
- **Application Metrics**: http://<APP_VM_IP>:8000
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (credentials from .env file)
