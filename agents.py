"""
=============================================
Agent 模块 -定义所有 CrewAI Agent 和 Task
=============================================
"""

from crewai import Agent, Task
from langchain_openai import ChatOpenAI

import config
from tools import (
    add_family_info,
    update_family_info,
    search_family_info,
    get_member_all_info,
    delete_family_info,
    get_all_members
)


# =============================================
# 初始化大语言模型
# =============================================

# 创建 MiniMax 大模型实例
llm = ChatOpenAI(
    model=config.MINIMAX_MODEL_NAME,
    openai_api_base=config.MINIMAX_BASE_URL,
    openai_api_key=config.MINIMAX_API_KEY
)


# =============================================
# Agent 1: 信息录入员（Recorder）
# =============================================

recorder_agent = Agent(
    role="信息录入员",
    goal="严格从用户输入中提取姓名，绝不自行推断或使用示例姓名",
    backstory=(
        "你是一个细心耐心的信息录入员，擅长从日常对话中捕捉家庭成员的点点滴滴。"
        "你必须严格按照用户输入的字面意思提取信息，绝不自行脑补。"
    ),
    verbose=True,
    allow_delegation=False,
    tools=[
        add_family_info,
        update_family_info,
        get_all_members
    ],
    llm=llm
)


# =============================================
# Agent 2: 知识库管理员（Librarian）
# =============================================

librarian_agent = Agent(
    role="知识库管理员",
    goal="高效管理家庭知识库，确保信息的准确存储和及时更新",
    backstory=(
        "你是家庭知识库的守护者，管理着一个装满家庭回忆的宝库。"
        "你熟悉每一个家庭成员的档案，能够快速定位和更新信息。"
        "你做事井井有条，确保知识库中的每一条记录都井然有序。"
    ),
    verbose=True,
    allow_delegation=False,
    tools=[
        add_family_info,
        update_family_info,
        delete_family_info,
        get_member_all_info,
        get_all_members
    ],
    llm=llm
)


# =============================================
# Agent 3: 智能查询员（Searcher）
# =============================================

searcher_agent = Agent(
    role="智能查询员",
    goal="理解用户的问题，从知识库中找到最相关的信息",
    backstory=(
        "你是一个聪明的搜索专家，擅长理解用户问题的真实意图。"
        "即使问题表述模糊，你也能通过语义理解找到相关信息。"
        "你熟悉语义检索技术，总能从海量信息中找出最匹配的那一条。"
    ),
    verbose=True,
    allow_delegation=False,
    tools=[
        search_family_info,
        get_member_all_info,
        get_all_members
    ],
    llm=llm
)


# =============================================
# Agent 4: 家庭管家（Steward）
# =============================================

steward_agent = Agent(
    role="家庭管家",
    goal="综合分析信息，生成温暖体贴的回复，并能为家庭成员生成画像总结",
    backstory=(
        "你是家庭的大管家，温文尔雅，谈吐亲切。"
        "你记得家里每一个人的喜好、特点和各种重要日子。"
        "你不仅能回答问题，还能根据零散的信息为家庭成员描绘出生动的人物画像。"
        "你说话温暖有力，总是能给出贴心又有用的回答。"
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm
)


# =============================================
# Task 1: 信息录入
# =============================================

record_task = Task(
    description=(
        "理解用户输入的自然语言，提取结构化信息并存储到知识库。\n"
        "\n"
        "【用户输入内容】\n"
        "{user_input}\n"
        "\n"
        "【强制规则】\n"
        "1. 用户输入的字 → 你输出的字，原文提取，不做任何修改\n"
        "2. 绝对禁止：用自己的理解改写、简化、或编造任何名字\n"
        "\n"
        "你需要：\n"
        "1. 从上述用户输入中精确提取成员的真实姓名\n"
        "2. 识别信息类型（basic_info/hobby/work_experience/life_event/personality/relationship）\n"
        "3. 提取具体内容\n"
        "4. 调用 add_family_info 工具存储信息\n"
        "\n"
        "属性类型判断规则：\n"
        "- 姓名、职业、生日、民族、学历 → basic_info\n"
        "- 爱好、特长 → hobby\n"
        "- 工作经历 → work_experience\n"
        "- 重要事件如旅游、搬家、结婚 → life_event\n"
        "- 性格描述 → personality\n"
        "- 家庭关系描述 → relationship\n"
        "\n"
        "重要提示：如果无法确定属性类型，默认使用 basic_info"
    ),
    expected_output="操作完成的确认信息，必须使用用户输入中的真实姓名",
    agent=recorder_agent
)


# =============================================
# Task 2: 智能查询
# =============================================

search_task = Task(
    description=(
        "接收用户的问题，从知识库中检索相关信息并返回结果。\n"
        "\n"
        "【用户问题】\n"
        "{user_input}\n"
        "\n"
        "你需要：\n"
        "1. 理解用户问题的真实意图\n"
        "2. 提取关键词和限定条件（如成员姓名）\n"
        "3. 调用检索工具搜索相关信息\n"
        "4. 对检索结果进行筛选和整理\n"
        "\n"
        "如果检索结果为空，诚实地告诉用户知识库中没有相关信息。"
    ),
    expected_output="检索到的相关信息列表，如果没有找到则说明情况",
    agent=searcher_agent
)


# =============================================
# Task 3: 画像总结
# =============================================

profile_task = Task(
    description=(
        "根据知识库中某个家庭成员的所有信息，生成一段人物画像总结。\n"
        "\n"
        "【用户请求】\n"
        "{user_input}\n"
        "\n"
        "你需要：\n"
        "1. 从用户请求中提取要总结的成员姓名\n"
        "2. 调用 get_member_all_info_tool 获取该成员的所有信息\n"
        "3. 分析和整理这些零散的信息\n"
        "4. 用大模型能力生成一段连贯、生动的人物画像\n"
        "5. 画像应该包含：基本信息、性格特点、爱好特长、重要经历等方面\n"
        "\n"
        "回复风格要温馨亲切，像是在描述一个真实的人。"
    ),
    expected_output="一段人物画像总结文字",
    agent=steward_agent
)


# =============================================
# Task 4: 综合回复
# =============================================

respond_task = Task(
    description=(
        "综合用户问题和检索到的信息，生成最终的自然语言回复。\n"
        "\n"
        "这个 Task 由 Steward（家庭管家）Agent 执行，接收 Searcher 的检索结果，\n"
        "结合大模型的理解能力，生成最终回复。\n"
        "\n"
        "回复原则：\n"
        "1. 语气温暖亲切，像家庭管家一样说话\n"
        "2. 如果检索到了信息，基于信息给出回答\n"
        "3. 如果信息不完整，说明已知的信息并承认局限性\n"
        "4. 如果没有检索到信息，诚实说明并友好引导用户补充信息\n"
        '5. 可以适当补充常识性的家庭角色知识（如"爸爸通常承担做饭"等）\n'
        "\n"
        "如果用户说「退出」或「再见」，回复告别语。"
    ),
    expected_output="面向用户的自然语言回复",
    agent=steward_agent
)