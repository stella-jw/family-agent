# 家庭信息记录 Agent - 问题汇总

## 一、环境与依赖问题

### 1. pkg_resources 模块找不到
- **原因**：Python 3.12 移除了 `pkgutil.ImpImporter`，setuptools 82+ 也移除了 pkg_resources
- **影响**：`import pkg_resources` 失败
- **尝试方案**：
  - `pip install --upgrade setuptools`
  - `pip install setuptools-pkg-resources`（找不到这个包）
  - `pip install 'setuptools<61'`（仍然报错 `AttributeError: module 'pkgutil' has no attribute 'ImpImporter'`）
- **最终解决**：修改 crewai 源码，移除 `import pkg_resources`，改用 `from importlib.metadata import version`

### 2. ChromaDB 嵌入模型配置问题
- **原因**：ChromaDB 0.4.24 默认使用英文嵌入模型（ONNXMiniLM_L6_V2），不支持中文
- **需要**：使用中文嵌入模型 `shibing624/text2vec-base-chinese`
- **尝试方案**：
  - 需要在 `create_collection` 时传入自定义 `embedding_function`
  - ChromaDB 要求 `embedding_function` 必须符合特定接口：`__call__(self, input)` → 返回 numpy array
- **最终解决**：创建 `ChineseEmbeddingFunction` 封装类

### 3. Hugging Face 模型下载超时
- **原因**：网络无法访问 huggingface.co
- **解决**：使用国内镜像 `HF_ENDPOINT=https://hf-mirror.com`

---

## 二、CrewAI API 兼容性问题

### 4. Task 导入路径错误
- **原因**：crewai 0.51.0 中 Task 不在 `crewai.tasks` 模块
- **错误**：`ImportError: cannot import name 'Task' from 'crewai.tasks'`
- **解决**：`from crewai import Agent, Task`

### 5. tool 装饰器导入错误
- **原因**：crewai 0.51.0 中没有 `from crewai.tools import tool`
- **错误**：`ImportError: cannot import name 'tool' from 'crewai.tools'`
- **解决**：使用 `BaseTool` 类自定义工具，定义 `_run` 方法

### 6. BaseTool 导入路径错误
- **原因**：BaseTool 在 `crewai.tools.tool_usage` 而不是 `crewai.tools`
- **错误**：`ImportError: cannot import name 'BaseTool' from 'crewai.tools'`
- **解决**：`from crewai.tools.tool_usage import BaseTool`

### 7. Embeddings 类不存在
- **原因**：crewai 0.51.0 没有 `Embeddings` 类
- **错误**：`ImportError: cannot import name 'Embeddings' from 'crewai'`
- **解决**：删除这段代码（ChromaDB 自己处理嵌入，不需要额外 Embeddings 类）

---

## 三、CrewAI 层次化模式问题

### 8. Manager agent 不能在 agents 列表中
- **原因**：hierarchical 模式下，manager_agent 不能同时出现在 agents 列表
- **错误**：`ValidationError: Manager agent should not be included in agents list`
- **解决**：从 `agents=[...]` 列表中移除 steward_agent

### 9. Manager agent 不能有工具
- **原因**：hierarchical 模式下，manager 只负责协调，不能有 tools
- **错误**：`AttributeError: Manager agent should not have tools`
- **解决**：移除 steward_agent 的 `tools=[]` 参数

### 10. hierarchical 模式委托 bug
- **原因**：CrewAI 0.51.0 的 hierarchical 模式在委托任务时格式错误
- **错误**：`task` 和 `context` 被传成对象而不是字符串，导致验证失败
- **错误信息**：`2 validation errors for Delegate work to coworkerSchema - task: str type expected`
- **解决**：改用 `Process.sequential` 或直接调用 `agent.execute_task()`

---

## 四、LLM 幻觉问题

### 11. Agent 使用示例名字而非用户输入的名字
- **原因**：
  - tools.py 工具描述中写了示例名字（如"林月"、"爸爸"、"妈妈"）
  - agents.py Task 描述中写了示例名字（如"林月的生日"）
  - Agent 被示例数据污染，忽略用户输入，自行编造姓名
