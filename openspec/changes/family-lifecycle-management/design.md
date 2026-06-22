## Context

Family-Agent 需要从"信息记录工具"演进为"家庭生命周期管理系统"。核心区别：

| 维度 | 旧定位 | 新定位 |
|------|--------|--------|
| **时间维度** | 无时间概念 | 日/周/月/季/年时序追踪 |
| **数据模型** | 平面记录 | 时序版本链 |
| **分析能力** | 无 | 横向对比+纵向分析 |
| **报告形式** | 文本回复 | 图表+时间轴 |
| **用户价值** | 信息存储 | 成长洞察+健康管理 |

## Goals / Non-Goals

**Goals:**
- 支持任意信息的时间序列存储和查询
- 自动识别信息变更（新增/修改/删除）
- 生成可读性强的可视化报告
- 支持健康指标的长期追踪和趋势分析
- 记录人生里程碑事件

**Non-Goals:**
- 不做医疗诊断（仅提供数据记录和分析）
- 不做社交功能（纯个人/家庭使用）
- 不做硬件数据自动同步（手动录入为主）

## Architecture

### 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户交互层                                 │
│   Web App（Vue 3 + ECharts）│ Mobile App │ Desktop App         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      REST API 层                                 │
│              FastAPI + 认证中间件 + 限流                         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    LangGraph Agent 层                            │
│  ┌─────────┐    ┌─────────┐    ┌──────────┐    ┌─────────┐  │
│  │classify │───▶│extract  │───▶│time_index│───▶│respond  │  │
│  └─────────┘    └─────────┘    └──────────┘    └─────────┘  │
│                      │                                          │
│                      ▼                                          │
│              ┌──────────────┐                                   │
│              │change_detect│  ← 变化检测引擎                     │
│              └──────────────┘                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      数据存储层                                   │
│   ChromaDB（向量）│ SQLite/PostgreSQL（关系）│ 文件存储         │
└─────────────────────────────────────────────────────────────────┘
```

### 数据模型设计

#### 1. 成员基础表（关系型）

```sql
CREATE TABLE family_members (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    gender ENUM('男', '女', '未知') DEFAULT '未知',
    birth_date DATE,
    birth_year INT,
    death_date DATE,  -- 去世日期，可为空
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 2. 信息记录表（时序）

```sql
CREATE TABLE member_records (
    id VARCHAR(36) PRIMARY KEY,
    member_id VARCHAR(36) NOT NULL,
    attribute_type VARCHAR(50) NOT NULL,  -- basic_info/hobby/health/work/life_event
    dimension VARCHAR(50),  -- 子维度：血压/分数/爱好等
    content TEXT NOT NULL,
    value_numeric DECIMAL(10,2),  -- 数值型数据（用于图表）
    unit VARCHAR(20),  -- 单位：cm/kg/mmHg/mg/dL
    effective_date DATE NOT NULL,  -- 信息生效日期
    source VARCHAR(50) DEFAULT 'manual',  -- manual/file/image/voice
    is_latest BOOLEAN DEFAULT TRUE,  -- 是否最新版本
    previous_record_id VARCHAR(36),  -- 指向前一个版本
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES family_members(id),
    FOREIGN KEY (previous_record_id) REFERENCES member_records(id)
);
```

#### 3. 里程碑事件表

```sql
CREATE TABLE milestone_events (
    id VARCHAR(36) PRIMARY KEY,
    member_id VARCHAR(36) NOT NULL,
    event_type VARCHAR(50) NOT NULL,  -- 升学/结婚/生子/就医/去世等
    event_date DATE NOT NULL,
    description TEXT,
    importance_level INT DEFAULT 1,  -- 1-5，重要性
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES family_members(id)
);
```

#### 4. 变更记录表（审计）

```sql
CREATE TABLE change_logs (
    id VARCHAR(36) PRIMARY KEY,
    member_id VARCHAR(36) NOT NULL,
    change_type ENUM('新增', '修改', '删除', '恢复') NOT NULL,
    attribute_type VARCHAR(50),
    old_content TEXT,
    new_content TEXT,
    change_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES family_members(id)
);
```

### ChromaDB Schema 扩展

```python
{
    "member_id": "uuid",
    "attribute_type": "basic_info|hobby|health|work|life_event|milestone",
    "dimension": "血压|分数|爱好|...",  # 子维度
    "content": "文本描述",
    "value": 120.5,  # 数值（如果有）
    "unit": "mmHg",
    "effective_date": "2024-01-15",
    "year_month": "2024-01"  # 用于月度聚合
}
```

## 功能模块设计

### Phase 1: 基础信息记录（已完成）

- [x] 多模态输入（文本/文件/图片/语音）
- [x] 智能意图分类
- [x] 双向关系存储
- [x] REST API
- [x] Vue 3 Web App

### Phase 2: 时序追踪（待实现）

#### 2.1 时间戳扩展
- 每次记录自动添加 `effective_date`
- 支持手动指定生效日期（backfill）
- 版本链追踪（previous_record_id）

#### 2.2 变化检测
```python
def detect_changes(member_id: str, start_date: date, end_date: date) -> list:
    """
    检测时间段内的信息变更
    1. 查询历史版本链
    2. 对比相邻版本差异
    3. 标记：新增/修改/删除
    """
    pass

def generate_change_summary(member_id: str, period: str) -> str:
    """
    生成变更摘要
    '本月新增3条记录，修改1条，爱好从绘画变为篮球'
    """
    pass
```

#### 2.3 历史查询
- 查询任意时间点的信息快照
- 时间范围查询（过去一年、某个成员的所有历史记录）

### Phase 3: 健康监控（待实现）

#### 3.1 健康指标模板
```python
HEALTH_DIMENSIONS = {
    "血压": {"unit": "mmHg", "normal_range": (90, 140), (60, 90)},
    "血糖": {"unit": "mmol/L", "normal_range": (3.9, 6.1)},
    "尿酸": {"unit": "μmol/L", "normal_range": (150, 420)},
    "体重": {"unit": "kg"},
    "身高": {"unit": "cm"},
    "BMI": {"unit": "kg/m²", "normal_range": (18.5, 24.9)},
}
```

#### 3.2 趋势图表
- 折线图：指标随时间变化
- 柱状图：多指标对比
- 饼图：爱好/时间分配

#### 3.3 异常预警
```python
def check_abnormal(member_id: str, dimension: str, value: float) -> bool:
    """
    检测异常值
    - 超出正常范围
    - 短期内剧烈变化
    - 趋势持续恶化
    """
    pass

def send_alert(member_id: str, alert_type: str, message: str):
    """
    发送预警通知
    - App 推送
    - 邮件
    - 微信
    """
    pass
```

### Phase 4: 人生里程碑（待实现）

#### 4.1 里程碑类型
```python
MILESTONE_TYPES = {
    "education": ["入学", "升学", "毕业", "留学"],
    "career": ["入职", "晋升", "离职", "退休"],
    "family": ["结婚", "生子", "乔迁", "丧事"],
    "health": ["住院", "手术", "确诊", "康复"],
    "achievement": ["获奖", "考证", "晋级"],
}
```

#### 4.2 人生时间轴
- 可视化展示人生重要节点
- 支持按成员、按时间筛选
- 导出为图片/PDF

#### 4.3 报告生成
```python
def generate_member_report(member_id: str, year: int) -> Report:
    """
    生成年度报告
    - 封面
    - 基本信息变化
    - 健康指标汇总
    - 重要事件回顾
    - 成长对比
    """
    pass

def generate_family_report(year: int) -> Report:
    """
    生成家庭年度报告
    - 家庭成员变化
    - 重大事件
    - 健康状况总览
    """
    pass
```

### Phase 5: AI 洞察（待实现）

#### 5.1 智能分析
- 从历史数据中发现规律
- 预测未来趋势
- 提供个性化建议

#### 5.2 自然语言查询
```
用户：汪佳齐这学期的学习怎么样？
AI：
- 英语进步明显（+15分）
- 数学略有下降（-5分）
- 建议加强数学练习
```

## 技术决策

### 1. 时序数据存储

**方案 A：扩展 ChromaDB**
- 优点：复用现有架构
- 缺点：不擅长时序查询

**方案 B：SQLite + ChromaDB 混合**
- SQLite：关系型数据、时序数据
- ChromaDB：语义搜索
- **选择：方案 B**

### 2. 可视化方案

| 方案 | 优点 | 缺点 |
|------|------|------|
| ECharts | 轻量、功能强 | 定制复杂 |
| D3.js | 高度定制 | 学习曲线陡峭 |
| Chart.js | 简单易用 | 功能有限 |

**选择：ECharts**（Vue 3 有 echarts-for-vue）

### 3. 报告导出

| 格式 | 适用场景 |
|------|----------|
| PDF | 正式存档、分享 |
| PNG | 快速预览 |
| Markdown | 可编辑 |

**选择：PDF + Markdown**

## Risks / Trade-offs

| 风险 | 影响 | 缓解 |
|------|------|------|
| 数据量增长 | 10年/家庭可能数万条记录 | 分表归档、懒加载 |
| 隐私安全 | 家庭数据敏感 | 加密存储、权限控制 |
| 版本冲突 | 多端同时录入 | 时间戳+乐观锁 |
| AI 幻觉 | 健康建议可能误导 | 明确免责声明 |

## Migration Plan

### 现有数据迁移
1. 保留现有 ChromaDB 数据
2. 增量添加 `effective_date`（默认 today）
3. 构建版本链

### 分阶段实施

```
Phase 1（当前）→ Phase 2 → Phase 3 → Phase 4 → Phase 5
   6月          7月       8月       9月      10月
```
