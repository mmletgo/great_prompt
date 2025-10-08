# 设计驱动的全栈产品开发系统

一个基于 Claude Code 的完整产品开发系统，从 PRD 到生产代码的全流程自动化：设计（用户流程+线框图） → 前后端拆分 → 跨栈依赖分析 → 并行 TDD 开发。

## ✨ 核心特性

- 🎨 **设计驱动**：PRD → 用户流程图（Mermaid） → 线框图（ASCII） → 代码实现
- 🔀 **前后端分离**：独立优化的拆分策略（UI组件 vs 分层函数）
- 🌐 **跨栈智能**：自动识别前端API调用 → 后端endpoint依赖
- 📦 **检查点机制**：支持分阶段执行，避免上下文溢出
- ⚡ **并行优化**：拓扑排序生成执行波次，最大化并行度
- 🧪 **专业化TDD**：前端（testing-library）vs 后端（clean architecture）
- 📝 **完整上下文**：每个任务的详细规格存储为独立 Markdown 文件

## 📁 文件结构

```
your-project/
├── docs/                           # 产品文档（用户准备）
│   ├── prd.md
│   ├── fullstack-architecture.md
│   └── front-end-spec.md
├── designs/                        # 设计产物（系统生成）
│   ├── user-flows.md             # Mermaid流程图
│   └── wireframes/               # ASCII线框图目录
│       ├── INDEX.md              # 线框图索引
│       ├── login-page.md         # 登录页线框图
│       └── ...                   # 其他页面线框图
├── CLAUDE.md                       # 主配置文件 (v2.0)
├── README.md                       # 项目概述
├── USAGE_GUIDE.md                  # 详细使用指南
├── QUICK_REFERENCE.md              # 命令速查手册
├── GET_STARTED.md                  # 快速入门
├── INDEX.md                        # 文档索引
├── FILE_MANIFEST.md                # 文件清单
├── TESTING_CHECKLIST.md            # 测试清单
├── SYSTEM_STATUS.md                # 系统状态总结
├── .claude/
│   ├── commands/                   # 10 个工作流命令
│   │   ├── init-design.md
│   │   ├── generate-wireframes.md
│   │   ├── init-decompose-frontend.md
│   │   ├── continue-decompose-frontend.md
│   │   ├── init-decompose-backend.md
│   │   ├── continue-decompose-backend.md
│   │   ├── build-deps-fullstack.md
│   │   ├── parallel-dev-fullstack.md
│   │   ├── status.md
│   │   └── retry.md
│   └── agents/                     # 8 个专业化 Agent
│       ├── user-flow-designer.md
│       ├── wireframe-designer.md
│       ├── frontend-decomposer.md
│       ├── backend-decomposer.md
│       ├── context-generator.md
│       ├── fullstack-dependency-analyzer.md
│       ├── frontend-developer.md
│       └── backend-developer.md
└── .claude_tasks/                  # 自动生成
    ├── state.json
    ├── task_registry.json
    └── contexts/
```

## 🚀 快速开始

### 1. 安装配置

将以下文件复制到你的项目根目录：

```bash
# 复制主配置
cp CLAUDE.md /your/project/

# 复制命令和 Agent 定义
cp -r .claude /your/project/
```

### 2. 准备需求（可选）

**准备产品文档**
```bash
mkdir docs
# 创建以下文件：
# docs/prd.md - 产品需求文档（必需）
# docs/fullstack-architecture.md - 技术架构（可选）
# docs/front-end-spec.md - 前端UX规范（可选）
# docs/back-end-spec.md - 后端技术规范（可选）
```

### 3. 执行完整工作流

```bash
# 在 Claude Code 中执行：

# 1. 设计阶段
/init-design
/generate-wireframes

# 2. 前端拆分
/init-decompose-frontend
/continue-decompose-frontend  # 重复直到完成

# 3. 后端拆分
/init-decompose-backend
/continue-decompose-backend  # 重复直到完成

# 4. 依赖分析与开发
/build-deps-fullstack
/parallel-dev-fullstack 5

# 5. 监控
/status  # 检查完成状态
```

## � 详细文档

查看以下文档获取更多信息：
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - 详细使用示例和故障排除
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 命令速查卡片
- [SYSTEM_STATUS.md](SYSTEM_STATUS.md) - 系统当前状态总结
- [INDEX.md](INDEX.md) - 完整文档索引

