## ADDED Requirements

### Requirement: Voice input accepts audio recording
The system SHALL accept audio input via microphone recording in WAV or MP3 format.

#### Scenario: Record audio via microphone
- **WHEN** user selects voice input mode and speaks into the microphone
- **THEN** system records the audio and sends it to STT service

### Requirement: Audio is converted to text via STT
The system SHALL use an STT (speech-to-text) service to convert recorded audio to text.

#### Scenario: Convert spoken Chinese to text
- **WHEN** user says "我老婆叫林月，是一名中学老师"
- **THEN** STT returns the text "我老婆叫林月，是一名中学老师"

### Requirement: Transcription is displayed for confirmation
Before processing, the system SHALL display the transcription and ask for user confirmation.

#### Scenario: Show transcription for confirmation
- **WHEN** STT returns text transcription
- **THEN** system displays "您说的是：'xxx'，确认发送？(y/n)"

#### Scenario: User confirms transcription
- **WHEN** user confirms the transcription with "y" or "是"
- **THEN** system passes the text to graph.invoke() for normal processing

#### Scenario: User rejects and re-records
- **WHEN** user rejects the transcription with "n" or "否"
- **THEN** system allows re-recording without losing context

### Requirement: Voice mode can be combined with text mode
The system SHALL allow users to switch between voice and text input freely within a session.

#### Scenario: Switch from voice to text mid-session
- **WHEN** user is in voice input mode and types text instead of speaking
- **THEN** system detects text input and processes it normally

### Requirement: Audio recording timeout
If no speech is detected for 30 seconds, the system SHALL stop recording and prompt the user.

#### Scenario: Recording timeout
- **WHEN** user starts voice recording but remains silent for 30 seconds
- **THEN** system stops recording and asks "没有检测到语音，请重试或切换到文字输入"
