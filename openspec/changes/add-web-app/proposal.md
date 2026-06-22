## Why

用户需要通过浏览器访问 family-agent，提供文件上传、文本输入、图片上传、语音录制等 UI 入口，无需安装桌面或移动应用即可使用。

## What Changes

- **Vue 3 单页应用**：使用 Vite + TypeScript 构建响应式 Web UI
- **输入模式选择器**：文本/文件/图片/语音四种输入模式
- **REST API 集成**：通过 Fetch API 连接后端 API
- **响应式设计**：支持桌面和移动浏览器访问

## Capabilities

### New Capabilities

- `web-app`：基于 Vue 3 的 Web 单页应用，提供多模态输入 UI

### Modified Capabilities

- （无）

## Impact

- **web/**：新增 Vue 3 项目目录
- 依赖 `add-rest-api` 提供后端 API 支持
