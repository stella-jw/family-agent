## Context

family-agent 使用 LangGraph 管理家庭成员信息工作流，当前仅支持 CLI 文本输入。需扩展为 REST API 服务，供 Electron/Vue/Flutter 等前端调用，并支持文件、图片、语音多模态输入。

## Goals / Non-Goals

**Goals:**
- 通过 REST API 向外部客户端暴露现有 Python 后端能力
- 支持文件（JSON/CSV/TXT）、图片、语音多种输入方式
- 保持现有 graph workflow 不变，适配器在边界处转换输入
- 提供一致的 API 接口供多端调用

**Non-Goals:**
- 实现前端应用（由 add-web-app/add-mobile-app/add-desktop-app 负责）
- 修改 ChromaDB schema
- 实时语音流处理

## Decisions

### 1. FastAPI 作为 REST 框架

**决策**：使用 FastAPI 构建 REST API

**理由**：
- 异步支持好，与 LangGraph 异步调用匹配
- 自动生成 OpenAPI 文档
- 类型安全，与 Python 类型提示配合良好
- 轻量级，学习曲线低

**备选方案**：
- Flask → 缺少自动文档和类型验证
- Django → 过于重量级
- 纯 ASGI → 需要自己处理很多细节

### 2. API 端点设计

```
POST /api/add            - 添加家庭成员信息（支持文本/文件/图片/语音）
POST /api/search         - 搜索家庭成员信息
GET  /api/profile/:name  - 获取成员完整档案
GET  /api/members        - 列出所有成员
DELETE /api/member/:name - 删除成员
GET  /api/health         - 健康检查
```

### 3. 输入模式检测

**决策**：API 接收预转换的文本或直接处理文件/图片/语音

**理由**：适配器在后端实现，统一处理逻辑。前端只需传递原始数据。

**API 请求格式**：
```json
{
  "input_type": "text" | "file" | "image" | "voice",
  "content": "文本内容或 base64 编码的文件/图片/音频"
}
```

### 4. 适配器模式

**决策**：在 API 层下使用适配器层处理不同输入类型

```
API Request → InputAdapter → Graph Workflow → ChromaDB
                  ↑
    ┌─────────────┼─────────────┐
    │             │             │
FileAdapter  ImageAdapter  VoiceAdapter
```

### 5. 文件格式支持

**决策**：按优先级支持 `.json` → `.csv` → `.txt`

**理由**：JSON/CSV 有结构化 schema，TXT 通过 classify 流程解析。

### 6. 视觉模型选择

**决策**：使用 MiniMax VL 或 GPT-4o（可配置）

**理由**：与现有 LLM 选择保持一致。

### 7. STT 服务选择

**决策**：使用 MiniMax T2A 或 Whisper API（可配置）

**理由**：可复用现有 API 账户，服务质量有保障。

## Risks / Trade-offs

[风险] 大文件上传可能超时或占用过多内存
→ **缓解措施**：限制文件大小 10MB，图片压缩到 2048px

[风险] 视觉模型识别不准确
→ **缓解措施**：返回识别结果供用户确认后再存储

[风险] 语音转文本准确度受噪音/口音影响
→ **缓解措施**：显示转录文本供用户确认

[风险] API 并发请求处理
→ **缓解措施**：配置合适的工作线程数，添加请求限流

## Migration Plan

1. 创建 backend/api/ 目录结构
2. 实现 FastAPI 核心（路由、CORS、错误处理）
3. 集成现有 graph.invoke()
4. 实现 FileInputAdapter
5. 实现 ImageRecognitionAdapter
6. 实现 VoiceInputAdapter
7. 添加配置管理
8. 测试和部署

## Open Questions

- 是否需要认证？（V1 开放，V2 添加 JWT）
- 是否需要 API 版本控制？（V1 用 /api/v1 前缀）
- 文件存储：内存还是临时文件？
