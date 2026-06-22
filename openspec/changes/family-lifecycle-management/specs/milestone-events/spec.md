## ADDED Requirements

### Requirement: 里程碑事件记录
The system SHALL record milestone life events with dates and descriptions.

#### Scenario: 记录升学
- **WHEN** user says "汪佳齐2028年考上大学了"
- **THEN** create milestone event: type=education, date=2028-09-01, description="考入大学"

#### Scenario: 记录结婚
- **WHEN** user says "汪佳齐2035年结婚了"
- **THEN** create milestone event: type=family, date=2035-XX-XX, description="结婚"

#### Scenario: 记录去世
- **WHEN** user says "刘和足2025年去世了"
- **THEN** create milestone event: type=death, date=2025-XX-XX, mark member as deceased

### Requirement: 人生时间轴展示
The system SHALL display milestones on an interactive timeline.

#### Scenario: 查看个人时间轴
- **WHEN** user opens 汪佳齐's timeline
- **THEN** display all milestones chronologically with icons

#### Scenario: 筛选事件类型
- **WHEN** user filters by "health" events only
- **THEN** show only health-related milestones

### Requirement: 里程碑到期提醒
The system SHALL remind users about upcoming milestone anniversaries.

#### Scenario: 周年提醒
- **WHEN** it's one month before 刘和足's death anniversary
- **THEN** remind user: "下月是刘和足去世一周年"

## Implementation Notes

### Milestone Types

```python
MILESTONE_CATEGORIES = {
    "education": ["入学", "升学", "毕业", "留学", "考级", "升学"],
    "career": ["入职", "晋升", "离职", "退休", "获奖"],
    "family": ["结婚", "生子", "乔迁", "丧事", "家庭旅行"],
    "health": ["住院", "手术", "确诊", "康复", "体检异常"],
    "achievement": ["获奖", "考证", "发明", "出版"],
}
```

### Timeline API

```
POST /api/member/{name}/milestone  # Add milestone
GET  /api/member/{name}/timeline?category=all&start_year=2000&end_year=2030
GET  /api/member/{name}/milestones?type=education
GET  /api/family/timeline  # Family-wide timeline
```

### Visualization

```
Timeline Component:
- Vertical scrollable timeline
- Year markers on left
- Event cards on right
- Color-coded by category
- Icons for event types
- Click to expand details
```
