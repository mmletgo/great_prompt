---
description: Execute parallel fullstack development with TDD
argument-hint: [workers]
---

# Execute Parallel Fullstack Development

## Your Task
Execute all frontend and backend tasks in parallel following the dependency graph.

## Prerequisites
- Fullstack dependency graph exists in task_registry.json
- Design artifacts available (wireframes, user flows)

## Steps

### 1. Load Configuration
Read execution_order from task_registry.json.
Parse workers argument (default: 5).

### 2. Process Each Wave
For each wave in execution order:

#### 2.1 Identify Wave Category
Determine task types in current wave:
- Backend tasks: Use @backend-developer
- Frontend tasks: Use @frontend-developer
- Mixed wave: Use appropriate developer for each task type

#### 2.2 Create Developer Subagents

**CRITICAL - BATCHED PARALLEL EXECUTION WITHIN WAVE**:
- You MUST create developer subagents for ALL tasks in the current wave
- If wave has more than 10 tasks, process in sub-batches of maximum 10 subagents
- Count wave tasks FIRST, calculate number of sub-batches needed
- Process ALL sub-batches within the wave - DO NOT skip any sub-batch
- Each sub-batch must complete before starting next sub-batch within the wave
- ALL tasks in a wave MUST be processed (100% wave coverage)

**Batching Rules for Large Waves**:
1. Count tasks in wave: `wave_task_count = tasks in current wave`
2. If wave_task_count <= 10: Create all subagents at once
3. If wave_task_count > 10: 
   - Calculate sub-batches: `num_batches = ceil(wave_task_count / 10)`
   - **MANDATORY PARALLEL EXECUTION WITHIN EACH SUB-BATCH**:
     * Within each sub-batch, you MUST create ALL subagents AT THE SAME TIME
     * DO NOT process sub-batch items one by one
     * Create 10 `<subagent_task>` blocks simultaneously in one response
   - Track: "Wave [N], sub-batch X of Y (10 tasks)..."
4. Verify: After processing wave, confirm all tasks completed

**Example - Wave 3 has 27 tasks**:
```
Wave 3: Backend Service Layer (27 tasks)
Sub-batches needed: 3 (10 + 10 + 7)

Wave 3, sub-batch 1 of 3 (10 tasks)...
  Creating ALL 10 developer subagents SIMULTANEOUSLY:
  
  <subagent_task>Agent: @backend-developer (backend_task_020 - validateUserCredentials)</subagent_task>
  <subagent_task>Agent: @backend-developer (backend_task_021 - hashPassword)</subagent_task>
  ... [ALL 10 subagent blocks in ONE response]
  
  Executing with worker pool (5 concurrent):
  [Running] 020, 021, 022, 023, 024
  [Queued]  025-029
  ✓ Sub-batch 1 complete: 10/10 tasks

Wave 3, sub-batch 2 of 3 (10 tasks)...
  ✓ Sub-batch 2 complete: 10/10 tasks

Wave 3, sub-batch 3 of 3 (7 tasks)...
  ✓ Sub-batch 3 complete: 7/7 tasks

✓ Wave 3 complete: 27/27 tasks (100% coverage)
```

**FORBIDDEN - PARTIAL WAVE PROCESSING**:
- ❌ "Processing first sub-batch, skipping remaining in wave"
- ❌ "Core tasks in sub-batch 1, others optional"
- ❌ "Processing task 1... Processing task 2..." (串行执行)
- ❌ "Let me continue with task X" (one-by-one 处理)
- ✅ REQUIRED: "Creating ALL 10 subagents simultaneously in one response"
- ✅ REQUIRED: "ALL sub-batches in wave processed" / "100% wave coverage"

**Verification Required**:
1. Count tasks in current wave: `wave_task_count = tasks in wave [N]`
2. Determine batching:
   - If wave_task_count <= 10: Single batch
   - If wave_task_count > 10: Calculate `num_batches = ceil(wave_task_count / 10)`
3. For each sub-batch (if applicable):
   - Output: "Wave [N], sub-batch {i} of {num_batches} ({size} tasks)..."
   - Create up to 10 subagents per sub-batch
   - Confirm: "✓ Sub-batch {i} complete: {size}/{size} tasks"
