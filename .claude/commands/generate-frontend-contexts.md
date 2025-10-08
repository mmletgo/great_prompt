---
description: Generate context files for all frontend component tasks
---

# Generate Frontend Context Files

## Your Task
Generate comprehensive context files for all frontend component-level tasks that are ready for context generation.

## Prerequisites
- `decomposition_phase.frontend_status == "completed"` OR at least some component tasks exist
- Component-level tasks exist in task_registry.json (type == "component", level == 3)

## Steps

### 1. Load Task Registry
Read `.claude_tasks/task_registry.json` and filter tasks:
- `category == "frontend"`
- `type == "component"`
- `level == 3`
- `status == "ready"` (not yet context-generated)

Count total tasks needing context generation.

### 2. Batch Processing Strategy

**Batching Rules**:
- Maximum 10 context generators per sub-batch
- Calculate: `num_batches = ceil(total_tasks / 10)`
- Process ALL batches sequentially
- Each sub-batch runs in parallel (all 10 subagents created simultaneously)

**Example**:
```
Total component tasks: 47
Sub-batches needed: 5 (10 + 10 + 10 + 10 + 7)
```

### 3. Invoke Context Generator Subagents (Batched Parallel)

For each sub-batch:

**CRITICAL - PARALLEL EXECUTION WITHIN SUB-BATCH**:
- Create ALL 10 (or remaining) subagents in ONE response
- DO NOT process one by one
- DO NOT wait for one to finish before creating next
- Output all `<subagent_task>` blocks together

**Example - Sub-batch of 10**:
```
Processing sub-batch 1 of 5 (10 components)...
Creating ALL 10 ContextGenerator subagents SIMULTANEOUSLY:

<subagent_task>
Agent: @context-generator
Input:
- Task ID: frontend_task_008
- Component: LoginForm
- Design reference: designs/wireframes/login-page.md
Task: Generate comprehensive context file
</subagent_task>

<subagent_task>
Agent: @context-generator
Input:
- Task ID: frontend_task_009
- Component: EmailInput
- Design reference: designs/wireframes/login-page.md
Task: Generate comprehensive context file
</subagent_task>

<subagent_task>
Agent: @context-generator
Input:
- Task ID: frontend_task_010
- Component: PasswordInput
- Design reference: designs/wireframes/login-page.md
Task: Generate comprehensive context file
</subagent_task>

... [7 more subagent blocks - ALL in ONE response]

[Wait for ALL 10 subagents to complete]
```

**For each component task, create this subagent**:
```
<subagent_task>
Agent: @context-generator
Input:
- Task ID: {task_id}
- Component metadata: from task_registry.json
- Design reference: {wireframe_file}
- Parent context: {parent_task_context if exists}

Task:
1. Read component metadata from task_registry.json:
   - Component name and type
   - Props and their types
   - State variables
   - Hooks needed
   - Event handlers
   - API calls

2. Read design reference (wireframe file):
   - Visual layout
   - UI states (default, loading, error, success, empty)
   - User interactions
   - Accessibility requirements

3. Analyze parent context (if applicable):
   - Data flow from parent
   - Callbacks to parent
   - Shared state

4. Generate context file at: .claude_tasks/contexts/{task_id}_context.md

Output format:

# Task {task_id}: {ComponentName}

## Component Overview
**Type**: {Presentational/Container/Form/etc}
**Purpose**: {Brief description}
**Parent**: {parent_task_id if exists}

## Component Specification

### Props
```typescript
interface {ComponentName}Props {
  prop1: type;  // description
  prop2: type;  // description
  onEvent?: (data: Type) => void;  // callback description
}
```

### State
```typescript
const [state1, setState1] = useState<Type>(initialValue);  // purpose
const [loading, setLoading] = useState<boolean>(false);
const [error, setError] = useState<string | null>(null);
```

### Hooks
- `useState`: For managing {what state}
- `useEffect`: For {what side effect}
- `useContext`: For accessing {what context}
- `useCallback`: For memoizing {what callback}
- Custom hooks: `use{CustomHook}` for {purpose}

### Event Handlers
```typescript
const handleClick = () => {
  // behavior description
};

