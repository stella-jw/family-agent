## Why

当前 family-agent 仅支持 CLI 文本输入，限制了可用性和数据录入便捷性。用户期望有跨平台应用（桌面端 + 移动端 + Web 端），提供文件上传、文本、图片、语音输入的 UI 入口，同时复用现有的 Python 后端核心能力。

## What Changes

- **REST API 层**：通过 FastAPI REST 接口暴露现有的 Python graph workflow
- **Electron 桌面应用**：跨平台桌面 UI，支持文件选择器、图片上传、语音录制
- **Flutter 移动应用**：iOS/Android 移动 UI，提供相同的输入方式
- **Vue Web 应用**：浏览器端 SPA，支持文件上传、图片上传、语音录制
- **后端多模态适配器**：文件处理（JSON/CSV/TXT）、图片处理（视觉 LLM）、语音处理（STT）
- 所有平台共享同一个 REST API 后端，保证行为一致性

## Capabilities

### New Capabilities

- `rest-api`：REST API 层，向外部客户端暴露 family-agent graph workflow
- `desktop-app`：基于 Electron 的桌面应用，提供多模态输入 UI
- `mobile-app`：基于 Flutter 的移动应用（iOS/Android），提供多模态输入 UI
- `web-app`：基于 Vue 3 的 Web 单页应用，提供多模态输入 UI
- `file-import`：解析结构化文件（JSON/CSV）和自由文本文件，提取并添加家庭成员信息
- `image-recognition`：接受照片输入，使用视觉 LLM 识别人物并描述属性，将结果添加到知识库
- `voice-input`：接受音频输入，通过 STT 服务将语音转换为文本，作为普通文本输入处理

### Modified Capabilities

- （无）

## Impact

- **backend/api/**：新的 REST API 服务器（FastAPI），封装 graph workflow
- **desktop/**：新的 Electron 项目，用于桌面 UI
- **mobile/**：新的 Flutter 项目，用于移动 UI
- **web/**：新的 Vue 3 项目，用于 Web UI
- **adapters/**：输入适配器类（FileInputAdapter、ImageInputAdapter、VoiceInputAdapter）
- **config.py**：新增 API 服务器、视觉模型、STT 端点的配置字段
- **现有流程**：不变——适配器在调用 `graph.invoke()` 前将输入转换为文本
