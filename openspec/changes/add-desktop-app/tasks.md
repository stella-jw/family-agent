## 1. 项目初始化

- [ ] 1.1 创建 Electron + Vite + Vue 3 项目
- [ ] 1.2 配置 electron-builder 打包工具
- [ ] 1.3 创建 Electron 主进程（electron/main.ts）
- [ ] 1.4 创建预加载脚本（electron/preload.ts）
- [ ] 1.5 配置 Vite 和 Electron 集成

## 2. 主进程功能

- [ ] 2.1 实现窗口创建和管理
- [ ] 2.2 实现系统托盘功能
- [ ] 2.3 实现 IPC 通信机制
- [ ] 2.4 添加全局快捷键支持
- [ ] 2.5 实现窗口状态持久化（位置、大小）

## 3. 基础 UI 结构

- [ ] 3.1 复用 Web 端 Vue 组件或创建适配版本
- [ ] 3.2 创建 InputModeSelector 输入模式选择器
- [ ] 3.3 实现与 Web 端一致的四模式切换

## 4. 文本输入组件

- [ ] 4.1 复用或适配 Web 端 TextInput 组件
- [ ] 4.2 实现发送逻辑和状态处理

## 5. 文件上传组件

- [ ] 5.1 复用或适配 Web 端 FileUpload 组件
- [ ] 5.2 添加拖拽文件到窗口的支持
- [ ] 5.3 实现文件预览

## 6. 图片上传组件

- [ ] 6.1 复用或适配 Web 端 ImageUpload 组件
- [ ] 6.2 实现图片预览

## 7. 语音录制组件

- [ ] 7.1 复用或适配 Web 端 VoiceRecord 组件
- [ ] 7.2 使用 WebAudio API 实现录音

## 8. API 服务集成

- [ ] 8.1 创建 Electron 专属的 API 服务
- [ ] 8.2 实现 /api/add 文本/文件/图片/语音上传
- [ ] 8.3 实现 /api/search、/api/members、/api/profile/:name
- [ ] 8.4 支持本地 API（localhost）和远程 API 配置
- [ ] 8.5 添加连接状态检测和重连

## 9. 结果展示组件

- [ ] 9.1 复用或适配 Web 端 ResponseDisplay 组件
- [ ] 9.2 格式化显示结果

## 10. 打包和发布

- [ ] 10.1 配置 Windows .exe 打包
- [ ] 10.2 配置 macOS .dmg/.app 打包
- [ ] 10.3 配置 Linux AppImage 打包
- [ ] 10.4 添加自动更新功能（electron-updater）
- [ ] 10.5 端到端测试：桌面 App → REST API → 数据存储
