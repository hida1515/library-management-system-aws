# AWS EC2 & RDS Deployment Guide

A step-by-step technical guide for deploying the **Library Management System** (Django + MySQL + Gunicorn + Nginx) on **AWS EC2** connected to **AWS RDS MySQL**.

---

## 1. AWS Account Preparation

Ensure you have access to the AWS Management Console with permissions to provision EC2, RDS, and VPC Security Groups.

---

## 2. EC2 Instance Creation

1. Open AWS Management Console &rarr; **EC2 Dashboard**.
2. Click **Launch Instance**.
3. Name your instance: `library-system-server`.

---

## 3. AMI Selection (Amazon Machine Image)

Choose an official operating system AMI:
* **Amazon Linux 2023 AMI** (Default username: `ec2-user`)
* **Ubuntu Server 22.04 LTS** (Default username: `ubuntu`)

---

## 4. Instance Type

Select **t2.micro** or **t3.micro** (Free Tier Eligible, 1 vCPU, 1 GiB Memory).

---

## 5. Key Pair Creation & Download

1. Click **Create new key pair**.
2. Name: `library-ec2-key`.
3. Private key file format: `.pem` (for SSH via OpenSSH).
4. Download and save `library-ec2-key.pem` safely on your computer.

---

## 6. Security Group Configuration

Create a Security Group named `library-ec2-sg` with inbound rules:

| Type | Protocol | Port Range | Source | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **SSH** | TCP | 22 | My IP (`x.x.x.x/32`) | Secure terminal access |
| **HTTP** | TCP | 80 | Anywhere (`0.0.0.0/0`) | Public web traffic |
| **HTTPS** | TCP | 443 | Anywhere (`0.0.0.0/0`) | Secure Web (if SSL configured) |
| **Custom TCP** | TCP | 8000 | Anywhere (`0.0.0.0/0`) | Django dev testing (optional) |

---

## 7. Connecting via SSH

Set private key permissions and connect to EC2:

* **For Amazon Linux 2023**:
  ```bash
  chmod 400 library-ec2-key.pem
  ssh -i library-ec2-key.pem ec2-user@YOUR_EC2_PUBLIC_IP
  ```

* **For Ubuntu Server**:
  ```bash
  chmod 400 library-ec2-key.pem
  ssh -i library-ec2-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
  ```

---

## 8. Uploading Files via SCP (Secure Copy Protocol)

To upload project files or archives directly from your local machine to EC2:
```bash
# Upload a compressed project archive
scp -i library-ec2-key.pem project.tar.gz ec2-user@YOUR_EC2_PUBLIC_IP:/home/ec2-user/
```

---

## 9. Essential Linux Setup Commands

Update system packages:
```bash
# On Amazon Linux:
sudo dnf update -y

# On Ubuntu:
sudo apt update && sudo apt upgrade -y
```

---

## 10. Python Installation

Ensure Python 3.9+ and pip are installed:
```bash
# Amazon Linux
sudo dnf install python3 python3-pip -y

# Ubuntu
sudo apt install python3 python3-pip python3-venv -y
```

---

## 11. Git Installation

Install Git:
```bash
# Amazon Linux
sudo dnf install git -y

# Ubuntu
sudo apt install git -y
```

---

## 12. Clone GitHub Repository

Clone the project repository to `/home/ec2-user/`:
```bash
git clone https://github.com/YOUR_USERNAME/library-management-system-aws.git
cd library-management-system-aws
```

---

## 13. Create Virtual Environment

Initialize and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 14. Install Requirements

Install required dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 15. AWS RDS MySQL Instance Setup

1. Open AWS Console &rarr; **RDS** &rarr; **Create Database**.
2. Select **MySQL** engine (Community edition).
3. DB Instance Identifier: `library-db-instance`.
4. Master Username: `admin`.
5. Master Password: `YourSecurePassword123!`.
6. VPC Security Group: Create `library-rds-sg` allowing **Inbound MySQL Port 3306** *only from `library-ec2-sg`*.
7. Copy the generated **RDS Endpoint** (e.g., `library-db-instance.xxxxxx.us-east-1.rds.amazonaws.com`).

---

## 16. Configure Environment & `ALLOWED_HOSTS`

Create `.env` file on EC2:
```bash
nano .env
```
Paste configuration:
```env
SECRET_KEY=your_production_secret_key_here
DEBUG=False
ALLOWED_HOSTS=YOUR_EC2_PUBLIC_IP,localhost,127.0.0.1
DB_NAME=library_db
DB_USER=admin
DB_PASSWORD=YourSecurePassword123!
DB_HOST=library-db-instance.xxxxxx.us-east-1.rds.amazonaws.com
DB_PORT=3306
```

---

## 17. Run Migrations & Populate Data

Initialize database schema on AWS RDS MySQL:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py populate_library
python manage.py createsuperuser
```

---

## 18. Gunicorn Setup

Test running Gunicorn:
```bash
gunicorn --bind 0.0.0.0:8000 library_management.wsgi:application
```

Create systemd service `/etc/systemd/system/gunicorn.service`:
```ini
[Unit]
Description=Gunicorn daemon for Library Management System
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/library-management-system-aws
ExecStart=/home/ec2-user/library-management-system-aws/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ec2-user/library-management-system-aws/gunicorn.sock library_management.wsgi:application

[Install]
WantedBy=multi-user.target
```

Enable & Start Gunicorn:
```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

---

## 19. Nginx Reverse Proxy Setup

Install Nginx:
```bash
# Amazon Linux
sudo dnf install nginx -y

# Ubuntu
sudo apt install nginx -y
```

Create configuration `/etc/nginx/conf.d/library.conf`:
```nginx
server {
    listen 80;
    server_name YOUR_EC2_PUBLIC_IP;

    location /static/ {
        alias /home/ec2-user/library-management-system-aws/staticfiles/;
    }

    location / {
        proxy_pass http://unix:/home/ec2-user/library-management-system-aws/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

## 20. Static Files Collection

Collect static files into `staticfiles/`:
```bash
python manage.py collectstatic --noinput
```

---

## 21. RDS Connectivity Verification

Test connectivity from EC2 to RDS:
```bash
mysql -h library-db-instance.xxxxxx.us-east-1.rds.amazonaws.com -u admin -p
```

---

## 22. Security Group Audit

* Verify Port 3306 is not open to `0.0.0.0/0`.
* Ensure Port 22 is restricted to authorized IPs.

---

## 23. Testing Live Application

Start and enable Nginx:
```bash
sudo systemctl restart nginx
sudo systemctl enable nginx
```
Open `http://YOUR_EC2_PUBLIC_IP/` in your browser.

---

## 24. Service Management Commands Quick Reference

```bash
# Check Gunicorn Status
sudo systemctl status gunicorn

# Restart Gunicorn
sudo systemctl restart gunicorn

# Check Nginx Status
sudo systemctl status nginx

# Restart Nginx
sudo systemctl restart nginx

# View Nginx Logs
sudo tail -f /var/log/nginx/error.log
```
