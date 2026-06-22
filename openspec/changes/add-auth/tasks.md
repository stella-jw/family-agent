## 1. 用户数据模型

- [ ] 1.1 设计用户数据结构（username、password_hash、created_at）
- [ ] 1.2 选择用户存储方案（ChromaDB 内或 SQLite）
- [ ] 1.3 实现用户模型类

## 2. 密码安全

- [ ] 2.1 添加 bcrypt 依赖
- [ ] 2.2 实现密码哈希函数
- [ ] 2.3 实现密码验证函数
- [ ] 2.4 验证相同密码生成不同哈希（salt）

## 3. 注册 API

- [ ] 3.1 实现 POST /api/auth/register 端点
- [ ] 3.2 添加用户名唯一性检查
- [ ] 3.3 添加密码强度验证（最少 8 位，字母+数字）
- [ ] 3.4 密码加密存储
- [ ] 3.5 返回注册成功响应

## 4. 登录 API

- [ ] 4.1 实现 POST /api/auth/login 端点
- [ ] 4.2 验证用户名和密码
- [ ] 4.3 生成 JWT Token
- [ ] 4.4 返回 Token 和过期时间

## 5. JWT 认证中间件

- [ ] 5.1 添加 PyJWT 依赖
- [ ] 5.2 实现 JWT 签名和验证函数
- [ ] 5.3 实现认证中间件
- [ ] 5.4 提取 user_id 注入请求上下文
- [ ] 5.5 处理 Token 过期情况

## 6. API 端点保护

- [ ] 6.1 为 /api/add 添加认证要求
- [ ] 6.2 为 /api/search 添加认证要求
- [ ] 6.3 为 /api/profile/:name 添加认证要求
- [ ] 6.4 为 /api/members 添加认证要求
- [ ] 6.5 为 /api/member/:name 添加认证要求
- [ ] 6.6 /api/auth/* 端点保持公开

## 7. 数据隔离实现

- [ ] 7.1 修改 ChromaDB 存储添加 user_id metadata
- [ ] 7.2 修改 /api/add 自动注入 user_id
- [ ] 7.3 修改 /api/search 过滤 user_id
- [ ] 7.4 修改 /api/profile/:name 验证 user_id
- [ ] 7.5 修改 /api/members 只返回当前用户数据
- [ ] 7.6 修改 /api/member/:name 删除验证 user_id

## 8. 前端登录/注册 UI

- [ ] 8.1 在 Web 端添加登录表单组件
- [ ] 8.2 在 Web 端添加注册表单组件
- [ ] 8.3 实现 Token 存储（localStorage）
- [ ] 8.4 实现请求自动携带 Token
- [ ] 8.5 实现登录状态管理
- [ ] 8.6 在 Mobile/App 添加登录/注册 UI（如需要）
- [ ] 8.7 在 Desktop/App 添加登录/注册 UI（如需要）

## 9. 测试

- [ ] 9.1 测试注册：成功/用户名重复/密码不符合要求
- [ ] 9.2 测试登录：成功/密码错误/用户不存在
- [ ] 9.3 测试 Token：有效/无效/过期
- [ ] 9.4 测试数据隔离：用户 A 无法访问用户 B 的数据
- [ ] 9.5 测试遗留数据（无 user_id）不可访问
- [ ] 9.6 端到端测试：注册 → 登录 → 添加数据 → 查询数据