## 🎯 工作流程

```
PRD + 架构 + UX文档
       ↓
┌──────────────────┐
│  设计阶段         │  用户流程图 + 线框图
└──────────┬─────────┘
         ↓
┌──────────────────┬──────────────────┐
│  前端拆分         │  后端拆分         │
│ 模块→页面→组件   │ 模块→服务→函数   │
└────────┬─────────┴────────┬─────────┘
         ↓                   ↓
┌────────────────────────────────────┐
│    跨栈依赖分析                     │
│ - 前端API调用 → 后端endpoint       │
│ - 组件层级依赖                      │
│ - 函数调用图                        │
│ - 垂直依赖(Level 1→1→1)       │
│ - 生成3阶段执行计划              │
└────────┬───────────────────────────┘
         ↓
┌────────────────────────────────────┐
│    阶段1: Level 3 实现              │
│ 并行TDD开发(叶子节点)              │
│ Wave 1: 后端基础层                  │
│ Wave 2: 后端数据层                  │
│ Wave 3: 后端业务层                  │
│ Wave 4: 后端API层                   │
│ Wave 5: 前端基础组件                │
│ Wave 6: 前端API集成                 │
└────────┬───────────────────────────┘
         ↓
┌────────────────────────────────────┐
│    阶段2: Level 2 集成              │
│ 组装子节点成完整单元              │
│ Wave 7: 后端服务集成                │
│ Wave 8: 前端页面集成                │
└────────┬───────────────────────────┘
         ↓
┌────────────────────────────────────┐
│    阶段3: Level 1 集成              │
│ 最终模块组装,可部署单元          │
│ Wave 9: 后端模块集成                │
│ Wave 10: 前端模块集成               │
└────────┬───────────────────────────┘
         ↓
      完成 ✅
```

## 💡 核心概念

### 设计阶段
- **用户流程图**: Mermaid语法，描述用户交互流程
- **线框图**: ASCII art，每个页面的详细布局

### 任务层级

**前端层级:**
1. **Level 1 - Module**: UI模块（如"认证模块"）
2. **Level 2 - Page**: 页面（如"登录页"）
3. **Level 3 - Component**: React/Vue组件（如"LoginButton"）

**后端层级:**
1. **Level 1 - Module**: 服务模块（如"认证服务"）
2. **Level 2 - Service**: 业务服务（如"AuthService"）
3. **Level 3 - Function**: 函数（如"login_user"）
   - API层：路由处理器
   - Service层：业务逻辑
   - Repository层：数据访问
   - Validator层：输入验证
   - Util层：工具函数

### 任务状态
- `pending`: 待拆分
- `decomposed`: 已拆分为子任务
- `ready`: 函数级任务，准备开发
- `in_progress`: 开发中
- `completed`: 已完成
- `failed`: 失败

### Subagent 角色

**设计专家:**
- **@user-flow-designer**: 分析PRD生成用户流程图
- **@wireframe-designer**: 生成页面线框图

**拆分专家:**
- **@frontend-decomposer**: 前端UI拆分（组件层级）
- **@backend-decomposer**: 后端服务拆分（函数分层）
- **@context-generator**: 生成任务上下文文档

**分析专家:**
- **@fullstack-dependency-analyzer**: 跨栈依赖分析

**开发专家(Level 3 - 实现):**
- **@frontend-developer**: React/Vue组件TDD开发
- **@backend-developer**: 后端函数TDD开发（分层架构）

**集成专家(Level 2 & 1 - 组装):**
- **@frontend-integrator**: 前端页面/模块集成（组装组件）
- **@backend-integrator**: 后端服务/模块集成（编排函数）

## 📊 示例：电商网站

