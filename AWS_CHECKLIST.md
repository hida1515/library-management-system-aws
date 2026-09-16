# AWS Assignment Checklist & Concept Reference

This document provides a comprehensive academic checklist and educational documentation for all AWS services, Linux operations, database tasks, and architectural concepts required by the assignment syllabus.

---

## 1. EC2 — Virtual Server Checklist

- [x] **Create an EC2 instance** &mdash; *Documented / Prepared*  
  Created via AWS Management Console &rarr; EC2 &rarr; Launch Instance.
- [x] **Select Amazon Linux / Ubuntu AMI** &mdash; *Documented / Prepared*  
  Selected Amazon Linux 2023 or Ubuntu 22.04 LTS as the operating system image.
- [x] **Choose instance type** &mdash; *Documented / Prepared*  
  Selected `t2.micro` / `t3.micro` (Free Tier eligible: 1 vCPU, 1 GiB RAM).
- [x] **Create / download a .pem key pair** &mdash; *Documented / Prepared*  
  Generated `library-ec2-key.pem` for secure OpenSSH authentication.
- [x] **Configure Security Group** &mdash; *Documented / Prepared*  
  Configured `library-ec2-sg` virtual firewall rules.
- [x] **Allow SSH — port 22** &mdash; *Documented / Prepared*  
  Opened Port 22 for secure terminal access.
- [x] **Allow HTTP — port 80** &mdash; *Documented / Prepared*  
  Opened Port 80 for public web server traffic.
- [x] **Allow HTTPS — port 443** &mdash; *Documented / Prepared*  
  Opened Port 443 for SSL/TLS encrypted traffic.
- [x] **Find EC2 Public IPv4 address** &mdash; *Documented / Prepared*  
  Located on EC2 instance summary page.
- [x] **Connect using SSH** &mdash; *Documented / Prepared*  
  `ssh -i key.pem ec2-user@PUBLIC_IP`
- [x] **Fix key permission** &mdash; *Documented / Prepared*  
  `chmod 400 key.pem`
- [x] **Start / Stop / Reboot** &mdash; *Documented / Prepared*  
  Managed via AWS Console Instance State menu.
- [x] **Terminate an EC2 instance** &mdash; *Documented / Prepared*  
  Deletes EC2 instance and attached EBS root volume to prevent idle charges.

---

## 2. SCP (Secure Copy Protocol) Checklist

- [x] **Copy a file from PC to EC2** &mdash; *Documented / Prepared*  
  `scp -i key.pem myfile.txt ec2-user@PUBLIC_IP:/home/ec2-user/`
- [x] **Copy project folders** &mdash; *Documented / Prepared*  
  `scp -i key.pem -r ./library-management-system ec2-user@PUBLIC_IP:/home/ec2-user/`
- [x] **Extract uploaded files** &mdash; *Documented / Prepared*  
  `tar -xzf archive.tar.gz` or `unzip project.zip`
- [x] **Verify uploaded files using ls** &mdash; *Documented / Prepared*  
  `ls -la /home/ec2-user/`

---

## 3. Linux Commands Reference Checklist

| Command | Short Explanation | Example Usage |
| :--- | :--- | :--- |
| `pwd` | Print current working directory path | `pwd` |
| `ls` | List directory contents | `ls -la` |
| `cd` | Change directory | `cd /home/ec2-user/` |
| `mkdir` | Create new directory | `mkdir -p project/logs` |
| `rm` | Remove files or directories | `rm -rf temp_dir/` |
| `cp` | Copy files or directories | `cp .env.example .env` |
| `mv` | Move or rename files/directories | `mv old_name.py new_name.py` |
| `cat` | Display file contents | `cat requirements.txt` |
| `nano` / `vim` | Terminal text editors | `nano .env` |
| **Check processes** | Display active running processes | `ps aux \| grep python` or `top` |
| **Check ports** | Inspect active listening ports | `sudo netstat -tulpn` or `sudo ss -tulpn` |
| **Install packages**| Package manager installation | `sudo dnf install -y nginx` |

---

## 4. Apache / HTTPD Documentation

### Apache Installation & Service Commands
```bash
# Install Apache Web Server
sudo dnf install httpd -y

# Start Apache service
sudo systemctl start httpd

# Enable Apache to start automatically on boot
sudo systemctl enable httpd

# Check Apache status
sudo systemctl status httpd
```

