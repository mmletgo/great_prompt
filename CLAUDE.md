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

The project uses two central JSON files for state management and task tracking. **IMPORTANT**: These files should be updated using Python scripts, not manually edited.

### state.json
Global state tracking file for all workflow phases. Supports checkpoint recovery and resuming from interruptions.

**📄 See complete format specification**: [state.json Template](.claude/templates/state.json.template)

**📄 Python API for updates**: [State Management Scripts](.claude/scripts/README.md)

**Key sections**:
- `design_phase`: User flows and wireframes status
- `decomposition_phase`: Frontend/backend decomposition progress
- `dependency_phase`: Dependency analysis status
- `development_phase`: Wave-by-wave execution progress
- `metadata`: Timestamps and project info

**How to update** (use Python scripts, NOT manual JSON edits):
```python
from state_manager import StateManager

manager = StateManager()

# Complete design phase
manager.complete_wireframes(wireframes_count=8, validation_status="passed")

# Start development
manager.start_development(total_waves=10, workers=5)

# Complete a task
manager.complete_task("FE_auth_LoginForm")

# Complete a wave
manager.complete_wave(wave_number=1)
```

**Example structure**:
```json
{
  "development_phase": {
    "status": "in_progress",
    "current_wave": 5,
    "completed_waves": 4,
    "completed_tasks": ["backend_task_001", "frontend_task_001"],
    "failed_tasks": [],
    "wave_progress": {
      "5": {
        "status": "in_progress",
        "tasks": 27,
        "completed": 10,
        "current_batch": 3
      }
    }
  }
}
```

### task_registry.json
Central task management file containing all frontend/backend tasks, dependencies, and execution order.

**📄 See complete format specification**: [task_registry.json Template](.claude/templates/task_registry.json.template)

**📄 Python API for updates**: [Task Registry Scripts](.claude/scripts/README.md)

**Key sections**:
- `tasks`: All frontend and backend tasks with metadata
- `frontend_metadata`: Framework, language, component counts
- `backend_metadata`: Framework, database, layer counts
- `dependency_graph`: Dependencies and wave execution order

**How to update** (use Python scripts, NOT manual JSON edits):
```python
from task_registry_manager import TaskRegistryManager

manager = TaskRegistryManager()

# Add a task
manager.add_task("FE_auth_LoginForm", {
    "name": "LoginForm Component",
    "category": "frontend",
    "type": "component",
    "status": "pending"
})

# Update task status
manager.update_task_status(
    task_id="FE_auth_LoginForm",
    status="completed",
    implementation_file="src/components/auth/LoginForm.tsx",
    test_coverage=95
)

# Set execution order
manager.set_execution_order(waves=[...])
```

**Example task**:
```json
{
  "tasks": {
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
  }
}
```

## Task Context Template
Each task context file provides detailed specifications for TDD implementation.

**📄 See complete template**: [Task Context Template](.claude/templates/context-template.md)

**Key sections**:
- Task Overview and hierarchy
- Dependencies
- Component/Function specifications
- TDD test cases
- Related files and success criteria

**File location**: `.claude_tasks/contexts/{task_id}_context.md`

## Workflow Phases

### Phase 1: Design (Read Docs → Generate Design Artifacts)
1. Read `docs/prd.md` (必需), `docs/fullstack-architecture.md` (可选), `docs/front-end-spec.md` (可选), `docs/back-end-spec.md` (可选)
2. Generate `designs/user-flows.md` with Mermaid diagrams
3. Generate `designs/wireframes/` ASCII wireframes for each page

**Status Flow:** `not_started` → `user_flows_completed` → `completed`

**Agents Used:**
- `@user-flow-designer` - Creates Mermaid user flow diagrams
- `@wireframe-designer` - Generates detailed ASCII wireframes

### Phase 2: Frontend Decomposition (Modules → Pages → Components)
1. Initialize frontend modules from wireframes
2. Decompose modules to pages
3. Decompose pages to component level

**Prerequisites:** `design_phase.status == "completed"`

**Status Flow:** `decomposition_phase.frontend_status`: `not_started` → `in_progress` → `completed`

**Agents Used:**
- `@frontend-decomposer` - Decomposes UI into component hierarchy
- `@context-generator` - Generates context files for each component (uses frontend component template)

### Phase 3: Backend Decomposition (Modules → Services → Functions)
1. Initialize backend modules from PRD + architecture
2. Decompose modules to services
3. Decompose services to function level (API/service/repository/validation/utility layers)

