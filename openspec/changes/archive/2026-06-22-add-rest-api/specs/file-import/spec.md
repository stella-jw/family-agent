## ADDED Requirements

### Requirement: 支持 JSON 文件解析
The system SHALL accept JSON files containing family member information.

#### Scenario: 导入 JSON 数组
- **WHEN** user provides JSON file with structure `[{"name": "张三", "relation": "父亲", "age": "50"}, ...]`
- **THEN** for each member, system checks if name exists → exists则update，不存在则add

#### Scenario: 导入 JSON 嵌套结构
- **WHEN** user provides JSON with `{"members": [...]}`
- **THEN** system extracts members array and processes each entry with 存在则update逻辑

### Requirement: 支持 CSV 文件解析
The system SHALL accept CSV files where each row is a family member.

#### Scenario: CSV 标准列导入
- **WHEN** CSV has headers: `name,relation,age,occupation`
- **THEN** for each row, system checks if name exists → exists则update，不存在则add

#### Scenario: CSV 灵活列名
- **WHEN** CSV headers don't exactly match attribute types
- **THEN** system uses LLM to infer column-to-attribute mapping, then applies 存在则update逻辑

### Requirement: 支持 TXT 文件解析
The system SHALL accept plain text files processed via existing classify flow.

#### Scenario: TXT 自由文本导入
- **WHEN** user provides .txt file with natural language family descriptions
- **THEN** system reads content and passes to classify node for processing

### Requirement: 同名成员智能合并（存在则update，不存在则add）
The system SHALL check if a member with the same name already exists before adding, and update existing records instead of creating duplicates.

#### Scenario: 导入已存在的成员
- **WHEN** file contains member "张三" and "张三" already exists in knowledge base
- **THEN** system updates existing record with new information, preserving unspecified fields

#### Scenario: 导入新成员
- **WHEN** file contains member "李四" and "李四" does not exist
- **THEN** system adds new record for "李四"

#### Scenario: 部分字段更新
- **WHEN** existing member "张三" has {name, age, occupation} and file only updates age
- **THEN** system updates only age field, preserving name and occupation

#### Scenario: 批量导入混合场景
- **WHEN** file contains 5 members: 3 existing, 2 new
- **THEN** system performs 3 updates and 2 adds, returns summary: "已添加2人，已更新3人"

### Requirement: 文件编码检测
The system SHALL attempt decoding with UTF-8, then GBK/GB2312 as fallback.

#### Scenario: UTF-8 文件
- **WHEN** file is UTF-8 encoded
- **THEN** system processes without encoding errors

#### Scenario: GBK 文件
- **WHEN** file is GBK-encoded Chinese text
- **THEN** system detects encoding and processes correctly

### Requirement: 文件大小验证
The system SHALL reject files larger than 10MB.

#### Scenario: 过大文件
- **WHEN** user imports file > 10MB
- **THEN** system returns error "File too large. Maximum size is 10MB."
