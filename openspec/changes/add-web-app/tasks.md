## 1. 项目初始化

- [x] 1.1 使用 Vite 创建 Vue 3 + TypeScript 项目
- [x] 1.2 配置项目结构（components/composables/assets）
- [x] 1.3 安装依赖（vue-router、axios 或 fetch）
- [x] 1.4 配置 Vite 代理解决开发环境 CORS

## 2. 基础组件开发

- [x] 2.1 创建 App.vue 主组件布局
- [x] 2.2 创建 InputModeSelector.vue 输入模式选择器
- [x] 2.3 创建基础样式和响应式布局

## 3. 文本输入组件

- [x] 3.1 创建 TextInput.vue 文本输入组件
- [x] 3.2 实现文本输入和发送逻辑
- [x] 3.3 添加加载状态和错误处理

## 4. 文件上传组件

- [x] 4.1 创建 FileUpload.vue 文件上传组件
- [x] 4.2 实现文件选择和预览
- [x] 4.3 支持 JSON/CSV/TXT 文件类型
- [x] 4.4 添加文件大小验证（最大 10MB）

## 5. 图片上传组件

- [x] 5.1 创建 ImageUpload.vue 图片上传组件
- [x] 5.2 实现图片选择和预览
- [x] 5.3 支持 JPEG/PNG/WebP 格式
- [x] 5.4 添加图片压缩或大小提示

## 6. 语音录制组件

- [x] 6.1 创建 VoiceRecord.vue 语音录制组件
- [x] 6.2 使用 MediaRecorder API 实现录音
- [x] 6.3 实现录音/停止/播放功能
- [x] 6.4 处理麦克风权限申请
- [x] 6.5 添加录音超时处理（30秒）

## 7. API 集成

- [x] 7.1 创建 useApi.ts composable 封装 API 调用
- [x] 7.2 实现 /api/add 文本输入
- [x] 7.3 实现 /api/add 文件上传
- [x] 7.4 实现 /api/add 图片上传
- [x] 7.5 实现 /api/add 语音上传
- [x] 7.6 实现 /api/search 搜索
- [x] 7.7 实现 /api/members 列表
- [x] 7.8 实现 /api/profile/:name 详情

## 8. 结果展示组件

- [x] 8.1 创建 ResponseDisplay.vue 结果展示组件
- [x] 8.2 格式化显示添加/搜索结果
- [x] 8.3 添加成功/失败状态展示

## 9. 测试和部署

- [ ] 9.1 浏览器兼容性测试（Chrome、Firefox、Safari、Edge）
- [ ] 9.2 响应式布局测试（桌面 1920px / 移动 375-428px）
- [ ] 9.3 配置 Vercel/Netlify 部署
- [ ] 9.4 端到端测试：Web → REST API → 数据存储
