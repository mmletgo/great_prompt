# 系统测试检查清单

> v2.0 - 设计驱动的全栈产品开发系统

使用本清单验证完整的设计驱动全栈开发工作流是否正确部署和运行。

## ✅ 第一阶段：安装验证

### 1. 文件存在性检查

在目标项目根目录执行：

**Windows (PowerShell):**
```powershell
# 检查核心文件
Test-Path CLAUDE.md

# 检查 10 个命令文件
Test-Path .claude\commands\init-design.md
Test-Path .claude\commands\generate-wireframes.md
Test-Path .claude\commands\init-decompose-frontend.md
Test-Path .claude\commands\continue-decompose-frontend.md
Test-Path .claude\commands\init-decompose-backend.md
Test-Path .claude\commands\continue-decompose-backend.md
Test-Path .claude\commands\build-deps-fullstack.md
Test-Path .claude\commands\parallel-dev-fullstack.md
Test-Path .claude\commands\status.md
Test-Path .claude\commands\retry.md

# 检查 8 个 agent 文件
Test-Path .claude\agents\user-flow-designer.md
Test-Path .claude\agents\wireframe-designer.md
Test-Path .claude\agents\frontend-decomposer.md
Test-Path .claude\agents\backend-decomposer.md
Test-Path .claude\agents\context-generator.md
Test-Path .claude\agents\fullstack-dependency-analyzer.md
Test-Path .claude\agents\frontend-developer.md
Test-Path .claude\agents\backend-developer.md
```

**Linux/Mac (Bash):**
```bash
# 检查核心文件
for file in \
  CLAUDE.md \
  .claude/commands/init-design.md \
  .claude/commands/generate-wireframes.md \
  .claude/commands/init-decompose-frontend.md \
  .claude/commands/continue-decompose-frontend.md \
  .claude/commands/init-decompose-backend.md \
  .claude/commands/continue-decompose-backend.md \
  .claude/commands/build-deps-fullstack.md \
  .claude/commands/parallel-dev-fullstack.md \
  .claude/commands/status.md \
  .claude/commands/retry.md \
  .claude/agents/user-flow-designer.md \
  .claude/agents/wireframe-designer.md \
  .claude/agents/frontend-decomposer.md \
  .claude/agents/backend-decomposer.md \
  .claude/agents/context-generator.md \
  .claude/agents/fullstack-dependency-analyzer.md \
  .claude/agents/frontend-developer.md \
  .claude/agents/backend-developer.md; do
  if [ -f "$file" ]; then
    echo "✓ $file"
  else
    echo "✗ $file (缺失)"
  fi
done
```

**预期结果**: 所有文件都存在（显示 ✓）

---

## ✅ 第二阶段：命令可用性检查

### 2. Claude Code 识别测试

在 Claude Code 中打开目标项目，输入 `/` 查看命令列表。

**预期结果**: 应该看到以下 10 个命令：
```
设计阶段:
☐ /init-design
☐ /generate-wireframes

前端拆分:
☐ /init-decompose-frontend
☐ /continue-decompose-frontend

后端拆分:
☐ /init-decompose-backend
☐ /continue-decompose-backend

依赖与开发:
☐ /build-deps-fullstack
☐ /parallel-dev-fullstack

监控:
☐ /status
☐ /retry
```

如果没有看到，尝试：
1. 重启 Claude Code
2. 检查 `.claude/commands/` 目录下文件是否正确
3. 检查文件开头是否有正确的 YAML front matter

---

## ✅ 第三阶段：功能测试（简单项目）

### 3. 创建测试 PRD

创建文件 `docs/prd.md`：

```markdown
# 测试项目：简单电商系统

## 产品需求

### 用户端功能
1. 用户注册/登录
2. 浏览商品列表
3. 查看商品详情
4. 添加到购物车
5. 提交订单

### 管理端功能
1. 商品管理（CRUD）
2. 订单管理

## 技术栈
前端：React 18 + TypeScript + Vite
后端：Python 3.11 + FastAPI + PostgreSQL
```

创建文件 `docs/front-end-spec.md`：

```markdown
# 前端技术规格

- UI 库: Material-UI
- 状态管理: React Context
- 路由: React Router
- HTTP: Axios
```

创建文件 `docs/back-end-spec.md`：

```markdown
# 后端技术规格

- Web 框架: FastAPI
- ORM: SQLAlchemy
- 认证: JWT
- 数据库: PostgreSQL
```

### 4. 测试设计阶段

**测试 4.1: init-design**

在 Claude Code 中执行：
```
/init-design
```

**预期输出**:
```
✓ Read PRD from docs/prd.md
✓ Read architecture from docs/fullstack-architecture.md
✓ Read UX spec from docs/front-end-spec.md
✓ Created user-flow-designer subagent
✓ Generated designs/user-flows.md with Mermaid diagrams
  - User Registration Flow
  - Product Browsing Flow
  - Checkout Flow
Next command: /generate-wireframes
```