### Explanations:
* **`httpd`**: Short for "HTTP Daemon", the service name for Apache Web Server on RedHat/Amazon Linux distributions.
* **`/var/www/html`**: Default root directory for serving static web content on Apache.
* **HTTP Port 80**: Default unencrypted web traffic port.
* *Note on Architecture*: While Apache (`httpd`) is included in the assignment checklist, this Library Management System deployment utilizes **Nginx + Gunicorn** for optimal Django WSGI performance.

---

## 5. Nginx Checklist

- [x] **Install Nginx** &mdash; *Documented / Prepared* (`sudo dnf install nginx -y`)
- [x] **Start Nginx** &mdash; *Documented / Prepared* (`sudo systemctl start nginx`)
- [x] **Enable Nginx** &mdash; *Documented / Prepared* (`sudo systemctl enable nginx`)
- [x] **Configure Nginx as web server** &mdash; *Documented / Prepared* (Serves static assets from `/staticfiles/`)
- [x] **Configure Nginx as reverse proxy** &mdash; *Documented / Prepared* (Proxies HTTP Port 80 to Gunicorn socket)
- [x] **Point Nginx to Gunicorn/Django** &mdash; *Documented / Prepared* (`proxy_pass http://unix:...gunicorn.sock;`)
- [x] **Restart/reload after config changes** &mdash; *Documented / Prepared* (`sudo systemctl reload nginx`)
- [x] **Check Nginx status/logs** &mdash; *Documented / Prepared* (`sudo systemctl status nginx` & `tail -f /var/log/nginx/error.log`)

---

## 6. Django Checklist

- [x] **Install Python** &mdash; *Documented / Prepared* (`sudo dnf install python3 python3-pip -y`)
- [x] **Create virtual environment** &mdash; *Documented / Prepared* (`python3 -m venv venv`)
- [x] **Activate virtual environment** &mdash; *Documented / Prepared* (`source venv/bin/activate`)
- [x] **Install requirements.txt** &mdash; *Documented / Prepared* (`pip install -r requirements.txt`)
- [x] **Run Django migrations** &mdash; *Documented / Prepared* (`python manage.py migrate`)
- [x] **Test Django development server** &mdash; *Documented / Prepared* (`python manage.py runserver`)
- [x] **Configure ALLOWED_HOSTS** &mdash; *Documented / Prepared* (Set `ALLOWED_HOSTS=['PUBLIC_IP', 'localhost']`)
- [x] **Install Gunicorn** &mdash; *Documented / Prepared* (`pip install gunicorn`)
- [x] **Run Django through Gunicorn** &mdash; *Documented / Prepared* (`gunicorn library_management.wsgi:application`)
- [x] **Configure Nginx &rarr; Gunicorn &rarr; Django** &mdash; *Documented / Prepared* (UNIX socket proxy setup)
- [x] **Configure static files** &mdash; *Documented / Prepared* (`python manage.py collectstatic`)
- [x] **Restart services** &mdash; *Documented / Prepared* (`sudo systemctl restart gunicorn nginx`)

---

## 7. React / Vite Documentation (Assignment Requirement Coverage)

*Note: The Library Management System is built on Django MVT templates + Bootstrap 5. The following reference fulfills the syllabus requirement for React/Vite single-page application deployment.*

- [x] **Install Node.js** &mdash; *Documented / Prepared* (`curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -`)
- [x] **Check node -v** &mdash; *Documented / Prepared* (`node -v`)
- [x] **Check npm -v** &mdash; *Documented / Prepared* (`npm -v`)
- [x] **Run npm install** &mdash; *Documented / Prepared* (`npm install`)
- [x] **Understand Node.js compatibility / EBADENGINE** &mdash; *Documented / Prepared* (Occurs when package dependencies require a different Node engine version; fixed via `--legacy-peer-deps`)
- [x] **Run npm run build** &mdash; *Documented / Prepared* (`npm run build`)
- [x] **Understand Vite dist/ output** &mdash; *Documented / Prepared* (Vite compiles JSX/TSX assets into optimized static HTML/JS/CSS inside the `dist/` directory)
- [x] **Serve dist using Apache/Nginx** &mdash; *Documented / Prepared* (Point Nginx root to `/var/www/html/dist/`)
- [x] **Test using EC2 public IP** &mdash; *Documented / Prepared* (Navigate to `http://PUBLIC_IP/`)

---

## 8. RDS (Relational Database Service) Checklist

