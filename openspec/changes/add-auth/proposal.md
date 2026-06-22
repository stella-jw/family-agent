## Why

当前 REST API 无认证机制，任何人都可以访问和修改家庭成员数据。需要添加用户认证系统，实现用户注册、登录、数据隔离，确保每个用户只能访问自己的家庭数据。

## What Changes

- **用户注册**：支持用户名、密码注册
- **用户登录**：JWT Token 认证机制
- **密码安全**：密码加密存储（bcrypt）
- **数据隔离**：用户只能访问自己创建的家庭成员数据
- **API 保护**：所有 API 端点需要认证（除 /api/auth/* 外）

## Capabilities

### New Capabilities

- `user-auth`：用户认证系统（注册、登录、Token 管理）
- `user-data-isolation`：用户数据隔离，确保多用户数据安全

### Modified Capabilities

- （无）

## Impact

- **API 层**：所有端点添加 JWT 认证中间件
- **数据模型**：ChromaDB metadata 添加 user_id 字段，或新增用户表
- **前端**：登录/注册 UI 组件
