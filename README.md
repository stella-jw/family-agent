# 家庭信息记录 Agent

一个基于大模型的智能家庭信息管理 Agent，能够记录、更新、查询家庭成员的所有信息，具备长期记忆和语义理解能力。

## 项目功能

### 核心功能

- **信息录入**：通过自然语言对话，把家人的信息存入知识库
  - 例如：`"我老婆叫林月，是一名中学老师，生日是5月20日，爱好画画和烘培"`

- **信息更新**：能够对已有信息进行补充和修正
  - 例如：`"对了，她的生日其实是5月21日"`

- **智能问答**：根据知识库中的信息回答问题，支持语义搜索
  - 例如：`"家里谁最会做饭？"` 能找到"爸爸的红烧肉做得一绝"

- **画像总结**：能根据某个人的所有零散信息，总结生成一段人物画像
  - 例如：`"帮我总结一下林月的人物画像"`

### 技术特点

- 🤖 **多 Agent 协作**：使用 CrewAI 框架，4 个专业 Agent 分工协作
- 🔍 **语义检索**：基于向量数据库，支持语义级别的信息检索
- 💾 **长期记忆**：使用 ChromaDB 持久化存储知识库
- 🌐 **中文优化**：使用 text2vec-base-chinese 本地嵌入模型，完全免费

## 技术栈

- **对话大模型**：MiniMax API（minimax-text-01）
- **嵌入模型**：text2vec-base-chinese（本地免费）
- **Agent 框架**：CrewAI
- **向量数据库**：ChromaDB
- **编程语言**：Python 3.12+

## 项目结构

```
family_agent/
├── main.py              # 主入口，命令行交互循环
├── agents.py            # 定义所有 CrewAI Agent 和 Task
├── tools.py             # 自定义工具（ChromaDB 操作函数）
├── chroma_manager.py # ChromaDB 管理类
├── config.py            # 配置（API Key、模型名称等）
├── requirements.txt     # Python 依赖列表
├── .env.example # 环境变量模板
└── README.md            # 本文档
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
| relationship | 家庭关系 | 夫妻、父子、兄妹等 |

## 常见问题

### Q:运行时提示 "No module named 'pkg_resources'"

这是 Python 3.12 与 setuptools 的兼容问题。运行：

```bash
pip install --upgrade setuptools
```

如果仍有问题，尝试降级：

```bash
pip install 'setuptools<61'
```

### Q: 嵌入模型下载失败

text2vec-base-chinese 模型较大（约 400MB），首次运行时会自动下载。
如果下载失败，可以手动下载：

```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/text2vec-base-chinese')"
```

### Q: MiniMax API 调用失败

1. 检查 `.env` 文件中的 API Key 是否正确
2. 确认 API Key 是否有效（以 "ey" 开头）
3. 检查网络连接是否正常

### Q: 如何查看知识库中的所有成员？

在对话中输入查询指令，如"有哪些家庭成员？"即可。

## 开发说明

### 修改配置

所有配置集中在 `config.py` 文件中，包括：

- `MINIMAX_API_KEY`：MiniMax API 密钥
- `MINIMAX_BASE_URL`：API 基础地址
- `MINIMAX_MODEL_NAME`：使用的模型名称
- `EMBEDDING_MODEL_NAME`：嵌入模型名称
- `CHROMA_DB_PATH`：知识库存储路径

### 扩展功能

如果要添加新的 Agent 或工具：

1. 在 `tools.py` 中定义新的工具函数
2. 在 `agents.py` 中创建新的 Agent
3. 在 `agents.py` 中创建对应的 Task
4. 在 `main.py` 的 Crew 配置中添加新的 Agent 和 Task

## 许可证

MIT License

## 作者

家庭信息记录 Agent 开发团队