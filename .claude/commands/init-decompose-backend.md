---
description: Initialize backend task decomposition based on PRD and architecture
---

# Initialize Backend Task Decomposition

## Your Task
Initialize backend API and service task decomposition based on PRD and architecture.

## Prerequisites
Check that frontend decomposition is complete (recommended but optional):
- `decomposition_phase.frontend_status == "completed"` (if frontend already decomposed)
- OR skip if doing backend-first development

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

### 3. Create Backend Root Tasks with Tree Structure
Create root tasks in tree-based registry:

**📄 Task Registry Format**: See [task_registry.json Template](../templates/task_registry.json.template)

**Tree Structure**:
- Tasks stored in `backend_tasks` array
- Root tasks (Level 1) get IDs: "1", "2", "3", etc.
- Subtasks use dot notation: "1.1", "1.2", "1.1.1", etc.
- Each task has `subtasks` array for children

### 4. Update State and Create Root Tasks
Use Python scripts to initialize and create tasks:

**📄 Script Reference**: See [.claude/scripts/README.md](../.claude/scripts/README.md)

**Python commands**:
```python
from state_manager import StateManager
from task_registry_manager import TaskRegistryManager

state_mgr = StateManager()
task_mgr = TaskRegistryManager()

# Initialize backend decomposition
state_mgr.start_backend_decomposition(total_modules=4)

# Initialize backend metadata
task_mgr.init_backend_metadata(
    framework="FastAPI",
    database="PostgreSQL",
    language="Python"
)

# Create root task for each backend module/service
auth_service_id = task_mgr.add_root_task("backend", {
    "title": "Authentication Service",
    "type": "service",
    "description": "Login, Signup, JWT, Session management",
    "api_endpoints": [
        "POST /api/auth/login",
        "POST /api/auth/signup",
        "POST /api/auth/logout"
    ],
    "database_tables": ["users", "sessions"]
})  # Returns "1"

user_service_id = task_mgr.add_root_task("backend", {
    "title": "User Management Service",
    "type": "service",
    "description": "CRUD operations for user profiles",
    "api_endpoints": [
        "GET /api/users/:id",
        "PUT /api/users/:id",
        "DELETE /api/users/:id"
    ],
    "database_tables": ["users", "profiles"]
})  # Returns "2"

# ... create more root tasks for other services
```

**Updates applied**:
- `decomposition_phase.status = "in_progress"`
- `decomposition_phase.backend_status = "in_progress"`
- Tree structure created with root tasks
- Metadata timestamps automatically set

### 5. Output Summary
```
Analyzed backend requirements:
✓ docs/prd.md (extracted [N] API requirements)
✓ docs/fullstack-architecture.md
✓ Frontend tasks (extracted [M] API calls)

Created backend root tasks (Level 1 services):
  - ID: "1" - Authentication Service
    - Endpoints: POST /auth/login, POST /auth/signup
    - Tables: users, sessions
  - ID: "2" - User Management Service
    - Endpoints: GET /users/:id, PUT /users/:id
    - Tables: users, profiles
  - ID: "3" - Data Persistence Layer
    - Endpoints: [Repository methods]
    - Tables: [all tables]
  ...

Backend framework: [FastAPI/Express/Django/etc]
Database: [PostgreSQL/MongoDB/etc]

📊 Tree Structure:
backend_tasks/
  ├─ [1] Authentication Service (pending)
  ├─ [2] User Management Service (pending)
  ├─ [3] Data Persistence Layer (pending)
  └─ ...

Checkpoint saved with [N] root services
Status: decomposition_phase = in_progress (backend)

Next command: /continue-decompose-backend
```

## Important Rules
- Extract API requirements from both PRD and frontend tasks
- Align backend modules with business domains
- Include database table requirements
- Reference architecture tech stack

## Next Steps
After initialization:
1. Use `/continue-decompose-backend` to decompose modules → services → functions
2. Use `/generate-backend-contexts` to generate context files for all functions
3. Then build dependency graph with `/build-deps-fullstack`

````
