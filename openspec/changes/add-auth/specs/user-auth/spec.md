## ADDED Requirements

### Requirement: 用户注册
The system SHALL allow new users to register with username and password.

#### Scenario: 成功注册
- **WHEN** user sends POST /api/auth/register with `{"username": "zhangsan", "password": "Pass1234"}`
- **THEN** system creates user, stores hashed password, returns `{"success": true, "message": "注册成功"}`

#### Scenario: 用户名已存在
- **WHEN** user tries to register with existing username
- **THEN** system returns `{"success": false, "message": "用户名已存在"}`

#### Scenario: 密码不符合要求
- **WHEN** user registers with password "123" (less than 8 chars)
- **THEN** system returns `{"success": false, "message": "密码至少8位，需包含字母和数字"}`

### Requirement: 用户登录
The system SHALL allow registered users to login and receive JWT token.

#### Scenario: 成功登录
- **WHEN** user sends POST /api/auth/login with correct credentials
- **THEN** system returns `{"success": true, "token": "<jwt_token>", "expires_in": 3600}`

#### Scenario: 密码错误
- **WHEN** user sends POST /api/auth/login with wrong password
- **THEN** system returns `{"success": false, "message": "用户名或密码错误"}`

#### Scenario: 用户不存在
- **WHEN** user sends POST /api/auth/login with non-existent username
- **THEN** system returns `{"success": false, "message": "用户名或密码错误"}`

### Requirement: JWT Token 验证
The system SHALL validate JWT token on protected endpoints.

#### Scenario: 有效 Token
- **WHEN** request includes valid `Authorization: Bearer <token>` header
- **THEN** request is processed with user context

#### Scenario: 无 Token
- **WHEN** request has no Authorization header
- **THEN** system returns 401 Unauthorized

#### Scenario: 过期 Token
- **WHEN** request includes expired JWT token
- **THEN** system returns 401 Unauthorized with "Token 已过期"

#### Scenario: 无效 Token
- **WHEN** request includes malformed JWT token
- **THEN** system returns 401 Unauthorized

### Requirement: 密码安全存储
The system SHALL store passwords using bcrypt hashing.

#### Scenario: 密码加密
- **WHEN** user registers with password "Pass1234"
- **THEN** system stores bcrypt hash, never stores plaintext password

#### Scenario: 相同密码不同哈希
- **WHEN** two users register with same password
- **THEN** stored hashes are different (due to salt)
