## Context

用户需要通过 iOS/Android 移动设备访问 family-agent。Flutter 应用需要连接到 `add-rest-api` 提供的 REST API，提供原生移动体验。

## Goals / Non-Goals

**Goals:**
- 构建 Flutter 跨平台移动应用（iOS + Android）
- 提供文本/文件/图片/语音四种输入模式
- 原生性能和使用体验
- 连接到 REST API 后端

**Non-Goals:**
- 实现后端 API（由 add-rest-api 负责）
- 实现 Web 或桌面应用

## Decisions

### 1. Flutter + Dart

**决策**：使用 Flutter 框架，Dart 语言

**理由**：
- 单一代码库支持 iOS 和 Android
- 原生性能
- 丰富的生态系统

### 2. 项目结构

```
mobile/
├── lib/
│   ├── main.dart
│   ├── screens/
│   │   └── HomeScreen.dart           # 主页面
│   ├── widgets/
│   │   ├── InputModeSelector.dart    # 输入模式选择
│   │   ├── TextInputWidget.dart      # 文本输入
│   │   ├── FileUploadWidget.dart      # 文件上传
│   │   ├── ImageUploadWidget.dart     # 图片上传
│   │   ├── VoiceRecordWidget.dart     # 语音录制
│   │   └── ResponseDisplay.dart       # 结果展示
│   ├── services/
│   │   └── ApiService.dart           # API 调用
│   └── models/
│       └── ApiModels.dart            # 数据模型
└── pubspec.yaml
```

### 3. 依赖包

- `http`：REST API 调用
- `image_picker`：图片选择
- `file_picker`：文件选择
- `record`：音频录制
- `audioplayers`：音频播放

### 4. API 集成

```dart
final response = await http.post(
  Uri.parse('$apiBaseUrl/api/add'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({'input_type': 'text', 'content': text})
);
```

## Risks / Trade-offs

[风险] 移动设备网络不稳定
→ **缓解措施**：添加网络状态检测和重试机制

[风险] 移动录音权限
→ **缓解措施**：引导用户在系统设置中授权

[风险] iOS/Android 行为差异
→ **缓解措施**：平台特定逻辑封装在条件编译中

## Migration Plan

1. 创建 Flutter 项目
2. 配置依赖包
3. 实现基础 UI 结构
4. 实现各输入模式组件
5. 集成 API 调用
6. 测试和发布
