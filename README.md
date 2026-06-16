# 家庭信息记录 Agent

一个基于大模型的智能家庭信息管理 Agent，能够记录、更新、查询家庭成员的所有信息，具备长期记忆和语义理解能力。

## 项目功能

### 核心功能

- **信息录入**：通过自然语言对话，把家人的信息存入知识库
  - 例如：`"我老婆叫林月，是一名中学老师，生日是5月20日，爱好画画和烘焙"`

- **信息更新**：能够对已有信息进行补充和修正
  - 例如：`"对了，她的生日其实是5月21日"`

- **智能问答**：根据知识库中的信息回答问题，支持语义搜索
  - 例如：`"家里谁最会做饭？"` 能找到"爸爸的红烧肉做得一绝"

- **画像总结**：能根据某个人的所有零散信息，总结生成一段人物画像
  - 例如：`"帮我总结一下林月的人物画像"`

- **代词关联**：支持"她/他/我的"等代词，根据上下文自动关联到正确成员

- **性别推理**：根据家庭关系自动推理性别（老公→男，妻子→女）

- **否定描述**：区分爱好（"爱做饭"）和能力否定（"不太会做饭"）

### 技术特点

- 🤖 **LangGraph 工作流**：使用 LangGraph 状态机实现分类→执行→回复流程
- 🔍 **语义检索**：基于向量数据库，支持语义级别的信息检索
- 💾 **长期记忆**：使用 ChromaDB 持久化存储知识库
- 🌐 **中文优化**：使用 MiniMax Embedding API 中文嵌入模型

## 技术栈

- **对话大模型**：MiniMax API（minimax-text-01）
- **嵌入模型**：MiniMax Embedding API（embo-01）
- **工作流框架**：LangGraph（微软、LangChain 团队维护）
- **向量数据库**：ChromaDB
- **编程语言**：Python 3.12+

## 项目结构

```
family_agent/
├── main.py              # 主入口，命令行交互循环
├── graph.py             # LangGraph 工作流定义（状态、节点、边）
├── tools.py             # 自定义工具（ChromaDB 操作函数）
├── chroma_manager.py    # ChromaDB 管理类
├── config.py           # 配置（API Key、模型名称等）
├── test_family_agent.py # 自动化测试用例集
├── requirements.txt     # Python 依赖列表
├── .env.example        # 环境变量模板
├── issue_lists.md      # 问题追踪文档
└── README.md           # 本文档
```

## 安装步骤

### 1. 克隆或下载项目

```bash
cd /Users/yiliatang/AI/ai-demo/family_agent
```

### 2. 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置 MiniMax API Key

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的 API Key
nano .env  # 或使用其他编辑器
```

#### 如何获取 MiniMax API Key

1. 访问 [MiniMax 开放平台](https://platform.minimaxi.com/)
2. 注册账号并登录
3. 进入「控制台」→「API Key」页面
4. 创建一个新的 API Key
5. 将 API Key 填入 `.env` 文件中的 `MINIMAX_API_KEY`

### 5. 首次运行

```bash
python main.py
```

## 使用示例

### 对话示例

```
╔══════════════════════════════════════════════════════════════╗
║       欢迎使用「家庭信息记录 Agent」智能管家                  ║
╚══════════════════════════════════════════════════════════════╝

👤 您：我老婆叫林月，是一名中学老师，生日是5月20日。

🤖 管家：已成功记录林月的基本信息：
   - 职业：中学老师
   - 生日：5月20日

👤 您：我老婆的生日是什么时候？

🤖 管家：根据知识库记录，林月的生日是5月20日。

👤 您：对了，她生日我记错了，是5月21日。

🤖 管家：已更新林月的生日为5月21日（原记录：5月20日）。

👤 您：帮我总结一下林月的人物画像。

🤖 管家：根据目前掌握的信息，林月的人物画像如下：
   姓名：林月
   职业：中学老师
   生日：5月21日
   性格特点：温柔细心，热爱生活
   兴趣爱好：画画、烘焙

👤 您：我们家几口人？

🤖 管家：您家有 3 口人，分别是：林月、爸爸、妈妈

👤 您：退出

🤖 管家：再见！家庭的每一份记忆，我都替您珍藏着。
```

### 支持的信息类型

| 类型 | 说明 | 示例 |
|------|------|------|
| basic_info | 基本信息 | 姓名、职业、生日等 |
| hobby | 爱好 | 画画、烘焙、做饭等 |
| work_experience | 工作经历 | 曾任职公司、职位等 |
| life_event | 生活事件 | 旅游、搬家、结婚等 |
| personality | 性格特点 | 开朗、细心、幽默等 |
| ability | 能力描述 | 不太会做饭、不擅长游泳等 |
| relationship | 家庭关系 | 夫妻、父子、兄妹等 |

### 支持的 Action 类型

| Action | 说明 | 示例输入 |
|--------|------|----------|
| add | 添加新信息 | "林月37岁" |
| update | 更新已有信息 | "其实她生日是5月21日" |
| search | 查询信息 | "林月的生日是什么时候？" |
| aggregate_search | 聚合查询 | "家里谁最会做饭？" |
| count_family | 统计成员数量 | "我们家几口人？" |
| profile | 生成人物画像 | "帮我总结林月的画像" |
| self_identify | 自我身份声明 | "我才是糖糖" |
| confirm | 代词确认 | 当无法确定"他"是谁时 |

## 常见问题

### Q: ChromaDB 只读错误

运行时出现 `(code: 1032) attempt to write a readonly database`，删除数据库目录后重新初始化：

```bash
rm -rf ./data/chroma_db/
```

### Q: MiniMax API 调用失败

1. 检查 `.env` 文件中的 API Key 是否正确
2. 确认 API Key 是否有效（以 "ey" 开头）
3. 检查网络连接是否正常
4. 确认 Token Plan 额度充足

### Q: 如何运行测试？

```bash
python test_family_agent.py
```

## 开发说明

### LangGraph 工作流

```
START → classify → [add_info/update_info/search_info/get_profile] → respond → END
                  ↑
           (根据 action 类型条件路由)
```

- **classify**：使用 LLM 分析用户输入，确定 action 类型
- **add_info**：添加新记录，支持多记录一次性录入
- **update_info**：更新已有记录
- **search_info**：语义搜索
- **get_profile**：获取成员画像
- **respond**：LLM 生成最终回复

### 扩展功能

如果要添加新的 action 类型：

1. 在 `graph.py` 的 classify prompt 中添加新的判断规则
2. 在 `route_action` 中添加新的路由
3. 在 `respond` 中添加新的处理逻辑

## 许可证

MIT License

## 更新日志

### 2026-06-16 迁移至 LangGraph
- 从 CrewAI 迁移到 LangGraph 工作流
- 支持多记录一次性录入
- 添加代词上下文关联与性别推理
- 添加 ability 类型区分否定描述
- 添加 aggregate_search 和 count_family
- 添加自动化测试用例集