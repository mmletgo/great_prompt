---
description: Initialize backend task decomposition based on PRD and architecture
argument-hint: [batch_size]
---

# Initialize Backend Task Decomposition

## Your Task
Initialize backend API and service task decomposition based on PRD and architecture.

## Prerequisites
Check that frontend decomposition is complete (optional but recommended):
- `decomposition_phase.frontend_status == "completed"`

Check input documents:
- `docs/prd.md`
- `docs/fullstack-architecture.md`

## Steps

### 1. Analyze Backend Requirements
Read and analyze:
- `docs/prd.md` - Extract data models, business logic, API requirements
- `docs/fullstack-architecture.md` - Extract backend tech stack, architecture patterns
- Frontend task registry - Extract API calls needed by frontend

### 2. Identify Backend Modules
Group backend functionality into modules (aim for 4-8):

Examples:
- Authentication Service (Login, Signup, JWT, Session)
- User Management Service (CRUD, Profile, Avatar)
- Data Persistence Layer (Database, ORM, Migrations)
- API Gateway/Routes (REST/GraphQL endpoints)
- Business Logic Layer (Core domain logic)
- External Integrations (Email, SMS, Payment, etc.)

### 3. Create Backend Tasks in Registry
Append to `.claude_tasks/task_registry.json`:
```json
{
  "tasks": {
    "backend_task_001": {
      "id": "backend_task_001",
      "title": "[Service Name]",
      "level": 1,
      "type": "module",
      "category": "backend",
      "status": "pending",
      "parent_id": null,
      "children": [],
      "dependencies": [],
      "context_file": "contexts/backend_task_001_context.md",
      "api_endpoints": [
        "POST /api/auth/login",
        "POST /api/auth/signup"
      ],
      "database_tables": ["users", "sessions"]
    }
  },
  "backend_metadata": {
    "framework": "extracted from architecture",
    "database": "PostgreSQL/MongoDB/etc",
    "orm": "SQLAlchemy/Prisma/etc",
    "auth_method": "JWT/Session/OAuth"
  }
}
```

### 4. Update State
```json
{
  "decomposition_phase": {
    "frontend_status": "completed",
    "backend_status": "in_progress",
    "last_checkpoint": "backend_task_XXX"
  }
}
```

### 5. Output Summary
```
Analyzed backend requirements:
✓ docs/prd.md (extracted [N] API requirements)
✓ docs/fullstack-architecture.md
✓ Frontend tasks (extracted [M] API calls)

Identified backend modules:
  - backend_task_001: Authentication Service
    - Endpoints: POST /auth/login, POST /auth/signup
    - Tables: users, sessions
  - backend_task_002: User Management Service
    - Endpoints: GET /users/:id, PUT /users/:id
    - Tables: users, profiles
  ...

Backend framework: [FastAPI/Express/Django/etc]
Database: [PostgreSQL/MongoDB/etc]

Checkpoint saved: backend_task_XXX
Status: decomposition_phase = in_progress (backend)

Next command: /continue-decompose-backend
```

## Important Rules
- Extract API requirements from both PRD and frontend tasks
- Align backend modules with business domains
- Include database table requirements
- Reference architecture tech stack
- Create 4-8 backend modules maximum

## Next Steps
After initialization, use `/continue-decompose-backend` which will:
- Invoke @backend-decomposer agent to decompose modules → services → functions (API/service/repository/validation/utility layers)
- Generate context files for each function using @context-generator

````
