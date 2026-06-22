## ADDED Requirements

### Requirement: 健康指标模板支持
The system SHALL support predefined health metric templates.

#### Scenario: 血压记录
- **WHEN** user says "刘和足血压135/85"
- **THEN** store as blood_pressure with systolic=135, diastolic=85, unit="mmHg"

#### Scenario: 血糖记录
- **WHEN** user says "刘和足空腹血糖5.6"
- **THEN** store as blood_sugar with value=5.6, unit="mmol/L", fasting=true

### Requirement: 健康指标趋势图表
The system SHALL display health metrics as line charts.

#### Scenario: 血压趋势图
- **WHEN** user views blood pressure trend for 刘和足
- **THEN** show line chart with systolic and diastolic over time

#### Scenario: 多指标对比
- **WHEN** user compares blood pressure and heart rate
- **THEN** show dual-axis line chart

### Requirement: 异常值预警
The system SHALL alert users when health metrics are abnormal.

#### Scenario: 血压偏高预警
- **WHEN** blood pressure exceeds 140/90 consistently
- **THEN** display warning: "刘和足血压持续偏高，请关注"

#### Scenario: 趋势恶化预警
- **WHEN** blood pressure trending upward over 3 measurements
- **THEN** display alert: "刘和足血压呈上升趋势"

### Requirement: 健康报告生成
The system SHALL generate health summary reports.

#### Scenario: 月度健康报告
- **WHEN** user requests monthly health report
- **THEN** generate markdown/PDF with all health metrics summary

## Implementation Notes

### Health Dimensions

```python
HEALTH_DIMENSIONS = {
    "血压": {"type": "dual", "unit": "mmHg", "normal_systolic": (90, 140), "normal_diastolic": (60, 90)},
    "血糖": {"type": "single", "unit": "mmol/L", "normal_fasting": (3.9, 6.1), "normal_postprandial": (<7.8)},
    "尿酸": {"type": "single", "unit": "μmol/L", "normal_male": (150, 420), "normal_female": (100, 360)},
    "体重": {"type": "single", "unit": "kg"},
    "身高": {"type": "single", "unit": "cm"},
    "BMI": {"type": "calculated", "formula": "weight / (height/100)^2"},
}
```

### API Endpoints

```
POST /api/member/{name}/health  # Add health record
GET  /api/member/{name}/health/trend?dimension=血压&period=6m
GET  /api/member/{name}/health/report?period=month
```

### Chart Specifications

```
Chart Type: Line Chart (dual axis for blood pressure)
X-Axis: Date (monthly aggregation for long term)
Y-Axis: Value + Reference Range Shading
Annotations: Abnormal points marked red
```
