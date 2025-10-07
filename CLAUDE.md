# Project: Full-Stack Product Development System

## Project Overview
This is a comprehensive product development system that takes you from PRD to production-ready code. It follows a design-first approach: read product requirements → generate user flows → create wireframes → decompose frontend components → decompose backend functions → parallel TDD development with checkpoint recovery.

## File Structure
```
docs/                          # Product documentation
├── prd.md                     # Product Requirements Document
├── fullstack-architecture.md  # Technical architecture
└── front-end-spec.md          # UX/UI specifications

designs/                       # Design artifacts (generated)
├── user-flows.md              # Mermaid user flow diagrams
└── wireframes/                # ASCII wireframes for each page
    ├── login-page.md
    ├── dashboard.md
    └── ...

.claude_tasks/                 # Task management
├── state.json                 # Global state & checkpoint
├── task_registry.json         # Task list & dependency graph
└── contexts/                  # Task context storage
    ├── frontend_task_001_context.md
    ├── backend_task_001_context.md
    └── ...
```

## State Files Format

### state.json
```json
{
  "design_phase": {
    "status": "completed",
    "user_flows_generated": true,
    "wireframes_count": 8
  },
  "decomposition_phase": {
    "frontend_status": "completed",
    "backend_status": "completed",
    "last_checkpoint_frontend": "frontend_task_050",
    "last_checkpoint_backend": "backend_task_030",
    "progress": {
      "frontend_components": 42,
      "backend_functions": 35
    }
  },
  "development_phase": {
    "status": "in_progress",
    "current_wave": 5,
    "completed_waves": 4,
    "completed_tasks": ["backend_task_001", "frontend_task_001"],
    "failed_tasks": []
  }
}
```

### task_registry.json
```json
{
  "tasks": {
    "frontend_task_001": {
      "id": "frontend_task_001",
      "title": "LoginButton",
      "level": 3,
      "type": "component",
      "category": "frontend",
      "status": "completed",
      "parent_id": "frontend_task_parent",
      "children": [],
      "dependencies": [],
      "context_file": "contexts/frontend_task_001_context.md",
      "component_type": "button",
      "props": ["onClick", "disabled", "loading"],
      "design_reference": "designs/wireframes/login-page.md"
    },
    "backend_task_001": {
      "id": "backend_task_001",
      "title": "login_user",
      "level": 3,
      "type": "function",
      "category": "backend",
      "status": "completed",
      "function_type": "endpoint",
      "http_method": "POST",
      "route": "/api/auth/login",
      "dependencies": ["backend_task_002", "backend_task_003"]
    }
  },
  "frontend_metadata": {
    "framework": "React",
    "total_components": 42
  },
  "backend_metadata": {
    "framework": "FastAPI",
    "database": "PostgreSQL",
    "total_functions": 35
  },
  "dependency_graph": {
    "frontend_dependencies": {},
    "backend_dependencies": {},
    "cross_stack_dependencies": {
      "frontend_task_050": ["backend_task_010"]
    },
    "execution_order": [
      {"wave": 1, "category": "backend_foundation", "tasks": ["backend_task_001"]},
      {"wave": 2, "category": "backend_api", "tasks": ["backend_task_010"]},
      {"wave": 3, "category": "frontend_foundation", "tasks": ["frontend_task_001"]},
      {"wave": 4, "category": "frontend_api", "tasks": ["frontend_task_050"]}
    ]
  }
}
```

## Task Context Template
Each task context file follows this structure:
```markdown
# Task XXX: [Task Title]

## Task Overview
[Description]

## Dependencies
- task_XXX: [What this task provides]

## Function Specification
### Function Signature
[Code block with signature]

### Input Parameters
- param: description

### Return Value
- type: description

## TDD Test Cases
### Test Case 1: [Name]
[Test code]

## Related Files
- Target file: path/to/file.py
- Dependency files: path/to/dep.py
```

## Workflow Phases

### Phase 1: Design (Read Docs → Generate Design Artifacts)
1. Read `docs/prd.md`, `docs/fullstack-architecture.md`, `docs/front-end-spec.md`
2. Generate `designs/user-flows.md` with Mermaid diagrams
3. Generate `designs/wireframes/` ASCII wireframes for each page

**Agents Used:**
- `@user-flow-designer` - Creates Mermaid user flow diagrams
- `@wireframe-designer` - Generates detailed ASCII wireframes