- **错误现象**：用户输入"汪佳齐的信息"，返回"已记录林月的基本信息"
- **解决**：
  - 移除 tools.py 描述中的所有示例名字
  - 移除 agents.py 中 Task 描述的所有示例名字和示例命令
  - 在 prompt 中强调"强制从用户输入提取，不允许编造"

---

## 五、其他问题

### 12. 中文引号导致语法错误
- **原因**：Python字符串中使用中文引号 `""` 与字符串定界符冲突
- **错误位置**：agents.py 第 260 行
- **解决**：使用单引号包裹包含中文双引号的字符串

### 13. ChromaDB collection 已存在导致重复创建
- **原因**：如果 collection 已存在，`get_or_create_collection` 会返回已有的
- **影响**：使用旧的 embedding function 配置
- **解决**：删除 `./data/chroma_db` 目录重新初始化

---

## 六、问题根因总结

| 问题类型 | 根本原因 | 影响 |
|---------|---------|------|
| 环境兼容 | Python 3.12 + setuptools 82+ + CrewAI 0.51.0 组合 | 多个 import 失败 |
| API 变化 | CrewAI 0.51.0 API 与文档/旧版本不一致 | 需要反复试错找正确导入路径 |
| 层次化模式 | CrewAI 0.51.0 hierarchical 模式实现不完整 | 委托任务格式错误 |
| LLM 幻觉 | prompt 中示例名字污染 | Agent 不读取用户输入，自行编造 |
| 网络问题 | 无法访问 Hugging Face | 嵌入模型下载失败 |

---

## 七、建议

1. **优先修复 LLM 幻觉问题**：这是功能性 bug，影响核心使用
2. **考虑降级 Python 或 CrewAI 版本**：如果稳定版本更重要
3. **增加输入验证**：在工具层校验名字是否来自用户输入
4. **完善错误提示**：当用户输入的名字在知识库中不存在时，给出明确提示

---

## 八、LangGraph 迁移后新问题（2026-06-12）

### 14. ChromaDB 1.5+ embed_query 返回格式错误
- **原因**：ChromaDB 1.5+ 期望 `embed_query` 返回嵌套列表 `[[0.1, 0.2, ...]]`，而非扁平列表 `[0.1, 0.2, ...]`
- **错误**：`TypeError: argument 'query_embeddings': 'float' object cannot be converted to 'Sequence'`
- **解决**：`embed_query` 返回 `vectors` 而非 `vectors[0]`