4. Final wave verification: "✓ Wave [N] complete: {wave_task_count}/{wave_task_count} tasks (100% coverage)"

**For backend tasks:**
```
<subagent_task>
Agent: @backend-developer
Input:
- Task ID: backend_XXX
- Context file: .claude_tasks/contexts/backend_task_XXX_context.md
- Task type: [API/Service/Repository/Validation/Utility]
- Dependencies: [list of completed dependency task IDs]
- PRD reference: docs/prd.md
- Architecture: docs/fullstack-architecture.md

Task:
Execute TDD workflow for this backend function:

1. RED Phase:
   - Read context file for function specification
   - Write comprehensive test cases (pytest/jest)
   - Tests should fail initially
   - Cover: happy path, edge cases, error handling
   - For API layer: include integration tests
   - For Repository layer: include database mocks

2. GREEN Phase:
   - Implement the function to pass all tests
   - Follow clean architecture principles
   - Respect layer boundaries (API → Service → Repository)
   - Use type hints/TypeScript types
   - Handle errors appropriately

3. REFACTOR Phase:
   - Optimize code quality
   - Add comprehensive docstrings/comments
   - Ensure proper error handling
   - Verify all tests still pass
   - For APIs: generate OpenAPI/Swagger docs

Output format:
- Implementation file: [path from context]
- Test file: [test path from context]
- Coverage report: indicate test coverage %
- API documentation (if API layer)

Success criteria:
✓ All tests pass
✓ Code follows project conventions
✓ Proper error handling
✓ Documentation complete
</subagent_task>
```

**For frontend tasks:**
```
<subagent_task>
Agent: @frontend-developer
Input:
- Task ID: frontend_XXX
- Context file: .claude_tasks/contexts/frontend_task_XXX_context.md
- Task type: [Page/Component]
- Design reference: designs/wireframes/[page].md
- Dependencies: [list of completed dependency task IDs]
- UX spec: docs/front-end-spec.md

Task:
Execute TDD workflow for this frontend component:

1. RED Phase:
   - Read context file for component specification
   - Read wireframe for visual design
   - Write component tests (testing-library/jest)
   - Tests should fail initially
   - Test: rendering, user interactions, state changes, API calls

2. GREEN Phase:
   - Implement React/Vue component
   - Match wireframe design
   - Implement all interactive behaviors
   - Handle all component states (loading, error, success, empty)
   - Integrate with API endpoints (if applicable)
   - Follow design system from front-end-spec.md

3. REFACTOR Phase:
   - Optimize component structure
   - Add accessibility attributes (ARIA labels, etc.)
   - Ensure responsive design
   - Add PropTypes/TypeScript types
   - Verify against wireframe

4. VERIFY Phase:
   - All tests pass
   - Visual matches wireframe
   - Interactions work correctly
   - Accessible (keyboard nav, screen readers)

Output format:
- Component file: [path from context]
- Test file: [test path from context]
- Storybook story (optional): [story path]
- Coverage report: indicate test coverage %

Success criteria:
✓ All tests pass
✓ Matches wireframe design
✓ Proper state management
✓ Accessibility compliant
✓ Responsive design
</subagent_task>
```

#### 2.3 Execute Wave in Parallel

**Parallel Execution Model**:
- Create ALL subagent tasks for the wave at once (not sequentially)
- Subagents execute concurrently (up to `workers` limit controls parallel threads)
- If wave has 15 tasks and workers=5: create 15 subagents, run 5 at a time
- System automatically schedules execution based on worker availability
- Monitor progress and collect results as they complete

