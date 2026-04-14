# TaskFlow API Documentation

This document provides request/response examples for every current API endpoint.

Base URL: `http://localhost:8000`

Seed credentials used in examples where authentication is needed:
- Email: `test@example.com`
- Password: `password123`

Authentication: use JWT access token for protected routes.

```http
Authorization: Bearer <access_token>
```

## 1) Register User

- Method: `POST`
- URL: `/auth/register`
- Auth required: No

Request:
```json
{
  "name": "Test User",
  "email": "test@example.com",
  "password": "password123"
}
```

If that user already exists from seed data, expected response (`400`):
```json
{
  "error": "validation failed",
  "fields": {
    "email": [
      "user with this email already exists."
    ]
  }
}
```

## 2) Login User

- Method: `POST`
- URL: `/auth/login`
- Auth required: No

Request:
```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

Success response (`200`):
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "f75d51d8-bcb7-4c9e-b885-225cc42e0d99",
    "name": "Test User",
    "email": "test@example.com",
    "created_at": "2026-04-14T13:51:22.181003Z"
  }
}
```

Invalid credentials (`400`):
```json
{
  "error": "validation failed",
  "fields": {
    "non_field_errors": [
      "Invalid credentials"
    ]
  }
}
```

## 3) List Projects

- Method: `GET`
- URL: `/projects`
- Auth required: Yes

Success response (`200`):
```json
{
  "projects": [
    {
      "id": "2e2c8579-4e41-4561-b53e-1a31ef6d14e2",
      "name": "Website Redesign",
      "description": "Q2 website redesign project",
      "owner_id": "f75d51d8-bcb7-4c9e-b885-225cc42e0d99",
      "created_at": "2026-04-14T13:51:22.211357Z"
    }
  ]
}
```

## 4) Create Project

- Method: `POST`
- URL: `/projects`
- Auth required: Yes

Request:
```json
{
  "name": "Mobile App",
  "description": "Build first Android release"
}
```

Success response (`201`):
```json
{
  "id": "9489a79f-4ef8-4553-b75c-4b6038e9d8ec",
  "name": "Mobile App",
  "description": "Build first Android release",
  "owner_id": "f75d51d8-bcb7-4c9e-b885-225cc42e0d99",
  "created_at": "2026-04-14T14:04:06.091646Z"
}
```

## 5) Get Project Details

- Method: `GET`
- URL: `/projects/{project_id}`
- Auth required: Yes

Success response (`200`):
```json
{
  "id": "9489a79f-4ef8-4553-b75c-4b6038e9d8ec",
  "name": "Mobile App",
  "description": "Build first Android release",
  "owner_id": "f75d51d8-bcb7-4c9e-b885-225cc42e0d99",
  "created_at": "2026-04-14T14:04:06.091646Z",
  "tasks": []
}
```

## 6) Update Project

- Method: `PATCH`
- URL: `/projects/{project_id}`
- Auth required: Yes (owner only)

Request:
```json
{
  "name": "Mobile App v2",
  "description": "Updated scope"
}
```

Success response (`200`):
```json
{
  "id": "9489a79f-4ef8-4553-b75c-4b6038e9d8ec",
  "name": "Mobile App v2",
  "description": "Updated scope",
  "owner_id": "f75d51d8-bcb7-4c9e-b885-225cc42e0d99",
  "created_at": "2026-04-14T14:04:06.091646Z"
}
```

Forbidden (`403`):
```json
{
  "error": "forbidden"
}
```

## 7) Delete Project

- Method: `DELETE`
- URL: `/projects/{project_id}`
- Auth required: Yes (owner only)

Success response (`204`): empty body

## 8) List Tasks In Project

- Method: `GET`
- URL: `/projects/{project_id}/tasks`
- Auth required: Yes
- Optional query params:
  - `status` (`todo`, `in_progress`, `done`)
  - `assignee` (user UUID)

Success response (`200`):
```json
{
  "tasks": [
    {
      "id": "4629f30c-a8a1-4c1e-aa94-a09d7eaba6fc",
      "title": "Task no slash",
      "description": null,
      "status": "todo",
      "priority": "high",
      "project_id": "9489a79f-4ef8-4553-b75c-4b6038e9d8ec",
      "assignee_id": null,
      "due_date": null,
      "created_at": "2026-04-14T14:09:57.940587Z",
      "updated_at": "2026-04-14T14:09:57.940597Z"
    }
  ]
}
```

## 9) Create Task In Project

- Method: `POST`
- URL: `/projects/{project_id}/tasks`
- Auth required: Yes

Request:
```json
{
  "title": "Design homepage",
  "description": "Create mockups",
  "priority": "high",
  "due_date": "2026-04-15",
  "assignee_id": "f75d51d8-bcb7-4c9e-b885-225cc42e0d99"
}
```

Success response (`201`):
```json
{
  "id": "41fe0fe8-6e72-4b22-8cf3-6f59d37c4b08",
  "title": "Design homepage",
  "description": "Create mockups",
  "status": "todo",
  "priority": "high",
  "project_id": "9489a79f-4ef8-4553-b75c-4b6038e9d8ec",
  "assignee_id": "f75d51d8-bcb7-4c9e-b885-225cc42e0d99",
  "due_date": "2026-04-15",
  "created_at": "2026-04-14T14:11:42.508234Z",
  "updated_at": "2026-04-14T14:11:42.508244Z"
}
```

Validation error (`400`):
```json
{
  "error": "validation failed",
  "fields": {
    "title": [
      "This field is required."
    ]
  }
}
```

## 10) Project Task Stats

- Method: `GET`
- URL: `/projects/{project_id}/stats`
- Auth required: Yes

Success response (`200`):
```json
{
  "status_counts": {
    "todo": 2,
    "in_progress": 1,
    "done": 1
  },
  "assignee_counts": {
    "Test User": 2
  },
  "total_tasks": 4
}
```

## 11) Update Task

- Method: `PATCH`
- URL: `/tasks/{task_id}`
- Auth required: Yes (project owner only)

Request:
```json
{
  "status": "done",
  "priority": "medium",
  "assignee_id": null
}
```

Success response (`200`):
```json
{
  "id": "41fe0fe8-6e72-4b22-8cf3-6f59d37c4b08",
  "title": "Design homepage",
  "description": "Create mockups",
  "status": "done",
  "priority": "medium",
  "project_id": "9489a79f-4ef8-4553-b75c-4b6038e9d8ec",
  "assignee_id": null,
  "due_date": "2026-04-15",
  "created_at": "2026-04-14T14:11:42.508234Z",
  "updated_at": "2026-04-14T14:15:10.188941Z"
}
```

## 12) Delete Task

- Method: `DELETE`
- URL: `/tasks/{task_id}`
- Auth required: Yes (project owner only)

Success response (`204`): empty body

## Common Error Responses

Unauthorized (`401`):
```json
{
  "detail": "Authentication credentials were not provided."
}
```

Not found (`404`):
```json
{
  "detail": "Not found."
}
```
