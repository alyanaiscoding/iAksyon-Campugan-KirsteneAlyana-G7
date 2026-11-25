# iAksyon

## Project Overview

iAksyon is a web-based community issue reporting and management system that allows residents to report community concerns and track their progress. It enables barangay administrators to review submitted reports and update their status.

## Implemented Features

### Account Management (PD1)
- User registration with validation
- Login and logout
- Role-based dashboards
- Resident profile viewing and editing
- Role-based access control

### Community Issue Reporting (PD2)

**Resident Features**
- Create community issue reports
- View submitted reports
- Edit pending reports
- Delete pending reports
- Track report status
- Form validation and confirmation messages

**Admin Features**
- View all submitted reports
- View individual report details
- Update report status

## Technology Stack

- Frontend: HTML and Django Templates
- Backend: Python and Django
- Database: Supabase PostgreSQL
- Version Control: Git and GitHub

## Database Relationships

The Report model has a many-to-one relationship with the CustomUser model. Each report belongs to one resident, while a resident can submit multiple reports.

## Installation and Setup

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install the dependencies using `pip install -r requirements.txt`.
4. Configure the environment variables for the Supabase PostgreSQL database.
5. Run `python manage.py migrate`.
6. Start the development server using `python manage.py runserver`.
7. Open `http://127.0.0.1:8000/` in your browser.

## Git Branches

- `main` — Stable project version
- `develop` — Development and integration branch
- `feature/issue-reporting` — Resident report CRUD functionality
- `feature/report-management` — Admin report management functionality

## Security and Validation

- Password hashing
- Authentication and role-based authorization
- Report ownership restrictions
- Pending-only report editing and deletion
- CSRF protection
- Server-side form validation
- Environment variables for database credentials

## Future Enhancements
- Report photo attachments
- Analytics dashboard
- Improved user interface

## Developer

Kirstene Alyana V. Campugan
BS Information Technology
Cebu Institute of Technology – University