**Example**: Wave 3 has 12 backend service functions, workers=5
```
Wave 3: Creating ALL 12 developer subagents SIMULTANEOUSLY in ONE response...

<subagent_task>Agent: @backend-developer (backend_task_020 - validateUserCredentials)</subagent_task>
<subagent_task>Agent: @backend-developer (backend_task_021 - hashPassword)</subagent_task>
<subagent_task>Agent: @backend-developer (backend_task_022 - generateJWT)</subagent_task>
... [ALL 12 subagent blocks together]
<subagent_task>Agent: @backend-developer (backend_task_031 - updateUserProfile)</subagent_task>

Subagents created: 12 total

Executing with worker pool (5 concurrent):
  [Running] backend_task_020, 021, 022, 023, 024
  [Queued]  backend_task_025-031
  
  ✓ backend_task_020 completed (2.3 min)
  [Running] backend_task_025 (filled slot)
  
  ✓ backend_task_021 completed (2.1 min)
  [Running] backend_task_026 (filled slot)
  ...
  
✓ All 12 tasks completed
```

**Verification**:
- Confirm all wave tasks have subagents created
- Track completion count matches task count
- Report any failures immediately

#### 2.4 Verify Wave Results
For each completed task:
- ✓ Check all tests pass
- ✓ Verify implementation matches specification
- ✓ For frontend: verify against wireframe
- ✓ For backend API: verify OpenAPI docs generated
- ✓ Confirm no breaking changes to dependencies

#### 2.5 Update Status
- Mark tasks as `completed` or `failed` in task_registry.json
- Update state.json with current wave progress
- Log any errors or warnings
- Save checkpoint after wave completion

### 3. Cross-Stack Integration Validation

After all waves complete, verify cross-stack integration:

#### 3.1 API Contract Validation
For each frontend → backend dependency:
```
Frontend component: frontend_008 (LoginForm)
  → Calls: POST /api/auth/login
Backend endpoint: backend_009 (login_api)
  → Implements: POST /api/auth/login

Verify:
✓ Endpoint path matches
✓ Request body structure matches
✓ Response structure matches
✓ Error responses handled
✓ Authentication/authorization correct
```

#### 3.2 Component Integration Check
- Verify shared components used correctly
- Check parent-child component relationships
- Validate state management flow
- Confirm routing/navigation works

#### 3.3 Generate Integration Report
Create `.claude_tasks/integration_report.md`:
```markdown
# Cross-Stack Integration Report

## API Integrations Verified
1. LoginForm → POST /api/auth/login ✓
2. ProfileEditor → GET /api/users/:id ✓
3. ProductCard → GET /api/products ✓
...

## Component Dependencies
- Button (shared) ← Used by 15 components ✓
- Form (shared) ← Used by 8 components ✓
...

## Issues Found
- [List any integration issues]

## Recommendations
- [Integration improvements]
```

### 4. Optional: End-to-End User Flow Tests

After cross-stack integration validation, optionally create E2E tests:

```
<subagent_task>
Agent: @integration-tester (optional custom agent)
Input:
- User flows: designs/user-flows.md
- Completed frontend components: [list]
- Completed backend endpoints: [list]
- Wireframes: designs/wireframes/

Task:
Create end-to-end tests for each user flow:

1. Browse Products Flow:
   - Test: Navigate to product list
   - Test: Apply filters
   - Test: View product details
   - Test: Add to cart
   - Verify: All API calls successful
   - Verify: UI updates correctly

2. Checkout Flow:
   - Test: View cart
   - Test: Update quantities
   - Test: Proceed to checkout
   - Test: Enter payment info
   - Test: Complete order
   - Verify: Order confirmation received

Output:
- E2E test suite (Cypress/Playwright)
- Test results report
</subagent_task>
```

