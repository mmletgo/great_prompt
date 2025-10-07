# 📚 文档索引

快速找到你需要的文档！

## 🎯 我想...

### 开始使用
- 🚀 **立即上手** → [GET_STARTED.md](GET_STARTED.md) - 3分钟快速开始
- 📘 **了解系统** → [README.md](README.md) - 系统概述和特性
- 📕 **学习使用** → [USAGE_GUIDE.md](USAGE_GUIDE.md) - 详细教程和示例
- 📙 **快速查阅** → [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 命令速查卡片

### 部署和测试
- 🔧 **部署系统** → [install.bat](install.bat) / [install.sh](install.sh) - 自动安装脚本
- ✅ **验证安装** → [TESTING_CHECKLIST.md](TESTING_CHECKLIST.md) - 测试清单
- 📋 **查看文件** → [FILE_MANIFEST.md](FILE_MANIFEST.md) - 完整文件清单

### 参考和深入
- 📓 **设计思路** → [task_decomposition_system.md](task_decomposition_system.md) - 原始设计
- 📄 **示例需求** → [example_requirements.md](example_requirements.md) - 完整需求示例
- ⚙️ **配置参考** → [CLAUDE.md](CLAUDE.md) - 主配置文件

---

## 📁 按文件类型分类

### 核心配置 (1)
| 文件 | 用途 |
|------|------|
| [CLAUDE.md](CLAUDE.md) | 项目主配置，定义架构和规则 |

### 使用文档 (5)
| 文件 | 用途 | 推荐度 |
|------|------|--------|
| [GET_STARTED.md](GET_STARTED.md) | 快速开始指南 | ⭐⭐⭐⭐⭐ |
| [README.md](README.md) | 系统概述 | ⭐⭐⭐⭐⭐ |
| [USAGE_GUIDE.md](USAGE_GUIDE.md) | 详细教程 | ⭐⭐⭐⭐⭐ |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | 快速参考 | ⭐⭐⭐⭐ |
| [TESTING_CHECKLIST.md](TESTING_CHECKLIST.md) | 测试清单 | ⭐⭐⭐⭐ |

### 管理文档 (2)
| 文件 | 用途 |
|------|------|
| [FILE_MANIFEST.md](FILE_MANIFEST.md) | 文件清单和依赖关系 |
| [INDEX.md](INDEX.md) | 本文件 - 文档索引 |

### 示例和参考 (2)
| 文件 | 用途 |
|------|------|
| [example_requirements.md](example_requirements.md) | 完整的需求示例 |
| [task_decomposition_system.md](task_decomposition_system.md) | 原始设计文档 |

### 工具脚本 (2)
| 文件 | 平台 |
|------|------|
| [install.bat](install.bat) | Windows |
| [install.sh](install.sh) | Linux/Mac |

### 命令定义 (10)
位置: `.claude/commands/`

**设计阶段:**
| 命令 | 用途 |
|------|------|
| [init-design.md](.claude/commands/init-design.md) | 读取PRD/架构/UX文档，生成用户流程图 |
| [generate-wireframes.md](.claude/commands/generate-wireframes.md) | 生成每个页面的线框图 |

**前端拆分:**
| 命令 | 用途 |
|------|------|
| [init-decompose-frontend.md](.claude/commands/init-decompose-frontend.md) | 初始化前端模块拆分 |
| [continue-decompose-frontend.md](.claude/commands/continue-decompose-frontend.md) | 继续拆分到组件级别 |

**后端拆分:**
| 命令 | 用途 |
|------|------|
| [init-decompose-backend.md](.claude/commands/init-decompose-backend.md) | 初始化后端服务拆分 |
| [continue-decompose-backend.md](.claude/commands/continue-decompose-backend.md) | 继续拆分到函数级别 |

**依赖与开发:**
| 命令 | 用途 |
|------|------|
| [build-deps-fullstack.md](.claude/commands/build-deps-fullstack.md) | 构建跨栈依赖图 |
| [parallel-dev-fullstack.md](.claude/commands/parallel-dev-fullstack.md) | 并行全栈开发 |
| [status.md](.claude/commands/status.md) | 查看状态 |
| [retry.md](.claude/commands/retry.md) | 重试失败 |

### Agent 定义 (8)
位置: `.claude/agents/`

**设计专家:**
| Agent | 职责 |
|-------|------|
| [user-flow-designer.md](.claude/agents/user-flow-designer.md) | 生成Mermaid用户流程图 |
| [wireframe-designer.md](.claude/agents/wireframe-designer.md) | 生成ASCII线框图 |

**拆分专家:**
| Agent | 职责 |
|-------|------|
| [frontend-decomposer.md](.claude/agents/frontend-decomposer.md) | 前端UI拆分（组件层级） |
| [backend-decomposer.md](.claude/agents/backend-decomposer.md) | 后端服务拆分（函数层级） |
| [context-generator.md](.claude/agents/context-generator.md) | 生成任务上下文 |

**分析专家:**
| Agent | 职责 |
|-------|------|
| [fullstack-dependency-analyzer.md](.claude/agents/fullstack-dependency-analyzer.md) | 全栈依赖分析 |

**开发专家:**
| Agent | 职责 |
|-------|------|
| [frontend-developer.md](.claude/agents/frontend-developer.md) | React/Vue组件TDD开发 |
| [backend-developer.md](.claude/agents/backend-developer.md) | 后端函数TDD开发 |

---

## 🎯 按使用阶段分类

### 阶段 1: 了解系统
1. [README.md](README.md) - 快速了解
2. [GET_STARTED.md](GET_STARTED.md) - 3分钟上手
3. [example_requirements.md](example_requirements.md) - 看看示例

### 阶段 2: 部署系统
1. [install.bat](install.bat) 或 [install.sh](install.sh) - 自动部署
2. [TESTING_CHECKLIST.md](TESTING_CHECKLIST.md) - 验证安装

### 阶段 3: 学习使用
1. [USAGE_GUIDE.md](USAGE_GUIDE.md) - 详细教程
2. [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 命令速查
3. [CLAUDE.md](CLAUDE.md) - 理解配置

### 阶段 4: 实战应用
1. 编写需求文档（参考 [example_requirements.md](example_requirements.md)）
2. 执行命令（参考 [QUICK_REFERENCE.md](QUICK_REFERENCE.md)）
3. 遇到问题（查看 [USAGE_GUIDE.md](USAGE_GUIDE.md) 故障排除）

### 阶段 5: 深入定制
1. [task_decomposition_system.md](task_decomposition_system.md) - 设计思路
2. [CLAUDE.md](CLAUDE.md) - 修改配置
3. `.claude/agents/*.md` - 自定义 Agent
4. `.claude/commands/*.md` - 自定义命令

---

## 📊 文档大小和阅读时间

| 文档 | 行数 | 阅读时间 | 适合 |
|------|------|---------|------|
| GET_STARTED.md | ~300 | 5-10 分钟 | 快速入门 |
| README.md | ~200 | 5 分钟 | 系统概述 |
| USAGE_GUIDE.md | ~600 | 20-30 分钟 | 深入学习 |
| QUICK_REFERENCE.md | ~250 | 2-5 分钟 | 日常参考 |
| TESTING_CHECKLIST.md | ~400 | 执行测试 | 验证系统 |
| CLAUDE.md | ~150 | 10 分钟 | 理解架构 |
| example_requirements.md | ~300 | 10 分钟 | 学习需求 |

---

## 🔍 按问题查找

### "我是新手，从哪开始？"
→ [GET_STARTED.md](GET_STARTED.md) → [README.md](README.md)

### "如何安装系统？"
→ [install.bat](install.bat) / [install.sh](install.sh) → [TESTING_CHECKLIST.md](TESTING_CHECKLIST.md)

### "命令怎么用？"
→ [QUICK_REFERENCE.md](QUICK_REFERENCE.md) → [USAGE_GUIDE.md](USAGE_GUIDE.md)

### "如何编写需求？"
→ [example_requirements.md](example_requirements.md) → [USAGE_GUIDE.md](USAGE_GUIDE.md)

### "遇到错误怎么办？"
→ [USAGE_GUIDE.md](USAGE_GUIDE.md) (故障排除) → [TESTING_CHECKLIST.md](TESTING_CHECKLIST.md)

### "如何自定义系统？"
→ [CLAUDE.md](CLAUDE.md) → `.claude/agents/` → `.claude/commands/`

### "查看所有文件？"
→ [FILE_MANIFEST.md](FILE_MANIFEST.md)

### "系统设计原理？"
→ [task_decomposition_system.md](task_decomposition_system.md)

---

## 💡 推荐阅读顺序

### 新手路径（第 1 天）
1. ⭐ [GET_STARTED.md](GET_STARTED.md) - 5 分钟
2. ⭐ [README.md](README.md) - 5 分钟
3. ⭐ 运行示例（使用 [example_requirements.md](example_requirements.md)）
4. ⭐ [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 收藏备用

### 进阶路径（第 2-3 天）
1. ⭐⭐ [USAGE_GUIDE.md](USAGE_GUIDE.md) - 完整阅读
2. ⭐⭐ [TESTING_CHECKLIST.md](TESTING_CHECKLIST.md) - 执行测试
3. ⭐⭐ 编写自己的需求文档
4. ⭐⭐ 在实际项目中使用

### 高级路径（第 4-7 天）
1. ⭐⭐⭐ [CLAUDE.md](CLAUDE.md) - 理解配置
2. ⭐⭐⭐ [task_decomposition_system.md](task_decomposition_system.md) - 设计思路
3. ⭐⭐⭐ 阅读所有 `.claude/agents/` 文件
4. ⭐⭐⭐ 阅读所有 `.claude/commands/` 文件
5. ⭐⭐⭐ 尝试自定义扩展

---

## 📱 快速访问（收藏这些）

**日常开发常用：**
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 命令速查
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - 问题解决

**首次使用必读：**
- [GET_STARTED.md](GET_STARTED.md) - 快速开始
- [README.md](README.md) - 系统概述

**深入研究推荐：**
- [CLAUDE.md](CLAUDE.md) - 核心配置
- [task_decomposition_system.md](task_decomposition_system.md) - 设计文档

---

## 🎓 学习资源

### 视频教程（假设）
1. 5分钟快速入门 → 看 [GET_STARTED.md](GET_STARTED.md)
2. 完整使用教程 → 看 [USAGE_GUIDE.md](USAGE_GUIDE.md)
3. 系统架构讲解 → 看 [CLAUDE.md](CLAUDE.md) + [task_decomposition_system.md](task_decomposition_system.md)

### 实战案例
- 用户管理系统 → [example_requirements.md](example_requirements.md)
- TODO 应用 → [USAGE_GUIDE.md](USAGE_GUIDE.md) 中的示例
- 计算器 → [TESTING_CHECKLIST.md](TESTING_CHECKLIST.md) 中的测试

---

## 📧 文档反馈

如果你发现：
- 📖 文档不清楚
- 🐛 示例有错误
- 💡 有改进建议
- ❓ 有未解答的问题

请记录并反馈！

---

## 🔄 文档更新日志

### v2.0.0 (2025-10-07)
- 🎨 新增设计阶段：PRD → 用户流程图 → 线框图
- 🔀 分离前后端拆分流程
- 🌐 跨栈依赖分析
- 🤖 8个专业化Agent（设计/拆分/分析/开发）
- 📦 10个命令支持完整全栈开发流程

### v2.0.0 (2025-10-07)
- 设计驱动的全栈产品开发系统正式发布
- 📚 12 个文档文件
- 🔧 6 个命令
- 🤖 4 个 Agent
- 📋 完整的索引系统

---

**提示**: 将本文件（INDEX.md）设为浏览器首页或编辑器起始页，快速访问所有文档！

---

**索引版本**: 2.0.0  
**最后更新**: 2025-10-07  
**总命令数**: 10  
**总Agent数**: 8  
**开发阶段**: 设计 → 前端拆分 → 后端拆分 → 依赖分析 → 并行开发
