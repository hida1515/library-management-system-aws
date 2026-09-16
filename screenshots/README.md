# Execution Screenshots Guidelines

This directory is designated for storing actual execution screenshots captured during live AWS deployment and project submission.

> [!IMPORTANT]
> In accordance with academic integrity guidelines, **no fake screenshots or fabricated AWS credentials have been committed**. Please replace the placeholder sections below with your genuine screenshots after completing live execution on AWS.

---

## Required Screenshots Checklist

| # | Screenshot Description | Suggested Filename |
| :--- | :--- | :--- |
| **1** | GitHub Repository Overview | `01_github_repository.png` |
| **2** | AWS EC2 Instance Management Console | `02_ec2_instance_console.png` |
| **3** | EC2 Inbound & Outbound Security Groups | `03_security_groups.png` |
| **4** | Terminal SSH Connection to EC2 | `04_ssh_terminal.png` |
| **5** | Basic Linux Commands Output (`pwd`, `ls -la`, `top`) | `05_linux_commands.png` |
| **6** | Django Library Management Dashboard (`http://PUBLIC_IP/`) | `06_django_dashboard.png` |
| **7** | Nginx Service Status (`sudo systemctl status nginx`) | `07_nginx_status.png` |
| **8** | Gunicorn Service Status (`sudo systemctl status gunicorn`) | `08_gunicorn_status.png` |
| **9** | AWS RDS MySQL Instance Console | `09_aws_rds_console.png` |
| **10**| MySQL Database Connection & Tables (`SHOW TABLES;`) | `10_mysql_tables.png` |
| **11**| Working Application CRUD (Book List, Issue Book Flow) | `11_crud_operations.png` |
| **12**| AWS Console Resource Billing / Resource Termination | `12_aws_console_cleanup.png` |

---

## How to Add Screenshots to README

After taking screenshots, place the image files in this `screenshots/` directory and embed them using standard markdown syntax:

```markdown
![01 GitHub Repository](01_github_repository.png)
![06 Django Dashboard](06_django_dashboard.png)
```