### 15. LLM 返回 JSON 被 markdown 代码块包裹
- **原因**：MiniMax 文本模型将 JSON 响应包裹在 markdown 代码块中（` ```json ... ``` `）
- **错误**：`json.loads()` 解析失败，返回 raw markdown 文本
- **解决**：解析前移除代码块标记
  ```python
  if content.startswith("```"):
      content = content.split("\n",1)[1]
      content = content.rsplit("```", 1)[0]
  ```

### 16. LLM 返回 JSON 数组而非对象
- **原因**：LLM 将一条信息拆分成多条记录，返回 JSON 数组 `[{...}, {...}]`
- **错误**：`'list' object has no attribute 'get'`
- **解决**：检测并取数组第一个元素
  ```python
  if isinstance(result, list):
      result = result[0] if result else {}
  ```

### 17. MiniMax Embedding API 需要 type 参数
- **原因**：MiniMax Embedding API 要求 `type: "query"` 参数，否则返回参数错误
- **错误**：`{'status_code': 2013, 'status_msg': 'invalid params, binding: expr_path=type, cause=missing required parameter'}`
- **解决**：在请求 JSON 中添加 `'type': 'query'`

### 18. ChromaDB 传入 embed_query 的参数类型
- **原因**：ChromaDB 调用 `embed_query` 时传入列表 `['糖糖']` 而非字符串 `'糖糖'`
- **解决**：`embed_query` 需要处理列表输入
  ```python
  def embed_query(self, input) -> list:
      if isinstance(input, list):
          texts = input
      else:
          texts = [input]
      vectors = self.embed(texts)
      return vectors if vectors else []
  ```

### 19. JSON 解析失败导致 member_name 为空
- **原因**：综合问题 15、16、17 导致 JSON 解析失败，classify 函数 fallback 到存储 raw input，member_name 为空
- **错误现象**：查询数据库发现 member_name 字段为空字符串
- **解决**：修复问题 15、16 后解决

---

## 九、问题根因总结（2026-06-12 更新）

| 问题类型 | 根本原因 | 影响 |
|---------|---------|------|
| Embedding 返回格式 | ChromaDB 1.5+ API 变更 | 语义搜索时类型错误 |
| LLM 响应格式 | MiniMax 模型输出格式 | JSON 解析失败 |
| API 参数要求 | MiniMax Embedding API 设计 | 缺少 type 参数导致请求失败 |

### 20. LLM 返回嵌套数组导致 member_name 为空
- **原因**：LLM 将用户输入拆分成多条记录，返回 JSON 数组 `[{...}, {...}, {...}]`
- **之前修复**：使用 `if isinstance(result, list): result = result[0]` 只处理单层数组
- **问题**：LLM 可能返回更深层的嵌套如 `[[{...}, {...}], ...]` 或数组第一个元素仍是数组
- **错误现象**：JSON 解析失败后 fallback，member_name 为空
- **解决**：改用 `while isinstance(result, list)` 递归 unwrap 直到得到 dict
  ```python
  while isinstance(result, list):
      result = result[0] if result else {}
  ```

### 21. 语义搜索返回不相关成员记录
- **原因**：当搜索的成员姓名不存在时，全局语义搜索返回最相似的向量匹配（其他成员的记录）
- **错误现象**：查询"糖糖"返回"汪佳齐"、"汪强"的记录
- **解决**：
  1. 改进 classify prompt，搜索查询时也提取 member_name
  2. search_info 增加成员存在性检查，不存在则返回明确提示
  ```python
  if member_name:
      all_members = chroma_manager.get_all_members()
      if member_name not in all_members:
          return {"tool_result": f"抱歉，知识库中还没有 {member_name} 的记录。"}
  ```

### 22. ChromaDB 1.5+ where clause 多条件查询语法错误
- **原因**：ChromaDB 1.5+ 的 `where` 参数不支持多字段字典 `{"field1": "val1", "field2": "val2"}`
- **错误**：`Expected where to have exactly one operator, got {...}`
- **解决**：使用 `$and` 操作符组合多个 `$eq` 条件
  ```python
  where_clause = {
      "$and": [
          {"member_name": {"$eq": member_name}},
          {"attribute_type": {"$eq": attribute_type}},
          {"content": {"$eq": old_content}}
      ]
  }
  ```

### 23. update_member_info 需要支持不精确匹配
- **原因**：用户说"其实XXX的生日是6月15日"，但数据库中可能存储的是"生日2018年3月"，两者不完全匹配
- **错误现象**：update 时找不到记录，更新失败
- **解决**：
  1. 先尝试精确匹配 old_content
  2. 如果没找到，尝试只按 member_name + attribute_type 查找
  3. 如果还没找到，只按 member_name 查找并过滤 attribute_type
  4. 找到后删除旧记录，添加新内容

### 24. LLM 返回多行 JSON 导致解析失败产生空记录
- **原因**：LLM 返回的 JSON 被 markdown 代码块包裹，但有多余内容或多个 JSON 对象
- **错误现象**：`json.loads()` 失败 "Extra data"，fallback 创建空 member_name 记录
- **错误信息**：`Extra data: line 6 column 2 (char 100)`
- **解决**：
  1. JSON 解析失败后，使用正则提取第一个 `{...}` JSON 对象
  2. 如果 member_name 为空，标记为 `action="unknown"` 而非 `action="add"`
  3. 防止创建空 member_name 记录
  ```python
  import re
  match = re.search(r'\{[^{}]*\}', content)
  if match:
      result = json.loads(match.group())
  ```

### 25. Agent 不支持上下文关联（代词解析）
- **原因**：Agent 处理每条输入时独立进行，没有记忆之前的对话内容
- **错误现象**：用户说"她还是一个跑步爱好者"，系统创建了 member_name="她" 的记录，而非"糖糖"
- **解决**：
  1. 在 state 中添加 `last_referenced_member` 字段
  2. 在 main.py 中维护对话上下文 `conversation_context`
  3. 在 classify 时检测代词（她/他/它），如果是代词则替换为 `last_referenced_member`
  4. 处理完信息后更新 `last_referenced_member`
  ```python
  # main.py 维护上下文
  conversation_context = {"last_referenced_member": ""}
  result = graph.invoke({"user_input": user_input, "last_referenced_member": conversation_context["last_referenced_member"]})
  if result.get("member_name") and result.get("member_name") not in ["她", "他", "它"]:
      conversation_context["last_referenced_member"] = result["member_name"]

  # classify 处理代词
  pronouns = ["她", "他", "它"]
  if member_name in pronouns and last_member:
      member_name = last_member
  ```
- **原因**：LLM 将用户输入拆分成多条记录，返回 JSON 数组 `[{...}, {...}, {...}]`
- **之前修复**：使用 `if isinstance(result, list): result = result[0]` 只处理单层数组
- **问题**：LLM 可能返回更深层的嵌套如 `[[{...}, {...}], ...]` 或数组第一个元素仍是数组
- **错误现象**：JSON 解析失败后 fallback，member_name 为空
- **解决**：改用 `while isinstance(result, list)` 递归 unwrap 直到得到 dict
  ```python
  while isinstance(result, list):
      result = result[0] if result else {}
  ```
### 26. 用户输入包含多条信息时只存储一条
- **原因**：用户输入 "她37岁，出生于1988年11月" 包含两条信息，但 JSON 格式只支持一条 content
- **错误现象**：LLM 只提取 "年龄37岁"，忽略 "出生于1988年11月"
- **解决**：在 prompt 中添加规则，用 "；" 分隔符连接多条信息
  ```
  如果用户输入包含多条信息，必须用"；"分隔符将所有信息连接在 content 中
  例如："年龄37岁；出生于1988年11月"
  ```

### 27. 数据库只读错误（频繁发生）
- **原因**：ChromaDB 持久化文件权限问题，可能与进程异常终止有关
- **错误**：`error returned from database: (code: 1032) attempt to write a readonly database`
- **解决**：删除 `./data/chroma_db/` 目录重新初始化

### 28. AI 推理出生年份错误（幻觉）
- **原因**：数据库中没有存储出生年份，AI 根据 "37岁" 自行推算为 1989年
- **错误现象**：用户说 "她是哪一年出生的？"，AI 回复 "1989年" 而非 "1988年11月"
- **解决**：这是 LLM 幻觉，不是代码 bug。需要确保数据库存储了完整的出生日期信息

### 29. 跨会话上下文丢失
- **原因**：`recent_members` 只在单次会话内维护，程序退出后上下文丢失
- **错误现象**：用户退出后重新启动程序，之前提到的代词 "她" 又无法识别
- **解决**：需要将上下文持久化存储到数据库或在启动时加载历史上下文

### 30. AI 误判"猜"为"add"操作
- **原因**：classify prompt 没有明确区分"询问/猜测" vs "确定/记录"
- **错误现象**：用户问 "你猜她是男的还是女的？"，AI 误判为 add 并存储 "性别女"，但回复却说 "没有性别信息"
- **幻觉问题**：respond 的回复与实际存储操作不一致
- **解决**：
  1. 在 classify prompt 中添加规则：询问 "猜"、"可能"、"是不是" → action="search"
  2. 添加示例："你猜她是男的还是女的？" → action="search"

### 31. 提到新家庭成员时没有自动录入
- **原因**：用户说"她老公是汪强"时，系统只存储了关系，没有把"汪强"作为独立家庭成员录入
- **错误现象**："汪强"没有出现在成员列表中
- **解决**：
  1. 在 state 中添加 `related_member_name` 字段
  2. 定义家庭成员关系词列表（老公、妻子、爸爸、妈妈等）
  3. 如果关系词是家庭成员关系词，自动为 related_member_name 创建基本记录
  4. 如果关系词不是家庭成员关系词（如好朋友、同学），不创建新成员
- **示例**：
  - "她老公是汪强" → 自动创建"汪强"为家庭成员 ✓
  - "糖糖的好朋友是张丽" → 不创建"张丽" ✗

---

## 十、向量数据库选型记录（2026-06-12）

### 32. 为什么选择 ChromaDB

**对比的数据库**：

| 数据库 | 特点 | 适合场景 |
|--------|------|----------|
| **Milvus** | 开源扛把子，大规模向量检索能力强 | 生产环境、大规模数据 |
| **Pinecone** | 云原生托管服务，零运维 | 云部署、快速上线 |
| **Weaviate** | 支持混合搜索（向量+关键词） | 混合检索场景 |
| **Qdrant** | Rust 实现，高性能 | 高性能需求 |
| **ChromaDB** | 轻量级、Python 原生、开发友好 | 小规模场景、原型开发 |

**选择 ChromaDB 的原因**：

1. **项目规模匹配**：家庭信息记录 Agent 数据量小（几十到几百条记录），无需 Milvus 的超大规模检索能力
2. **Python 原生**：与 LangGraph、LangChain 生态无缝集成
3. **开发友好**：API 简洁，LocalFile 持久化，一行代码启动
4. **快速原型**：无需额外部署服务，开箱即用

**结论**：ChromaDB 适合当前项目规模和开发阶段。如果未来数据量增长（>10万条记录），可考虑迁移到 Milvus 或 Qdrant。

**ChromaDB 的缺点**：

| 缺点 | 说明 |
|------|------|
| **只读错误频繁** | 进程异常终止（Ctrl+C、崩溃）会导致 SQLite 持久化文件损坏，产生 `(code: 1032) attempt to write a readonly database` 错误 |
| **不适合大规模数据** | 设计目标是轻量级，10万+ 记录时性能明显下降 |
| **持久化不稳定** | 底层 SQLite 在异常退出时容易产生文件锁残留、WAL 日志损坏 |
| **多用户支持弱** | 无内置访问控制，不适合多用户并发场景 |
| **生产环境不推荐** | 官方定位是"for building prototypes with not too much data"，非生产级解决方案 |

---

## 十一、架构设计决策：LLM 处理 vs 手动解析

### 问题
当需要从用户输入中提取结构化信息（如性别推理）时，应该：
- **方案 A**：在 prompt 中让 LLM 返回额外字段
- **方案 B**：用 Python 代码手动解析

### 对比

| 维度 | LLM 处理 | 手动解析 |
|------|----------|----------|
| **Token 消耗** | prompt 多加 300-500 token | 0 extra token |
| **代码复杂度** | 简单，只需解析 JSON | 复杂，要维护关系词映射 |
| **可维护性** | 易扩展，添加新规则只需改 prompt | 边界情况多，容易漏 |
| **准确性** | LLM 推理准确，不漏边界 | 依赖人工覆盖所有情况 |
| **适合场景** | 逻辑复杂、需要知识推理 | 简单字符串匹配 |

### 当前决策
选择 **LLM 处理**，理由：
1. **代码可维护性更重要**：当前项目 token 不是瓶颈
2. **关系逻辑复杂**：家庭成员关系种类多，手动映射易漏
3. **易于扩展**：未来添加新规则只需改 prompt

### 适用场景建议
- **用 LLM**：需要推理、判断、上下文理解的内容
- **用手写**：简单的关键词匹配、格式转换

### 回滚记录
- 2026-06-12：初始实现使用 LLM 处理性别推理
- 如需回滚到手动解析：
  1. 删除 prompt 中的性别推理规则和 member_genders 示例
  2. 恢复之前的手动关系词解析代码（graph.py 中已删除）
  3. main.py 中恢复 content 检测逻辑

---

## 十二、REST API 开发问题（2026-06-18）

### 33. 依赖缺失问题
- **类型**：技术栈问题
- **原因**：requirements.txt 缺少 FastAPI 相关依赖
- **错误**：`ModuleNotFoundError: No module named 'fastapi'`
- **解决**：添加 `fastapi>=0.110.0`, `uvicorn>=0.29.0`, `python-multipart>=0.0.9`, `Pillow>=10.3.0`, `pydub>=0.25.1`

### 34. ChromaManager 单例导入问题
- **类型**：代码问题
- **原因**：`chroma_manager.py` 没有导出单例，API 层无法直接导入
- **错误**：`ImportError: cannot import name 'chroma_manager'`
- **解决**：
  - tools.py 中初始化单例：`chroma_manager = ChromaManager()`
  - API 层从 tools 导入

---

## 十三、add-rest-api 功能问题（2026-06-18）

### 35. hobbies 爱好被覆盖而非追加
- **类型**：代码问题
- **原因**：`add_member_info` 在成员已存在时总是调用 `update`，导致相同 attribute_type 的记录被覆盖
- **错误现象**：
  - 输入 "喜欢画画和跳舞" 生成两条 hobby 记录
  - 但实际只有一条 hobby 记录，另一条被覆盖
- **解决**：改为**先检查完全相同的记录是否存在**
  - 如果已存在 → 跳过（避免重复）
  - 如果不存在 → 添加新记录

### 36. update 找不到记录时未添加新记录
- **类型**：代码问题
- **原因**：`update_member_info` 在找不到匹配记录时返回 False
- **错误现象**：当添加的关系记录不存在时，不会自动创建
- **解决**：找不到时改为**添加新记录**

### 37. "我女儿叫XXX" 句式未提取关系和反向关系
- **类型**：提示词问题
- **原因**：LLM 未正确识别这是关系描述
- **错误现象**：
  - 输入："我女儿叫汪佳齐，是一名二年级的小盆友，喜欢画画和跳舞"
  - 实际提取：basic_info (上二年级) + hobby (喜欢画画) + hobby (喜欢跳舞)
  - 缺失：relationship (女儿是汪佳齐) 和 member_genders (汪佳齐: 女)
- **解决**：
  - 在 pronouns 中添加 `"我"`
  - 添加示例：`"我女儿叫汪佳齐..."` → 生成 relationship + member_genders

### 38. 反向关系生成逻辑错误（一）
- **类型**：代码问题
- **原因**：关系词匹配时未按长度排序，"女儿" 优先于 "女儿是" 匹配
- **错误现象**：
  - 输入："女儿是汪佳齐"
  - 期望反向："妈妈是糖糖"
  - 实际反向："妈妈糖糖"（缺少"是"）
- **解决**：按 key 长度降序排序，优先匹配更长的 key

### 39. 反向关系生成逻辑错误（二）
- **类型**：代码问题
- **原因**：`FIXED_REVERSE_MAPPING` 包含 "妈妈是" → "女儿是"，但应该根据对方性别决定
- **错误现象**：
  - 输入："妈妈是糖糖"，对方是男性（汪莯晨）
  - 期望反向："儿子是汪莯晨"（汪莯晨是儿子）
  - 实际反向："女儿是糖糖"（错误！）
- **解决**：
  - 将 "妈妈是"、"爸爸是" 移到 `GENDER_BASED_RELATIONSHIP`
  - 根据 **related_member 的性别**（不是说话人性别）决定反向关系

### 40. "妈妈是XXX" 被 LLM 错误解析
- **类型**：提示词问题
- **原因**：LLM 把 "妈妈是糖糖" 解析为 `attribute_type="母亲"`, `content="糖糖"`
- **错误现象**：
  - 期望：`content="妈妈是糖糖"`, `attribute_type="relationship"`
  - 实际：`content="糖糖"`, `attribute_type="母亲"`
- **影响**：无法匹配反向关系映射，因为 key 不匹配
- **解决**：在 classify prompt 中添加示例 `"汪莯晨的妈妈是糖糖" → `content:"妈妈是糖糖"`