**验证点**:
- ☐ 创建了 `designs/` 目录
- ☐ 存在 `designs/user-flows.md` 文件
- ☐ 文件包含 Mermaid 流程图

**测试 4.2: generate-wireframes**

执行：
```
/generate-wireframes
```

**预期输出**:
```
✓ Created wireframe-designer subagent
✓ Generated designs/wireframes/ directory
  - designs/wireframes/home-page.md
  - designs/wireframes/product-list-page.md
  - designs/wireframes/product-detail-page.md
  - designs/wireframes/cart-page.md
✓ Created designs/wireframes/INDEX.md
Next command: /init-decompose-frontend
```

**验证点**:
- ☐ 存在 `designs/wireframes/` 目录
- ☐ 存在多个页面线框图文件
- ☐ 每个文件包含 ASCII art 线框图
- ☐ 存在 INDEX.md 索引文件

---

### 5. 测试前端拆分

**测试 5.1: init-decompose-frontend**

执行：
```
/init-decompose-frontend
```

**预期输出**:
```
✓ Created .claude_tasks/ directory structure
✓ Initialized state.json with frontend phase
✓ Created [4-6] frontend module-level tasks
Checkpoint saved: frontend_XXX
Next command: /continue-decompose-frontend
```

**验证点**:
- ☐ 创建了 `.claude_tasks/` 目录
- ☐ 存在 `state.json` 文件
- ☐ 存在 `task_registry.json` 文件
- ☐ 创建了 4-6 个前端模块任务

### 6. 检查 state.json

```bash
cat .claude_tasks/state.json
```

**预期内容**:
```json
{
  "design_phase": {
    "status": "completed"
  },
  "frontend_decomposition_phase": {
    "status": "in_progress",
    "last_checkpoint": "frontend_00X"
  },
  "backend_decomposition_phase": {
    "status": "not_started"
  }
}
```

### 7. 测试 continue-decompose-frontend

执行：
```
/continue-decompose-frontend
```

**预期输出**:
```
Resuming from checkpoint: frontend_XXX
Creating frontend-decomposer subagent...
Processing batch...
✓ Processed [N] tasks
Updated checkpoint: frontend_XXX
```

**重复执行 2-3 次**，直到看到：
```
✓ All frontend tasks decomposed to component-level!
✓ Total: [N] frontend components
frontend_decomposition_phase.status = completed
Next command: /init-decompose-backend
```

**验证点**:
- ☐ 能够从检查点恢复
- ☐ 逐步拆分任务（Module → Page → Component）
- ☐ 最终达到组件级别
- ☐ 创建了 `contexts/` 目录下的前端上下文文件 (如 1_1_1_context.md)

---

### 8. 测试后端拆分

**测试 8.1: init-decompose-backend**

执行：
```
/init-decompose-backend
```

**预期输出**:
```
✓ Initialized backend_decomposition phase
✓ Created [4-6] backend module-level tasks
Checkpoint saved: backend_XXX
Next command: /continue-decompose-backend
```

**验证点**:
- ☐ state.json 中添加了 backend_decomposition_phase
- ☐ 创建了后端模块任务

**测试 8.2: continue-decompose-backend**

执行：
```
/continue-decompose-backend
```

**重复直到**:
```
✓ All backend tasks decomposed to function-level!
✓ Total: [N] backend functions across 5 layers
backend_decomposition_phase.status = completed
Next command: /build-deps-fullstack
```

**验证点**:
- ☐ 拆分到函数级别（Module → Service → Function）
- ☐ 函数按 5 层分类：API/Service/Repository/Validation/Utility
- ☐ 创建了 backend context 文件

### 9. 检查 context 文件

```bash
ls .claude_tasks/contexts/
```bash
# 查看前端组件上下文 (点号ID 1.1.1 转换为 1_1_1_context.md)
cat .claude_tasks/contexts/1_1_1_context.md

# 查看后端函数上下文 (点号ID 2.1.1 转换为 2_1_1_context.md)
cat .claude_tasks/contexts/2_1_1_context.md
```
```

**预期内容**:

**前端 context**:
- ☐ 包含组件名称和类型
- ☐ 包含 Props 定义
- ☐ 包含 State 定义
- ☐ 包含 Hooks 使用
- ☐ 包含测试用例（testing-library）

**后端 context**:
- ☐ 包含函数签名
- ☐ 标明所属层（API/Service/Repository/Validation/Utility）
- ☐ 包含输入参数和返回值
- ☐ 包含测试用例（pytest/jest）
- ☐ 包含实现要求

### 10. 测试 build-deps-fullstack

执行：
```
/build-deps-fullstack
```

