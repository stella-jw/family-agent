## Why

用户需要通过移动设备（iOS/Android）访问 family-agent，提供与 Web 端一致的多模态输入体验，随时随地添加和查询家庭成员信息。

## What Changes

- **Flutter 移动应用**：使用 Flutter 构建 iOS/Android 双平台应用
- **输入模式选择器**：文本/文件/图片/语音四种输入模式
- **REST API 集成**：通过 http 包连接后端 API
- **原生体验**：适配各平台的设计规范

## Capabilities

### New Capabilities

- `mobile-app`：基于 Flutter 的移动应用（iOS/Android），提供多模态输入 UI

### Modified Capabilities

- （无）

## Impact

- **mobile/**：新增 Flutter 项目目录
- 依赖 `add-rest-api` 提供后端 API 支持
