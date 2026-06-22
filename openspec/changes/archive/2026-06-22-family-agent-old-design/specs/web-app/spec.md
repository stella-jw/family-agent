# web-app Specification

## Purpose
TBD - created by archiving change add-multi-modal-input. Update Purpose after archive.
## Requirements
### Requirement: Web 应用支持现代浏览器访问
The system SHALL provide a Vue 3 single-page application accessible via web browser on desktop and mobile devices.

#### Scenario: 用户在 Chrome 浏览器中访问 Web 应用
- **WHEN** user navigates to the web app URL in Chrome
- **THEN** the application loads and displays the input mode selector

#### Scenario: 用户在移动设备浏览器中访问 Web 应用
- **WHEN** user opens the web app on a mobile browser
- **THEN** the UI adapts to mobile screen size (responsive design)

### Requirement: Web 应用提供文本输入入口
The system SHALL provide a text input field for direct natural language entry of family member information.

#### Scenario: 用户输入文本添加成员信息
- **WHEN** user types "我老婆叫林月，是一名中学老师" in the text input
- **THEN** system sends the text to REST API and displays the result

### Requirement: Web 应用支持文件上传
The system SHALL provide a file upload interface using browser's native file picker.

#### Scenario: 用户上传 JSON 文件
- **WHEN** user clicks file input and selects a .json file
- **THEN** system reads the file, displays its content preview, and sends to API

#### Scenario: 用户上传 CSV 文件
- **WHEN** user selects a .csv file
- **THEN** system parses headers, shows preview, and sends to API for processing

### Requirement: Web 应用支持图片上传
The system SHALL provide image upload with browser-based preview before sending to API.

#### Scenario: 用户上传照片
- **WHEN** user selects an image file (JPEG/PNG/WebP)
- **THEN** system displays image preview and sends to API for vision processing

### Requirement: Web 应用支持语音录制
The system SHALL provide in-browser audio recording using MediaRecorder API.

#### Scenario: 用户录制语音
- **WHEN** user clicks record button and speaks, then clicks stop
- **THEN** system records audio, shows duration, and provides playback preview

#### Scenario: 浏览器拒绝录音权限
- **WHEN** browser denies microphone permission
- **THEN** system displays message "请在浏览器设置中允许使用麦克风" with instructions

### Requirement: Web 应用响应式设计
The system SHALL render properly on desktop (1920px+) and mobile (375px - 428px) screen sizes.

#### Scenario: 桌面端显示
- **WHEN** user opens web app on desktop browser
- **THEN** input controls are displayed in a comfortable desktop layout

#### Scenario: 移动端显示
- **WHEN** user opens web app on mobile browser
- **THEN** UI elements are touch-friendly with appropriate sizing

### Requirement: Web 应用连接到 REST API
The system SHALL communicate with the REST API backend using Fetch API.

#### Scenario: API 请求成功
- **WHEN** web app sends a request to /api/add and receives success response
- **THEN** system displays the successful result to user

#### Scenario: API 请求失败
- **WHEN** web app sends a request but API returns error
- **THEN** system displays error message and allows retry

