## ADDED Requirements

### Requirement: 用户数据隔离
The system SHALL ensure each user can only access their own family member data.

#### Scenario: 用户只能看到自己的数据
- **WHEN** user A searches for members
- **THEN** system returns only records where metadata.user_id = user_A's_id

#### Scenario: 用户只能修改自己的数据
- **WHEN** user A tries to update member belonging to user B
- **THEN** system returns 403 Forbidden

#### Scenario: 用户只能删除自己的数据
- **WHEN** user A tries to delete member belonging to user B
- **THEN** system returns 403 Forbidden

### Requirement: 添加数据自动关联用户
The system SHALL automatically associate new data with the authenticated user.

#### Scenario: 添加数据带 user_id
- **WHEN** authenticated user A adds member "林月"
- **THEN** system stores record with metadata.user_id = user_A's_id

### Requirement: ChromaDB metadata 存储 user_id
The system SHALL store user_id in ChromaDB metadata for each record.

#### Scenario: 元数据包含 user_id
- **WHEN** system stores a family member record
- **THEN** metadata includes user_id field linking to the owner user

### Requirement: 注册时初始化用户数据
The system SHALL create empty data structure for new user.

#### Scenario: 新用户注册
- **WHEN** new user completes registration
- **THEN** system initializes user record, no existing data visible

### Requirement: 数据迁移兼容性
The system SHALL handle existing data without user_id (from pre-auth version).

#### Scenario: 遗留数据处理
- **WHEN** querying records where user_id is null (legacy data)
- **THEN** system returns no records (legacy data inaccessible without auth)
