## ADDED Requirements

### Requirement: 每次信息录入带时间戳
The system SHALL record the effective date for each piece of information.

#### Scenario: 自动时间戳
- **WHEN** user adds "汪佳齐喜欢篮球"
- **THEN** record is stored with `effective_date = today`

#### Scenario: 指定历史日期
- **WHEN** user says "汪佳齐2023年喜欢画画"
- **THEN** record is stored with `effective_date = 2023-01-01`

### Requirement: 支持历史版本查询
The system SHALL support querying historical versions of any record.

#### Scenario: 查询历史记录
- **WHEN** user queries "汪佳齐两年前喜欢什么"
- **THEN** return the version from 2 years ago

#### Scenario: 版本链展示
- **WHEN** user views a record's history
- **THEN** display all versions in chronological order

### Requirement: 自动变更检测
The system SHALL automatically detect changes between versions.

#### Scenario: 检测到新增
- **WHEN** user adds a new hobby
- **THEN** mark as "新增" in change log

#### Scenario: 检测到修改
- **WHEN** same attribute changes (e.g., hobby changed from painting to basketball)
- **THEN** mark as "修改" in change log

### Requirement: 变更摘要生成
The system SHALL generate human-readable summaries of changes.

#### Scenario: 月度变更摘要
- **WHEN** user requests monthly summary
- **THEN** generate: "汪佳齐本月新增2个爱好，修改1条健康记录"

## Implementation Notes

### Database Schema

```sql
ALTER TABLE member_records
ADD COLUMN effective_date DATE NOT NULL DEFAULT CURRENT_DATE,
ADD COLUMN is_latest BOOLEAN DEFAULT TRUE,
ADD COLUMN previous_record_id UUID REFERENCES member_records(id);
```

### API Endpoints

```
GET  /api/member/{name}/history?start_date=&end_date=
GET  /api/member/{name}/changes?period=month|quarter|year
GET  /api/member/{name}/snapshot?date=YYYY-MM-DD
```
