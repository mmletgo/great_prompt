# 设计驱动的全栈产品开发系统 - 使用指南

> v2.0 - 从 PRD 到代码的完整工作流

## 📦 文件结构总览

```
your-project/
├── CLAUDE.md                                  # 项目主配置
├── docs/                                      # 设计文档目录
│   ├── prd.md                                # 产品需求文档
│   ├── fullstack-architecture.md             # 系统架构文档
│   ├── front-end-spec.md                     # 前端技术规格
│   └── back-end-spec.md                      # 后端技术规格
├── designs/                                   # 设计产物目录
│   ├── user-flows.md                         # 用户流程图（Mermaid）
│   └── wireframes/                           # 线框图目录
│       ├── INDEX.md                          # 线框图索引
│       ├── login-page.md                     # 登录页线框图
│       ├── register-page.md                  # 注册页线框图
│       └── ...                               # 其他页面线框图
├── .claude/
│   ├── commands/                              # 10个工作流命令
│   │   ├── init-design.md                    # 生成用户流程
│   │   ├── generate-wireframes.md            # 生成线框图
│   │   ├── init-decompose-frontend.md        # 前端拆分初始化
│   │   ├── continue-decompose-frontend.md    # 前端继续拆分
│   │   ├── init-decompose-backend.md         # 后端拆分初始化
│   │   ├── continue-decompose-backend.md     # 后端继续拆分
│   │   ├── build-deps-fullstack.md           # 全栈依赖分析
│   │   ├── parallel-dev-fullstack.md         # 全栈并行开发
│   │   ├── status.md                         # 查看状态
│   │   └── retry.md                          # 重试失败任务
│   └── agents/                                # 8个专业化 Agent
│       ├── user-flow-designer.md             # 用户流程设计师
│       ├── wireframe-designer.md             # 线框图设计师
│       ├── frontend-decomposer.md            # 前端拆分器
│       ├── backend-decomposer.md             # 后端拆分器
│       ├── context-generator.md              # 上下文生成器
│       ├── fullstack-dependency-analyzer.md  # 全栈依赖分析器
│       ├── frontend-developer.md             # 前端TDD开发者
│       └── backend-developer.md              # 后端TDD开发者
└── .claude_tasks/                             # 自动生成的工作目录
    ├── state.json                             # 全局状态（设计/前端/后端阶段）
    ├── task_registry.json                     # 任务清单 + 跨栈依赖图
    └── contexts/                              # 每个任务的详细上下文
        ├── 1_1_1_context.md                   # 前端组件上下文 (ID: 1.1.1)
        ├── 2_1_1_context.md                   # 后端函数上下文 (ID: 2.1.1)
        └── ...
```

## 🚀 快速开始

### 第一步：准备项目

1. **复制配置文件**到你的项目根目录：
   - `CLAUDE.md`
   - `.claude/commands/` 目录下的所有 10 个命令文件
   - `.claude/agents/` 目录下的所有 8 个 agent 文件

2. **准备设计文档**（推荐，也可以直接在命令中描述）：
   ```bash
   mkdir docs
   mkdir designs
   ```
   
   在 `docs/` 目录中创建：
   - `prd.md` - 产品需求文档（必需）
   - `fullstack-architecture.md` - 系统架构（可选）
   - `front-end-spec.md` - 前端技术规格（可选）
   - `back-end-spec.md` - 后端技术规格（可选）

### 第二步：执行完整工作流

#### 阶段0️⃣：设计阶段（Design Phase）

**步骤1：生成用户流程图**
```
/init-design
```

**期望输出**：
```
✓ Read PRD from docs/prd.md
✓ Read architecture from docs/fullstack-architecture.md
✓ Read UX spec from docs/front-end-spec.md
✓ Created user-flow-designer subagent
✓ Generated designs/user-flows.md with Mermaid diagrams
  - User Registration Flow
  - Login Flow
  - Product Browsing Flow
  - Password Reset Flow

Next command: /generate-wireframes
```

**步骤2：生成线框图**
```
/generate-wireframes
```

**期望输出**：
```
✓ Read user flows from designs/user-flows.md
✓ Read front-end spec from docs/front-end-spec.md
✓ Created wireframe-designer subagent
✓ Generated designs/wireframes/ directory
✓ Created wireframe files:
  - designs/wireframes/registration-page.md
  - designs/wireframes/login-page.md
  - designs/wireframes/product-list-page.md
  - designs/wireframes/dashboard-page.md
✓ Created designs/wireframes/INDEX.md

Design phase completed!
Next command: /init-decompose-frontend
```

