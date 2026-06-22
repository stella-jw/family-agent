## Context

用户需要通过桌面应用访问 family-agent。Electron 应用需要连接到 `add-rest-api` 提供的 REST API，提供桌面原生体验。

## Goals / Non-Goals

**Goals:**
- 构建 Electron 跨平台桌面应用（Windows/macOS/Linux）
- 提供文本/文件/图片/语音四种输入模式
- 桌面原生体验（系统托盘、窗口管理）
- 连接到 REST API 后端

**Non-Goals:**
- 实现后端 API（由 add-rest-api 负责）
- 实现 Web 或移动应用

## Decisions

### 1. Electron + Vue 3

**决策**：使用 Electron 作为桌面框架，Vue 3 作为前端框架

**理由**：
- 成熟的跨平台桌面解决方案
- Web 技术栈统一（与 Vue Web 应用共享代码）
- Node.js 后端可运行本地 API 服务器

### 2. 项目结构

```
desktop/
├── electron/
│   ├── main.ts              # Electron 主进程
│   ├── preload.ts            # 预加载脚本
│   └── ipc/                  # IPC 通信
├── src/
│   ├── components/           # Vue 组件（与 Web 共享）
│   ├── App.vue
│   └── main.ts
├── package.json
└── vite.config.ts
```

### 3. 本地 API 服务器选项

**决策**：Electron 可选择连接本地或远程 API

**理由**：
- 开发模式：Electron 内嵌本地 FastAPI 服务器
- 生产模式：连接远程 API 或本地已安装的服务

### 4. 桌面特性

- **系统托盘**：最小化到托盘，后台运行
- **窗口管理**：记住窗口位置和大小
- **本地文件**：直接拖拽文件到窗口上传
- **快捷键**：全局快捷键呼起应用

## Risks / Trade-offs

[风险] Electron 包体积较大
→ **缓解措施**：使用 electron-builder 优化打包

[风险] 多平台打包配置复杂
→ **缓解措施**：使用 GitHub Actions 进行 CI/CD 多平台构建

[风险] 本地 API 服务器端口冲突
→ **缓解措施**：动态端口分配，配置文件记录

## Migration Plan

1. 创建 Electron + Vite + Vue 3 项目
2. 配置 Electron 主进程和预加载脚本
3. 复用或适配 Web 端的 Vue 组件
4. 实现本地文件拖拽
5. 添加系统托盘功能
6. 配置多平台打包
7. 测试和发布
