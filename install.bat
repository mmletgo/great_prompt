@echo off
REM Task Decomposition System - Windows 安装脚本
REM 用法: install.bat <目标项目路径>

setlocal enabledelayedexpansion

REM 检查参数
if "%~1"=="" (
    echo 错误: 请指定目标项目路径
    echo 用法: install.bat C:\path\to\your\project
    exit /b 1
)

set TARGET_DIR=%~1

REM 检查目标目录是否存在
if not exist "%TARGET_DIR%" (
    echo 错误: 目标目录不存在: %TARGET_DIR%
    exit /b 1
)

echo ========================================
echo Task Decomposition System 安装程序
echo ========================================
echo.
echo 目标目录: %TARGET_DIR%
echo.

REM 复制主配置文件
echo [1/4] 复制主配置文件...
copy /Y CLAUDE.md "%TARGET_DIR%\CLAUDE.md" >nul
if %errorlevel% neq 0 (
    echo 错误: 无法复制 CLAUDE.md
    exit /b 1
)
echo   ✓ CLAUDE.md

REM 复制文档
echo.
echo [2/4] 复制文档文件...
copy /Y README.md "%TARGET_DIR%\README.md" >nul
copy /Y USAGE_GUIDE.md "%TARGET_DIR%\USAGE_GUIDE.md" >nul
copy /Y QUICK_REFERENCE.md "%TARGET_DIR%\QUICK_REFERENCE.md" >nul
echo   ✓ README.md
echo   ✓ USAGE_GUIDE.md
echo   ✓ QUICK_REFERENCE.md

REM 复制 .claude 目录结构
echo.
echo [3/4] 复制命令定义...
if not exist "%TARGET_DIR%\.claude" mkdir "%TARGET_DIR%\.claude"
if not exist "%TARGET_DIR%\.claude\commands" mkdir "%TARGET_DIR%\.claude\commands"

xcopy /Y /Q .claude\commands\*.md "%TARGET_DIR%\.claude\commands\" >nul
if %errorlevel% neq 0 (
    echo 错误: 无法复制命令文件
    exit /b 1
)
echo   ✓ 10 个命令文件已复制

echo.
echo [4/4] 复制 Agent 定义...
if not exist "%TARGET_DIR%\.claude\agents" mkdir "%TARGET_DIR%\.claude\agents"

xcopy /Y /Q .claude\agents\*.md "%TARGET_DIR%\.claude\agents\" >nul
if %errorlevel% neq 0 (
    echo 错误: 无法复制 Agent 文件
    exit /b 1
)
echo   ✓ 8 个 Agent 文件已复制

REM 可选：复制示例需求文档
echo.
set /p COPY_EXAMPLE="是否复制示例需求文档? (Y/N): "
if /i "%COPY_EXAMPLE%"=="Y" (
    if not exist "%TARGET_DIR%\specs" mkdir "%TARGET_DIR%\specs"
    copy /Y example_requirements.md "%TARGET_DIR%\specs\example_requirements.md" >nul
    echo   ✓ 示例需求文档已复制到 specs\example_requirements.md
)

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 已安装到: %TARGET_DIR%
echo.
echo 文件清单:
echo   - CLAUDE.md (v2.0)
echo   - README.md
echo   - USAGE_GUIDE.md
echo   - QUICK_REFERENCE.md
echo   - .claude\commands\ (10 个命令)
echo   - .claude\agents\ (8 个 Agent)
if /i "%COPY_EXAMPLE%"=="Y" echo   - specs\example_requirements.md
echo.
echo 下一步:
echo   1. 进入项目目录: cd %TARGET_DIR%
echo   2. 在 Claude Code 中打开该目录
echo   3. 准备产品文档: docs/prd.md, docs/fullstack-architecture.md
echo   4. 执行设计阶段: /init-design
echo.
echo 详细使用说明请查看: USAGE_GUIDE.md
echo 快速参考: QUICK_REFERENCE.md
echo.

endlocal