### 5. Output Summary
```
=== Fullstack Parallel Development Summary ===

Design Phase:
  User flows: ✓ designs/user-flows.md
  Wireframes: ✓ designs/wireframes/ ([N] pages)

Backend Development:
  Total functions: [N]
  ✓ Completed: [N]
  ✗ Failed: [0]
  
  By Layer:
  - API Layer: [X] functions ✓
  - Service Layer: [Y] functions ✓
  - Repository Layer: [Z] functions ✓
  - Validation Layer: [W] functions ✓
  - Utility Layer: [V] functions ✓
  
Frontend Development:
  Total components: [M]
  ✓ Completed: [M]
  ✗ Failed: [0]
  
  By Type:
  - Pages: [A] components ✓
  - Shared Components: [B] components ✓
  - Feature Components: [C] components ✓

Execution Timeline:
  Wave 1 (Backend Utils + Shared Components): [N] tasks
    - Tasks in wave: [N]
    - Sub-batches: [1 if N<=10, else ceil(N/10)]
    - Sub-batch 1: 10/10 tasks ✓ (if applicable)
    - Sub-batch 2: [X]/[X] tasks ✓ (if applicable)
    - Total completed: [N]/[N]
    ✓ Wave 1 coverage: 100%
    
  Wave 2 (Backend Repositories): [M] tasks
    - Tasks in wave: [M]
    - Sub-batches: [1 if M<=10, else ceil(M/10)]
    - Sub-batch processing details...
    - Total completed: [M]/[M]
    ✓ Wave 2 coverage: 100%
    
  Wave 3 (Backend Services): [K] tasks
    - Tasks in wave: [K]
    - Sub-batches: [1 if K<=10, else ceil(K/10)]
    - Sub-batch processing details...
    - Total completed: [K]/[K]
    ✓ Wave 3 coverage: 100%
    
  Wave 4 (Backend APIs): [L] tasks - COMPLETED
  Wave 5 (Frontend Basic Components): [P] tasks - COMPLETED
  Wave 6 (Frontend API Components): [Q] tasks - COMPLETED
  Wave 7 (Frontend Pages): [R] tasks - COMPLETED
  Wave 8 (Integration Tests): [S] tests - COMPLETED

✓ ALL WAVES: 100% task coverage (no tasks skipped)

Cross-Stack Integration:
  ✓ API contracts validated: [N] integrations
  ✓ Component dependencies verified
  ✓ User flow coverage: 100%

Test Coverage:
  Backend: [X]% (target: >80%)
  Frontend: [Y]% (target: >80%)

Parallel Execution Verification:
  ✓ All waves executed with full parallelization
  ✓ No sequential processing detected
  ✓ Worker pool utilized efficiently
  Average tasks per wave: [N]
  Total waves: [M]
  Total tasks: [T]
  
Failed Tasks (if any):
  [List of failed tasks with reasons]

Next Steps:
  1. Review any failed tasks
  2. Run full test suite: npm test && pytest
  3. Start development servers
  4. Manual testing against wireframes
  5. Check integration_report.md
  6. Prepare for deployment
```

### 6. Generate Development Report
Create `DEVELOPMENT_REPORT.md`:
```markdown
### 6. Generate Development Report
Create `.claude_tasks/DEVELOPMENT_REPORT.md`:
```markdown
# Fullstack Development Report

Generated: [TIMESTAMP]

## Project Overview
- PRD: docs/prd.md
- Architecture: docs/fullstack-architecture.md
- User Flows: designs/user-flows.md
- Wireframes: designs/wireframes/ ([N] pages)

## Backend Summary

### Completed Endpoints
#### Authentication API
- POST /api/auth/login - User login
- POST /api/auth/register - User registration
- POST /api/auth/logout - User logout
- GET /api/auth/verify - Token verification

#### User API
- GET /api/users/:id - Get user profile
- PUT /api/users/:id - Update user profile
- DELETE /api/users/:id - Delete user account

#### [Other API Groups]
...

### Database Schema
#### Tables Created
- `users`: id, email, password_hash, created_at, updated_at
- `sessions`: id, user_id, token, expires_at
- `[other_tables]`: [schema]

### Service Layer Functions
- UserService: [N] functions
- AuthService: [M] functions
- [OtherServices]: [K] functions

### Test Coverage
- API Layer: [X]% coverage
- Service Layer: [Y]% coverage
- Repository Layer: [Z]% coverage
- Total Backend: [W]% coverage

## Frontend Summary

### Completed Pages
#### Authentication Pages
- Login Page (3 components)
  - LoginForm
  - SocialLoginButtons
  - LoginHeader
- Register Page (4 components)
  - RegisterForm
  - TermsCheckbox
  - PasswordStrengthIndicator
  - RegisterButton

#### Dashboard Pages
- Main Dashboard (8 components)
  - DashboardHeader
  - StatsCards
  - ActivityFeed
  - QuickActions
  - ...

