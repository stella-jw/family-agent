## ADDED Requirements

### Requirement: 成长曲线图
The system SHALL display growth curves for children.

#### Scenario: 身高体重曲线
- **WHEN** user views 汪佳齐's growth chart
- **THEN** show height and weight curves over time with percentile lines

#### Scenario: 学习进度曲线
- **WHEN** user views academic progress
- **THEN** show grades/scores trend line

### Requirement: 健康趋势图
The system SHALL display health metric trends.

#### Scenario: 血压趋势
- **WHEN** user views blood pressure trend
- **THEN** show line chart with normal range shading

#### Scenario: 多指标对比
- **WHEN** user compares multiple health metrics
- **THEN** show multi-axis chart or separate charts

### Requirement: 报告导出
The system SHALL export reports in multiple formats.

#### Scenario: 导出年度报告
- **WHEN** user requests annual report for 汪佳齐
- **THEN** generate PDF with:
  - Basic info changes summary
  - Health metrics charts
  - Milestone events
  - Growth analysis

#### Scenario: 导出人生时间轴
- **WHEN** user exports timeline as image
- **THEN** generate PNG with all milestones

## Implementation Notes

### Chart Types

| Data Type | Recommended Chart |
|-----------|-------------------|
| Health metrics (time series) | Line Chart |
| Hobby changes | Stacked Bar Chart |
| Academic scores | Line Chart with markers |
| Milestone distribution | Scatter plot / Timeline |
| Attribute comparison | Pie Chart / Radar Chart |

### Report Templates

```python
ANNUAL_REPORT_SECTIONS = [
    "cover",           # Name, year, family photo
    "basic_changes",   # Info changes summary
    "health_summary",  # Health metrics with charts
    "milestones",     # Major events
    "growth_analysis", # Year-over-year comparison
    "highlights",     # AI-generated summary
]
```

### API Endpoints

```
GET  /api/member/{name}/chart/growth?metric=height|weight|grade
GET  /api/member/{name}/chart/health?dimension=血压&period=6m
GET  /api/member/{name}/report/annual?year=2024&format=pdf|markdown
GET  /api/member/{name}/timeline/image
```

### Technology Stack

```
Frontend: Vue 3 + ECharts (echarts-for-vue)
Charts: Apache ECharts
Export: html2canvas + jsPDF (for PDF)
Timeline: Custom Vue component with D3.js (optional)
```
