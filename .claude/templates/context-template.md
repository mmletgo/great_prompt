# Task Context Template

## Overview
Task context files provide detailed specifications for individual development tasks. Each Level 3 task (component or function) has its own context file that guides TDD implementation.

## File Location
```
.claude_tasks/contexts/{task_id}_context.md
```
Where `{task_id}` is the task identifier (e.g., `frontend_task_001`, `backend_task_020`)

## Complete Template

### For Frontend Components
```markdown
# Task {task_id}: {Component Name}

## Task Overview
{Brief description of the component's purpose and role}

## Component Hierarchy
- **Parent**: {parent_task_id} - {Parent Component Name}
- **Children**: {child_task_ids if any}
- **Level**: 3 (Component)
- **Type**: {component_type} (e.g., button, form, page, card)

## Dependencies
- {dependency_task_id_1}: {What this dependency provides}
- {dependency_task_id_2}: {What this dependency provides}
- None (if no dependencies)

## Design Reference
**Wireframe**: designs/wireframes/{page-name}.md
**Section**: {Specific section/component in wireframe}
**UX Specification**: docs/front-end-spec.md

## Component Specification

### Component Props
```typescript
interface {ComponentName}Props {
  {propName1}: {type};  // {description}
  {propName2}: {type};  // {description}
  {propName3}?: {type}; // {description} (optional)
}
```

### Component State
- `{stateName1}`: {type} - {description}
- `{stateName2}`: {type} - {description}

### Events/Callbacks
- `{eventName1}`: ({params}) => void - {description}
- `{eventName2}`: ({params}) => void - {description}

## Visual Specifications
From wireframe:
- **Layout**: {layout description}
- **Styling**: {key styling requirements}
- **Responsive behavior**: {breakpoint behavior}
- **States**: {loading, error, success, empty states}

## Component States to Handle
1. **Loading**: {description}
2. **Error**: {error scenarios}
3. **Success**: {success state}
4. **Empty**: {empty state handling}

## TDD Test Cases

### Test Case 1: Component Renders
```typescript
describe('{ComponentName}', () => {
  it('should render without crashing', () => {
    // Test implementation
  });
});
```

### Test Case 2: Props Handling
```typescript
it('should render with correct props', () => {
  // Test prop values display correctly
});
```

### Test Case 3: User Interactions
```typescript
it('should handle {interaction} correctly', () => {
  // Test click, input, etc.
});
```

### Test Case 4: State Changes
```typescript
it('should update state when {event} occurs', () => {
  // Test state updates
});
```

### Test Case 5: Edge Cases
```typescript
it('should handle {edge_case}', () => {
  // Test edge cases
});
```

### Test Case 6: Accessibility
```typescript
it('should be accessible', () => {
  // Test ARIA labels, keyboard navigation
});
```

## Related Files
- **Target file**: src/components/{ComponentName}.tsx
- **Test file**: src/components/__tests__/{ComponentName}.test.tsx
- **Story file** (optional): src/components/{ComponentName}.stories.tsx
- **Dependency files**: {list dependency component files}

## Implementation Notes
- Follow design system from front-end-spec.md
- Use consistent naming conventions
- Implement responsive design (mobile-first)
- Add proper TypeScript types
- Include accessibility attributes (ARIA)

## Success Criteria
✓ All test cases pass
✓ Visual matches wireframe
✓ Props and state work correctly
✓ User interactions function as expected
✓ Accessible (keyboard nav, screen readers)
✓ Responsive on all breakpoints
✓ Test coverage > 80%
```

### For Backend Functions
```markdown
# Task {task_id}: {Function Name}

## Task Overview
{Brief description of the function's purpose and role}

## Function Hierarchy
- **Parent**: {parent_task_id} - {Parent Service/Module Name}
- **Children**: {child_task_ids if any}
- **Level**: 3 (Function)
- **Type**: {function_type} (endpoint, service, repository, validator, util)
- **Layer**: {layer} (api, service, repository, validation, utility)

## Dependencies
- {dependency_task_id_1}: {What this dependency provides}
- {dependency_task_id_2}: {What this dependency provides}
- None (if no dependencies)

## Function Specification

### Function Signature
```python
def {function_name}({param1}: {type}, {param2}: {type}) -> {return_type}:
    """
    {Function description}
    
    Args:
        {param1}: {description}
        {param2}: {description}
    
    Returns:
        {return_type}: {description}
    
    Raises:
        {ExceptionType}: {when this is raised}
    """
    pass
```

### Input Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `{param1}` | {type} | Yes | {description} |
| `{param2}` | {type} | No | {description} |

### Return Value
- **Type**: {type}
- **Description**: {what it returns}
- **Structure** (if complex):
  ```python
  {
    "field1": "value1",
    "field2": "value2"
  }
  ```

### Exceptions
- `{ExceptionType1}`: {when raised}
- `{ExceptionType2}`: {when raised}

## API Endpoint Details (if function_type == "endpoint")
- **HTTP Method**: {GET|POST|PUT|DELETE|PATCH}
- **Route**: /api/{route}
- **Authentication**: {Required|Optional|None}
- **Authorization**: {Required roles/permissions}

### Request Schema
```json
{
  "field1": "type1",
  "field2": "type2"
}
```

### Response Schema
**Success (200/201)**:
```json
{
  "data": {},
  "message": "string"
}
```

**Error (4xx/5xx)**:
```json
{
  "error": "string",
  "details": {}
}
```

## Business Logic
1. {Step 1 description}
2. {Step 2 description}
3. {Step 3 description}

## Validation Rules
- {Rule 1}
- {Rule 2}
- {Rule 3}

## TDD Test Cases

### Test Case 1: Happy Path
```python
def test_{function_name}_success():
    """Test successful execution with valid inputs"""
    # Arrange
    {input_setup}
    
    # Act
    result = {function_name}({params})
    
    # Assert
    assert result == {expected_output}