### Component Library
#### Shared Components ([N] total)
- Button (Primary, Secondary, Text variants)
- Input (Text, Email, Password, Number)
- Card, Modal, Tooltip, Dropdown
- ...

#### Page-Specific Components ([M] total)
- [List by page]

### Design System Compliance
- ✓ All components follow front-end-spec.md
- ✓ Consistent naming conventions
- ✓ Responsive design (mobile, tablet, desktop)
- ✓ Accessibility (ARIA labels, keyboard nav)

### Test Coverage
- Component tests: [X]% coverage
- Integration tests: [Y] tests
- Total Frontend: [Z]% coverage

## Cross-Stack Integration

### API Integrations ([N] total)
1. LoginForm → POST /api/auth/login ✓
2. RegisterForm → POST /api/auth/register ✓
3. ProfileEditor → GET /api/users/:id ✓
4. ProfileEditor → PUT /api/users/:id ✓
...

### Verification Status
- ✓ All API contracts match
- ✓ Request/response schemas validated
- ✓ Error handling tested
- ✓ Authentication flows working

## Execution Metrics

### Development Timeline
- Total waves: [N]
- Total tasks: [M]
- Average wave time: [X] minutes
- Total development time: [Y] hours

### Parallel Efficiency
- Maximum parallelism: [N] tasks
- Average parallelism: [M] tasks
- Worker utilization: [X]%

## Test Results

### Backend Tests
- Total tests: [N]
- Passed: [M]
- Failed: [0]
- Coverage: [X]%

### Frontend Tests
- Total tests: [N]
- Passed: [M]
- Failed: [0]
- Coverage: [Y]%

### Integration Tests
- User flow tests: [N]
- API integration tests: [M]
- All tests: ✓ PASSED

## Known Issues

[List any failed tasks or issues]
- None / [Issue description]

## Deployment Checklist

### Backend
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] API documentation generated (Swagger/OpenAPI)
- [ ] Health check endpoint implemented
- [ ] Logging configured
- [ ] Error monitoring setup

### Frontend
- [ ] Build successful (npm run build)
- [ ] Environment variables configured
- [ ] API base URL configured
- [ ] Static assets optimized
- [ ] Service worker configured (if PWA)
- [ ] Analytics setup

### Testing
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] E2E tests passing (if implemented)
- [ ] Manual testing completed

### Documentation
- [ ] API documentation complete
- [ ] Component documentation (Storybook)
- [ ] README updated
- [ ] Deployment guide ready

## Next Steps

1. **Code Review**
   - Review failed tasks (if any)
   - Check code quality
   - Verify test coverage

2. **Manual Testing**
   - Test all user flows against wireframes
   - Test responsive design
   - Test accessibility
   - Cross-browser testing

3. **Performance Testing**
   - API response times
   - Frontend rendering performance
   - Database query optimization

4. **Deployment Preparation**
   - Complete deployment checklist
   - Prepare production environment
   - Plan rollout strategy

5. **Monitoring Setup**
   - Application monitoring
   - Error tracking
   - Performance monitoring
   - User analytics
```

## Important Rules
- **CRITICAL**: Create ALL subagents for each wave at once (parallel, not sequential)
- **NO PARTIAL PROCESSING**: Every task in a wave MUST have a subagent created
- **Verify counts**: Tasks in wave = Subagents created = Tasks completed
- Use @backend-developer for all backend tasks (API, Service, Repository, Validation, Utility layers)
- Use @frontend-developer for all frontend tasks (Pages and Components)
- Backend APIs must complete before dependent frontend components
- Follow dependency graph strictly (from build-deps-fullstack)
- Worker limit controls concurrent execution, NOT how many subagents to create
- Save state after each wave completion
- Verify all tests pass before marking tasks complete
- Generate comprehensive cross-stack integration report
- Verify frontend components match wireframe designs
- Ensure all API contracts are validated
- Update task_registry.json after each wave
- Report 100% wave coverage in output summary
```

## Important Rules
- Backend APIs before dependent frontend components
- Follow dependency graph strictly
- Save state after each wave
- Generate comprehensive test coverage
- Create integration tests for user flows
- Verify frontend matches wireframes
