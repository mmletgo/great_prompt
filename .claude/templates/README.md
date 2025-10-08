# Templates Directory

## Overview
This directory contains authoritative templates for all data structures used in the fullstack development system. All agents and commands should reference these templates instead of defining structures inline.

## Available Templates

### 1. state.json.template
**File**: [state.json.template](./state.json.template)
**Purpose**: Global state tracking for all workflow phases
**Used By**: All commands that track progress
**Key Sections**:
- `design_phase`: User flows and wireframes status
- `decomposition_phase`: Frontend/backend decomposition progress  
- `dependency_phase`: Dependency analysis status
- `development_phase`: Wave-by-wave TDD execution
- `metadata`: Timestamps and project info

### 2. task_registry.json.template
**File**: [task_registry.json.template](./task_registry.json.template)
**Purpose**: Central task management and dependency tracking
**Used By**: All decomposition and development commands
**Key Sections**:
- `tasks`: All frontend/backend task definitions
- `frontend_metadata`: Framework, component counts
- `backend_metadata`: Framework, database, function counts
- `dependency_graph`: Dependencies and execution order

### 3. context-template.md
**File**: [context-template.md](./context-template.md)
**Purpose**: Task context files for TDD implementation
**Used By**: @context-generator, decomposition commands
**Variants**:
- **Frontend**: Component specifications, props, states, design reference
- **Backend**: Function specifications, API details, layer architecture

### 4. wireframe-output.template
**File**: [wireframe-output.template](./wireframe-output.template)
**Purpose**: ASCII wireframe specifications for pages
**Used By**: @wireframe-designer, /generate-wireframes command
**Key Sections**:
- Page structure and layout
- ASCII visual representation
- Component breakdown
- States (loading, error, empty, success)
- Interactions and API calls
- Navigation and accessibility

## Usage Guidelines

### For Command Documentation
Instead of including full JSON/Markdown examples:

❌ **Don't do this**:
```markdown
Create state.json:
```json
{
  "design_phase": {
    "status": "completed",
    ... (50+ lines)
  }
}
```
```

✅ **Do this**:
```markdown
Create state.json with initial structure.

**📄 State File Format**: See [state.json Template](../templates/state.json.template)

**Required fields**:
- `design_phase.status = "completed"`
- `design_phase.user_flows_file = "designs/user-flows.md"`
```

### For Agent Documentation
Reference templates in "Output Format" sections:

```markdown
## Output Format
Create task context file following the template.

**📄 Context Template**: See [Task Context Template](../../templates/context-template.md#for-frontend-components)
```

### For Main Documentation (CLAUDE.md)
Keep only essential examples, link to templates for full specifications:

```markdown
### state.json
Global state tracking file for all workflow phases.

**📄 See complete format**: [state.json Template](.claude/templates/state.json.template)

**Example structure**:
```json
{
  "development_phase": {
    "current_wave": 3,
    "completed_tasks": ["task_001"]
  }
}
```
```

## Template Maintenance

### When to Update Templates
- Adding new fields to data structures
- Changing field types or constraints
- Adding new sections or requirements
- Fixing errors in specifications

### Where NOT to Update
- ❌ Individual command files
- ❌ Agent files  
- ❌ CLAUDE.md
- ❌ Inline JSON examples elsewhere

### Update Process
1. **Update template file** with changes
2. **Check all references**: Ensure commands still reference correctly
3. **Update examples**: If template changes break existing examples
4. **Test integration**: Verify commands work with new format

## Benefits of This Approach

### Single Source of Truth
✅ Format defined in one place
✅ Updates propagate automatically (through references)
✅ No conflicting definitions across files

### Better Maintainability
✅ Easier to find and update specifications
✅ Reduces duplicate content
✅ Smaller command files, clearer focus

### Improved Documentation
✅ Commands focus on workflow, not data formats
✅ Templates provide comprehensive field descriptions
✅ Examples and validation rules in one place
✅ Easier to learn the system

## Cross-References

### Template → Commands
Each template lists which commands use it (see "Used By" in each template)

### Commands → Templates
Each command references relevant templates in "Prerequisites" or inline sections

### CLAUDE.md → Templates
Main documentation references all templates in "State Files Format" section

## File Structure
```
.claude/templates/
├── README.md                      # This file
├── state.json.template            # Global state format
├── task_registry.json.template    # Task management format
├── context-template.md            # Task context format
└── wireframe-output.template      # Wireframe format
```

## See Also
- [CLAUDE.md](../../CLAUDE.md) - Main project documentation
- [Commands Directory](../commands/) - Workflow commands
- [Agents Directory](../agents/) - Specialized agents