const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
  // behavior description
};
```

### API Calls
```typescript
// GET /api/endpoint
const fetchData = async () => {
  // API call description
  // Error handling
  // Loading states
};
```

## UI States

### Default State
- Description: {when this state is shown}
- Visual: {what user sees}
- Data: {what data is displayed}

### Loading State
- Description: While data is being fetched
- Visual: Spinner/skeleton loader
- Props disabled: {list}

### Error State
- Description: When API call fails
- Visual: Error message display
- User actions: Retry button

### Success State
- Description: After successful operation
- Visual: Success feedback
- Next action: {what happens next}

### Empty State
- Description: No data to display
- Visual: Empty state message
- User actions: Call-to-action button

## Design Reference
**Wireframe**: {wireframe_file_path}
**Section**: {specific section in wireframe}

**Visual Requirements**:
- Layout: {flexbox/grid/etc}
- Spacing: {margins/paddings}
- Colors: {from design system}
- Typography: {font sizes, weights}
- Icons: {list of icons needed}

## Component Hierarchy
**Parent**: {parent_component} - provides {data/callbacks}
**Children**: {child_components} - receive {props}
**Siblings**: {related_components}

## Data Flow
```
Parent Component
  ↓ (props: data, callbacks)
Current Component
  ↓ (props: filtered data)
Child Components
```

## TDD Test Cases

### Test Case 1: Component Renders
```typescript
import { render, screen } from '@testing-library/react';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  it('should render with required props', () => {
    render(<ComponentName prop1="value" />);
    expect(screen.getByRole('...')).toBeInTheDocument();
  });
});
```

### Test Case 2: User Interaction
```typescript
it('should handle click event', async () => {
  const mockHandler = jest.fn();
  render(<ComponentName onClick={mockHandler} />);
  
  const button = screen.getByRole('button');
  await userEvent.click(button);
  
  expect(mockHandler).toHaveBeenCalledWith(expectedData);
});
```

### Test Case 3: State Management
```typescript
it('should update state on input change', async () => {
  render(<ComponentName />);
  
  const input = screen.getByRole('textbox');
  await userEvent.type(input, 'test value');
  
  expect(input).toHaveValue('test value');
});
```

### Test Case 4: API Integration
```typescript
it('should fetch and display data', async () => {
  const mockData = { ... };
  global.fetch = jest.fn(() =>
    Promise.resolve({
      ok: true,
      json: async () => mockData,
    })
  ) as jest.Mock;
  
  render(<ComponentName />);
  
  await waitFor(() => {
    expect(screen.getByText(mockData.title)).toBeInTheDocument();
  });
});
```

### Test Case 5: Error Handling
```typescript
it('should display error message on API failure', async () => {
  global.fetch = jest.fn(() =>
    Promise.reject(new Error('API Error'))
  ) as jest.Mock;
  
  render(<ComponentName />);
  
  await waitFor(() => {
    expect(screen.getByText(/error/i)).toBeInTheDocument();
  });
});
```

### Test Case 6: Loading State
```typescript
it('should show loading spinner while fetching', () => {
  render(<ComponentName />);
  expect(screen.getByRole('progressbar')).toBeInTheDocument();
});
```

## Accessibility Requirements

### ARIA Attributes
- `role`: {appropriate role}
- `aria-label`: {descriptive label}
- `aria-labelledby`: {reference to label element}
- `aria-describedby`: {reference to description}
- `aria-expanded`: {for expandable components}
- `aria-selected`: {for selectable items}

### Keyboard Navigation
- `Tab`: Navigate to component
- `Enter/Space`: Activate button/checkbox
- `Escape`: Close modal/dismiss
- `Arrow keys`: Navigate between items

### Screen Reader Support
- Meaningful text for all interactive elements
- Live regions for dynamic content updates
- Focus management after interactions
- Announced loading/error states

### Focus Management
```typescript
const inputRef = useRef<HTMLInputElement>(null);

useEffect(() => {
  // Auto-focus on mount or error
  if (error) {
    inputRef.current?.focus();
  }
}, [error]);
```

## Performance Considerations

### Memoization
```typescript
const memoizedValue = useMemo(() => 
  expensiveCalculation(data),
  [data]
);