---

#### 阶段1️⃣：前端拆分（Frontend Decomposition）

**步骤3：初始化前端任务拆分**
```
/init-decompose-frontend
```

**期望输出**：
```
✓ Created .claude_tasks/ directory structure
✓ Initialized state.json with frontend_decomposition phase
✓ Created task_registry.json
✓ Created 4 frontend module-level tasks:
  - frontend_001: User Auth Module
  - frontend_002: Product Display Module
  - frontend_003: Shopping Cart Module
  - frontend_004: Shared Components Module

Checkpoint saved: frontend_004
Status: frontend_decomposition_phase = in_progress

Next command: /continue-decompose-frontend
```

**步骤4：继续前端拆分（重复直到完成）**
```
/continue-decompose-frontend
```

**输出示例**：
```
Resuming from checkpoint: frontend_004
Creating frontend-decomposer subagent...

✓ Decomposed frontend_001 (Module) into:
  - frontend_005: LoginPage (Page)
  - frontend_006: RegisterPage (Page)
  - frontend_007: ResetPasswordPage (Page)

✓ Decomposed frontend_005 (Page) into:
  - frontend_008: LoginForm (Component)
  - frontend_009: SocialLoginButtons (Component)
  - frontend_010: LoginHeader (Component)

Processed 3 pages in this batch
Updated checkpoint: frontend_010

Next command: /continue-decompose-frontend (until all components defined)
```

重复执行直到看到：
```
✓ All frontend tasks decomposed to component-level!
✓ Total: 45 frontend components
  - 12 Page components
  - 33 Sub-components

frontend_decomposition_phase.status = completed
Next command: /init-decompose-backend
```

---

#### 阶段2️⃣：后端拆分（Backend Decomposition）

**步骤5：初始化后端任务拆分**
```
/init-decompose-backend
```

**期望输出**：
```
✓ Initialized backend_decomposition phase in state.json
✓ Created 5 backend module-level tasks:
  - backend_001: User Service Module
  - backend_002: Product Service Module
  - backend_003: Order Service Module
  - backend_004: Payment Service Module
  - backend_005: Validation Layer

Checkpoint saved: backend_005
Status: backend_decomposition_phase = in_progress

Next command: /continue-decompose-backend
```

**步骤6：继续后端拆分（重复直到完成）**
```
/continue-decompose-backend
```

**输出示例**：
```
Resuming from checkpoint: backend_005
Creating backend-decomposer subagent...

✓ Decomposed backend_001 (Module) into:
  - backend_006: UserService (Service)
  - backend_007: AuthService (Service)

✓ Decomposed backend_006 (Service) into:
  - backend_008: register_user (API Layer)
  - backend_009: login_user (API Layer)
  - backend_010: validate_user_data (Service Layer)
  - backend_011: create_user_record (Repository Layer)
  - backend_012: hash_password (Utility Layer)

Processed 2 services in this batch
Updated checkpoint: backend_012

Next command: /continue-decompose-backend (until all functions defined)
```

重复执行直到看到：
```
✓ All backend tasks decomposed to function-level!
✓ Total: 68 backend functions across 5 layers
  - API Layer: 15 functions
  - Service Layer: 22 functions
  - Repository Layer: 18 functions
  - Validation Layer: 8 functions
  - Utility Layer: 5 functions

backend_decomposition_phase.status = completed
Next command: /build-deps-fullstack
```

---

#### 阶段3️⃣：全栈依赖分析（Dependency Analysis）

**步骤7：构建跨栈依赖图**
```
/build-deps-fullstack
```

