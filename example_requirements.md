# 示例项目需求：用户管理系统

## 项目概述
开发一个完整的用户管理系统后端 API，支持用户注册、登录、个人信息管理等功能。

## 功能需求

### 1. 用户注册
- **邮箱注册**
  - 验证邮箱格式
  - 检查邮箱唯一性
  - 发送验证邮件
  - 邮箱验证链接有效期 24 小时
  
- **密码要求**
  - 最小长度 8 位
  - 必须包含大小写字母
  - 必须包含数字
  - 必须包含特殊字符
  - 密码加密存储（bcrypt）

- **用户名规则**
  - 3-20 个字符
  - 仅支持字母、数字、下划线
  - 检查唯一性

### 2. 用户登录
- **登录方式**
  - 支持邮箱登录
  - 支持用户名登录
  
- **安全控制**
  - 登录失败 5 次锁定账户 30 分钟
  - 记录登录日志（IP、时间、设备）
  - Session 有效期 7 天
  - 支持"记住我"功能（30 天）

- **JWT Token**
  - 生成 access_token（2 小时有效）
  - 生成 refresh_token（7 天有效）
  - Token 刷新机制

### 3. 用户信息管理
- **查看个人资料**
  - 用户名
  - 邮箱
  - 头像 URL
  - 注册时间
  - 最后登录时间

- **编辑个人资料**
  - 修改用户名（检查唯一性）
  - 修改个人简介（最多 200 字）
  - 验证后修改邮箱
  
- **头像上传**
  - 支持 JPG、PNG 格式
  - 最大 2MB
  - 自动生成缩略图（200x200）
  - 存储到云存储（S3/OSS）

### 4. 密码管理
- **修改密码**
  - 验证旧密码
  - 新密码符合强度要求
  
- **重置密码**
  - 通过邮箱重置
  - 生成重置令牌（1 小时有效）
  - 发送重置邮件

### 5. 账户管理
- **注销账户**
  - 软删除（保留数据 30 天）
  - 清除所有 Session
  
- **账户恢复**
  - 30 天内可恢复
  - 通过邮箱验证

## 技术栈

### 后端框架
- Python 3.11+
- FastAPI 0.100+
- Pydantic v2（数据验证）

### 数据库
- PostgreSQL 15+
- SQLAlchemy 2.0（ORM）
- Alembic（数据库迁移）

### 缓存
- Redis 7+（Session、验证码缓存）

### 存储
- AWS S3 / 阿里云 OSS（头像存储）

### 安全
- bcrypt（密码加密）
- PyJWT（Token 生成）
- python-multipart（文件上传）

### 邮件服务
- aiosmtplib（异步邮件发送）

### 测试
- pytest
- pytest-asyncio
- pytest-cov（覆盖率）

## 非功能需求

### 性能要求
- API 响应时间 < 200ms（P95）
- 支持 1000 并发用户
- 数据库查询优化（索引）

### 安全要求
- 所有密码必须加密存储
- API 使用 HTTPS
- 防止 SQL 注入
- 防止 XSS 攻击
- CSRF Token 验证

### 可用性
- 系统可用性 99.9%
- 数据库主从复制
- Redis 哨兵模式

## API 设计

### 认证相关
- POST /api/v1/auth/register - 用户注册
- POST /api/v1/auth/login - 用户登录
- POST /api/v1/auth/logout - 用户登出
- POST /api/v1/auth/refresh - 刷新 Token
- POST /api/v1/auth/verify-email - 验证邮箱
- POST /api/v1/auth/reset-password - 重置密码

### 用户信息
- GET /api/v1/users/me - 获取当前用户信息
- PUT /api/v1/users/me - 更新个人信息
- POST /api/v1/users/me/avatar - 上传头像
- PUT /api/v1/users/me/password - 修改密码
- DELETE /api/v1/users/me - 注销账户

## 数据库设计

### users 表
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    avatar_url VARCHAR(500),
    bio VARCHAR(200),
    is_email_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);
```

### login_logs 表
```sql
CREATE TABLE login_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    login_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    success BOOLEAN DEFAULT TRUE
);
```

### verification_tokens 表
```sql
CREATE TABLE verification_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    token VARCHAR(255) UNIQUE NOT NULL,
    token_type VARCHAR(20) NOT NULL, -- email_verify, password_reset
    expires_at TIMESTAMP NOT NULL,
    used_at TIMESTAMP NULL
);
```

## 项目结构

```
user-management-system/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       └── users.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── dependencies.py
│   ├── models/
│   │   ├── user.py
│   │   └── token.py
│   ├── schemas/
│   │   ├── user.py
│   │   └── auth.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── email_service.py
│   │   └── storage_service.py
│   ├── repositories/
│   │   └── user_repository.py
│   └── utils/
│       ├── validators.py
│       └── helpers.py
├── tests/
├── alembic/
├── requirements.txt
└── main.py
```

## 验收标准

1. ✅ 所有 API 接口正常工作
2. ✅ 测试覆盖率 > 90%
3. ✅ 所有安全要求已实现
4. ✅ API 文档完整（OpenAPI/Swagger）
5. ✅ 性能测试通过
6. ✅ 代码符合 PEP 8 规范
7. ✅ 所有边界条件已处理
8. ✅ 错误处理完善

## 开发优先级

1. **P0 - 核心功能**（第一阶段）
   - 用户注册
   - 用户登录
   - JWT Token 管理

2. **P1 - 基础功能**（第二阶段）
   - 个人信息查看/编辑
   - 密码修改
   - 邮箱验证

3. **P2 - 高级功能**（第三阶段）
   - 头像上传
   - 密码重置
   - 账户注销/恢复
   - 登录日志
