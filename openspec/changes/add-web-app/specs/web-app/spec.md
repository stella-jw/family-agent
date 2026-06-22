## ADDED Requirements

### Requirement: Web 应用可通过浏览器访问
The system SHALL provide a Vue 3 single-page application accessible via web browser.

#### Scenario: 桌面浏览器访问
- **WHEN** user opens web app URL in Chrome/Firefox/Edge on desktop
- **THEN** application loads with input mode selector

#### Scenario: 移动浏览器访问
- **WHEN** user opens web app on mobile browser
- **THEN** UI adapts to mobile screen (responsive design)

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

#### Scenario: 上传 JSON 文件
- **WHEN** user selects .json file and clicks upload
- **THEN** file preview shown and sent to API

### Requirement: 图片上传功能
The system SHALL provide image picker with preview.

#### Scenario: 上传图片
- **WHEN** user selects image (JPEG/PNG/WebP) and clicks upload
- **THEN** image preview shown and sent to API for vision processing

### Requirement: 语音录制功能
The system SHALL provide in-browser audio recording using MediaRecorder API.

#### Scenario: 录制语音
- **WHEN** user clicks record, speaks, clicks stop, then clicks send
- **THEN** audio is recorded, preview played, and sent to API

#### Scenario: 浏览器拒绝录音权限
- **WHEN** browser denies microphone permission
- **THEN** display message with instructions to enable permission

### Requirement: API 通信
The system SHALL communicate with REST API using Fetch API.

#### Scenario: API 请求成功
- **WHEN** API returns success response
- **THEN** display result message to user

#### Scenario: API 请求失败
- **WHEN** API returns error
- **THEN** display error message with retry option

### Requirement: 结果展示
The system SHALL display API response to user in readable format.

#### Scenario: 显示添加成功
- **WHEN** /api/add returns success
- **THEN** display "信息已添加成功"

#### Scenario: 显示搜索结果
- **WHEN** /api/search returns results
- **THEN** display formatted member information
