# TutorFlow — Security Documentation

## 1. Current Security Controls

| Control | Status | Implementation |
|---|---|---|
| Environment-based secret key | Implemented | SECRET_KEY loaded from environment |
| Secret configuration validation | Implemented | Application refuses to start without SECRET_KEY |
| CSRF protection | Enabled | Flask-WTF |
| Environment file exclusion | Implemented | .env excluded through .gitignore |
| Database migrations | Implemented | Flask-Migrate / Alembic |
| Debug mode | Disabled in run.py | app.run(debug=False) |
| Authentication | Not implemented | Planned |
| Authorization | Not implemented | Planned |
| HTTPS | Not configured | Planned for deployment |

## 2. Security Priorities

### Authentication and Authorization
Implement secure user authentication and role-based access control before allowing multiple tutors to access the application.

### Secret Management
Keep development secrets in local environment variables. Use AWS Secrets Manager for production credentials.

### Database Security
Move from local SQLite to PostgreSQL on AWS RDS. Restrict database network access to authorized application resources.

### Infrastructure Security
Use Terraform to define AWS infrastructure. Apply least-privilege IAM permissions and secure network rules.

### Application Security
Review input validation, session security, access controls and error handling before production deployment.

### Monitoring
Use CloudWatch for application logs, operational monitoring and security-related alerts.

## 3. Production Readiness

TutorFlow is currently under active development.

It is not yet ready for public production use or real student data.

Authentication, authorization, production HTTPS, secure cloud deployment and additional security validation remain outstanding.

## 4. Security Development Roadmap

1. Implement authentication.
2. Add authorization and access restrictions.
3. Validate and sanitize user input.
4. Configure production session and cookie security.
5. Deploy using HTTPS.
6. Secure AWS infrastructure with IAM and network restrictions.
7. Store production credentials in Secrets Manager.
8. Introduce automated dependency and security scanning.