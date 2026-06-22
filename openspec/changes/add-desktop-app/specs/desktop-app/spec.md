## ADDED Requirements

### Requirement: 桌面应用可在 Windows、macOS、Linux 运行
The system SHALL provide an Electron application that runs on major desktop platforms.

#### Scenario: Windows 运行
- **WHEN** user installs and runs .exe on Windows
- **THEN** app window opens with input mode selector

#### Scenario: macOS 运行
- **WHEN** user installs and runs .app on macOS
- **THEN** app window opens with input mode selector

#### Scenario: Linux 运行
- **WHEN** user runs AppImage on Linux
- **THEN** app window opens with input mode selector

### Requirement: 输入模式选择器
The system SHALL provide four input modes: text, file, image, voice.

#### Scenario: 切换输入模式
- **WHEN** user clicks on input mode button
- **THEN** corresponding input panel is displayed

### Requirement: 文本输入功能
The system SHALL provide text input field for natural language entry.

#### Scenario: 输入文本添加成员
- **WHEN** user types "我老婆叫林月" and clicks send
- **THEN** text is sent to API and result displayed

### Requirement: 文件上传功能
The system SHALL provide file picker for JSON/CSV/TXT files.

#### Scenario: 上传文件
- **WHEN** user clicks file picker and selects .json/.csv/.txt
- **THEN** file is sent to API

#### Scenario: 拖拽文件上传
- **WHEN** user drags file onto window
- **THEN** file is uploaded automatically

### Requirement: 图片上传功能
The system SHALL provide image picker with preview.

#### Scenario: 上传图片
- **WHEN** user selects image (JPEG/PNG/WebP) and clicks upload
- **THEN** image preview shown and sent to API

### Requirement: 语音录制功能
The system SHALL provide audio recording capability.

#### Scenario: 录制语音
- **WHEN** user clicks record, speaks, clicks stop, then clicks send
- **THEN** audio is recorded and sent to API

### Requirement: API 通信
The system SHALL communicate with REST API using Node.js http/fetch.

#### Scenario: 连接本地 API
- **WHEN** app starts with local API server
- **THEN** app connects to localhost:8000

#### Scenario: 连接远程 API
- **WHEN** app configured for remote server
- **THEN** app connects to configured remote URL

### Requirement: 系统托盘
The system SHALL minimize to system tray and run in background.

#### Scenario: 最小化到托盘
- **WHEN** user clicks minimize button
- **THEN** window hides and tray icon appears

#### Scenario: 托盘菜单
- **WHEN** user right-clicks tray icon
- **THEN** menu shows "Show", "Quit" options

### Requirement: 结果展示
The system SHALL display API response to user.

#### Scenario: 显示添加成功
- **WHEN** /api/add returns success
- **THEN** display "信息已添加成功"

#### Scenario: 显示搜索结果
- **WHEN** /api/search returns results
- **THEN** display formatted member information
