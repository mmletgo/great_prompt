---
description: Generate low-fidelity wireframes from user flows
---

# Generate Wireframes

## Your Task
Generate detailed low-fidelity wireframes for each page/screen identified in the user flows.

## Prerequisites
Check that the following files exist:
- `designs/user-flows.md` - User flow diagrams
- `docs/front-end-spec.md` - UX design specifications (if available)

Check state:
- `design_phase.status` should be "user_flows_completed"

## Steps

### 1. Extract Pages from User Flows
Read `designs/user-flows.md` and identify all unique pages/screens.

Create a list of pages, for example:
- Login Page
- Dashboard
- User Profile
- Settings Page
- etc.

### 2. Create Wireframe Directory
Ensure `designs/wireframes/` directory exists.

### 3. Generate Wireframes for All Pages

**CRITICAL - NO PARTIAL PROCESSING**:
- You MUST create WireframeDesigner subagents for EVERY SINGLE page from step 1
- Count total pages FIRST, then verify you created exactly that many subagents
- DO NOT split into "first batch" / "core pages" / "remaining pages"
- DO NOT process only "important" pages - ALL pages are equally important
- If you have 20 pages → create 20 subagents simultaneously
- If you cannot handle all pages at once, that indicates a system error

**Verification Required**:
1. Count pages: `page_count = total unique pages from user-flows.md`
2. Create subagents: MUST equal `page_count`
3. Output: "Creating {page_count} WireframeDesigner subagents in parallel..."
4. Confirm: "✓ All {page_count} wireframe files generated"

**Important**: Create subagent tasks for ALL pages at once to enable parallel processing.

#### 3.1 Create All WireframeDesigner Subagents in Parallel

For the complete list of pages from step 1, create subagent tasks for all pages simultaneously:

```
Create WireframeDesigner subagents for ALL pages in parallel.

For each page in the list:

<subagent_task>
Agent: @wireframe-designer
Input:
- Page name: [PageName]
- User flows: designs/user-flows.md
- UX spec: docs/front-end-spec.md
- Context: How this page appears in user flows

Task:
1. Identify page purpose and user goals
2. List all UI components needed
3. Define layout structure (header, nav, content, footer)
4. Specify interactive elements (buttons, forms, etc.)
5. Include states (loading, error, empty, success)
6. Add annotations for behavior and interactions
7. Use ASCII art or Mermaid for wireframe visualization
8. Consider responsive design (mobile, tablet, desktop)

Output format: Create designs/wireframes/[page-name].md with:
# [Page Name] - Wireframe

## Page Overview
[Purpose and context]

## User Goals
- Goal 1
- Goal 2

## Layout Structure
[ASCII art or Mermaid diagram showing layout]

## Components
### Component 1
- Type: [button/form/card/etc]
- Position: [location]
- Behavior: [interaction]
- States: [default/hover/active/disabled]

## Responsive Breakpoints
### Desktop (>1024px)
[Layout description]

### Tablet (768-1024px)
[Layout adjustments]

### Mobile (<768px)
[Mobile layout]

## Interaction Notes
- [Key interactions]
- [Transitions to other pages]
- [API calls triggered]

## Edge Cases
- Loading state
- Error state
- Empty state
- Success feedback
</subagent_task>
```

**Example**: If you have 8 pages (Login, Signup, Dashboard, Profile, Settings, Products, Cart, Checkout), create 8 subagent tasks simultaneously:
- Subagent 1: Login Page → designs/wireframes/login-page.md
- Subagent 2: Signup Page → designs/wireframes/signup-page.md
- Subagent 3: Dashboard → designs/wireframes/dashboard.md
- Subagent 4: Profile → designs/wireframes/profile.md
- Subagent 5: Settings → designs/wireframes/settings.md
- Subagent 6: Products → designs/wireframes/products.md
- Subagent 7: Cart → designs/wireframes/cart.md
- Subagent 8: Checkout → designs/wireframes/checkout.md

**Wait for ALL subagents to complete before proceeding to step 4.**

### 4. Validate Wireframes Quality

After all wireframes are generated, perform comprehensive validation:

#### 5.1 Design Consistency Check
For each wireframe file, verify:

**Component Consistency**:
- [ ] All buttons follow the same naming convention (e.g., PrimaryButton, SecondaryButton)
- [ ] Form components use consistent field types (TextInput, SelectDropdown, etc.)
- [ ] Card/Container components have consistent structure
- [ ] Navigation elements match across pages
- [ ] Color/styling references match front-end-spec.md

**Layout Consistency**:
- [ ] Header/Navigation placement is consistent
- [ ] Footer placement is consistent
- [ ] Content area structure follows patterns
- [ ] Spacing/padding annotations are uniform

**State Coverage**:
- [ ] Each interactive component defines all states (default, hover, active, disabled, loading, error)
- [ ] Page-level states documented (loading, error, empty, success)
- [ ] Transition states specified (page-to-page navigation)

