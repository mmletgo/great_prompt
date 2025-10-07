# 快速参考卡片

## 🎯 命令速查

### 核心命令（按执行顺序）

**v2.0 全栈开发流程:**

```bash
# 设计阶段
1. /init-design
   └─ 读取PRD/架构/UX文档，生成用户流程图（Mermaid）

2. /generate-wireframes
   └─ 生成每个页面的ASCII线框图

# 前端拆分
3. /init-decompose-frontend
   └─ 初始化前端模块拆分

4. /continue-decompose-frontend
   └─ 继续拆分到组件级别（重复执行）

# 后端拆分
5. /init-decompose-backend
   └─ 初始化后端服务拆分

6. /continue-decompose-backend
   └─ 继续拆分到函数级别（重复执行）

# 依赖分析与开发
7. /build-deps-fullstack
   └─ 构建跨栈依赖图，生成执行波次

8. /parallel-dev-fullstack [workers]
   └─ 并行执行全栈TDD开发（默认 5 个 worker）

# 监控
9. /status
   └─ 查看当前项目状态和进度

10. /retry
   └─ 重试失败的开发任务
```

## 📊 状态说明

### 任务状态
- `pending` - 待拆分
- `decomposed` - 已拆分
- `ready` - 函数级，待开发
- `in_progress` - 开发中
- `completed` - 已完成
- `failed` - 失败

### 阶段状态
- `decomposition_phase.status`
  - `in_progress` - 拆分中
  - `completed` - 拆分完成
  
- `development_phase.status`
  - `not_started` - 未开始
  - `in_progress` - 进行中
  - `completed` - 已完成

## 🗂️ 文件结构

```
docs/                       # 产品文档（用户准备）
├── prd.md
├── fullstack-architecture.md
└── front-end-spec.md

designs/                    # 设计产物（系统生成）
├── user-flows.md
└── wireframes/
    ├── login-page.md
    └── ...

.claude_tasks/              # 任务管理（系统生成）
├── state.json              # 全局状态
├── task_registry.json      # 任务清单 + 跨栈依赖图
└── contexts/               # 每个任务的详细上下文
    ├── frontend_task_001_context.md
    ├── backend_task_001_context.md
    └── ...
```

## 🔄 典型工作流

### 场景1：完整全栈流程
```
# 准备产品文档
docs/prd.md, docs/fullstack-architecture.md, docs/front-end-spec.md
↓
# 设计阶段
/init-design
↓
/generate-wireframes
↓
# 前端拆分
/init-decompose-frontend
↓
/continue-decompose-frontend (多次)
↓
# 后端拆分
/init-decompose-backend
↓
/continue-decompose-backend (多次)
↓
# 依赖分析与开发
/build-deps-fullstack
↓
/parallel-dev-fullstack 5
↓
/status (确认完成)
```

### 场景2：中断恢复
```
/status (查看当前进度)
↓
/continue-decompose (从检查点继续)
↓
... (继续后续步骤)
```

### 场景3：处理失败
```
/parallel-dev --workers 5
↓ (部分失败)
/retry
↓ (仍有失败)
手动修复 + 更新状态
```

## 🎨 命令示例

### init-design
```bash
# 自动读取 docs/ 目录下的设计文档
/init-design
```
技术栈：Python + FastAPI
```

### parallel-dev-fullstack
```bash
# 默认 5 个 worker
/parallel-dev-fullstack

# 自定义 worker 数量
/parallel-dev-fullstack 10

# 少量 worker（调试时）
/parallel-dev-fullstack 2
```

## 📈 进度判断

### 何时停止 continue-decompose？
```
输出显示：
✓ All tasks decomposed to function-level!
decomposition_phase.status = completed
→ 可以执行 /build-deps
```

### 何时执行 retry？
```
/parallel-dev 输出显示：
✗ Failed: N
→ 执行 /retry 重试失败任务
```

## 🔧 调优参数

### 批处理大小（默认 10）
编辑 `.claude/commands/continue-decompose.md`:
```markdown
- Limit to 5 tasks maximum  # 改为 5
```

### Worker 数量（默认 5）
```bash
/parallel-dev-fullstack 8  # 根据并行度调整
```

## 🐛 常见问题快速诊断

| 症状 | 可能原因 | 解决方案 |
|------|---------|---------|
| 拆分很多次还未完成 | 层级太深 | 检查 `task_registry.json`，手动调整 |
| `/build-deps` 报错循环依赖 | 任务设计有循环 | 重构任务，打破循环 |
| 上下文太长 | 批处理太大 | 减少批处理大小到 5 或 3 |
| 大量任务失败 | 上下文不清晰 | 增强 context 模板描述 |
| 无法从中断恢复 | 状态文件损坏 | 从备份恢复或手动修复 JSON |

## 📋 Subagent 角色

**设计阶段:**
| Agent | 职责 | 调用时机 |
|-------|------|----------|
| @user-flow-designer | 生成用户流程图 | `/init-design` |
| @wireframe-designer | 生成线框图 | `/generate-wireframes` |

**拆分阶段:**
| Agent | 职责 | 调用时机 |
|-------|------|----------|
| @frontend-decomposer | 前端UI拆分 | `/continue-decompose-frontend` |
| @backend-decomposer | 后端服务拆分 | `/continue-decompose-backend` |
| @context-generator | 生成上下文文档 | 组件/函数级任务创建时 |

**分析阶段:**
| Agent | 职责 | 调用时机 |
|-------|------|----------|
| @fullstack-dependency-analyzer | 跨栈依赖分析 | `/build-deps-fullstack` |

**开发阶段:**
| Agent | 职责 | 调用时机 |
|-------|------|----------|
| @frontend-developer | React/Vue组件TDD | `/parallel-dev-fullstack` |
| @backend-developer | 后端函数TDD | `/parallel-dev-fullstack` |

## 💡 最佳实践速记

✅ **DO**
- 需求描述清晰完整
- 定期执行 `/status` 检查进度
- 使用 git 追踪 `.claude_tasks/` 变更
- 根模块控制在 3-8 个
- 批处理失败时减小批次大小

❌ **DON'T**
- 不要手动编辑正在使用的状态文件
- 不要创建过多根任务（>10）
- 不要在 decomposition 未完成时执行 build-deps
- 不要忽略循环依赖警告
- 不要在 failed_tasks 未清空时认为完成

## 🚀 性能优化

| 场景 | 优化方案 |
|------|---------|
| 大型项目（>100 函数） | 减小批处理到 5，增加 worker 到 10 |
| 上下文经常超限 | 简化 context 模板，减少示例代码 |
| 拆分速度慢 | 确保需求描述清晰，减少 agent 理解时间 |
| 依赖分析慢 | 优先使用显式依赖声明，减少推断 |

## 📞 获取帮助

```bash
# 查看当前状态
/status

# 查看完整文档
cat USAGE_GUIDE.md

# 查看命令定义
cat .claude/commands/<command-name>.md

# 查看 agent 定义
cat .claude/agents/<agent-name>.md
```

## 🎓 学习路径

1. **新手** → 阅读 README.md，运行示例项目
2. **进阶** → 阅读 USAGE_GUIDE.md，理解工作流
3. **高级** → 阅读 CLAUDE.md 和各个 agent 定义，自定义扩展

---

**提示**: 将此文件打印或保存为书签，方便随时查阅！
