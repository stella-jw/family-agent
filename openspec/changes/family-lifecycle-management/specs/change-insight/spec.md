## ADDED Requirements

### Requirement: 自动变化检测
The system SHALL automatically detect changes in member information.

#### Scenario: 爱好变化检测
- **WHEN** 汪佳齐's hobby changes from "绘画" to "篮球"
- **THEN** detect "爱好变化" and log in change_records

#### Scenario: 健康指标异常检测
- **WHEN** 刘和足's blood pressure exceeds normal range
- **THEN** mark as "异常" and suggest follow-up

### Requirement: AI 生成变化洞察
The system SHALL use LLM to generate human-readable insights.

#### Scenario: 月度洞察
- **WHEN** generating monthly summary
- **THEN** LLM generates: "汪佳齐本月最明显的变化是爱好从静态转向动态，建议多参与户外活动"

#### Scenario: 健康风险提示
- **WHEN** detecting blood pressure trend increase
- **THEN** LLM generates: "刘和足血压连续3个月上升，建议就医检查"

### Requirement: 智能问答
The system SHALL answer questions about changes and trends.

#### Scenario: 自然语言查询
- **WHEN** user asks "汪佳齐这学期学习怎么样"
- **THEN** query records and generate comparison with previous period

#### Scenario: 趋势问答
- **WHEN** user asks "刘和足最近健康状况如何"
- **THEN** summarize recent health records and trends

## Implementation Notes

### Change Detection Algorithm

```python
def detect_changes(member_id: str, period: str = "month") -> list[Change]:
    """
    1. Query records for current period
    2. Query records for previous period
    3. Compare each attribute
    4. Categorize: 新增/修改/删除/稳定
    5. Calculate change magnitude
    """
    pass

def generate_insight(changes: list[Change]) -> str:
    """
    Use LLM to generate natural language summary
    """
    prompt = f"""
    汪佳齐本月的变化：
    {changes}

    请用温暖的语气生成一段变化总结，包含：
    1. 主要变化
    2. 可能的建议
    3. 积极鼓励
    """
    return llm.invoke(prompt)
```

### API Endpoints

```
GET  /api/member/{name}/changes?period=month|quarter|year
GET  /api/member/{name}/insight?period=month
POST /api/chat  # Natural language Q&A
```

### Prompt Templates

```python
INSIGHT_PROMPTS = {
    "hobby_change": "分析{prefix}的爱好变化趋势，提出建议",
    "health_alert": "根据{prefix}的健康数据，判断是否需要提醒就医",
    "study_progress": "对比{prefix}的学习成绩变化，给出鼓励性评价",
    "family_events": "总结{prefix}家庭本月的重要事件",
}
```
