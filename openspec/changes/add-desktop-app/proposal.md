## Why

用户需要通过桌面应用访问 family-agent，提供更丰富的本地集成能力（如本地文件访问、系统通知、窗口管理），以及更稳定的桌面端体验。

## What Changes

- **Electron 桌面应用**：使用 Electron + Vue 3 构建跨平台桌面 UI
- **输入模式选择器**：文本/文件/图片/语音四种输入模式
- **REST API 集成**：连接后端 API（本地或远程）
- **桌面特性**：系统托盘、窗口管理、本地文件访问

## Capabilities

### New Capabilities

- `desktop-app`：基于 Electron 的桌面应用，提供多模态输入 UI

### Modified Capabilities

- （无）

## Impact

- **desktop/**：新增 Electron 项目目录
- 依赖 `add-rest-api` 提供后端 API 支持
