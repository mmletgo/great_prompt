# Integration Task Support

## 概述

脚本现在支持完整的三层开发和整合流程:
- **Level 3**: 叶子节点(组件/函数) - 直接实现
- **Level 2**: 中间节点(页面/服务) - 整合子节点
- **Level 1**: 根节点(模块) - 最终组装

## 新增功能

### 1. TaskRegistryManager 新方法

#### `get_integration_ready_tasks(level, category)`
获取准备好进行整合的任务(所有子任务已完成)。

```python
from task_registry_manager import TaskRegistryManager

manager = TaskRegistryManager()

# 获取所有可以整合的 Level 2 前端页面
ready_pages = manager.get_integration_ready_tasks(level=2, category="frontend")

# 获取所有可以整合的 Level 2 后端服务
ready_services = manager.get_integration_ready_tasks(level=2, category="backend")

# 获取所有可以整合的 Level 1 模块
ready_modules = manager.get_integration_ready_tasks(level=1)
```

**返回值**: 所有子任务都已完成的任务列表

**判断逻辑**:
- 递归检查所有子孙任务
- 所有子孙任务的 `status == "completed"` 才返回此任务
- 跳过已完成或进行中的任务

---

### 2. ProjectManager 新方法

#### `complete_integration_task_full(task_id, ...)`
完成一个整合任务(Level 1 或 2),更新两个文件。

```python
from utils import ProjectManager

manager = ProjectManager()

# 整合 Level 2 页面 (组装组件)
manager.complete_integration_task_full(
    task_id="1.1",  # LoginPage
    integration_file="src/pages/auth/LoginPage.tsx",
    test_file="src/pages/auth/LoginPage.integration.test.tsx",
    test_coverage=88,
    duration_minutes=25.0
)

# 整合 Level 2 服务 (组装函数)
manager.complete_integration_task_full(
    task_id="2.1",  # AuthService
    integration_file="src/services/auth/AuthService.ts",
    test_file="src/services/auth/AuthService.integration.test.ts",
    test_coverage=92,
    duration_minutes=35.0
)

# 整合 Level 1 模块 (组装页面/服务)
manager.complete_integration_task_full(
    task_id="1",  # Auth Module
    integration_file="src/modules/auth/index.tsx",
    test_file="src/modules/auth/e2e.test.tsx",
    test_coverage=85,
    duration_minutes=45.0
)
```

**验证**:
- 检查任务是否存在
- 验证任务是 Level 1 或 2
- 确认所有子任务已完成(递归检查)
- 如果有未完成的子任务,抛出 `ValueError`

**更新**:
- `task_registry.json`: 设置 status="completed", 记录文件和覆盖率
- `state.json`: 添加到 completed_tasks 数组

#### `get_integration_ready_tasks(level, category)`
便捷方法,委托给 TaskRegistryManager。

```python
manager = ProjectManager()

# 检查哪些页面可以整合
ready = manager.get_integration_ready_tasks(level=2, category="frontend")
print(f"Ready for integration: {len(ready)} pages")
```

---

## 完整工作流示例

### 场景: 开发一个认证模块

```
树结构:
  1 (Auth Module) - Level 1
    ├─ 1.1 (LoginPage) - Level 2
    │   ├─ 1.1.1 (LoginForm) - Level 3 ✓
    │   ├─ 1.1.2 (SocialButtons) - Level 3 ✓
    │   └─ 1.1.3 (LoginHeader) - Level 3 ✓
    ├─ 1.2 (RegisterPage) - Level 2
    │   ├─ 1.2.1 (RegisterForm) - Level 3 ✓
    │   └─ 1.2.2 (TermsCheckbox) - Level 3 ✓
    └─ 1.3 (ResetPage) - Level 2
        └─ 1.3.1 (ResetForm) - Level 3 ✓
```

### Phase 1: Level 3 实现 (组件开发)

```python
from utils import ProjectManager

manager = ProjectManager()

# 完成所有 Level 3 组件
components = [
    ("1.1.1", "LoginForm.tsx", 95),
    ("1.1.2", "SocialButtons.tsx", 90),
    ("1.1.3", "LoginHeader.tsx", 88),
    ("1.2.1", "RegisterForm.tsx", 92),
    ("1.2.2", "TermsCheckbox.tsx", 85),
    ("1.3.1", "ResetForm.tsx", 87),
]

for task_id, file, coverage in components:
    manager.complete_task_full(
        task_id=task_id,
        implementation_file=f"src/components/auth/{file}",
        test_file=f"src/components/auth/{file.replace('.tsx', '.test.tsx')}",
        test_coverage=coverage,
        duration_minutes=12.0
    )
    print(f"✓ Completed {task_id}: {file}")

print("\n✓ Phase 1 complete: All components implemented")
```

### Phase 2: Level 2 整合 (页面组装)