---

## 十四、Token 优化方案（2026-06-18）

### 41. Token 消耗过高
- **类型**：性能问题
- **原因**：classify prompt 包含约 20 个完整示例（约 167 行），每次调用消耗约 2000 tokens
- **问题**：
  - 示例太多导致每次 API 调用消耗大量 token
  - 大部分示例与当前输入无关（如用户只问"几口人"，却加载了所有关系示例）
- **解决方案**：实施方案 A - 动态加载相关示例
  1. 将所有示例移到外部文件 `data/classify_examples.json`
  2. 根据用户输入关键词匹配最相关的 3-5 个示例
  3. 只加载与当前输入相关的示例
- **预期效果**：prompt 从 ~2000 tokens 减少到 ~500 tokens，节省 60-70% token

### 42. count_family/aggregate_search 返回 unknown
- **类型**：代码问题
- **原因**：classify 函数中，检查 `member_name` 是否为空的代码错误地将 `first_action` 设置为 `"unknown"`
- **错误代码**：
  ```python
  if not first_member_name:
      first_action = "unknown"
  ```
- **问题**：对于 `count_family`、`aggregate_search` 等 action 类型，`member_name` 本身即为空字符串，但代码错误地据此将有效的 action 覆盖为 `"unknown"`
- **影响**：
  - "我们家几口人？" → action 返回 "unknown" 而非 "count_family"
  - "我们家谁爱做饭？" → action 返回 "unknown" 而非 "aggregate_search"