```

### Test Case 2: Invalid Input
```python
def test_{function_name}_invalid_input():
    """Test error handling for invalid inputs"""
    with pytest.raises({ExceptionType}):
        {function_name}({invalid_params})
```

### Test Case 3: Edge Case
```python
def test_{function_name}_edge_case():
    """Test {specific edge case}"""
    # Test implementation
```

### Test Case 4: Database Operations (if repository layer)
```python
def test_{function_name}_database():
    """Test database interactions"""
    # Mock database
    # Test queries
```

### Test Case 5: API Integration (if endpoint layer)
```python
def test_{function_name}_api():
    """Test API endpoint behavior"""
    # Test request/response
    # Test status codes
```

## Related Files
- **Target file**: src/{layer}/{module}.py
- **Test file**: tests/test_{module}.py
- **Dependency files**: {list dependency files}
- **Database models** (if applicable): src/models/{model}.py

## Architecture Notes
- **Layer**: {api|service|repository|validation|utility}
- **Layer boundaries**: {what this layer should/shouldn't do}
- **Clean architecture**: {how this fits in the architecture}

## Database Schema (if repository layer)
**Table**: {table_name}
```sql
CREATE TABLE {table_name} (
  {column1} {type} {constraints},
  {column2} {type} {constraints}
);
```

## Implementation Notes
- Follow clean architecture principles
- Respect layer boundaries
- Use type hints
- Handle errors appropriately
- Add comprehensive docstrings
- For APIs: generate OpenAPI/Swagger docs

## Success Criteria
✓ All test cases pass
✓ Code follows project conventions
✓ Proper error handling
✓ Type hints included
✓ Docstrings complete
✓ Layer boundaries respected
✓ Test coverage > 80%
✓ API docs generated (if endpoint)
```

## Field Descriptions

### Common Fields
| Field | Description |
|-------|-------------|
| `task_id` | Unique task identifier (e.g., frontend_task_001) |
| `Task Overview` | Brief description of purpose |
| `Component/Function Hierarchy` | Parent-child relationships |
| `Dependencies` | Other tasks this task depends on |
| `TDD Test Cases` | Comprehensive test scenarios |
| `Related Files` | Implementation and test file paths |
| `Success Criteria` | Checklist for completion |

### Frontend-Specific Fields
| Field | Description |
|-------|-------------|
| `Design Reference` | Wireframe location and section |
| `Component Props` | TypeScript interface definition |
| `Component State` | State variables and types |
| `Events/Callbacks` | Event handlers |
| `Visual Specifications` | Layout and styling requirements |
| `Component States` | Loading, error, success, empty states |

### Backend-Specific Fields
| Field | Description |
|-------|-------------|
| `Function Signature` | Complete function definition |
| `API Endpoint Details` | HTTP method, route, auth |
| `Request/Response Schema` | JSON schemas |
| `Business Logic` | Step-by-step logic description |
| `Validation Rules` | Input validation requirements |
| `Database Schema` | Table structure (if repository) |
| `Architecture Notes` | Layer boundaries and patterns |

## Usage Guidelines

### When to Create Context Files
- **During decomposition phase**: Generate context for every Level 3 task
- **Use @context-generator agent**: Automated generation from task definitions
- **One file per task**: Each Level 3 component/function gets its own file

### Context File Generation Process
1. **Frontend decomposition** → Generate frontend_task_XXX_context.md files
2. **Backend decomposition** → Generate backend_task_XXX_context.md files
3. **Reference in task_registry.json**: Set `context_file` field to path

### Best Practices
1. **Comprehensive TDD specs**: Include all test scenarios upfront
2. **Clear dependencies**: List what each dependency provides
3. **Detailed specifications**: Enough detail for implementation without ambiguity
4. **Design references**: Link to wireframes for frontend, architecture for backend
5. **Success criteria**: Clear checklist for task completion

## Integration with Other Files

### task_registry.json
```json
{
  "tasks": {
    "frontend_task_001": {
      "context_file": ".claude_tasks/contexts/frontend_task_001_context.md"
    }
  }
}
```

### Subagent Task Input
```xml
<subagent_task>
Agent: @frontend-developer
Input:
- Task ID: frontend_task_001
- Context file: .claude_tasks/contexts/frontend_task_001_context.md
Task: Execute TDD workflow for this component
</subagent_task>
```

## See Also
- [task_registry.json Template](task_registry.json.template) - Task definitions
- [state.json Template](state.json.template) - Progress tracking
- [CLAUDE.md - Workflow Phases](../CLAUDE.md#workflow-phases) - Development process