```python
# 检查哪些页面可以整合
ready_pages = manager.get_integration_ready_tasks(level=2, category="frontend")

print(f"\n{len(ready_pages)} pages ready for integration:")
for page in ready_pages:
    children = [c["id"] for c in page["subtasks"]]
    print(f"  - {page['id']} ({page['title']}): {', '.join(children)}")

# 整合所有页面
pages = [
    ("1.1", "LoginPage", ["1.1.1", "1.1.2", "1.1.3"]),
    ("1.2", "RegisterPage", ["1.2.1", "1.2.2"]),
    ("1.3", "ResetPage", ["1.3.1"]),
]

for page_id, page_name, children in pages:
    print(f"\nIntegrating {page_id} ({page_name}):")
    print(f"  Children: {', '.join(children)}")
    
    manager.complete_integration_task_full(
        task_id=page_id,
        integration_file=f"src/pages/auth/{page_name}.tsx",
        test_file=f"src/pages/auth/{page_name}.integration.test.tsx",
        test_coverage=88,
        duration_minutes=25.0
    )
    print(f"  ✓ Page {page_id} integrated")

print("\n✓ Phase 2 complete: All pages integrated")
```

### Phase 3: Level 1 整合 (模块组装)

```python
# 检查模块是否可以整合
ready_modules = manager.get_integration_ready_tasks(level=1, category="frontend")

if ready_modules:
    module = ready_modules[0]
    print(f"\nModule {module['id']} ready for integration:")
    children = [c["id"] for c in module["subtasks"]]
    print(f"  Children (pages): {', '.join(children)}")
    
    manager.complete_integration_task_full(
        task_id=module["id"],
        integration_file="src/modules/auth/index.tsx",
        test_file="src/modules/auth/e2e.test.tsx",
        test_coverage=85,
        duration_minutes=45.0
    )
    print(f"  ✓ Module {module['id']} integrated")
    
    print("\n✓ Phase 3 complete: Module ready for deployment")
else:
    print("\n⏳ Module not ready yet (some pages incomplete)")
```

---

## 错误处理

### 场景 1: 子任务未完成

```python
# 尝试整合页面,但有子组件还没完成
try:
    manager.complete_integration_task_full(
        task_id="1.1",
        integration_file="src/pages/auth/LoginPage.tsx"
    )
except ValueError as e:
    print(f"Error: {e}")
    # 输出: Cannot complete integration task 1.1: 
    #       Incomplete children: ['1.1.2', '1.1.3']
```

**解决方案**: 先完成所有子任务,再整合父任务。

### 场景 2: 错误的任务层级

```python
# 尝试对 Level 3 任务调用整合方法
try:
    manager.complete_integration_task_full(
        task_id="1.1.1",  # Level 3 component
        integration_file="..."
    )
except ValueError as e:
    print(f"Error: {e}")
    # 输出: Task 1.1.1 is Level 3. Integration only applies to Level 1 or 2.
```

**解决方案**: Level 3 任务使用 `complete_task_full()`,不用 `complete_integration_task_full()`。

---

## CLI 使用

### 命令行检查整合就绪状态

```bash
# 检查哪些 Level 2 前端页面可以整合
python task_registry_manager.py get_integration_ready_tasks --level 2 --category frontend

# 检查哪些 Level 2 后端服务可以整合
python task_registry_manager.py get_integration_ready_tasks --level 2 --category backend

# 检查哪些 Level 1 模块可以整合
python task_registry_manager.py get_integration_ready_tasks --level 1
```

---

## 测试示例

运行集成示例脚本:

```bash
# 运行所有示例
python integration_examples.py

# 运行特定示例
python integration_examples.py 1  # 检查整合就绪状态
python integration_examples.py 2  # 整合页面
python integration_examples.py 3  # 整合服务
python integration_examples.py 4  # 整合模块
python integration_examples.py 5  # 完整工作流
python integration_examples.py 6  # 错误处理
```

---

## 与命令文档的集成

这些新方法应该在以下命令中使用:

### `parallel-dev-fullstack.md`

**Level 2 整合波次**:
```markdown
Wave 4: Level 2 Integration (Backend Services)

<subagent_task>
Agent: @backend-integrator
Input: Task 2.1 (AuthService)

After integration complete:
```python
manager.complete_integration_task_full(
    task_id="2.1",
    integration_file="src/services/auth/AuthService.ts",
    test_file="src/services/auth/AuthService.integration.test.ts",
    test_coverage=92
)
```
</subagent_task>
```

**Level 1 整合波次**:
```markdown
Wave 6: Level 1 Integration (Frontend Modules)

<subagent_task>
Agent: @frontend-integrator
Input: Task 1 (Auth Module)

After integration complete:
```python
manager.complete_integration_task_full(
    task_id="1",
    integration_file="src/modules/auth/index.tsx",
    test_file="src/modules/auth/e2e.test.tsx",
    test_coverage=85
)
```
</subagent_task>
```

---

## 总结

**新增功能**:
1. ✅ `get_integration_ready_tasks()` - 查找可整合任务
2. ✅ `complete_integration_task_full()` - 完成整合任务
3. ✅ 递归子任务完成检查
4. ✅ 完整的错误验证

**支持的整合场景**:
- ✅ Level 2 前端: 组件 → 页面
- ✅ Level 2 后端: 函数 → 服务
- ✅ Level 1 前端: 页面 → 模块
- ✅ Level 1 后端: 服务 → 模块

**工作流完整性**:
- ✅ Level 3 实现 (叶子节点)
- ✅ Level 2 整合 (中间节点)
- ✅ Level 1 整合 (根节点)
- ✅ 自底向上的完整流程

现在脚本完全支持三层开发和整合的完整生命周期! 🎉