const memoizedCallback = useCallback(() => {
  doSomething(value);
}, [value]);
```

### Code Splitting
```typescript
// Lazy load heavy components
const HeavyComponent = lazy(() => import('./HeavyComponent'));
```

### Optimization Tips
- Use React.memo for pure presentational components
- Avoid inline function definitions in render
- Debounce input handlers for search/filter
- Virtualize long lists

## Related Files

### Implementation
- **Target file**: `src/components/{module}/{ComponentName}.tsx`
- **Styles**: `src/components/{module}/{ComponentName}.module.css` OR styled-components

### Testing
- **Test file**: `src/components/{module}/{ComponentName}.test.tsx`
- **Test utilities**: `src/test-utils/` (custom renders, mocks)

### Documentation
- **Storybook**: `src/components/{module}/{ComponentName}.stories.tsx`
- **README**: Component usage documentation

### Dependencies
- **Parent component**: {parent_file_path}
- **Child components**: {list of child component files}
- **Hooks**: {custom hook files}
- **Types**: {type definition files}
- **API client**: {API service files}

## Success Criteria

### Functional Requirements
- ✅ All props work as specified
- ✅ State updates correctly
- ✅ Events trigger expected behavior
- ✅ API calls successful
- ✅ Error handling works

### Quality Requirements
- ✅ Test coverage ≥80%
- ✅ No TypeScript errors
- ✅ No accessibility violations
- ✅ Passes linting
- ✅ Storybook story exists

### Design Requirements
- ✅ Matches wireframe design
- ✅ Responsive on all breakpoints
- ✅ Follows design system
- ✅ Animations smooth
- ✅ Loading states clear

## Dependencies on Other Tasks
{list of task IDs this component depends on}

## Tasks Depending on This
{list of task IDs that depend on this component}
</subagent_task>
```

**Wait for all subagents in current sub-batch to complete before proceeding to next sub-batch.**

### 4. Verify Context Generation

After each sub-batch completes:
```
✓ Sub-batch {i} complete: {count}/{count} contexts generated

Verification:
  - frontend_task_008: ✓ Context file created
  - frontend_task_009: ✓ Context file created
  - frontend_task_010: ✓ Context file created
  ...
```

### 5. Update Task Status

Use Python script to mark tasks as context-generated:

```python
from task_registry_manager import TaskRegistryManager

task_mgr = TaskRegistryManager()

# Update all tasks in batch
completed_tasks = [
    "frontend_task_008",
    "frontend_task_009",
    # ... all tasks in sub-batch
]

for task_id in completed_tasks:
    task_mgr.update_task_status(
        task_id=task_id,
        status="context_ready"  # Ready for development
    )
```

### 6. Summary Output

After ALL sub-batches complete:

```
=== Frontend Context Generation Summary ===

Total component tasks: 47
Sub-batches processed: 5

Sub-batch Results:
  Sub-batch 1: 10/10 contexts ✓
  Sub-batch 2: 10/10 contexts ✓
  Sub-batch 3: 10/10 contexts ✓
  Sub-batch 4: 10/10 contexts ✓
  Sub-batch 5: 7/7 contexts ✓

✓ ALL contexts generated: 47/47 (100% coverage)

Context files created in: .claude_tasks/contexts/
  - frontend_task_008_context.md (LoginForm)
  - frontend_task_009_context.md (EmailInput)
  - frontend_task_010_context.md (PasswordInput)
  ... (47 total)

Updated task statuses: 47 tasks → "context_ready"

✓ Frontend components ready for TDD development

Next command: /generate-backend-contexts OR /build-deps-fullstack
```

## Important Rules

### Parallel Execution
- ✅ REQUIRED: Create ALL subagents in sub-batch simultaneously
- ✅ REQUIRED: Process ALL sub-batches (no skipping)
- ✅ REQUIRED: 100% coverage across all component tasks
- ❌ FORBIDDEN: Processing tasks one by one
- ❌ FORBIDDEN: Skipping sub-batches
- ❌ FORBIDDEN: Partial processing

### Verification
- Count total component tasks before starting
- Calculate number of sub-batches needed
- Track progress after each sub-batch
- Verify 100% completion at end

### Quality
- All context files must follow template format
- Include all required sections
- Provide comprehensive TDD test cases
- Include accessibility requirements
- Reference correct wireframe files

## Edge Cases

### No Tasks Need Context
```
No component tasks found needing context generation.
All tasks either:
  - Already have contexts (status = "context_ready")
  - Not yet decomposed to component level
  
Recommendation: Run /continue-decompose-frontend first
```

### Partial Generation
```
If interrupted mid-batch:
- Already generated contexts remain valid
- Re-run command to generate remaining
- Command automatically skips tasks with status = "context_ready"
```

### Missing Design References
```
Warning: frontend_task_XXX references missing wireframe file
  Expected: designs/wireframes/page.md
  Action: Creating context with available information
  TODO: Update context after wireframe is added
```
