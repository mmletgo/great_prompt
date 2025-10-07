---
description: Retry failed development tasks
argument-hint: [task_ids...]
---

# Retry Failed Tasks

## Your Task
Retry all tasks that failed during development with enhanced context.

## Prerequisites
Check that `development_phase.failed_tasks` is not empty.

## Steps

### 1. Load Failed Tasks
From `state.json`, get `development_phase.failed_tasks` array.

For each failed task:
- Load task from task_registry.json
- Load error information (if logged)

### 2. Enhance Context
For each failed task:
- Read original context file
- Add section: "## Previous Failure Analysis"
- Include error message and potential fixes
- Add more test cases if needed

### 3. Retry with TDD Developer
For each failed task:
```
Create a TDDDeveloper subagent to retry task_XXX.

<subagent_task>
Agent: @tdd-developer
Input:
- Task ID: task_XXX
- Context file: .claude_tasks/contexts/task_XXX_context.md (enhanced)
- Previous error: [error details]
- Retry attempt: [N]

Note: This is a retry. Pay special attention to the previous failure.

[Same TDD workflow as before]
</subagent_task>
```

### 4. Update Results
For each retry:
- If success: move from failed_tasks to completed_tasks
- If failed again: keep in failed_tasks, increment retry count

### 5. Output Summary
```
Retrying [N] failed tasks...

Retry task_XXX (attempt [N]/3):
  [Result]

---
Retry Summary:
  Succeeded: [N]
  Still failed: [N]

[If still have failures:]
Remaining failed tasks:
- task_XXX: [error]

Recommendation: Manual review required for remaining failures.
```

## Important Rules
- Maximum 3 retry attempts per task
- Enhance context with previous error info
- If all retries fail, mark for manual review