**期望输出**：
```
✓ Loaded frontend tasks: 45 components
✓ Loaded backend tasks: 68 functions
✓ Created fullstack-dependency-analyzer subagent

Analyzing dependencies...
✓ Frontend component dependencies: 42 edges
✓ Backend function dependencies: 85 edges
✓ Cross-stack API dependencies: 23 edges
  - frontend_008 (LoginForm) → backend_009 (login_api)
  - frontend_015 (ProductCard) → backend_025 (get_product_api)
  - frontend_023 (CheckoutForm) → backend_048 (create_order_api)
  ...

✓ Generated execution waves (topological sort):
  Wave 1: 15 tasks (backend utility + shared frontend components)
  Wave 2: 18 tasks (backend repositories)
  Wave 3: 22 tasks (backend services)
  Wave 4: 15 tasks (backend APIs)
  Wave 5: 8 tasks (frontend basic components)
  Wave 6: 12 tasks (frontend API-dependent components)
  Wave 7: 7 tasks (frontend layout components)
  Wave 8: 3 tasks (integration tests)

✓ Updated task_registry.json with cross_stack_dependency_graph
✓ Ready for full-stack parallel development

Next command: /parallel-dev-fullstack 5
```

---

#### 阶段4️⃣：全栈并行开发（Full-Stack Parallel TDD Development）

**步骤8：执行全栈并行 TDD 开发**
```
/parallel-dev-fullstack 5
```

**输出示例**：
```
Starting full-stack parallel TDD development with 5 workers...

=== Wave 1: Backend Utils + Shared Components ===
Creating 5 developer subagents...
✓ backend_012 (hash_password) - @backend-developer - COMPLETED
✓ backend_015 (validate_email) - @backend-developer - COMPLETED
✓ frontend_030 (Button) - @frontend-developer - COMPLETED
✓ frontend_031 (Input) - @frontend-developer - COMPLETED
✓ frontend_032 (Card) - @frontend-developer - COMPLETED
... (15 tasks total)

=== Wave 2: Backend Repositories ===
Creating 5 developer subagents...
✓ backend_011 (create_user_record) - @backend-developer - COMPLETED
✓ backend_018 (get_user_by_email) - @backend-developer - COMPLETED
✓ backend_024 (create_product) - @backend-developer - COMPLETED
... (18 tasks total)

=== Wave 3: Backend Services ===
... (22 tasks)

=== Wave 4: Backend APIs ===
... (15 tasks)

=== Wave 5: Frontend Basic Components ===
... (8 tasks)

=== Wave 6: Frontend API Components ===
... (12 tasks)

=== Wave 7: Frontend Pages ===
... (7 tasks)

=== Wave 8: Integration Tests ===
... (3 tasks)

========================================
Full-Stack Development Summary
========================================

Backend Development:
  Total functions: 68
  ✓ Completed: 68
  ✗ Failed: 0

Frontend Development:
  Total components: 45
  ✓ Completed: 45
  ✗ Failed: 0

Cross-Stack Integration:
  ✓ All API contracts verified
  ✓ All component dependencies satisfied

Test Coverage:
  Backend: 87%
  Frontend: 82%

Total Time: ~45 minutes

🎉 Full-stack development completed successfully!
```

---

## 📊 实际使用示例

### 场景1：完整电商产品开发

**背景**：开发一个电商网站，包含用户认证、商品浏览、购物车、订单功能

**完整工作流记录**：

```bash
# 第1步：设计阶段
User: /init-design

System: ✓ Generated designs/user-flows.md
Next: /generate-wireframes

User: /generate-wireframes

System: ✓ Generated designs/wireframes/ (8 pages)
Next: /init-decompose-frontend

# 第2步：前端拆分
User: /init-decompose-frontend

System: ✓ Created 5 frontend modules
Next: /continue-decompose-frontend

User: /continue-decompose-frontend

System: ✓ Decomposed to 12 pages
Next: /continue-decompose-frontend

User: /continue-decompose-frontend

System: ✓ All decomposed to 38 components
Next: /init-decompose-backend

# 第3步：后端拆分
User: /init-decompose-backend

System: ✓ Created 6 backend modules
Next: /continue-decompose-backend

User: /continue-decompose-backend

System: ✓ Decomposed to 55 functions
Next: /continue-decompose-backend

User: /continue-decompose-backend

System: ✓ All decomposed (55 functions)
Next: /build-deps-fullstack

# 第4步：依赖分析
User: /build-deps-fullstack

System: ✓ Generated 8 execution waves
✓ Cross-stack dependencies: 18 API calls
Next: /parallel-dev-fullstack 5

# 第5步：并行开发
User: /parallel-dev-fullstack 5

System: [45 minutes later]
✓ 93 tasks completed
✓ 0 failures
Test coverage: Backend 89%, Frontend 85%

# 第6步：验证
User: /status

System: 
Design Phase: ✓ COMPLETED
Frontend Decomposition: ✓ COMPLETED (38 components)
Backend Decomposition: ✓ COMPLETED (55 functions)
Development: ✓ COMPLETED (93/93 tasks)

Project ready for deployment! 🎉
```

