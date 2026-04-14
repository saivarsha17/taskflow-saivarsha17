# TaskFlow - Backend API

A minimal but complete task management system backend built with Django and PostgreSQL. Users can register, log in, create projects, and manage tasks with real-time filtering and status tracking.

## Overview

**What is this?**  
TaskFlow is a RESTful API backend for a task management system. It provides authentication, project management, and task tracking with role-based access control.

**Tech Stack:**

- **Framework:** Django 5.1 + Django REST Framework 3.15
- **Database:** PostgreSQL 15
- **Authentication:** JWT (djangorestframework-simplejwt)
- **Language:** Python 3.11
- **Containerization:** Docker

---

## Architecture Decisions

### 1. **Framework Choice: Django + DRF**

- **Why:** Django's ORM, and migration system significantly reduce boilerplate
- **Trade-off:** Slightly heavier than minimal Go frameworks, but gains developer velocity and built-in tooling
- **Decision:** Prioritized shipping a complete, maintainable product over raw performance for this use case

### 2. **Explicit Permission Checks**

- Manually check permissions in views (owner-only for project updates/deletes) rather than using Django's permission framework
- **Why:** Simpler for this scope

### 3. **Automatic Migrations & Seeding**

- The Docker container runs migrations and seeds test data automatically on startup
- **Why:** Single `docker compose up` accomplishes full setup (no manual SQL)

---

## Running Locally

### Prerequisites

- Docker installed

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/saivarsha17/taskflow-saivarsha17
cd taskflow-saivarsha17/backend

# 2. Create .env file (required variables)
cp .env.example .env

# 3. Start all services (PostgreSQL + API server)
docker compose up

# 4. API is ready at http://localhost:8000
```

**That's it!** The server will:

1. Wait for PostgreSQL to be ready
2. Run all database migrations automatically
3. Seed the database with test data
4. Start the Django development server

You can immediately test with:

```bash
curl http://localhost:8000/api/auth/login/ \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

---

## Running Migrations

Migrations run automatically on container startup and seed script is added to create dummy data

## Test Credentials

Use these credentials immediately after `docker compose up`:

```
Email:    test@example.com
Password: password123
```

## API Reference

Read detailed API information in `API_DOCUMENTATION.md`.

### Base URL

`http://localhost:8000`

### Auth Header

All protected routes require:
`Authorization: Bearer <access_token>`

---

## Error Handling

### Status Codes

- `200 OK` — Success
- `201 Created` — Resource created
- `204 No Content` — Deleted successfully
- `400 Bad Request` — Validation error
- `401 Unauthorized` — No/invalid token
- `403 Forbidden` — Insufficient permissions
- `404 Not Found` — Resource not found
- `500 Internal Server Error` — Server error

### Error Response Format

```json
{
  "error": "validation failed",
  "fields": {
    "email": "Email already registered",
    "password": "Ensure this field has at least 8 characters."
  }
}
```

---

## What Would I Do With More Time

### 1. Authentication Flow (Production-Style)

I would implement a flow commonly used in production apps:

- First login via OTP or link.
- On successful login, issue:
  - short-lived access token
  - long-lived refresh token
- On next time when opens:
  - if access token is valid -> auto login
  - if expired -> refresh silently
  - if refresh token expired -> require OTP/magic-link login again

### 2. Database Indexing for Optimization

I would introduce targeted indexes using real query metrics so read-heavy endpoints stay fast as data grows that includes:

- owner + created_at for project list endpoints
- project + status for project task-list filtering
- assignee + status for assignee-based task views

### 3. Volume Strategy (Database Only)

I would use a dedicated named volume only for PostgreSQL data, and avoid broad bind mounts for the whole app in production-style environments.

This improves reliability and operational clarity:

- persistent database data across container restarts

### 4. API Query Improvements

I would expand API query capabilities for large datasets and better client performance:

- add pagination (cursor or page-number, endpoint-specific as needed)
- add richer search filters (keyword search, date ranges, priority ranges, assignee filters)
- add stable sorting options (created date, due date, priority)

---
