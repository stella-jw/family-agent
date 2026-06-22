## ADDED Requirements

### Requirement: 支持常见图片格式
The system SHALL accept JPEG, PNG, WebP images.

#### Scenario: JPEG 图片
- **WHEN** user provides .jpg/.jpeg image
- **THEN** system loads and processes successfully

#### Scenario: PNG 图片
- **WHEN** user provides .png image
- **THEN** system loads and processes successfully

### Requirement: 图片缩放处理
The system SHALL resize images to max 2048px on longest edge before vision API call.

#### Scenario: 大图缩放
- **WHEN** user provides 4000x3000 image
- **THEN** system resizes to 2048x1536 before sending to vision model

#### Scenario: 小图保持
- **WHEN** user provides 800x600 image
- **THEN** system sends without resizing

### Requirement: 视觉 LLM 识别
The system SHALL use vision LLM to analyze image and output family member descriptions.

#### Scenario: 单人照片
- **WHEN** image contains one person
- **THEN** vision model outputs description like "照片中有一位男性，看起来40多岁"

#### Scenario: 多人照片
- **WHEN** image contains multiple people
- **THEN** vision model outputs descriptions for each person

### Requirement: 识别结果确认
The system SHALL display recognized descriptions for user confirmation before adding to knowledge base.

#### Scenario: 用户确认
- **WHEN** system displays descriptions and user confirms
- **THEN** system adds information to ChromaDB

#### Scenario: 用户拒绝
- **WHEN** user rejects the recognition results
- **THEN** system discards results and returns to input mode selection