---

### 场景2：SaaS 平台核心功能开发

**背景**：开发一个项目管理 SaaS 平台的核心功能（团队管理、项目管理、任务分配）

**工作流记录**：

```bash
User: /init-design

System: ✓ Created user flows for:
  - Team Management Flow
  - Project Creation Flow
  - Task Assignment Flow
  - Dashboard View Flow

User: /generate-wireframes

System: ✓ Generated wireframes for 6 pages:
  - Team Settings Page
  - Project List Page
  - Project Detail Page
  - Task Board Page
  - Member Management Page
  - Dashboard Page

User: /init-decompose-frontend

System: ✓ Created 4 frontend modules

User: /continue-decompose-frontend

System: ✓ Decomposed to 6 pages

User: /continue-decompose-frontend

System: ✓ All decomposed to 28 components
Frontend decomposition complete!

User: /init-decompose-backend

System: ✓ Created 4 backend modules

User: /continue-decompose-backend

System: ✓ Decomposed to 42 functions

User: /continue-decompose-backend

System: ✓ All functions defined (42 total)

User: /build-deps-fullstack

System: ✓ Generated 7 execution waves
✓ Cross-stack: 15 API dependencies

User: /parallel-dev-fullstack 3

System: [30 minutes later]
✓ 70 tasks completed
✓ Backend: 42/42 ✓
✓ Frontend: 28/28 ✓
```

---

### 场景3：移动端 + Web 端双端开发

**背景**：开发一个健身应用，包含 Web 端和移动端（共享后端）

**策略**：先完成后端，再分别开发 Web 和移动端前端

```bash
# 第1阶段：设计阶段（Web + Mobile）
User: /init-design

System: ✓ Generated user flows for both platforms
  - Web: Dashboard, Workout Library, Progress Tracking
  - Mobile: Quick Workout, Stats View, Profile

User: /generate-wireframes

System: ✓ Generated wireframes:
  - designs/wireframes/web/ (5 pages)
  - designs/wireframes/mobile/ (6 pages)

# 第2阶段：后端优先开发
User: /init-decompose-backend

System: ✓ Created 5 backend modules

User: /continue-decompose-backend

System: ✓ All decomposed to 38 functions

User: /build-deps-fullstack

System: ✓ Generated backend-only waves (4 waves)

User: /parallel-dev-fullstack 3

System: ✓ Backend completed (38/38)
Note: Frontend decomposition not started yet

# 第3阶段：Web 前端开发
User: /init-decompose-frontend

System: ✓ Created Web frontend modules (3 modules)

User: /continue-decompose-frontend

System: ✓ All decomposed to 22 components

User: /build-deps-fullstack

System: ✓ Updated dependency graph
✓ Web frontend can now use completed backend APIs

User: /parallel-dev-fullstack 3

System: ✓ Web frontend completed (22/22)

# 第4阶段：Mobile 前端开发（React Native）
# [Similar process for mobile frontend]
```

---

### 场景4：API 优先的微服务开发

**背景**：为现有前端开发新的微服务后端

**工作流**：跳过设计和前端拆分，直接进行后端开发

```bash
# 直接开始后端拆分
User: /init-decompose-backend

System: ✓ Created 3 backend service modules
  - Auth Service
  - Data Service
  - Notification Service

User: /continue-decompose-backend

System: ✓ Decomposed to 25 functions

User: /continue-decompose-backend

System: ✓ All functions defined (25 total)
  API Layer: 8 endpoints
  Service Layer: 10 functions
  Repository Layer: 5 functions
  Utility Layer: 2 functions

User: /build-deps-fullstack

System: ✓ Generated 4 waves (backend only)

User: /parallel-dev-fullstack 5

System: ✓ Backend API development completed
✓ All 8 endpoints have OpenAPI documentation
✓ Test coverage: 91%

# 结果：
# - 完整的 REST API
# - OpenAPI/Swagger 文档
# - 单元测试 + 集成测试
```

---

## 🔧 高级配置

### 批处理大小配置（拆分阶段）

**场景**：控制每次拆分处理的任务数量

