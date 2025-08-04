# Task: Monitoring Setup with Prometheus and Grafana
The objective is to deploy a monitoring system using Prometheus and Grafana, collect metrics from a
sample application, and visualize key data points on dashboards.
## Requirements
1. Deploy Prometheus and Grafana and configure them for use in a typical SRE environment.
2. Use or create a sample application that exposes Prometheus-compatible metrics (e.g., request count, latency, error rate).
3. Important: Application should be running within separate VM running Linux distribution of your choice.
4. Instrument at least 3 custom metrics in the application.
5. Visualize collected metrics in Grafana dashboards.
6. Configure at least one alerting rule (e.g., high response time or error rate).
7. Optional: Use Docker or Docker Compose to containerize and simplify deployment.

## Components

- Dummy application with Prometheus metrics (deployed on a separate VM using Ansible)
- Prometheus for metrics collection
- Grafana for visualization with pre-configured dashboards
- Ansible for application deployment automation
- Cloud-init for VM provisioning

## VM Deployment

### Prerequisites

1. A VM provider that supports cloud-init (e.g., AWS, GCP, Azure, or local hypervisor)
2. SSH client for connecting to VMs

### Deployment Architecture

The deployment architecture consists of:

1. **Application VM** - Runs the Dummy application as a systemd service
2. **Ansible Control VM** - Dedicated VM for managing deployments with Ansible
3. **Monitoring Stack** - Prometheus and Grafana running locally or on a separate host

### Deployment Steps

#### 1. Create the Application VM

Create a VM using the cloud-init file:

```bash
# Example with a cloud provider that supports cloud-init
orb create ubuntu app-vm -c vm-deployment/cloud-init/app-vm-cloud-init.yml
```

Note the IP address of the VM after creation.

#### 2. Create the Ansible Control VM

Create a VM for Ansible using the cloud-init file:

```bash
orb create ubuntu ansible-vm -c vm-deployment/cloud-init/ansible-vm-cloud-init.yml
```

Note the IP address of this VM as well.

#### 3. Configure the Ansible Control VM

SSH into the Ansible control VM using the default password:

```bash
ssh ansible@<ANSIBLE_VM_IP>
# Password: ansible123 visible in the cloud-init file
```

Copy your monitoring system files to the Ansible VM:

```bash
# From your local machine
scp -r /path/to/monitoring-system/* ansible@<ANSIBLE_VM_IP>:~/monitoring-system/
# Password: ansible123 visible in the cloud-init file
```

#### 4. Update Configuration Files

On the Ansible control VM, update the inventory file with the application VM's IP:

```bash
# Replace APP_VM_IP with the actual IP address
sed -i 's/APP_VM_IP/<ACTUAL_APP_VM_IP>/g' ~/monitoring-system/vm-deployment/ansible/inventory.ini
```

#### 5. Deploy the Application

From the Ansible control VM, run the deployment playbook:

```bash
cd ~/monitoring-system/vm-deployment/ansible
ansible-playbook -i inventory.ini deploy_app.yml
```

#### 6. Configure Prometheus

On your local machine or monitoring host, update the Prometheus configuration:

```bash
# Replace APP_VM_IP with the actual IP address
sed -i 's/APP_VM_IP/<ACTUAL_APP_VM_IP>/g' prometheus/prometheus.yml
```

#### 7. Start the Monitoring Stack

Start Prometheus and Grafana:

```bash
docker-compose up -d
```

## Accessing Services

- Flask Application: http://<VM_IP>:5000
- Application Metrics: http://<VM_IP>:8000
- Prometheus: http://localhost:9090
- **Grafana**: http://localhost:3000 (credentials from .env file)
  - Prometheus datasource is pre-configured
  - Dashboards are automatically provisioned

## Metrics Collected

1. Request Count (`request_count`)
   - Total number of requests by endpoint and method
2. Request Latency (`request_latency_seconds`)
   - Histogram of request processing time
3. Error Count (`error_count`)
   - Number of errors by endpoint and status code
3. Error Count (`error_count`)
   - Number of errors by endpoint and status code

### Screenshot
<img width="2325" height="1585" alt="image" src="https://github.com/user-attachments/assets/3c8cedbe-69cf-4b02-96b4-04b87b9a984a" />

## Alerting

- High Request Latency Alert:
  - Triggers when 95th percentile latency exceeds 500ms for 5 minutes
  - Severity: warning

## Sample Endpoints

- `/`: Home page
- `/api/data`: Simulated API endpoint with variable latency and error rate