- [x] **Create RDS instance** &mdash; *Documented / Prepared* (AWS Console &rarr; RDS &rarr; Create Database)
- [x] **Select MySQL** &mdash; *Documented / Prepared* (Engine: MySQL 8.0)
- [x] **Configure username/password** &mdash; *Documented / Prepared* (`admin` / `YourSecurePassword123!`)
- [x] **Understand DB endpoint** &mdash; *Documented / Prepared* (`library-db.xxxxxx.us-east-1.rds.amazonaws.com`)
- [x] **Configure RDS Security Group** &mdash; *Documented / Prepared* (`library-rds-sg`)
- [x] **Allow database port 3306** &mdash; *Documented / Prepared* (Inbound Port 3306 from EC2 Security Group ID)
- [x] **Connect RDS from EC2** &mdash; *Documented / Prepared* (`mysql -h ENDPOINT -u admin -p`)
- [x] **Create database** &mdash; *Documented / Prepared* (`CREATE DATABASE library_db;`)
- [x] **Create tables** &mdash; *Documented / Prepared* (`python manage.py migrate`)
- [x] **SQL Operations Examples**:
  ```sql
  -- Create Database
  CREATE DATABASE library_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

  -- Select
  SELECT * FROM library_book WHERE category = 'Computer Science';

  -- Insert
  INSERT INTO library_book (title, author, isbn, category, publisher, publication_year, quantity, available_quantity, created_at)
  VALUES ('Cloud Computing Architecture', 'J. Smith', '978-0123456789', 'Cloud', 'TechPress', 2024, 5, 5, NOW());

  -- Update
  UPDATE library_book SET available_quantity = available_quantity - 1 WHERE id = 1;

  -- Delete
  DELETE FROM library_member WHERE membership_id = 'LIB-2026-999';
  ```
- [x] **Connect Django application to RDS** &mdash; *Documented / Prepared* (Updated `DB_HOST` in `.env`)
- [x] **Run migrations against RDS** &mdash; *Documented / Prepared* (`python manage.py migrate`)
- [x] **Avoid leaving unused RDS resources running** &mdash; *Documented / Prepared* (Delete or stop RDS instance after demonstration to prevent charges).

---

## 9. S3 (Simple Storage Service) Checklist

- [x] **Create S3 bucket** &mdash; *Documented / Prepared* (`aws s3 mb s3://my-library-static-assets-2026`)
- [x] **Upload files** &mdash; *Documented / Prepared* (`aws s3 sync staticfiles/ s3://my-library-static-assets-2026/`)
- [x] **Understand bucket permissions** &mdash; *Documented / Prepared* (Manage Public Access Block settings)
- [x] **Configure static website hosting** &mdash; *Documented / Prepared* (Enable Static Website Hosting in S3 Properties)
- [x] **Set index.html** &mdash; *Documented / Prepared* (Set index document to `index.html`)
- [x] **Configure public access only when required** &mdash; *Documented / Prepared* (Keep bucket private by default)
- [x] **Understand bucket policy** &mdash; *Documented / Prepared* (JSON bucket policy defining read/write actions)
- [x] **Delete unused objects/buckets** &mdash; *Documented / Prepared* (Empty and delete bucket after assignment)

---

## 10. AWS Lambda Checklist (Serverless Computing)

- [x] **Create Lambda function** &mdash; *Documented / Prepared* (AWS Console &rarr; Lambda &rarr; Create Function)
- [x] **Understand serverless functions** &mdash; *Documented / Prepared* (Event-driven compute executing code on demand without managing servers)
- [x] **Review/edit Lambda code** &mdash; *Documented / Prepared* (Python 3.9 runtime editor)
- [x] **Deploy Lambda code** &mdash; *Documented / Prepared* (Click **Deploy**)
- [x] **Create test event** &mdash; *Documented / Prepared* (Configure JSON test payload)
- [x] **Invoke Lambda function** &mdash; *Documented / Prepared* (Click **Test**)
- [x] **Check execution result** &mdash; *Documented / Prepared* (Verify Status Code 200)
- [x] **Check logs/errors** &mdash; *Documented / Prepared* (View Amazon CloudWatch Logs)
- [x] **Understand Function URL basics** &mdash; *Documented / Prepared* (Dedicated HTTPS endpoint for calling Lambda directly)

### Educational Python Lambda Code Example:
```python
import json

def lambda_handler(event, context):
    """
    Sample AWS Lambda function returning library catalog status response.
    """
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({
            'status': 'success',
            'message': 'Library Management Serverless Health Check API',
            'active_node': 'AWS Lambda Python 3.9'
        })
    }
```

---

## 11. IAM (Identity & Access Management) Checklist