#### 5.2 Completeness Check
Verify each wireframe includes:
- [ ] Page Overview (purpose and context)
- [ ] User Goals section
- [ ] Layout Structure (ASCII art or Mermaid diagram)
- [ ] Components list with specifications
- [ ] Responsive breakpoints (Desktop, Tablet, Mobile)
- [ ] Interaction notes
- [ ] Edge cases

#### 5.3 Cross-Reference Validation
- [ ] All pages mentioned in user-flows.md have wireframes
- [ ] All components referenced follow front-end-spec.md design system
- [ ] Navigation links match actual page files
- [ ] API interaction notes align with backend requirements (if specified)

#### 5.4 Naming Convention Check
- [ ] All file names use lowercase-with-hyphens.md format
- [ ] File names match page titles (normalized)
- [ ] No duplicate file names
- [ ] INDEX.md exists and is properly formatted

#### 5.5 Generate Validation Report
Create `designs/WIREFRAME_VALIDATION.md`:
```markdown
# Wireframes Validation Report

Generated: [TIMESTAMP]

## Summary
- Total wireframes: [N]
- Passed validation: [M]
- Issues found: [X]

## Design Consistency
✓ Component naming: Consistent
✓ Layout structure: Consistent
✓ State coverage: Complete
⚠ [Issue description if any]

## Completeness
✓ All required sections present
⚠ [Missing sections in specific files]

## Cross-References
✓ User flows coverage: 100%
✓ Design system compliance: [percentage]
⚠ [Mismatches if any]

## Issues to Fix
1. [Issue 1 - file: designs/wireframes/page-x.md]
2. [Issue 2 - file: designs/wireframes/page-y.md]

## Recommendations
- [Recommendation 1]
- [Recommendation 2]

## Status
[PASSED / NEEDS REVIEW / FAILED]
```

#### 4.6 Address Validation Issues
If issues found:
1. List all issues clearly
2. Re-generate problematic wireframes with corrections
3. Re-run validation
4. Repeat until all issues resolved

### 5. Update State
When all wireframes complete and pass validation:
```json
{
  "design_phase": {
    "status": "completed",
    "wireframes_generated": true,
    "wireframes_count": [N],
    "wireframes_directory": "designs/wireframes/",
    "validation_status": "passed",
    "validation_report": "designs/WIREFRAME_VALIDATION.md"
  },
  "decomposition_phase": {
    "status": "not_started"
  }
}
```

### 6. Generate Wireframes Index
Create `designs/WIREFRAMES_INDEX.md`:
```markdown
# Wireframes Index

## All Pages ([N] total)

### Authentication
- [Login](./wireframes/login-page.md)
- [Signup](./wireframes/signup-page.md)

### Dashboard
- [Main Dashboard](./wireframes/dashboard.md)

### [Category]
- [Page Name](./wireframes/page-name.md)

## Design System Reference
See: docs/front-end-spec.md

## User Flows Reference
See: user-flows.md

## Validation Report
See: WIREFRAME_VALIDATION.md
```

### 7. Output Summary

### 7. Output Summary
Print:
```
Generating wireframes for [N] pages...

=== Page Count Verification ===
Pages identified from user-flows.md: [N]
WireframeDesigner subagents to create: [N]
✓ Count verified - proceeding with parallel generation

Creating [N] wireframe-designer subagents in parallel...
✓ [Page 1]: designs/wireframes/page-1.md
✓ [Page 2]: designs/wireframes/page-2.md
✓ [Page 3]: designs/wireframes/page-3.md
...
✓ [Page N]: designs/wireframes/page-n.md

=== Wireframe Generation Complete ===
Total pages: [N]
✓ Generated: [N]
✗ Failed: [0]
✓ Coverage: 100% (all pages processed)

=== Validation Results ===
Running comprehensive validation...

Component Consistency: ✓ PASSED
Layout Consistency: ✓ PASSED
State Coverage: ✓ PASSED
Completeness Check: ✓ PASSED
Cross-References: ✓ PASSED
Naming Conventions: ✓ PASSED

Issues found: [X]
[List any issues]

Validation status: [PASSED / NEEDS REVIEW]

Generated files:
- designs/wireframes/ ([N] wireframe files - only .md files for pages)
- designs/WIREFRAMES_INDEX.md (index file at designs/ level)
- designs/WIREFRAME_VALIDATION.md (validation report at designs/ level)

Design phase: completed (status changed from user_flows_completed to completed)

Next command: /init-decompose-frontend
```

## Important Rules
- **Create ALL wireframe subagents at once for maximum parallelization**
- Subagents process pages in parallel (no sequential processing)
- Each wireframe must be in a separate file in `designs/wireframes/`
- Use consistent naming: lowercase-with-hyphens.md
- **Index and validation files go in `designs/` (not `designs/wireframes/`)**
- Always create WIREFRAMES_INDEX.md and WIREFRAME_VALIDATION.md after completion
- **Always run validation after generation**
- Include all UI states (loading, error, empty, success)
- Fix validation issues before marking phase complete
- All components must reference design system from front-end-spec.md
- Component names must be consistent across all wireframes
