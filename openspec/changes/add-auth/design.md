## Context

REST API 当前无认证机制，需要添加用户认证和数据隔离能力。用户注册登录后，API 返回 JWT Token，客户端携带 Token 访问受保护资源。

## Goals / Non-Goals

**Goals:**
- 支持用户注册和登录
- 使用 JWT Token 进行 API 认证
- 实现用户数据隔离
- 密码安全存储

**Non-Goals:**
- 实现忘记密码/密码重置
- OAuth 第三方登录（后续扩展）
- 用户角色/权限管理（V1 只有普通用户）

## Decisions

### 1. JWT 认证方案

**决策**：使用 JWT（JSON Web Token）进行无状态认证

**理由**：
- 无状态，适合 REST API
- 可设置过期时间
- 客户端存储简单（localStorage）

**备选方案**：
- Session + Cookie → 需要服务端存储 Session
- API Key → 不适合多用户场景

### 2. 密码存储

**决策**：使用 bcrypt 加密存储密码

**理由**：
- 专为密码设计的哈希算法
- 可配置 cost factor 控制计算时间
- 防止彩虹表攻击

### 3. 用户数据存储

**决策**：ChromaDB metadata 添加 user_id 字段

```python
{
    "id": "uuid",
    "document": "...",
    "metadata": {
        "member_name": "林月",
        "attribute_type": "basic_info",
        "content": "...",
        "user_id": "user_uuid"  # 新增
    }
}
```

**理由**：复用现有 ChromaDB，不增加新存储

### 4. API 端点设计

```
POST /api/auth/register  - 用户注册
POST /api/auth/login     - 用户登录，返回 JWT
POST /api/auth/refresh   - 刷新 Token

# 以下端点需要认证
POST /api/add
POST /api/search
GET  /api/profile/:name
GET  /api/members
DELETE /api/member/:name
```

### 5. 认证中间件

```python
# 请求头格式
Authorization: Bearer <jwt_token>

# 中间件逻辑
1. 检查 Authorization 头
2. 验证 JWT 签名和过期时间
3. 从 Token 提取 user_id
4. 将 user_id 注入到请求上下文
```

## Risks / Trade-offs

[风险] JWT Token 泄露
→ **缓解措施**：短期 Token（1小时），敏感操作可要求 re-auth

[风险] 用户密码简单
→ **缓解措施**：注册时要求密码最少 8 位，包含字母和数字

[风险] 忘记 Token 过期
→ **缓解措施**：提供 refresh token 机制

## Migration Plan

1. 创建用户表/集合存储用户信息
2. 实现注册 API（密码加密）
3. 实现登录 API（返回 JWT）
4. 添加 JWT 认证中间件
5. 修改现有 API 添加 user_id 过滤
6. 添加注册/登录 UI 组件（前端）
7. 测试数据隔离

## Open Questions

- 是否需要 refresh token？（简单版用短期 Token 即可）
- 用户名是否需要唯一？（需要）
- 是否支持邮箱登录？（V1 用用户名即可）
