## ADDED Requirements

### Requirement: REST API 服务可启动并响应请求
The system SHALL provide a FastAPI server that starts on configured host:port and responds to HTTP requests.

#### Scenario: 启动 API 服务器
- **WHEN** API server starts with `uvicorn backend.api.main:app`
- **THEN** server listens on configured host (default 0.0.0.0) and port (default 8000)

#### Scenario: 健康检查端点
- **WHEN** client sends GET /api/health
- **THEN** server returns `{"status": "ok"}` with 200 status code

### Requirement: 添加家庭成员信息（存在则update，不存在则add）
The system SHALL accept family member information via POST /api/add and process it through the graph workflow. Before adding, system SHALL check if member already exists → exists则update，否则add。

#### Scenario: 添加新成员
- **WHEN** client sends POST /api/add with `{"input_type": "text", "content": "我老婆叫林月，是一名中学老师"}`
- **THEN** server checks if 林月 exists → not exists, so adds new record and returns `{"success": true, "message": "已添加林月的信息"}`

#### Scenario: 更新已存在成员
- **WHEN** client sends POST /api/add with `{"input_type": "text", "content": "林月是中学老师"}` and 林月 already exists
- **THEN** server checks if 林月 exists → exists, so updates existing record and returns `{"success": true, "message": "已更新林月的信息"}`

#### Scenario: 添加图片信息（识别后确认）
- **WHEN** client sends POST /api/add with `{"input_type": "image", "content": "<base64>"}`
- **THEN** server processes image through vision LLM, returns recognized descriptions for user confirmation

### Requirement: 搜索家庭成员信息
The system SHALL search family member information via POST /api/search.

#### Scenario: 搜索成员
- **WHEN** client sends POST /api/search with `{"query": "林月"}`
- **THEN** server returns matching records from ChromaDB

### Requirement: 获取成员完整档案
The system SHALL return complete profile for a member via GET /api/profile/{name}.

#### Scenario: 获取档案
- **WHEN** client sends GET /api/profile/林月
- **THEN** server returns all stored information about 林月

### Requirement: 列出所有成员
The system SHALL return list of all family members via GET /api/members.

#### Scenario: 列出成员
- **WHEN** client sends GET /api/members
- **THEN** server returns `{"members": ["林月", "张三", ...]}`

### Requirement: 删除成员
The system SHALL delete member via DELETE /api/member/{name}.

#### Scenario: 删除成员
- **WHEN** client sends DELETE /api/member/林月
- **THEN** server deletes all records for 林月 and returns `{"success": true}`

### Requirement: CORS 支持
The system SHALL enable CORS to allow frontend clients to access the API.

#### Scenario: 前端跨域请求
- **WHEN** Vue/Electron app sends request from different origin
- **THEN** server responds with appropriate CORS headers allowing the origin

### Requirement: 错误处理
The system SHALL return appropriate error responses with status codes and messages.

#### Scenario: 处理无效请求
- **WHEN** client sends invalid request body
- **THEN** server returns 422 Unprocessable Entity with validation error details

#### Scenario: 处理服务器错误
- **WHEN** internal error occurs during processing
- **THEN** server returns 500 Internal Server Error with error message (without exposing internals)
