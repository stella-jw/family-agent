## Context

family-agent 使用 LangGraph 管理家庭成员信息的对话式工作流程。当前所有输入通过 `main.py` 中的 `input()` 以文本形式接收，数据存储在 ChromaDB 中（向量化存储）。

用户期望有跨平台应用（桌面端 + 移动端 + Web 端），提供以下输入入口：
- 文本输入（类聊天界面）
- 文件上传（JSON/CSV/TXT）
- 图片上传（通过视觉识别家庭成员）
- 语音输入（语音转文本）

## Goals / Non-Goals

**Goals:**
- 通过 REST API 向多客户端暴露现有 Python 后端
- 构建 Electron 桌面应用，提供多模态输入 UI
- 构建 Flutter 移动应用（iOS/Android），提供多模态输入 UI
- 构建 Vue 3 Web 应用，浏览器端即可访问
- 保留 graph.py 中的 classify→execute→respond 模式
- 复用现有 LLM 分类能力处理所有输入类型
- 在所有平台上提供一致的用户体验

**Non-Goals:**
- 实时语音流（仅支持批量 STT）
- 人脸识别/身份关联（仅描述可见内容）
- 修改 ChromaDB schema 或现有工具实现
- 原生移动应用（Flutter 处理跨平台）

## Decisions

### 1. REST API 作为后端接口

**决策**：创建 FastAPI REST 服务器，封装现有的 graph workflow

**理由**：REST 简单、广泛理解，与 family-agent 工作流的请求-响应无状态特性匹配良好。客户端（Electron、Flutter、Web）可以通过 HTTP 请求调用，无需嵌入 Python 逻辑。

**备选方案**：
- GraphQL → 对此场景过于复杂，增加复杂度
- WebSocket → 适合实时场景，但此场景不需要
- gRPC → 效率更高但通用性较差

### 2. Electron 桌面应用

**决策**：使用 Electron + Vue 3 前端

**理由**：用户选择 Electron。Electron 的 Node.js 后端可以本地运行 REST API 或连接远程 API 端点。

### 3. Flutter 移动应用

**决策**：使用 Flutter 的 http 包与 REST API 通信

**理由**：用户选择。Flutter 从单一代码库提供 iOS 和 Android 的原生体验。

### 4. Vue 3 Web 应用

**决策**：使用 Vue 3 + Vite + TypeScript 构建单页应用

**理由**：用户选择 Vue。Vue 3 组合式 API 适合复杂状态管理，Vite 提供快速的开发体验。

### 5. 适配器模式处理输入转换

**决策**：创建 `InputAdapter` 抽象层，在调用 `graph.invoke()` 前将 file/image/voice 转换为文本

**理由**：classify 节点基于 LLM，期望文本输入。在边界处将所有输入转换为文本可以保持现有 graph 流程不变。

### 6. API 端点设计

```
POST /api/add            - 添加家庭成员信息（文本/文件/图片/语音）
POST /api/search         - 搜索家庭成员信息
GET  /api/profile/:name - 获取成员档案
GET  /api/members       - 列出所有成员
DELETE /api/member/:name - 删除成员
```

### 7. 文件格式支持

**决策**：按优先级支持 `.json` → `.csv` → `.txt`

**理由**：JSON/CSV 有结构化 schema，能清晰映射到家庭成员属性。TXT 通过现有 classify 流程进行自由文本解析。

## 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        REST API (FastAPI)                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐│
│  │ /api/add    │  │ /api/search │  │ /api/profile/:name      ││
│  └──────┬──────┘  └──────┬──────┘  └───────────┬─────────────┘│
└─────────┼────────────────┼─────────────────────┼────────────────┘
          │                │                     │
    ┌─────┴─────┐    ┌──────┴──────┐        ┌─────┴─────┐
    │适配器     │    │  Graph      │        │ ChromaDB  │
    │(file/image│    │  (现有)     │        │ (现有     │
    │ /voice)   │───▶│  工作流     │───────▶│ 存储)     │
    └───────────┘    └─────────────┘        └───────────┘
```

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Electron    │  │   Flutter     │  │    Vue       │
│  Desktop     │  │   Mobile      │  │    Web       │
│  App         │  │   App         │  │    App       │
│              │  │              │  │              │
│[文本][文件] │  │[文本][文件]  │  │[文本][文件] │
│[图片][语音] │  │[图片][语音]  │  │[图片][语音] │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │ HTTP/REST        │ HTTP/REST       │ HTTP/REST
       └──────────────────┴───────┬────────┘
                                  ▼
                         ┌───────────────┐
                         │   REST API    │
                         │   (FastAPI)   │
                         └───────────────┘
```

## Risks / Trade-offs

[风险] 视觉模型可能无法正确识别照片中的关系
→ **缓解措施**：视觉模型输出观察结果（性别、年龄、明显关系），classify 节点使用 LLM 推断正确的关系术语

[风险] 大图片文件可能超过 API payload 限制
→ **缓解措施**：发送前将图片缩放到最大 2048px

[风险] STT 准确度可能因口音/噪音而异
→ **缓解措施**：处理前向用户展示转录文本供确认

[风险] 文件编码问题（非 UTF-8 CSV/TXT）
→ **缓解措施**：尝试多种编码（utf-8、gbk、gb2312）逐一尝试

[风险] Web 端浏览器录音权限限制
→ **缓解措施**：首次使用语音时引导用户授权，备选文件上传方式

[风险] 移动应用离线使用
→ **缓解措施**：初期版本需要网络连接，离线模式作为后续增强

## Migration Plan

**阶段 1：REST API（后端）**
1. 创建 FastAPI 服务器项目结构
2. 定义与 graph workflow 输入匹配的 API 端点
3. 将现有 graph.invoke() 集成到 API 请求处理器
4. 添加 CORS 支持，供所有客户端访问

**阶段 2：Electron 桌面应用**
1. 使用 npm 创建 Electron + Vue 3 项目
2. 构建输入模式选择器 UI（文本/文件/图片/语音）
3. 实现文件选择器和图片上传
4. 使用 WebAudio API 实现语音录制
5. 将 UI 连接到 REST API 后端

**阶段 3：Flutter 移动应用**
1. 创建 Flutter 项目
2. 构建与桌面端相同的输入模式 UI
3. 实现平台特定的图片选择器
4. 实现平台特定的音频录制
5. 将 UI 连接到 REST API 后端

**阶段 4：Vue Web 应用**
1. 使用 Vite 创建 Vue 3 + TypeScript 项目
2. 构建与桌面端相同的输入模式 UI
3. 实现浏览器 File API 进行文件上传
4. 使用 MediaRecorder API 实现浏览器内语音录制
5. 使用 Fetch API 连接到 REST API 后端
6. 部署到静态托管服务器

## Open Questions

- REST API 是否需要认证？（V1 可以开放，认证后续添加）
- Web 应用部署在哪里？（Vercel / Netlify / 自建服务器？）
- 桌面应用：运行本地 API 服务器还是连接远程？
- 移动应用：打包本地 API 还是始终连接远程？
- 语音输入：连续监听（多轮）还是单次说话？
