## Why

当前 family-agent 仅支持 CLI 文本输入，无法被前端应用调用。需要通过 REST API 暴露后端能力，并添加文件解析、图片识别、语音转文本的多模态输入支持，供 Electron/Vue/Flutter 等前端应用调用。

## What Changes

- **FastAPI REST API**：创建 REST 服务器，封装 graph.invoke() 调用
- **文件解析适配器**：支持 JSON/CSV/TXT 文件解析
- **图片识别适配器**：支持图片上传和视觉 LLM 识别
- **语音输入适配器**：支持音频录制和 STT 转换
- **CORS 支持**：允许前端跨域访问 API

## Capabilities

### New Capabilities

- `rest-api`：REST API 层，向外部客户端暴露 family-agent 功能
- `file-import`：解析 JSON/CSV/TXT 文件，提取家庭成员信息
- `image-recognition`：接受图片输入，使用视觉 LLM 识别人物并描述
- `voice-input`：接受音频输入，通过 STT 将语音转换为文本

### Modified Capabilities

- （无）

## Impact

- **backend/api/**：新增 FastAPI REST 服务器
- **adapters/**：新增输入适配器目录（FileInputAdapter、ImageRecognitionAdapter、VoiceInputAdapter）
- **config.py**：新增 API 服务器、视觉模型、STT 配置项
- **现有流程**：保持不变，适配器在调用 graph.invoke() 前转换输入
