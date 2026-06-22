## 1. REST API 后端搭建

- [ ] 1.1 创建 FastAPI 项目结构（backend/api/）
- [ ] 1.2 定义 API 端点：POST /api/add、POST /api/search、GET /api/profile/:name、GET /api/members、DELETE /api/member/:name
- [ ] 1.3 将 graph.invoke() 集成到 API 请求处理器
- [ ] 1.4 添加 CORS 中间件支持跨域请求
- [ ] 1.5 添加 API 错误处理和日志记录

## 2. 配置和适配器基础设施

- [ ] 2.1 在 config.py 中添加新配置字段（API 服务器、视觉模型、STT 端点）
- [ ] 2.2 创建 adapters/ 目录和 __init__.py
- [ ] 2.3 在 adapters/base.py 中创建基类 InputAdapter 抽象类

## 3. FileImportAdapter 实现

- [ ] 3.1 在 adapters/file_adapter.py 中实现 FileInputAdapter 类
- [ ] 3.2 添加 JSON 解析支持（数组和嵌套-members 结构检测）
- [ ] 3.3 添加 CSV 解析（表头映射和 LLM 列名推断）
- [ ] 3.4 添加 TXT 文件读取（编码检测：UTF-8、GBK、GB2312）
- [ ] 3.5 添加文件大小验证（最大 10MB）
- [ ] 3.6 实现 detect_input_mode() 方法进行文件类型检测

## 4. ImageRecognitionAdapter 实现

- [ ] 4.1 在 adapters/image_adapter.py 中实现 ImageInputAdapter 类
- [ ] 4.2 使用 PIL 添加图片加载（支持 JPEG、PNG、WebP）
- [ ] 4.3 实现图片缩放（最长边最大 2048px）
- [ ] 4.4 集成视觉 LLM（MiniMax VL 或 GPT-4o）进行图片分析
- [ ] 4.5 设计家庭成员描述提取的 prompt
- [ ] 4.6 在添加到知识库前实现确认流程

## 5. VoiceInputAdapter 实现

- [ ] 5.1 在 adapters/voice_adapter.py 中实现 VoiceInputAdapter 类
- [ ] 5.2 使用 pyaudio 或类似库添加音频录制功能
- [ ] 5.3 集成 STT 服务（MiniMax T2A 或 Whisper API）
- [ ] 5.4 实现转录文本确认流程
- [ ] 5.5 添加 30 秒静音检测和超时处理
- [ ] 5.6 支持 WAV 和 MP3 格式转换（如需要）

## 6. Electron 桌面应用

- [ ] 6.1 使用 npm 创建 Electron + Vue 3 项目
- [ ] 6.2 构建输入模式选择器 UI（文本/文件/图片/语音）
- [ ] 6.3 实现文件选择器和图片上传组件
- [ ] 6.4 使用 WebAudio API 实现语音录制组件
- [ ] 6.5 将 UI 连接到 REST API 后端
- [ ] 6.6 添加响应展示和错误处理

## 7. Flutter 移动应用

- [ ] 7.1 创建 Flutter 项目
- [ ] 7.2 构建与桌面端相同的输入模式 UI
- [ ] 7.3 实现平台特定的图片选择器（image_picker）
- [ ] 7.4 实现平台特定的音频录制（record）
- [ ] 7.5 使用 http 包连接 REST API 后端
- [ ] 7.6 添加响应展示和错误处理

## 8. Vue Web 应用

- [ ] 8.1 使用 Vite 创建 Vue 3 + TypeScript 项目
- [ ] 8.2 构建与桌面端相同的输入模式 UI（响应式设计）
- [ ] 8.3 使用浏览器 File API 实现文件选择和图片预览
- [ ] 8.4 使用 MediaRecorder API 实现浏览器内语音录制
- [ ] 8.5 使用 Fetch API 连接到 REST API 后端
- [ ] 8.6 处理浏览器录音权限申请和降级处理
- [ ] 8.7 部署配置（Vercel/Netlify/其他静态托管）

## 9. 测试和验证

- [ ] 9.1 使用示例 JSON、CSV、TXT 文件测试 FileImportAdapter
- [ ] 9.2 使用示例照片测试 ImageRecognitionAdapter
- [ ] 9.3 使用麦克风输入测试 VoiceInputAdapter
- [ ] 9.4 验证现有文本输入流程仍正常工作
- [ ] 9.5 测试错误处理（无效文件、API 失败、编码错误）
- [ ] 9.6 端到端测试：桌面 App → REST API → 添加/查询数据
- [ ] 9.7 端到端测试：移动 App → REST API → 添加/查询数据
- [ ] 9.8 端到端测试：Web App → REST API → 添加/查询数据
- [ ] 9.9 浏览器兼容性测试（Chrome、Firefox、Safari、Edge）
