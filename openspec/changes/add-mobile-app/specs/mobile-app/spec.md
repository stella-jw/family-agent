## ADDED Requirements

### Requirement: 移动应用可在 iOS 和 Android 上运行
The system SHALL provide a Flutter application that runs on iOS and Android devices.

#### Scenario: iOS 设备运行
- **WHEN** user installs and opens app on iPhone
- **THEN** app displays input mode selector

#### Scenario: Android 设备运行
- **WHEN** user installs and opens app on Android phone
- **THEN** app displays input mode selector

### Requirement: 输入模式选择器
The system SHALL provide four input modes: text, file, image, voice.

#### Scenario: 切换输入模式
- **WHEN** user taps on input mode tab/icon
- **THEN** corresponding input panel is displayed

### Requirement: 文本输入功能
The system SHALL provide text input field for natural language entry.

#### Scenario: 输入文本添加成员
- **WHEN** user types "我老婆叫林月" and taps send
- **THEN** text is sent to API and result displayed

### Requirement: 文件上传功能
The system SHALL provide file picker for JSON/CSV/TXT files.

#### Scenario: 上传 JSON 文件
- **WHEN** user selects .json file and taps upload
- **THEN** file is sent to API

### Requirement: 图片上传功能
The system SHALL provide image picker with camera/gallery options.

#### Scenario: 从相册选择图片
- **WHEN** user taps image input and selects from gallery
- **THEN** image preview shown and sent to API

#### Scenario: 拍照上传
- **WHEN** user taps image input and chooses camera
- **THEN** camera opens, photo taken, and sent to API

### Requirement: 语音录制功能
The system SHALL provide audio recording capability.

#### Scenario: 录制语音
- **WHEN** user taps record, speaks, taps stop, then taps send
- **THEN** audio is recorded and sent to API

#### Scenario: 拒绝录音权限
- **WHEN** user denies microphone permission
- **THEN** display message with instructions to enable in settings

### Requirement: API 通信
The system SHALL communicate with REST API using http package.

#### Scenario: API 请求成功
- **WHEN** API returns success response
- **THEN** display result message

#### Scenario: API 请求失败
- **WHEN** API returns error or network fails
- **THEN** display error message with retry option

### Requirement: 结果展示
The system SHALL display API response to user.

#### Scenario: 显示添加成功
- **WHEN** /api/add returns success
- **THEN** display "信息已添加成功"

#### Scenario: 显示搜索结果
- **WHEN** /api/search returns results
- **THEN** display formatted member information
