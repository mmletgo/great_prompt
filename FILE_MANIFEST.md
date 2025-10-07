# 项目文件清单

## 📦 完整文件列表

### 核心配置 (1)
```
CLAUDE.md                           # 项目主配置文件，定义系统架构和规则
```

### 文档文件 (4)
```
README.md                           # 项目概述和快速入门
USAGE_GUIDE.md                      # 详细使用指南（含示例和故障排除）
QUICK_REFERENCE.md                  # 命令和概念快速参考卡片
example_requirements.md             # 示例需求文档（用户管理系统）
```

### Commands (.claude/commands/)

**设计阶段:**
| 文件 | 大小 | 作用 | 依赖 Agent |
|------|------|------|------------|
| init-design.md | ~2 KB | 读取PRD/架构/UX，生成用户流程图 | @user-flow-designer |
| generate-wireframes.md | ~2 KB | 生成每个页面的线框图 | @wireframe-designer |

**前端拆分:**
| 文件 | 大小 | 作用 | 依赖 Agent |
|------|------|------|------------|
| init-decompose-frontend.md | ~2 KB | 初始化前端模块拆分 | 无 |
| continue-decompose-frontend.md | ~2.5 KB | 拆分到组件级别 | @frontend-decomposer, @context-generator |

**后端拆分:**
| 文件 | 大小 | 作用 | 依赖 Agent |
|------|------|------|------------|
| init-decompose-backend.md | ~2 KB | 初始化后端服务拆分 | 无 |
| continue-decompose-backend.md | ~2.5 KB | 拆分到函数级别 | @backend-decomposer, @context-generator |

**依赖与开发:**
| 文件 | 大小 | 作用 | 依赖 Agent |
|------|------|------|------------|
| build-deps-fullstack.md | ~2 KB | 构建跨栈依赖图 | @fullstack-dependency-analyzer |
| parallel-dev-fullstack.md | ~3 KB | 并行全栈TDD开发 | @frontend-developer, @backend-developer |
| status.md | ~1 KB | 查看项目状态 | 无 |
| retry.md | ~1 KB | 重试失败任务 | @frontend-developer, @backend-developer |

### Agent 定义 (4)
```
.claude/agents/decomposer.md               # 任务拆分专家
.claude/agents/context-generator.md        # 上下文文档生成器
.claude/agents/dependency-analyzer.md      # 依赖关系分析器
.claude/agents/tdd-developer.md            # TDD 开发执行者
```

### 安装脚本 (2)
```
install.bat                         # Windows 安装脚本
install.sh                          # Linux/Mac 安装脚本
```

---

## 📊 统计信息

- **总文件数**: 18
- **配置文件**: 1
- **文档文件**: 4
- **命令文件**: 6
- **Agent 文件**: 4
- **工具脚本**: 2
- **参考文件**: 1

---

## 🗂️ 目录结构

```
great_prompt/
├── CLAUDE.md                       # 核心配置
├── README.md                       # 项目概述
├── USAGE_GUIDE.md                  # 使用指南
├── QUICK_REFERENCE.md              # 快速参考
├── FILE_MANIFEST.md                # 本文件
├── example_requirements.md         # 示例需求
├── install.bat                     # Windows 安装
├── install.sh                      # Linux/Mac 安装
└── .claude/
    ├── commands/                   # Slash 命令
    │   ├── init-decompose.md
    │   ├── continue-decompose.md
    │   ├── build-deps.md
    │   ├── parallel-dev.md
    │   ├── status.md
    │   └── retry.md
    └── agents/                     # Agent 定义
        ├── decomposer.md
        ├── context-generator.md
        ├── dependency-analyzer.md
        └── tdd-developer.md
```

---

## 📋 文件用途说明

### 必须文件（部署到目标项目）
这些文件是系统运行所必需的：