批处理大小影响**拆分阶段**的每批处理的任务数量：

**默认配置**：每批处理 5-10 个待拆分任务（在命令内部固定）

**调整方法**：

需要手动编辑命令定义文件：
- `.claude/commands/continue-decompose-frontend.md`
- `.claude/commands/continue-decompose-backend.md`

找到步骤1 "Load State and Get Next Batch"，将 "Get next 5-10 pending tasks" 改为你需要的数量。

**示例修改**：
```markdown
### 1. Load State and Get Next Batch
Read state and task registry.
Get next 5 pending tasks.  # 改为 5（小批次）
# 或
Get next 15 pending tasks.  # 改为 15（大批次）
```

**何时使用小批次（3-5）**：
- Token 限制较紧张
- 需要更细粒度的检查点
- 复杂模块需要更多上下文描述

**何时使用大批次（15+）**：
- 简单、重复性高的模块
- Token 限制充足
- 想要加快拆分速度

---

### 开发阶段并行度配置

开发阶段的并行度由 `parallel-dev-fullstack` 命令的 `workers` 参数控制：

**默认配置**：5 个并行 worker

```bash
# 默认 5 个 worker
/parallel-dev-fullstack

# 自定义 10 个 worker
/parallel-dev-fullstack 10

# 调试时用 3 个 worker
/parallel-dev-fullstack 3

# 高性能服务器用 15 个 worker
/parallel-dev-fullstack 15
```

**Worker 数量建议**：

| 场景 | 推荐 Worker 数 | 原因 |
|------|--------------|------|
| 调试/验证 | 2-3 | 便于观察每个任务输出 |
| 普通开发 | 5 | 平衡速度和可控性 |
| 大型项目 | 8-10 | 充分利用并行能力 |
| 超大项目 | 10-15 | 最大化吞吐量 |

**注意事项**：
- Worker 过多可能导致输出难以追踪
- 受限于 Claude API 的速率限制
- 建议根据实际项目大小调整

---

### 批处理大小 vs Worker 数量对比

| 配置项 | 影响阶段 | 作用 | 默认值 | 调整方式 | 调整场景 |
|--------|---------|------|--------|----------|----------|
| **批处理大小** | 拆分阶段 | 每批处理多少待拆分任务 | 5-10 | 编辑命令定义文件 | Token限制、复杂度 |
| **Worker 数量** | 开发阶段 | 同时执行多少开发任务 | 5 | 命令参数 | 并行度、项目规模 |

**示例**：

```bash
# 场景1：小项目，快速验证
/continue-decompose-frontend       # 默认批次(5-10)
/continue-decompose-backend
/parallel-dev-fullstack 3          # 少量并行

# 场景2：中型项目，标准流程
/continue-decompose-frontend       # 默认批次(5-10)
/continue-decompose-backend
/parallel-dev-fullstack 5          # 默认并行(5)

# 场景3：大型项目，加速开发
# 需编辑命令文件增加批次到 15
/continue-decompose-frontend       # 需修改命令定义
/continue-decompose-backend
/parallel-dev-fullstack 10         # 高并行度

# 场景4：复杂项目，精细控制
# 需编辑命令文件减小批次到 3-5
/continue-decompose-frontend       # 需修改命令定义
/continue-decompose-backend
/parallel-dev-fullstack 8          # 高并行（加速开发）
```

---

## 📈 监控与故障排除

### 使用 /status 命令

```bash
User: /status

System:
========================================
Project Status Summary
========================================

Design Phase: ✓ COMPLETED
  User Flows: designs/user-flows.md
  Wireframes: designs/wireframes/ (8 pages)

Frontend Decomposition: ✓ COMPLETED
  Total Components: 45
  - Modules: 5
  - Pages: 12
  - Components: 28

Backend Decomposition: ✓ COMPLETED
  Total Functions: 68
  - API Layer: 15
  - Service Layer: 22
  - Repository Layer: 18
  - Validation Layer: 8
  - Utility Layer: 5

Dependency Analysis: ✓ COMPLETED
  Execution Waves: 8
  Cross-Stack Dependencies: 23

Development Phase: IN PROGRESS
  Wave 1: ✓ COMPLETED (15/15)
  Wave 2: ✓ COMPLETED (18/18)
  Wave 3: ✓ COMPLETED (22/22)
  Wave 4: IN PROGRESS (8/15)
    ✓ backend_038: create_order_api
    ✓ backend_039: update_order_api
    ⏳ backend_040: delete_order_api (in progress)
    ⏳ backend_041: get_order_details_api (in progress)
    ⏳ backend_042: list_orders_api (in progress)
    ... (3 more pending)
  Wave 5-8: PENDING

Overall Progress: 63/113 tasks (55.8%)
```