**预期输出**:
```
Creating fullstack-dependency-analyzer subagent...
✓ Analyzing frontend dependencies...
✓ Analyzing backend dependencies...
✓ Analyzing cross-stack dependencies...

Full-Stack Dependency Graph Summary:
- Total tasks: [N] ([frontend] frontend + [backend] backend)
- Execution waves: [N]
- Max parallelism: [N]
- Cross-stack dependencies: [N]
```

**验证点**:
- ☐ 没有循环依赖错误
- ☐ `task_registry.json` 中添加了 `cross_stack_dependency_graph`
- ☐ 输出了执行波次信息
- ☐ 正确识别了前端→后端 API 调用依赖
- ☐ 后端内部分层依赖正确（Utility → Repository → Service → API）

### 11. 测试 status

执行：
```
/status
```

**预期输出**:
```
=== Full-Stack Project Status ===

Design Phase: completed
Frontend Decomposition Phase: completed
Backend Decomposition Phase: completed
Dependency Analysis: completed
Development Phase: not_started
...
Next Steps: /parallel-dev-fullstack 5
```

**验证点**:
- ☐ 正确显示所有阶段状态
- ☐ 显示前后端任务统计信息
- ☐ 显示跨栈依赖数量
- ☐ 给出下一步建议

### 12. 测试 parallel-dev-fullstack（可选）

⚠️ **警告**: 这会实际创建前后端代码文件

执行：
```
/parallel-dev-fullstack 3
```

**预期输出**:
```
Starting full-stack parallel TDD development with 3 workers...

=== Wave 1: [N] tasks ===
Creating backend-developer and frontend-developer subagents...

[Backend] Worker 1: backend_XXX
  RED: Generated [N] tests
  GREEN: Implementation complete
  ✓ All tests passed

[Frontend] Worker 2: frontend_XXX
  RED: Generated component tests
  GREEN: React component implemented
  ✓ All tests passed

...

=== Full-Stack Development Summary ===
Frontend: [N]/[N] ✓
Backend: [N]/[N] ✓
✗ Failed: 0
```

**验证点**:
- ☐ 创建了前端测试文件（.test.tsx）
- ☐ 创建了前端组件文件（.tsx）
- ☐ 创建了后端测试文件（test_*.py）
- ☐ 创建了后端实现文件（*.py）
- ☐ 测试全部通过
- ☐ 跨栈依赖正确处理（前端等待后端API完成）
- ☐ 更新了 `state.json`

---

## ✅ 第四阶段：错误处理测试

### 13. 测试中断恢复

1. 执行 `/continue-decompose-frontend`
2. 在处理过程中记下 checkpoint
3. 再次执行 `/continue-decompose-frontend`
4. 验证从上次 checkpoint 继续

**预期**: 不重复处理已完成的任务

**后端也重复测试**：
- ☐ `/continue-decompose-backend` 中断恢复
- ☐ `/parallel-dev-fullstack` 中断恢复

### 14. 测试 status 命令在各阶段

在不同阶段执行 `/status`：
- ☐ 设计阶段完成后
- ☐ 前端拆分进行中
- ☐ 前端拆分完成后
- ☐ 后端拆分进行中
- ☐ 后端拆分完成后
- ☐ 依赖图构建后
- ☐ 开发进行中
- ☐ 开发完成后

**预期**: 每次都给出正确的状态和下一步建议

### 15. 测试重复命令

尝试在已完成的阶段重复执行命令：

```
# 前端拆分已完成后再次执行
/continue-decompose-frontend

# 后端拆分已完成后再次执行
/continue-decompose-backend
```

**预期**: 提示已完成，建议执行下一步

---

## ✅ 第五阶段：性能和限制测试

### 16. 测试大批量任务

创建复杂 PRD（预期 >40 个前端组件 + >30 个后端函数），测试：
- ☐ 批处理是否正确工作（每批 ≤10 个任务）
- ☐ 检查点是否正确保存
- ☐ 能否从任意检查点恢复
- ☐ 前后端拆分独立工作

### 17. 测试并发限制

执行 `/parallel-dev-fullstack` 时：
- ☐ 测试不同 worker 数量（2, 5, 10）
- ☐ 验证同一波次内并发执行
- ☐ 验证不同波次间串行执行
- ☐ 前端和后端 worker 正确分配

### 18. 测试跨栈依赖关系

创建有明确跨栈依赖的 PRD：
```markdown
前端 LoginForm 组件依赖后端 login_api
前端 ProductList 组件依赖后端 get_products_api
后端 get_products_api 依赖 ProductRepository
ProductRepository 依赖 validate_product_id
```