```
设计阶段:
- 用户流程: 浏览商品 → 加购物车 → 下单 → 支付
- 线框图: 8个页面（首页/商品列表/详情/购物车/结算/支付/订单/个人中心）

前端拆分 (树形结构):
├── 1. 商品展示模块 (Level 1 - Module)
│   ├── 1.1 商品列表页 (Level 2 - Page)
│   │   ├── 1.1.1 ProductCard (Level 3 - Component)
│   │   ├── 1.1.2 FilterPanel (Level 3 - Component)
│   │   └── 1.1.3 Pagination (Level 3 - Component)
│   └── 1.2 商品详情页 (Level 2 - Page)
│       ├── 1.2.1 ProductInfo (Level 3 - Component)
│       ├── 1.2.2 ImageGallery (Level 3 - Component)
│       └── 1.2.3 AddToCartButton (Level 3 - Component)
└── ...

后端拆分 (树形结构):
├── 1. 商品管理服务 (Level 1 - Module)
│   ├── 1.1 ProductService (Level 2 - Service)
│   │   ├── 1.1.1 GET /api/products (Level 3 - Endpoint)
│   │   ├── 1.1.2 get_product_list (Level 3 - Service层)
│   │   ├── 1.1.3 find_products_by_filter (Level 3 - Repository层)
│   │   └── 1.1.4 validate_product_filter (Level 3 - Validator层)
│   └── ...
└── ...

开发和集成流程:

阶段1 - Level 3 实现 (叶子节点):
  - 前端: 45个组件 (ProductCard, FilterPanel, etc.)
  - 后端: 68个函数 (API/Service/Repository/Validator layers)
  - Agent: @frontend-developer, @backend-developer
  - 执行波次: Wave 1-6 (并行开发)

阶段2 - Level 2 集成 (组装子节点):
  - 前端: 12个页面 (由组件组装而成)
    * 1.1 ProductListPage = 1.1.1 + 1.1.2 + 1.1.3 + ...
  - 后端: 10个服务 (由函数编排而成)
    * 1.1 ProductService = 1.1.1 + 1.1.2 + 1.1.3 + 1.1.4 + ...
  - Agent: @frontend-integrator, @backend-integrator
  - 执行波次: Wave 7-8 (集成测试)

阶段3 - Level 1 集成 (最终模块):
  - 前端: 3个模块 (由页面组装而成)
    * 1 ProductModule = 1.1 + 1.2 + ...
  - 后端: 4个模块 (由服务集成而成)
    * 1 ProductManagementModule = 1.1 + 1.2 + ...
  - Agent: @frontend-integrator, @backend-integrator
  - 执行波次: Wave 9-10 (E2E测试)

总计:
- Level 3: 113个任务 (45组件 + 68函数)
- Level 2: 22个任务 (12页面 + 10服务)
- Level 1: 7个模块 (3前端 + 4后端)
- 执行波次: 10波
- 总时间: ~60分钟
- 最终产出: 7个可部署模块
```

## 🛠️ 配置选项

### 批处理大小
拆分阶段的批处理大小固定为 5-10 个任务，在命令内部自动控制。如需调整，可编辑 `.claude/commands/continue-decompose-frontend.md` 和 `.claude/commands/continue-decompose-backend.md` 文件中的步骤描述。

### 调整并行数量
```bash
/parallel-dev-fullstack 10  # 默认 5 workers
```

## 🔧 常见问题

**Q: 如何从中断处恢复？**  
A: 直接执行上次建议的命令，系统会自动从检查点恢复。

**Q: 任务拆分太深怎么办？**  
A: 检查 `task_registry.json`，必要时手动调整任务类型。

**Q: 遇到循环依赖怎么办？**  
A: `/build-deps` 会检测并报告，需要重构任务打破循环。

**Q: 某些任务开发失败怎么办？**  
A: 执行 `/retry` 自动重试，或手动修复后更新状态。

## 📦 系统要求

- Claude Code（支持 subagent 机制）
- 项目支持的编程语言（Python、JavaScript 等）
- 测试框架（pytest、jest 等）

## 🤝 贡献

欢迎提出改进建议！主要改进方向：
- 支持更多编程语言
- 优化拆分策略
- 增强依赖分析
- 改进错误恢复

## 📄 许可

MIT License

## 🙏 致谢

本系统基于 Claude Code 的强大功能构建，利用：
- Slash Commands 机制
- Subagent 并行执行
- 上下文管理
- 文件系统操作

---

**开始使用**: 查看 [USAGE_GUIDE.md](USAGE_GUIDE.md)  
**问题反馈**: 提交 Issue  
**快速参考**: 查看 [CLAUDE.md](CLAUDE.md)
