---
description: Initialize design phase by reading PRD and generating user flows
---

# Initialize Design Phase

## Your Task
Read project documentation and generate comprehensive user flow diagrams.

## Prerequisites
Check that the following files exist:
- `docs/prd.md` - Product Requirements Document (必需)
- `docs/fullstack-architecture.md` - Technical architecture design (可选)
- `docs/front-end-spec.md` - UX design specifications (可选)
- `docs/back-end-spec.md` - Backend technical specifications (可选)

## Steps

### 1. Create Directory Structure
```bash
mkdir -p designs
mkdir -p designs/wireframes
mkdir -p .claude_tasks/contexts
```

### 2. Read Input Documents
Read all three documents:
- `docs/prd.md` - Understand product requirements and user stories
- `docs/fullstack-architecture.md` - Understand technical constraints and architecture
- `docs/front-end-spec.md` - Understand UX guidelines and design principles

### 3. Invoke UserFlowDesigner Subagent
```
Create a UserFlowDesigner subagent to generate user flows.

<subagent_task>
Agent: @user-flow-designer
Input:
- PRD: docs/prd.md
- Architecture: docs/fullstack-architecture.md
- UX Spec: docs/front-end-spec.md

Task:
1. Identify all user roles from PRD
2. Extract key user journeys and scenarios
3. Map user interactions with system components
4. Create detailed Mermaid flowcharts for each user flow
5. Include decision points, error states, and edge cases
6. Consider architecture constraints from fullstack-architecture.md
7. Follow UX principles from front-end-spec.md

Output:
Generate designs/user-flows.md with:
- Overview of all user flows
- Detailed Mermaid diagrams for each flow
- Page/screen transitions
- API interactions
- State management considerations
</subagent_task>
```

### 4. Validate User Flows
Check that `designs/user-flows.md` contains:
- At least one user flow diagram
- Proper Mermaid syntax
- Clear start and end points
- All identified pages/screens

### 5. Initialize State
Create `.claude_tasks/state.json`:
```json
{
  "design_phase": {
    "status": "user_flows_completed",
    "user_flows_file": "designs/user-flows.md",
    "wireframes_generated": false,
    "wireframes_count": 0
  },
  "decomposition_phase": {
    "status": "not_started",
    "frontend_status": "not_started",
    "backend_status": "not_started",
    "last_checkpoint": null
  },
  "development_phase": {
    "status": "not_started",
    "completed_tasks": 0,
    "failed_tasks": 0
  },
  "metadata": {
    "created_at": "[CURRENT_TIMESTAMP]",
    "last_updated": "[CURRENT_TIMESTAMP]"
  }
}
```

### 6. Output Summary
Print:
```
✓ Read input documents:
  - docs/prd.md
  - docs/fullstack-architecture.md
  - docs/front-end-spec.md

✓ Generated user flows:
  - designs/user-flows.md
  - [N] user flows identified
  - [M] pages/screens identified

Design phase: user_flows_completed

Next command: /generate-wireframes
```

## Important Rules
- All three input documents must exist
- User flows must use valid Mermaid syntax
- Identify ALL pages/screens mentioned in PRD
- Consider architecture constraints in flow design
- Save state after completion