验证：
- ☐ 前端内部依赖正确识别
- ☐ 后端分层依赖正确识别
- ☐ 跨栈依赖正确识别
- ☐ 执行波次正确排序：
  * Utility 函数在 Wave 1
  * Repository 在 Wave 2
  * Service 在 Wave 3  
  * API 在 Wave 4
  * 调用 API 的前端组件在 Wave 5+

---

## ✅ 第六阶段：边界情况测试

### 17. 测试空需求

```
/init-decompose

需求：无具体功能
```

**预期**: 提示需求不明确或创建最少任务

### 18. 测试循环依赖

手动创建循环依赖的需求，执行到 `/build-deps`：

**预期**: 检测到循环依赖并报错

### 19. 测试文件系统错误

模拟文件系统问题：
- ☐ `.claude_tasks/` 目录不可写
- ☐ `state.json` 文件损坏

**预期**: 合理的错误提示

---

## 📊 测试结果汇总

### 通过标准

系统测试通过的标准：

✅ **核心功能**（必须全部通过）
- ☐ 所有 10 个命令可识别
- ☐ init-design 能生成用户流程
- ☐ generate-wireframes 能生成线框图
- ☐ init-decompose-frontend 能创建前端根任务
- ☐ continue-decompose-frontend 能递归拆分前端
- ☐ init-decompose-backend 能创建后端根任务
- ☐ continue-decompose-backend 能递归拆分后端
- ☐ build-deps-fullstack 能构建全栈依赖图
- ☐ status 能显示正确状态
- ☐ 检查点机制正常工作

✅ **高级功能**（至少通过 80%）
- ☐ parallel-dev-fullstack 能全栈并行开发
- ☐ retry 能重试失败任务
- ☐ 前端内部依赖正确识别
- ☐ 后端分层依赖正确识别
- ☐ 跨栈依赖正确识别
- ☐ 前端TDD流程正确执行
- ☐ 后端TDD流程正确执行
- ☐ 中断恢复机制有效

✅ **文档完整性**
- ☐ README.md 清晰易懂，反映 v2.0 设计驱动全栈架构
- ☐ USAGE_GUIDE.md 包含完整全栈工作流示例
- ☐ QUICK_REFERENCE.md 准确，列出 10 个命令
- ☐ INDEX.md 反映 8 个 agent 和 10 个命令
- ☐ SYSTEM_STATUS.md 完整总结系统状态

### 测试记录模板

```
日期: ________
测试人: ________
目标项目: ________
第一阶段（安装验证）: [ ] 通过  [ ] 失败  (问题: ______)
第二阶段（命令可用性）: [ ] 通过  [ ] 失败  (问题: ______)
第三阶段（设计与拆分）: [ ] 通过  [ ] 失败  (问题: ______)
第四阶段（错误处理）: [ ] 通过  [ ] 失败  (问题: ______)
第五阶段（性能测试）: [ ] 通过  [ ] 失败  (问题: ______)
第六阶段（边界情况）: [ ] 通过  [ ] 失败  (问题: ______)

跨栈依赖测试: [ ] 通过  [ ] 失败
前后端分离: [ ] 正确  [ ] 有问题
全栈并行开发: [ ] 正常  [ ] 异常

总体评价: [ ] 可用  [ ] 需修复  [ ] 不可用

建议:
_________________________________________________
_________________________________________________
```

---

## 🔧 常见问题诊断

### 问题：命令不显示

**可能原因**:
1. `.claude/commands/` 目录位置错误
2. Markdown 文件格式错误
3. YAML front matter 缺失或格式错误

**解决方案**:
```bash
# 检查文件格式
head -n 5 .claude/commands/init-decompose.md
# 应该看到:
# ---
# name: init-decompose
# description: ...
# ---
```

### 问题：subagent 不工作

**可能原因**:
1. `.claude/agents/` 目录位置错误
2. Agent 定义文件格式错误
3. 命令中的 subagent 调用语法错误

**解决方案**:
```bash
# 检查 agent 文件
cat .claude/agents/decomposer.md
# 检查命令中的调用
grep -n "subagent" .claude/commands/continue-decompose.md
```

### 问题：状态文件损坏

**解决方案**:
```bash
# 备份当前状态
cp .claude_tasks/state.json .claude_tasks/state.json.backup

# 验证 JSON 格式（需要 jq）
jq . .claude_tasks/state.json

# 如果损坏，从检查点重建
# 删除损坏文件，重新执行对应命令
```

---

## 📝 测试完成后

完成测试后：

1. **清理测试数据**:
   ```bash
   rm -rf .claude_tasks/
   rm -rf docs/
   rm -rf designs/
   ```

2. **记录测试结果**: 填写上方的测试记录模板

3. **报告问题**: 如有问题，记录详细步骤和错误信息

4. **准备生产使用**: 测试通过后，即可用于实际项目

---

**测试清单版本**: 2.0.0 (设计驱动全栈)  
**最后更新**: 2025-10-07
