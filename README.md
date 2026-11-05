# TutorFlow — Tutoring Management Platform

A Python-based tutoring management application designed to simplify the organisation of students, lessons, homework and learning activities.

**Project status:** Active development  
**Repository:** [MyTutor — GitHub](https://github.com/paulevensdestima11-gif/MyTutor)

## 1. Project Overview

TutorFlow is a web application built with Flask to support tutors in managing their everyday teaching activities.

The project focuses on building a maintainable application architecture and progressively applying cloud engineering, infrastructure automation and DevSecOps practices.

## 2. Current Features

- **Student Management:** Register and manage student records.
- **Lesson Management:** Create and organise lessons.
- **Homework Management:** Assign and manage homework.
- **Dashboard:** Access the main tutoring management interface.
- **Database Migrations:** Manage database schema changes with Flask-Migrate and Alembic.
- **Form Security:** CSRF protection using Flask-WTF.
- **Testing:** Automated tests using pytest.

## 3. Technology Stack

| Area | Technology |
|---|---|
| Programming language | Python |
| Web framework | Flask |
| Database ORM | SQLAlchemy |
| Current database | SQLite |
| Database migrations | Alembic / Flask-Migrate |
| Form security | Flask-WTF |
| Authentication | Planned |
| Testing | pytest |
| Version control | Git / GitHub |

## 4. Application Architecture

The application follows a modular Flask structure.

```text
MyTutorFlow/
│
├── app/
│   ├── models/
│   │   └── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── dashboard.py
│   │   ├── students.py
│   │   ├── lessons.py
│   │   └── homework.py
│   ├── templates/
│   ├── static/
│   ├── extensions.py
│   └── __init__.py
│
├── docs/
│   ├── architecture.md
│   ├── security.md
│   └── screenshots/
│       ├── dashboard.png
│       ├── students.png
│       ├── lessons.png
│       └── homework.png
│
├── migrations/
├── tests/
├── config.py
├── requirements.txt
├── run.py
└── .gitignore
```

The application uses separate modules for database models, routes, templates and extensions to support maintainability and future expansion.

## 5. Run Locally

### Prerequisites

- Python 3.14.4 (tested)
- Git

### Clone the repository

```powershell
git clone https://github.com/paulevensdestima11-gif/MyTutor.git
cd MyTutor
```

### Create a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file in the project root.

```env
SECRET_KEY=your-generated-secret-key
DATABASE_URL=sqlite:///tutorflow.db
```

Never commit `.env` or real credentials to GitHub.

### Initialise the database

```powershell
flask --app run db upgrade
```

### Start the application

```powershell
python run.py
```

Open the local address displayed in the terminal.

## 6. Testing

Run the automated test suite:

```powershell
pytest -v
```

## 7. Cloud Engineering Roadmap

The next development phase focuses on transforming TutorFlow into a cloud-hosted application using AWS.

| Component | Planned technology |
|---|---|
| Application hosting | AWS EC2 |
| Database | Amazon RDS PostgreSQL |
| Infrastructure as Code | Terraform |
| Containerisation | Docker |
| Cloud CLI | AWS CLI |
| Secrets management | AWS Secrets Manager |
| Monitoring | Amazon CloudWatch |
| CI/CD | GitHub Actions |
| Application language | Python |

### Planned architecture

```text
Developer
    |
    v
GitHub Repository
    |
    v
GitHub Actions CI/CD
    |
    v
Docker Application
    |
    v
AWS EC2
    |
    v
Amazon RDS PostgreSQL

Supporting services:
- AWS Secrets Manager
- Amazon CloudWatch
- Terraform
```

This architecture is a development target, not a claim of an existing AWS deployment.

## 8. Security and Development Priorities

The project will progressively implement:

- Secure user authentication and authorisation.
- Environment-based configuration.
- Secure handling of application secrets.
- PostgreSQL database integration.
- Container security.
- Infrastructure security through Terraform.
- Automated CI/CD checks.
- Centralised application monitoring.

**Current limitation:** Authentication has not yet been implemented. The current application is a development baseline and is not ready for public production use or real student data.

## 9. Application Screenshots

### Dashboard

![TutorFlow Dashboard](docs/screenshots/dashboard.png)

### Student Management

![TutorFlow Student Management](docs/screenshots/students.png)

### Lesson Management

![TutorFlow Lessons](docs/screenshots/lessons.png)

### Homework Management

![TutorFlow Homework](docs/screenshots/homework.png)

## 10. Technical Documentation

- [System Architecture](docs/architecture.md)
- [Security Documentation](docs/security.md)

These documents describe the current application architecture, planned AWS deployment and security improvements.

## 11. Project Objective

TutorFlow is both a practical software project and a portfolio demonstration of cloud engineering skills.

The objective is to demonstrate the ability to:

- Develop a modular Python web application.
- Manage relational databases and migrations.
- Apply application security principles.
- Automate infrastructure using Terraform.
- Deploy applications on AWS.
- Build CI/CD pipelines.
- Monitor and maintain cloud workloads.

---

**Author:** Paul  
**Project:** TutorFlow  
**Focus:** Python · AWS · Terraform · Docker · DevSecOps