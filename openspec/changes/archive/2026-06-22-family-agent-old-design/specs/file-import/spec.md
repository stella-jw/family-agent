# file-import Specification

## Purpose
TBD - created by archiving change add-multi-modal-input. Update Purpose after archive.
## Requirements
### Requirement: File import supports JSON format
The system SHALL accept JSON files containing family member information. JSON structure SHALL be either an array of member objects or a single object with a "members" key containing the array.

#### Scenario: Import JSON array of members
- **WHEN** user selects file import and provides a JSON file with structure `[{"name": "张三", "relation": "父亲", "age": "50"}, ...]`
- **THEN** system parses each member object and adds them to the knowledge base

#### Scenario: Import JSON with nested members key
- **WHEN** user provides JSON file with structure `{"members": [{"name": "李四", "hobby": "钓鱼"}]}`
- **THEN** system extracts the members array and processes each entry

### Requirement: File import supports CSV format
The system SHALL accept CSV files where each row represents a family member. The first row SHALL contain column headers mapping to attribute types.

#### Scenario: Import CSV with standard columns
- **WHEN** user provides CSV file with headers: `name,relation,age,occupation`
- **THEN** system maps each column to corresponding attribute and adds member info

#### Scenario: Import CSV with flexible columns
- **WHEN** user provides CSV with headers that don't exactly match attribute types
- **THEN** system SHALL use LLM to infer the mapping between column names and attribute types

### Requirement: File import supports TXT format
The system SHALL accept plain text files and process them using the existing classify flow.

#### Scenario: Import free-text description file
- **WHEN** user provides a .txt file containing natural language family descriptions
- **THEN** system reads the file content and passes it to the classify node for processing

### Requirement: File encoding detection
The system SHALL attempt to decode files using UTF-8, then GBK/GB2312 encodings as fallback.

#### Scenario: Handle UTF-8 encoded file
- **WHEN** user imports a UTF-8 encoded file
- **THEN** system processes it successfully without encoding errors

#### Scenario: Handle GBK encoded file
- **WHEN** user imports a GBK-encoded Chinese text file
- **THEN** system detects the encoding and processes correctly

### Requirement: File size validation
The system SHALL reject files larger than 10MB with an appropriate error message.

#### Scenario: Attempt to import oversized file
- **WHEN** user selects a file larger than 10MB
- **THEN** system displays error "File too large. Maximum size is 10MB."