---

### 常见问题排查

#### 问题1：拆分进行了很多次还未完成

**症状**：
```
User: /continue-decompose-frontend (第10次)
System: Still 15 pending tasks...
```

**原因**：
- 层级太深（Module → Page → Container → Component → SubComponent）
- 批处理太小

**解决方案**：
```bash
# 检查当前层级
/status

# 如果发现层级过深，手动检查 task_registry.json
# 调整批处理大小
/continue-decompose-frontend 15

# 或直接查看任务状态
cat .claude_tasks/task_registry.json
```

---

#### 问题2：依赖分析报错"检测到循环依赖"

**症状**：
```
User: /build-deps-fullstack
System: ✗ ERROR: Circular dependency detected:
  frontend_008 → backend_009 → backend_015 → frontend_008
```

**原因**：
- 任务设计有循环引用
- 前端组件直接依赖后端，后端又依赖该前端组件

**解决方案**：
```bash
# 1. 检查依赖关系
cat .claude_tasks/task_registry.json

# 2. 重构任务，打破循环
# 通常需要手动编辑 task_registry.json，移除错误的依赖声明

# 3. 重新运行依赖分析
/build-deps-fullstack
```

---

#### 问题3：上下文太长导致命令失败

**症状**：
```
User: /continue-decompose-backend
System: ✗ ERROR: Token limit exceeded (context too long)
```

**原因**：
- 批处理太大（一次处理太多任务）
- 单个任务的上下文太复杂

**解决方案**：
```bash
# 减小批处理大小
/continue-decompose-backend 5

# 或分多次处理
/continue-decompose-backend 3  # 处理3个
/continue-decompose-backend 3  # 再处理3个
```

---

#### 问题4：大量任务开发失败

**症状**：
```
User: /parallel-dev-fullstack 5
System: 
  ✓ Completed: 45
  ✗ Failed: 23
```

**原因**：
- 上下文文件不清晰
- 依赖关系错误
- 测试要求太复杂

**解决方案**：
```bash
# 1. 查看失败任务列表
/status

# 2. 重试失败任务
/retry

# 3. 如果仍然失败，检查具体任务的上下文
cat .claude_tasks/contexts/backend_task_XXX_context.md

# 4. 手动修复上下文后重试
/retry backend_XXX backend_YYY
```

---

#### 问题5：无法从中断恢复

**症状**：
```
User: /continue-decompose-frontend
System: ✗ ERROR: Cannot find checkpoint
```

**原因**：
- state.json 文件损坏
- 检查点丢失

**解决方案**：
```bash
# 1. 检查 state.json
cat .claude_tasks/state.json

# 2. 如果损坏，从备份恢复
cp .claude_tasks/state.json.backup .claude_tasks/state.json

# 3. 如果没有备份，手动重建检查点
# 编辑 state.json，设置正确的 checkpoint_task_id

# 4. 重新执行
/continue-decompose-frontend
```

---

#### 问题6：前端组件找不到对应的后端 API

**症状**：
```
Build warnings:
  frontend_008 (LoginForm) calls POST /api/auth/login
  but no backend endpoint found!
```

**原因**：
- 后端拆分时未创建对应的 API 端点
- API 路径不匹配

**解决方案**：
```bash
# 1. 检查后端任务列表
grep "login" .claude_tasks/task_registry.json

# 2. 如果缺少，需要手动添加后端任务
# 编辑 task_registry.json，添加 backend API 任务

# 3. 重新运行依赖分析
/build-deps-fullstack

# 4. 开发缺失的后端 API
/parallel-dev-fullstack 5
```

---

## 💡 最佳实践

### 1. 需求准备阶段

**✅ DO**：
- 在 `docs/prd.md` 中清晰描述用户需求和功能点
- 提供完整的用户流程描述
- 明确前后端技术栈
- 定义清晰的 API 接口规范

**❌ DON'T**：
- 需求描述模糊不清
- 缺少关键的用户交互流程
- 未定义数据模型和接口

