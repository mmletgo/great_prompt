#!/bin/bash
# Task Decomposition System - Linux/Mac 安装脚本
# 用法: ./install.sh <目标项目路径>

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查参数
if [ -z "$1" ]; then
    echo -e "${RED}错误: 请指定目标项目路径${NC}"
    echo "用法: ./install.sh /path/to/your/project"
    exit 1
fi

TARGET_DIR="$1"

# 检查目标目录是否存在
if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${RED}错误: 目标目录不存在: $TARGET_DIR${NC}"
    exit 1
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Task Decomposition System 安装程序${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "目标目录: ${YELLOW}$TARGET_DIR${NC}"
echo ""

# 复制主配置文件
echo -e "${GREEN}[1/4] 复制主配置文件...${NC}"
cp CLAUDE.md "$TARGET_DIR/CLAUDE.md"
echo "  ✓ CLAUDE.md"

# 复制文档
echo ""
echo -e "${GREEN}[2/4] 复制文档文件...${NC}"
cp README.md "$TARGET_DIR/README.md"
cp USAGE_GUIDE.md "$TARGET_DIR/USAGE_GUIDE.md"
cp QUICK_REFERENCE.md "$TARGET_DIR/QUICK_REFERENCE.md"
echo "  ✓ README.md"
echo "  ✓ USAGE_GUIDE.md"
echo "  ✓ QUICK_REFERENCE.md"

# 复制 .claude 目录结构
echo ""
echo -e "${GREEN}[3/4] 复制命令定义...${NC}"
mkdir -p "$TARGET_DIR/.claude/commands"
cp .claude/commands/*.md "$TARGET_DIR/.claude/commands/"
echo "  ✓ 10 个命令文件已复制"

echo ""
echo -e "${GREEN}[4/4] 复制 Agent 定义...${NC}"
mkdir -p "$TARGET_DIR/.claude/agents"
cp .claude/agents/*.md "$TARGET_DIR/.claude/agents/"
echo "  ✓ 8 个 Agent 文件已复制"

# 可选：复制示例需求文档
echo ""
read -p "是否复制示例需求文档? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    mkdir -p "$TARGET_DIR/specs"
    cp example_requirements.md "$TARGET_DIR/specs/example_requirements.md"
    echo "  ✓ 示例需求文档已复制到 specs/example_requirements.md"
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}安装完成！${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "已安装到: ${YELLOW}$TARGET_DIR${NC}"
echo ""
echo "文件清单:"
echo "  - CLAUDE.md (v2.0)"
echo "  - README.md"
echo "  - USAGE_GUIDE.md"
echo "  - QUICK_REFERENCE.md"
echo "  - .claude/commands/ (10 个命令)"
echo "  - .claude/agents/ (8 个 Agent)"
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "  - specs/example_requirements.md"
fi
echo ""
echo -e "${YELLOW}下一步:${NC}"
echo "  1. 进入项目目录: cd $TARGET_DIR"
echo "  2. 在 Claude Code 中打开该目录"
echo "  3. 准备产品文档: docs/prd.md, docs/fullstack-architecture.md"
echo "  4. 执行设计阶段: /init-design"
echo ""
echo -e "详细使用说明请查看: ${BLUE}USAGE_GUIDE.md${NC}"
echo -e "快速参考: ${BLUE}QUICK_REFERENCE.md${NC}"
echo ""