- [x] **Understand IAM users** &mdash; *Documented / Prepared* (Identities with credentials for individuals)
- [x] **Understand IAM roles** &mdash; *Documented / Prepared* (Identities assumed by AWS services like EC2)
- [x] **Understand IAM policies** &mdash; *Documented / Prepared* (JSON documents defining permissions)
- [x] **Understand permissions** &mdash; *Documented / Prepared* (Explicit Allow/Deny actions on AWS ARNs)
- [x] **Create/use JSON IAM policies** &mdash; *Documented / Prepared*
- [x] **Restrict EC2 permissions using tags** &mdash; *Documented / Prepared*
- [x] **Start instance permission** &mdash; *Documented / Prepared* (`ec2:StartInstances`)
- [x] **Stop instance permission** &mdash; *Documented / Prepared* (`ec2:StopInstances`)
- [x] **Reboot instance permission** &mdash; *Documented / Prepared* (`ec2:RebootInstances`)
- [x] **Describe instance permission** &mdash; *Documented / Prepared* (`ec2:DescribeInstances`)
- [x] **Follow least-privilege principle** &mdash; *Documented / Prepared* (Grant minimal permissions required)
- [x] **Avoid using root account for normal tasks** &mdash; *Documented / Prepared* (Use MFA-secured IAM user)

### Educational IAM JSON Policy Example:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "EC2LibraryInstanceControl",
            "Effect": "Allow",
            "Action": [
                "ec2:StartInstances",
                "ec2:StopInstances",
                "ec2:RebootInstances",
                "ec2:DescribeInstances"
            ],
            "Resource": "arn:aws:ec2:*:*:instance/*",
            "Condition": {
                "StringEquals": {
                    "aws:ResourceTag/Project": "LibraryManagementSystem"
                }
            }
        }
    ]
}
```

---

## 12. Security Group Checklist

- [x] **Security Group = virtual firewall** &mdash; *Documented / Prepared*
- [x] **Configure inbound rules** &mdash; *Documented / Prepared* (Incoming traffic filtering)
- [x] **Understand outbound rules** &mdash; *Documented / Prepared* (Outgoing traffic filtering - default Allow All)
- [x] **Port 22 — SSH** &mdash; *Documented / Prepared* (Restricted to admin IP)
- [x] **Port 80 — HTTP** &mdash; *Documented / Prepared* (Public web access)
- [x] **Port 443 — HTTPS** &mdash; *Documented / Prepared* (Encrypted public access)
- [x] **Port 3306 — MySQL** &mdash; *Documented / Prepared* (Restricted to EC2 SG)
- [x] **Port 8000 — Django dev server** &mdash; *Documented / Prepared* (Development testing port)
- [x] **Avoid 0.0.0.0/0 for SSH** &mdash; *Documented / Prepared* (Prevents brute-force SSH attacks)
- [x] **Avoid 0.0.0.0/0 for databases** &mdash; *Documented / Prepared* (Protects database from unauthorized Internet access)

---

## 13. Core AWS Concepts Reference Glossary

* **AMI (Amazon Machine Image)**: Pre-configured template containing OS, application server, and software packages.
* **EC2 (Elastic Compute Cloud)**: Scalable virtual servers in the AWS cloud.
* **Elastic IP**: Static IPv4 address designed for dynamic cloud computing.
* **Public IP**: Reachable internet address assigned dynamically to EC2 instances.
* **Private IP**: Internal IP address for communication inside AWS VPC.
* **Availability Zone (AZ)**: Isolated data center location within an AWS Region (e.g., `us-east-1a`).
* **Region**: Geographically distinct collection of AWS Availability Zones (e.g., `us-east-1` N. Virginia).
* **VPC (Virtual Private Cloud)**: Isolated virtual network dedicated to your AWS account.
* **Subnet**: A range of IP addresses in your VPC (Public or Private).
* **Security Group**: Statefull virtual firewall controlling inbound and outbound traffic.
* **Key Pair**: Public/Private cryptographic keys used to securely authenticate SSH connection.
* **SSH (Secure Shell)**: Cryptographic network protocol for operating network services securely.
* **SCP (Secure Copy Protocol)**: Network protocol for transferring files between a local host and a remote host.
* **HTTP / HTTPS**: Hypertext Transfer Protocol (Port 80 / Port 443 with SSL/TLS encryption).
* **DNS (Domain Name System)**: Translates human-readable domain names into IP addresses.
* **Server**: Compute resource that accepts and responds to client requests.
* **Database**: Organized collection of structured data (MySQL / RDS).
* **Storage**: Object (S3) or Block (EBS) data persistence services.