✅ **CLAUDE.md** - 主配置，Claude Code 自动加载  
✅ **.claude/commands/*.md** - 6 个 slash 命令定义  
✅ **.claude/agents/*.md** - 4 个 agent 定义  

### 推荐文件（帮助用户理解）
强烈建议复制到目标项目：

📘 **README.md** - 快速了解系统  
📘 **USAGE_GUIDE.md** - 详细操作指南  
📘 **QUICK_REFERENCE.md** - 快速查阅命令  

### 可选文件（辅助开发）
根据需要选择性复制：

📄 **example_requirements.md** - 学习如何编写需求  

### 工具文件（不需要复制）
仅在源项目中使用：

🔧 **install.bat** - Windows 部署工具  
🔧 **install.sh** - Linux/Mac 部署工具  
🔧 **FILE_MANIFEST.md** - 本清单文件  

---

## 🚀 部署方式

### 方式 1: 使用安装脚本（推荐）

**Windows:**
```cmd
install.bat C:\path\to\your\project
```

**Linux/Mac:**
```bash
chmod +x install.sh
./install.sh /path/to/your/project
```

### 方式 2: 手动复制

复制以下文件到目标项目：
1. `CLAUDE.md` → 项目根目录
2. `.claude/` 整个目录 → 项目根目录
3. `README.md`, `USAGE_GUIDE.md`, `QUICK_REFERENCE.md` → 项目根目录（可选）

---

## 🔍 文件依赖关系

```
CLAUDE.md
  └─ 引用 .claude/commands/ 中的所有命令
      └─ 命令调用 .claude/agents/ 中的 Agent
```

### 命令与 Agent 的关系

| 命令 | 调用的 Agent |
|------|------------|
| `/init-decompose` | - |
| `/continue-decompose` | @decomposer, @context-generator |
| `/build-deps` | @dependency-analyzer |
| `/parallel-dev` | @tdd-developer |
| `/status` | - |
| `/retry` | @tdd-developer |

---

## 📦 完整性检查清单

部署后，确保以下文件存在：

```
☐ 目标项目/CLAUDE.md
☐ 目标项目/.claude/commands/init-decompose.md
☐ 目标项目/.claude/commands/continue-decompose.md
☐ 目标项目/.claude/commands/build-deps.md
☐ 目标项目/.claude/commands/parallel-dev.md
☐ 目标项目/.claude/commands/status.md
☐ 目标项目/.claude/commands/retry.md
☐ 目标项目/.claude/agents/decomposer.md
☐ 目标项目/.claude/agents/context-generator.md
☐ 目标项目/.claude/agents/dependency-analyzer.md
☐ 目标项目/.claude/agents/tdd-developer.md
```

推荐同时包含：
```
☐ 目标项目/README.md
☐ 目标项目/USAGE_GUIDE.md
☐ 目标项目/QUICK_REFERENCE.md
```

---

## 🎯 版本信息

- **系统名称**: Task Decomposition & Parallel TDD Development System
- **版本**: 1.0.0
- **创建日期**: 2025-10-07
- **适用于**: Claude Code with Subagent Support
- **文件总数**: 18

---

## 📝 更新日志

### v2.0.0 (2025-10-07)
- 设计驱动的全栈产品开发系统正式发布
- 10个命令和8个Agent
- 支持设计→前端→后端→全栈开发工作流
- 📦 包含 12 个核心配置文件
- 📘 完整的文档体系
- 🔧 自动化安装脚本
- 📋 示例需求文档

---

## 🤝 贡献指南

如需修改系统，请注意：

1. **修改 CLAUDE.md**: 影响全局行为
2. **修改命令文件**: 影响对应 slash 命令
3. **修改 Agent 文件**: 影响对应 subagent 行为
4. **修改文档**: 仅影响用户理解，不影响功能

---

## 📞 获取帮助

- 📖 查看 `USAGE_GUIDE.md` 了解详细用法
- 🔍 查看 `QUICK_REFERENCE.md` 快速查阅命令
- 📄 查看 `README.md` 了解系统概述
- 💡 查看 `example_requirements.md` 学习需求编写

---

**文件清单版本**: 1.0.0  
**最后更新**: 2025-10-07
