## ADDED Requirements

### Requirement: 接受音频录制
The system SHALL accept audio input via WAV or MP3 format.

#### Scenario: 录音输入
- **WHEN** user provides audio recording
- **THEN** system sends to STT service for transcription

### Requirement: 语音转文本
The system SHALL convert audio to text using STT service.

#### Scenario: 中文语音转文本
- **WHEN** user says "我老婆叫林月，是一名中学老师"
- **THEN** STT returns text "我老婆叫林月，是一名中学老师"

### Requirement: 转录文本确认
The system SHALL display transcription for user confirmation before processing.

#### Scenario: 显示转录
- **WHEN** STT returns transcription
- **THEN** system displays "您说的是：'xxx'，确认发送？(y/n)"

#### Scenario: 用户确认转录
- **WHEN** user confirms transcription
- **THEN** system passes text to graph.invoke() for processing

#### Scenario: 用户拒绝重录
- **WHEN** user rejects transcription
- **THEN** system allows re-recording

### Requirement: 录音超时处理
The system SHALL stop recording after 30 seconds of silence and prompt user.

#### Scenario: 静音超时
- **WHEN** recording has no speech for 30 seconds
- **THEN** system stops recording and asks user to retry or switch to text input
