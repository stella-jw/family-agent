## Context

用户需要通过浏览器访问 family-agent。Web 应用需要连接到 `add-rest-api` 提供的 REST API，呈现与桌面/移动端一致的多模态输入体验。

## Goals / Non-Goals

**Goals:**
- 构建 Vue 3 单页应用，浏览器即可访问
- 提供文本/文件/图片/语音四种输入模式
- 响应式设计，适配桌面和移动浏览器
- 连接到 REST API 后端

**Non-Goals:**
- 实现后端 API（由 add-rest-api 负责）
- 实现 Electron 桌面应用或 Flutter 移动应用
- 离线支持

## Decisions

### 1. Vue 3 + Vite + TypeScript

**决策**：使用 Vite 作为构建工具，Vue 3 组合式 API，TypeScript 类型支持

**理由**：
- Vite 快速的开发体验
- Vue 3 组合式 API 适合复杂状态管理
- TypeScript 提供类型安全

### 2. 项目结构

```
web/
├── src/
│   ├── components/
│   │   ├── InputModeSelector.vue    # 输入模式选择
│   │   ├── TextInput.vue             # 文本输入
│   │   ├── FileUpload.vue             # 文件上传
│   │   ├── ImageUpload.vue           # 图片上传
│   │   ├── VoiceRecord.vue           # 语音录制
│   │   └── ResponseDisplay.vue       # 结果展示
│   ├── composables/
│   │   └── useApi.ts                 # API 调用
│   ├── App.vue
│   └── main.ts
├── index.html
└── vite.config.ts
```

### 3. 组件设计

**InputModeSelector**：四个按钮切换输入模式（文本/文件/图片/语音）

**TextInput**：简单的文本输入框 + 发送按钮

**FileUpload**：文件选择器 + 文件预览 + 发送

**ImageUpload**：图片选择器 + 预览 + 发送

**VoiceRecord**：录音按钮 + 停止按钮 + 播放预览 + 发送

### 4. API 集成

使用 Fetch API 调用 REST API：
```typescript
const response = await fetch('/api/add', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ input_type, content })
});
```

### 5. 语音录制

使用 MediaRecorder API：
```typescript
const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
const recorder = new MediaRecorder(stream);
```

## Risks / Trade-offs

[风险] 浏览器录音权限限制
→ **缓解措施**：引导用户授权，提供备选文件上传方式

[风险] 浏览器兼容性
→ **缓解措施**：主要测试 Chrome、Firefox、Safari、Edge

[风险] 大文件上传超时
→ **缓解措施**：前端限制文件大小，显示上传进度

## Migration Plan

1. 创建 Vite + Vue 3 + TypeScript 项目
2. 实现基础组件结构和样式
3. 实现各输入模式组件
4. 集成 API 调用
5. 添加响应式样式
6. 测试和部署到 Vercel/Netlify