**Prerequisites:** `design_phase.status == "completed"` (前端分解完成是推荐但非必需)

**Status Flow:** `decomposition_phase.backend_status`: `not_started` → `in_progress` → `completed`

**Agents Used:**
- `@backend-decomposer` - Decomposes services into layered functions
- `@context-generator` - Generates context files for each function (uses backend function template)

### Phase 4: Dependency Analysis (Build Cross-Stack Execution Plan)
1. Analyze frontend internal dependencies
2. Analyze backend internal dependencies
3. Analyze cross-stack dependencies (frontend API calls → backend endpoints)
4. Create execution waves with topological sort

**Prerequisites:** 
- `decomposition_phase.frontend_status == "completed"`
- `decomposition_phase.backend_status == "completed"`
- All component-level and function-level tasks registered

**Agents Used:**
- `@fullstack-dependency-analyzer` - Creates optimized execution plan

### Phase 5: Parallel Development (TDD Implementation)
1. Execute tasks in waves following dependency graph
2. Backend waves use `@backend-developer` (TDD for API/service/repository)
3. Frontend waves use `@frontend-developer` (TDD for React/Vue components)
4. Update state after each task, batch, and wave using Python scripts

**Agents Used:**
- `@backend-developer` - Implements backend functions with TDD
- `@frontend-developer` - Implements frontend components with TDD

**State Updates (use Python scripts)**:
```python
from utils import ProjectManager

manager = ProjectManager()

# After task completes
manager.complete_task_full(
    task_id="FE_auth_LoginForm",
    implementation_file="src/components/auth/LoginForm.tsx",
    test_file="src/components/auth/LoginForm.test.tsx",
    test_coverage=95,
    duration_minutes=12.5
)

# After batch completes
manager.complete_batch(
    wave_number=1,
    completed_tasks=["task1", "task2", "task3"],
    failed_tasks=[]
)

# After wave completes
result = manager.complete_wave_full(wave_number=1)
```

## Python Script Usage

**CRITICAL**: Always use Python scripts to update state.json and task_registry.json. Never manually edit these JSON files.

**📄 Complete API Documentation**: [.claude/scripts/README.md](.claude/scripts/README.md)

**Available Scripts**:
- `state_manager.py` - Manages state.json operations
- `task_registry_manager.py` - Manages task_registry.json operations
- `utils.py` - High-level convenience functions

**Common Operations**:
```python
# 1. Check project status
from utils import print_dashboard
print_dashboard()

# 2. Complete a task (updates both files atomically)
from utils import ProjectManager
manager = ProjectManager()
manager.complete_task_full(
    task_id="FE_auth_LoginForm",
    implementation_file="src/components/auth/LoginForm.tsx",
    test_file="src/components/auth/LoginForm.test.tsx",
    test_coverage=95
)

# 3. Check resume status
status = manager.check_resume_status()
if status['can_resume']:
    next_batch = manager.get_next_batch_tasks(
        wave_number=status['current_wave'],
        batch_size=5
    )

# 4. Complete a wave with validation
result = manager.complete_wave_full(wave_number=3)
if not result['success']:
    print(f"Incomplete tasks: {result['incomplete_tasks']}")
```

**Benefits**:
- ✅ Atomic operations - both files updated consistently
- ✅ Data validation - prevents invalid states
- ✅ Error prevention - no JSON syntax errors
- ✅ Convenience - high-level functions handle multiple operations
- ✅ Type safety - Python type hints prevent errors

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
- `/generate-wireframes [count]` - Generate ASCII wireframes for each page (optional: specify count)

**Decomposition Phase:**
- `/init-decompose-frontend` - Initialize frontend module decomposition
- `/continue-decompose-frontend` - Decompose to component level (resumes from checkpoint)
- `/init-decompose-backend` - Initialize backend service decomposition
- `/continue-decompose-backend` - Decompose to function level (resumes from checkpoint)

**Dependency Phase:**
- `/build-deps-fullstack` - Build cross-stack dependency graph and execution plan

**Development Phase:**
- `/parallel-dev-fullstack [workers]` - Execute parallel fullstack TDD development (default: 5 workers)

**Monitoring:**
- `/status [phase]` - Check project status (optional: specify phase)
- `/retry [task_id]` - Retry failed tasks (optional: specify task ID)

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