- **解决**：删除该错误代码块，因为 `member_name` 为空对于某些 action 类型是正常的，不应影响 action 的有效性
- **类型**：性能问题
- **原因**：classify prompt 包含约 20 个完整示例（约 167 行），每次调用消耗约 2000 tokens
- **问题**：
  - 示例太多导致每次 API 调用消耗大量 token
  - 大部分示例与当前输入无关（如用户只问"几口人"，却加载了所有关系示例）
- **解决方案**：实施方案 A - 动态加载相关示例
  1. 将所有示例移到外部文件 `data/classify_examples.json`
  2. 根据用户输入关键词匹配最相关的 3-5 个示例
  3. 只加载与当前输入相关的示例
- **预期效果**：prompt 从 ~2000 tokens 减少到 ~500 tokens，节省 60-70% token

### 实施步骤
1. ✅ 创建 `data/classify_examples.json` 存储所有示例
2. ✅ 添加 `_load_classify_examples()` 和 `_get_relevant_examples()` 函数
3. ✅ 修改 `classify()` 函数动态构建 prompt
4. ✅ 根据关键词匹配选择相关示例

---

## 十五、问题分类汇总

| ID | 问题 | 类型 | 子类 |
|----|------|------|------|
| 1-13 | 环境与依赖问题 | 技术栈 | Python/CrewAI 版本兼容 |
| 14-31 | LangGraph 迁移问题 | 技术栈 + 代码 | ChromaDB API/Embedding |
| 32 | 向量数据库选型 | 架构 | 设计决策 |
| 33 | REST API 依赖缺失 | 技术栈 | 依赖管理 |
| 34 | 单例导入问题 | 代码 | Import |
| 35 | hobbies 覆盖问题 | 代码 | 智能合并逻辑 |
| 36 | update 失败未添加 | 代码 | 边界处理 |
| 37 | 关系提取不完整 | 提示词 | Prompt 覆盖 |
| 38 | 反向关系缺少"是" | 代码 | 字符串匹配 |
| 39 | 反向关系性别错误 | 代码 | 关系映射逻辑 |
| 40 | LLM 解析格式错误 | 提示词 | Prompt 覆盖 |
| 41 | Token 消耗过高 | 性能 | Prompt 优化 |

### 问题类型统计

| 类型 | 数量 | 占比 |
|------|------|------|
| 技术栈问题 | 5 | 24% |
| 代码问题 | 8 | 38% |
| 提示词问题 | 5 | 24% |
| 架构/设计决策 | 2 | 10% |
| 性能优化 | 1 | 5% |
