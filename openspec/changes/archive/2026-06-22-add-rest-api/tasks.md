## 1. 项目结构和依赖

- [x] 1.1 创建 backend/api/ 目录结构
- [x] 1.2 添加 FastAPI、uvicorn 到依赖
- [x] 1.3 创建 config.py 配置项（API 服务器、视觉模型、STT 端点）
- [x] 1.4 创建 adapters/ 目录和 __init__.py
- [x] 1.5 在 adapters/base.py 中创建 InputAdapter 抽象基类

## 2. FastAPI 核心实现

- [x] 2.1 创建 backend/api/main.py FastAPI 应用入口
- [x] 2.2 配置 CORS 中间件允许前端跨域
- [x] 2.3 实现 GET /api/health 健康检查端点
- [x] 2.4 实现 POST /api/add 添加信息端点
- [x] 2.5 实现 POST /api/search 搜索端点
- [x] 2.6 实现 GET /api/profile/{name} 档案端点
- [x] 2.7 实现 GET /api/members 成员列表端点
- [x] 2.8 实现 DELETE /api/member/{name} 删除端点
- [x] 2.9 添加统一的错误处理和日志记录

## 3. FileInputAdapter 实现

- [x] 3.1 在 adapters/file_adapter.py 中实现 FileInputAdapter 类
- [x] 3.2 实现 JSON 解析（数组和嵌套-members 结构）
- [x] 3.3 实现 CSV 解析（表头映射）
- [x] 3.4 实现 TXT 文件读取（编码检测：UTF-8、GBK、GB2312）
- [x] 3.5 实现文件大小验证（最大 10MB）
- [x] 3.6 实现 detect_input_mode() 文件类型检测

## 4. ImageRecognitionAdapter 实现

- [x] 4.1 在 adapters/image_adapter.py 中实现 ImageInputAdapter 类
- [x] 4.2 使用 PIL 添加图片加载（支持 JPEG、PNG、WebP）
- [x] 4.3 实现图片缩放（最长边最大 2048px）
- [x] 4.4 集成视觉 LLM（MiniMax VL 或 GPT-4o）
- [x] 4.5 设计家庭成员描述提取的 prompt
- [x] 4.6 实现识别结果确认流程（由前端处理）

## 5. VoiceInputAdapter 实现

- [x] 5.1 在 adapters/voice_adapter.py 中实现 VoiceInputAdapter 类
- [x] 5.2 添加音频格式验证（WAV、MP3）
- [x] 5.3 集成 STT 服务（MiniMax T2A 或 Whisper API）
- [x] 5.4 实现转录文本确认流程（由前端处理）
- [x] 5.5 添加音频超时处理（由前端处理）

## 6. Graph 集成

- [x] 6.1 将 graph.invoke() 集成到 API 请求处理器
- [x] 6.2 处理输入类型路由（text/file/image/voice → classify）
- [x] 6.3 复用 ChromaDB 连接和配置
- [x] 6.4 实现添加前检查成员是否已存在（存在则update，否则add）
- [x] 6.5 实现部分字段更新（只更新传入的字段，保留其他字段）

## 7. 测试和验证

- [ ] 7.1 启动 API 服务器并验证健康检查
- [ ] 7.2 测试 POST /api/add 文本输入
- [ ] 7.3 测试文件上传（JSON、CSV、TXT）
- [ ] 7.4 测试图片上传和视觉识别
- [ ] 7.5 测试语音输入和 STT 转换
- [ ] 7.6 测试所有 CRUD 端点
- [ ] 7.7 测试 CORS 跨域请求
- [ ] 7.8 验证现有 CLI 流程仍正常工作