### Phase 2: Frontend Decomposition (Modules → Pages → Components)
1. Initialize frontend modules from wireframes
2. Decompose modules to pages
3. Decompose pages to component level

**Agents Used:**
- `@frontend-decomposer` - Decomposes UI into component hierarchy
- `@context-generator` - Generates context files for each component

### Phase 3: Backend Decomposition (Modules → Services → Functions)
1. Initialize backend modules from PRD + architecture
2. Decompose modules to services
3. Decompose services to function level (API/service/repository/validation/utility layers)

**Agents Used:**
- `@backend-decomposer` - Decomposes services into layered functions
- `@context-generator` - Generates context files for each function

### Phase 4: Dependency Analysis (Build Cross-Stack Execution Plan)
1. Analyze frontend internal dependencies
2. Analyze backend internal dependencies
3. Analyze cross-stack dependencies (frontend API calls → backend endpoints)
4. Create execution waves with topological sort

**Agents Used:**
- `@fullstack-dependency-analyzer` - Creates optimized execution plan

### Phase 5: Parallel Development (TDD Implementation)
1. Execute tasks in waves following dependency graph
2. Backend waves use `@backend-developer` (TDD for API/service/repository)
3. Frontend waves use `@frontend-developer` (TDD for React/Vue components)
4. Save checkpoint after each wave

**Agents Used:**
- `@backend-developer` - Implements backend functions with TDD
- `@frontend-developer` - Implements frontend components with TDD

### Checkpoint Management
- Save checkpoint after processing each batch
- Maximum 10 tasks per batch
- Separate checkpoints for frontend and backend
- Always resume from last checkpoint

### TDD Requirements
- Tests must be written before implementation (RED phase)
- Minimal implementation to pass tests (GREEN phase)
- Refactor for quality (REFACTOR phase)
- All tests must pass before marking completed

## Custom Commands
Use slash commands defined in .claude/commands/ directory:

**Design Phase:**
- `/init-design` - Read PRD/architecture/UX docs, generate user flows (Mermaid)
- `/generate-wireframes` - Generate ASCII wireframes for each page

**Decomposition Phase:**
- `/init-decompose-frontend` - Initialize frontend module decomposition
- `/continue-decompose-frontend` - Decompose to component level
- `/init-decompose-backend` - Initialize backend service decomposition
- `/continue-decompose-backend` - Decompose to function level

**Dependency Phase:**
- `/build-deps-fullstack` - Build cross-stack dependency graph

**Development Phase:**
- `/parallel-dev-fullstack` - Execute parallel fullstack TDD development

**Monitoring:**
- `/status` - Check project status
- `/retry` - Retry failed tasks

## Task Type Hierarchy

### Frontend Hierarchy
1. **Level 1 - Module**: UI modules (e.g., "Authentication Module")
2. **Level 2 - Page**: Individual pages (e.g., "Login Page")
3. **Level 3 - Component**: React/Vue components (e.g., "LoginButton")

### Backend Hierarchy
1. **Level 1 - Module**: Service modules (e.g., "Authentication Service")
2. **Level 2 - Service**: Business logic services (e.g., "AuthService")
3. **Level 3 - Function**: Individual functions (e.g., "login_user")

### Backend Function Types
- **endpoint**: API route handlers (controllers)
- **service**: Business logic layer
- **repository**: Data access layer
- **validator**: Input validation
- **util**: Helper utilities

## Status Values
- **pending**: Not yet decomposed
- **decomposed**: Has been broken down into subtasks
- **ready**: Function-level task ready for development
- **in_progress**: Currently being developed
- **completed**: Development and tests passed
- **failed**: Development failed

## Best Practices
1. **Design First**: Always generate user flows and wireframes before decomposition
2. **Separate Frontend/Backend**: Decompose and develop them independently
3. **Respect Dependencies**: Backend APIs complete before frontend components that use them
4. **Batch Processing**: Process tasks in batches (max 10) to avoid context overflow
5. **Checkpoint Recovery**: Save state after each batch for resumability
6. **TDD Discipline**: Follow RED → GREEN → REFACTOR strictly
7. **Verify Design**: Frontend components must match wireframes
8. **API Contracts**: Validate frontend-backend interface compatibility
9. **Use Specialized Agents**: Each agent has specific expertise
10. **Integration Testing**: Test cross-stack functionality after parallel development