---

### 2. 设计阶段最佳实践

**✅ DO**：
- 仔细审查生成的用户流程图，确保覆盖所有场景
- 检查线框图是否符合 UX 规范
- 确保每个页面的交互元素完整

**❌ DON'T**：
- 跳过设计阶段直接拆分（会导致前端结构混乱）
- 忽略线框图中的设计细节

---

### 3. 拆分阶段最佳实践

**✅ DO**：
- 定期执行 `/status` 检查进度
- 控制根任务数量在 3-8 个
- 确保每个组件/函数有清晰的职责
- 保持合理的层级深度（通常 3 层）

**❌ DON'T**：
- 创建过多根任务（>10 个）
- 拆分层级过深（>4 层）
- 在未完成前一阶段时开始下一阶段

---

### 4. 依赖分析最佳实践

**✅ DO**：
- 确保前后端拆分都已完成
- 仔细检查循环依赖警告
- 验证跨栈 API 依赖的正确性

**❌ DON'T**：
- 忽略循环依赖警告
- 在拆分未完成时运行依赖分析

---

### 5. 开发阶段最佳实践

**✅ DO**：
- 根据项目规模选择合适的 worker 数量
- 保存开发日志以便问题追踪
- 在每个 wave 完成后验证关键功能
- 重视测试覆盖率

**❌ DON'T**：
- 使用过多 worker 导致难以追踪问题
- 在有 failed_tasks 时认为项目完成
- 忽略测试覆盖率低于 80% 的警告

---

### 6. Git 版本控制

**推荐的 .gitignore 配置**：
```
# 跟踪配置和定义
CLAUDE.md
.claude/

# 跟踪任务状态（方便团队协作）
.claude_tasks/state.json
.claude_tasks/task_registry.json

# 忽略临时上下文（可重新生成）
.claude_tasks/contexts/

# 跟踪设计产物
designs/
```

**提交策略**：
```bash
# 阶段1：完成设计
git add designs/
git commit -m "feat: complete design phase (user flows + wireframes)"

# 阶段2：完成前端拆分
git add .claude_tasks/state.json .claude_tasks/task_registry.json
git commit -m "feat: complete frontend decomposition (45 components)"

# 阶段3：完成后端拆分
git add .claude_tasks/task_registry.json
git commit -m "feat: complete backend decomposition (68 functions)"

# 阶段4：完成依赖分析
git add .claude_tasks/task_registry.json
git commit -m "feat: complete dependency analysis (8 waves)"

# 阶段5：完成开发
git add src/ tests/
git commit -m "feat: complete full-stack development (113 tasks)"
```

---

## 🚀 性能优化建议

### 大型项目优化（100+ 函数）

**策略**：
1. 减小批处理到 5
2. 增加 worker 到 10
3. 分模块逐步开发

```bash
# 拆分阶段：小批次
/continue-decompose-frontend 5
/continue-decompose-backend 5

# 开发阶段：高并行
/parallel-dev-fullstack 10
```

---

### 上下文经常超限的解决方案

**策略**：
1. 简化 context 模板
2. 减少示例代码
3. 使用更精简的描述

```bash
# 极小批次
/continue-decompose-frontend 3
/continue-decompose-backend 3
```

---

### 加速拆分的技巧

**策略**：
1. 确保需求描述清晰（减少 agent 理解时间）
2. 使用标准化的命名规范
3. 优先使用显式依赖声明

---

## 📞 获取更多帮助

- **快速参考**：查看 `QUICK_REFERENCE.md`
- **命令详情**：查看 `.claude/commands/<command-name>.md`
- **Agent 详情**：查看 `.claude/agents/<agent-name>.md`
- **系统架构**：查看 `CLAUDE.md`
- **示例项目**：查看 `example_requirements.md`

---

## 🎓 学习路径建议

1. **新手**（0-1 小时）
   - 阅读 README.md
   - 运行 GET_STARTED.md 中的简单示例
   - 熟悉 10 个命令

2. **进阶**（1-3 小时）
   - 阅读本文档完整内容
   - 理解设计驱动的工作流
   - 实践一个中型项目

3. **高级**（3+ 小时）
   - 阅读所有 agent 定义
   - 理解依赖分析算法
   - 自定义扩展 agent 和命令

---

**提示**：将本文档加入书签，开发过程中随时查阅！
