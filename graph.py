"""
=============================================
LangGraph 模块 -定义家庭信息记录 Agent 的工作流
=============================================

使用 LangGraph 实现状态机工作流：
START → classify → [add/update/search/profile] → respond → END
"""

import json
from typing import TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

import config
from tools import (
    add_family_info,
    update_family_info,
    search_family_info,
    get_member_all_info,
    chroma_manager,
)


# =============================================
# State 定义
# =============================================

class FamilyAgentState(TypedDict):
    """LangGraph 状态定义"""
    user_input: str                    # 用户原始输入
    action: str                         # 动作类型：add/update/search/profile/unknown/confirm
    member_name: str # 成员姓名
    attribute_type: str                 # 属性类型
    content: str # 内容
    tool_result: str                   # 工具执行结果
    response: str                      # 最终回复
    recent_members: list               # 最近提到的成员列表（用于代词关联）
    related_member_name: str           # 关系中提到的另一个成员姓名（如"老公是XXX"中的XXX）
    records: list                      # 解析后的多条记录列表（每条包含 action, member_name, attribute_type, content, related_member_name）
    member_genders: dict               # 成员性别映射 {"糖糖": "女", "汪强": "男"}


# =============================================
# LLM 初始化
# =============================================

llm = ChatOpenAI(
    model=config.MINIMAX_MODEL_NAME,
    openai_api_base=config.MINIMAX_BASE_URL,
    openai_api_key=config.MINIMAX_API_KEY
)


# =============================================
# LangGraph 节点函数
# =============================================

def classify(state: FamilyAgentState) -> FamilyAgentState:
    """
    分类节点：使用 LLM 分析用户输入，确定动作类型和提取信息
    """
    user_input = state["user_input"]
    recent_members = state.get("recent_members", [])

    # 构建最近提到的成员上下文（用于代词关联）
    members_context = ""
    if recent_members:
        members_context = f"\n最近提到的成员：{', '.join(recent_members)}\n注意：如果用户输入中提到代词（她/他/它），应关联到上述成员。\n"

    prompt = f"""你是一个家庭信息录入助手。请分析用户输入，提取结构化信息。
{members_context}
用户输入：{user_input}

请严格按照以下JSON格式返回（只返回JSON，不要任何解释）：
{{"records":[...],"member_genders":{{"姓名":"性别",...}}}}

**重要规则**：
1. 当用户输入中包含代词（她/他/它/我的）时，必须根据对话历史推断出该代词指代的具体成员姓名，并填入 member_name。特别注意："我的女儿是汪佳齐"应理解为"主语的女儿是汪佳齐"，member_name应填主语。
2. 如果用户输入包含多条信息（如年龄、出生年月、职业等），必须用"；"分隔符将所有信息连接在 content 中，例如："年龄37岁；出生于1988年11月"
3. 如果输入是关系描述（如"XXX的老公是YYY"），需要：
   - 如果关系词是家庭成员关系词（老公、妻子、爸爸等），member_name="XXX"，related_member_name="YYY"
   - 如果关系词是非家庭成员关系词（好朋友、同学等），member_name="XXX"，related_member_name=""（留空）
4. 每条信息单独一条记录，不要合并多条不同类型的信息到一条 content 中。例如：
   - "她37岁，职业是老师" →两条记录：{{"content":"年龄37岁"}} 和 {{"content":"职业是老师"}}
   - "她老公是汪强" →一条记录：{{"content":"老公是汪强","related_member_name":"汪强"}}
5. 根据关系描述推理性别并填入 member_genders：
   - "X的老公是Y" → member_genders["X"]="女", member_genders["Y"]="男"
   - "X的妻子是Y" → member_genders["X"]="男", member_genders["Y"]="女"
   - "X的爸爸是Y" → member_genders["Y"]="男"（X是孩子，性别未知）
   - "X的妈妈是Y" → member_genders["Y"]="女"（X是孩子，性别未知）
   - "X的儿子是Y" → member_genders["Y"]="男"
   - "X的女儿是Y" → member_genders["Y"]="女"
   - "X的爷爷是Y" 或 "X的外公是Y" → member_genders["Y"]="男"
   - "X的奶奶是Y" 或 "X的外婆是Y" → member_genders["Y"]="女"

判断规则：
- action="add"：用户**明确提供**或**确定**家庭成员的信息（姓名、年龄、职业、生日等）。注意：询问"猜"、"可能"、"是不是"等不确定的表达 → action="search"
- action="update"：用户提到"其实"、"不对"、"记错了"、"更正"、"修改"等词，表示要修改已有信息
- action="search"：用户问"查询"、"什么"、"有没有"、"猜"、"可能"等问题
- action="aggregate_search"：用户问"谁"、"哪个"等需要从多个成员记录中分析比较的问题，如"谁最爱做饭"、"谁的职业是老师"
- action="count_family"：用户问"几口人"、"多少人"、"请问...几口人"等统计家庭成员数量的问题
- action="self_identify"：用户说"我是X"、"X是我"、"我才是X"等自我身份声明，如"糖糖是我"、"我才是糖糖"
- action="profile"：用户请求"总结"、"画像"
- action="unknown"：无法理解用户意图

attribute_type取值：
- 姓名、年龄、职业、生日、民族、学历等 → "basic_info"
- 爱好、特长 → "hobby"
- 工作经历 → "work_experience"
- 重要事件如旅游、搬家、结婚 → "life_event"
- 性格描述 → "personality"
- 能力描述（如"不太会做饭"、"不擅长游泳"） → "ability"
- 家庭关系 → "relationship"

**否定描述检测**：
如果输入包含"不太会"、"不擅长"、"不会"、"没兴趣"等否定词，即使内容涉及爱好，也应存为 "ability" 而非 "hobby"。
例如：
- "汪强不太会做饭" → attribute_type="ability", content="不太会做饭"
- "糖糖不爱运动" → attribute_type="ability", content="不爱运动"

**家庭成员关系词（必须同时录入关系中的另一方为家庭成员）**：
老公、妻子、丈夫、老婆、爸、妈妈、儿子、女儿、哥哥、弟弟、姐姐、妹妹、爷爷、奶奶、外公、外婆、公公、婆婆、岳父、岳母、配偶

**非家庭成员关系词（只存储关系，不录入另一方）**：
好朋友、朋友、同学、同事、老师、学生、邻居、亲戚等

示例：
- "我叫糖糖，今年37岁" → {{"records":[{{"action":"add", "member_name":"糖糖", "attribute_type":"basic_info", "content":"年龄37岁", "related_member_name":""}}], "member_genders":{{"糖糖":"女"}}}}
- "她37岁，出生于1988年11月" → {{"records":[{{"action":"add", "member_name":"糖糖", "attribute_type":"basic_info", "content":"年龄37岁", "related_member_name":""}}, {{"action":"add", "member_name":"糖糖", "attribute_type":"basic_info", "content":"出生于1988年11月", "related_member_name":""}}], "member_genders":{{"糖糖":"女"}}}}
- "汪佳齐上二年级，喜欢画画" → {{"records":[{{"action":"add", "member_name":"汪佳齐", "attribute_type":"basic_info", "content":"上二年级", "related_member_name":""}}, {{"action":"add", "member_name":"汪佳齐", "attribute_type":"hobby", "content":"喜欢画画", "related_member_name":""}}], "member_genders":{{}}}}
- "她今年38岁，出生于1988年11月，职业是软件测试工程师，老公是汪强" → {{
  "records":[
    {{"action":"add", "member_name":"糖糖", "attribute_type":"basic_info", "content":"年龄38岁", "related_member_name":""}},
    {{"action":"add", "member_name":"糖糖", "attribute_type":"basic_info", "content":"出生于1988年11月", "related_member_name":""}},
    {{"action":"add", "member_name":"糖糖", "attribute_type":"basic_info", "content":"职业是软件测试工程师", "related_member_name":""}},
    {{"action":"add", "member_name":"糖糖", "attribute_type":"relationship", "content":"老公是汪强", "related_member_name":"汪强"}}
  ],
  "member_genders":{{"糖糖":"女", "汪强":"男"}}
}}
- "她老公是汪强" → {{"records":[{{"action":"add", "member_name":"糖糖", "attribute_type":"relationship", "content":"老公是汪强", "related_member_name":"汪强"}}], "member_genders":{{"糖糖":"女", "汪强":"男"}}}}
- "汪佳齐的爸爸是汪强" → {{"records":[{{"action":"add", "member_name":"汪佳齐", "attribute_type":"relationship", "content":"爸爸是汪强", "related_member_name":"汪强"}}], "member_genders":{{"汪强":"男"}}}}
- "糖糖的好朋友是张丽" → {{"records":[{{"action":"add", "member_name":"糖糖", "attribute_type":"relationship", "content":"好朋友是张丽", "related_member_name":""}}], "member_genders":{{}}}}
- "查询糖糖" → {{"records":[{{"action":"search", "member_name":"糖糖", "attribute_type":"basic_info", "content":"糖糖", "related_member_name":""}}], "member_genders":{{}}}}
- "她还是跑步爱好者" → {{"records":[{{"action":"add", "member_name":"糖糖", "attribute_type":"hobby", "content":"跑步爱好者", "related_member_name":""}}], "member_genders":{{"糖糖":"女"}}}}
- "他的职业是老师" → {{"records":[{{"action":"add", "member_name":"汪强", "attribute_type":"basic_info", "content":"职业是老师", "related_member_name":""}}], "member_genders":{{"汪强":"男"}}}}
- "糖糖爱做饭，汪强不太会做饭" → [
  {{"records":[{{"action":"add", "member_name":"糖糖", "attribute_type":"hobby", "content":"爱做饭", "related_member_name":""}}, {{"action":"add", "member_name":"汪强", "attribute_type":"ability", "content":"不太会做饭", "related_member_name":""}}], "member_genders":{{}}}}
- "汪强不爱运动" → {{"records":[{{"action":"add", "member_name":"汪强", "attribute_type":"ability", "content":"不爱运动", "related_member_name":""}}], "member_genders":{{"汪强":"男"}}}}
- "请问我们家谁最爱做饭？" → {{"records":[{{"action":"aggregate_search", "member_name":"", "attribute_type":"hobby", "content":"爱做饭", "related_member_name":""}}], "member_genders":{{}}}}
- "请问我们家谁职业是老师？" → {{"records":[{{"action":"aggregate_search", "member_name":"", "attribute_type":"basic_info", "content":"职业是老师", "related_member_name":""}}], "member_genders":{{}}}}
- "我们家几口人？" → {{"records":[{{"action":"count_family", "member_name":"", "attribute_type":"", "content":"", "related_member_name":""}}], "member_genders":{{}}}}
- "请问我们一家几口人？" → {{"records":[{{"action":"count_family", "member_name":"", "attribute_type":"", "content":"", "related_member_name":""}}], "member_genders":{{}}}}
- "糖糖是我" → {{"records":[{{"action":"self_identify", "member_name":"糖糖", "attribute_type":"", "content":"我是糖糖", "related_member_name":""}}], "member_genders":{{}}}}
- "我才是糖糖" → {{"records":[{{"action":"self_identify", "member_name":"糖糖", "attribute_type":"", "content":"我才是糖糖", "related_member_name":""}}], "member_genders":{{}}}}
"""

    response = llm.invoke(prompt)

    # 代词列表，用于上下文关联
    pronouns = ["她", "他", "它", "我的"]
    recent_members = state.get("recent_members", [])
    member_genders = dict(state.get("member_genders", {}))

    try:
        content = response.content.strip()
        # 移除 markdown 代码块标记
        if content.startswith("```"):
            content = content.split("\n",1)[1]
            content = content.rsplit("```", 1)[0]
        content = content.strip()

        result = json.loads(content)

        # 处理 LLM 返回的新格式 {"records":[...], "member_genders":{...}}
        parsed_records = []
        if isinstance(result, dict):
            parsed_records = result.get("records", [])
            llm_genders = result.get("member_genders", {})
            if llm_genders:
                member_genders.update(llm_genders)
        elif isinstance(result, list):
            # 旧格式（数组）：保持向后兼容
            parsed_records = result
        else:
            parsed_records = []

        # 处理每条记录的代词关联
        processed_records = []
        first_action = "unknown"
        first_member_name = ""

        for record in parsed_records:
            if not isinstance(record, dict):
                continue

            member_name = record.get("member_name", "")

            # 处理代词关联
            if member_name in pronouns and recent_members:
                # 根据性别解析代词
                target_gender = "女" if member_name == "她" else "男"
                resolved_name = None

                # 在 recent_members 中查找匹配性别的成员
                for rm in recent_members:
                    if member_genders.get(rm) == target_gender:
                        resolved_name = rm
                        break

                if resolved_name:
                    print(f"[classify] 检测到代词 '{member_name}'，根据性别解析为 '{resolved_name}'")
                    member_name = resolved_name
                else:
                    # 无法根据性别解析，返回 confirm 让用户确认
                    print(f"[classify] 检测到代词 '{member_name}'，但无法确定是谁，标记为 confirm")
                    record["action"] = "confirm"
                    record["member_name"] = ""
                    record["content"] = f"您说的「{member_name}」是指哪位？"
            elif member_name in pronouns and not recent_members:
                # 代词无法解析，标记为 unknown
                print(f"[classify] 检测到代词 '{member_name}'，但 recent_members 为空，标记为 unknown")
                record["action"] = "unknown"
                record["member_name"] = ""
            elif member_name and member_name not in pronouns:
                # 更新 recent_members
                if member_name not in recent_members:
                    recent_members.insert(0, member_name)
                recent_members = recent_members[:3]

            # 更新 record 的 member_name
            record["member_name"] = member_name

            # 保留第一条记录的信息用于路由
            if first_action == "unknown" and record.get("action") != "unknown":
                first_action = record.get("action", "unknown")
                first_member_name = member_name

            processed_records.append(record)

        # 如果没有找到有效action，使用第一条记录的action
        if first_action == "unknown" and processed_records:
            first_action = processed_records[0].get("action", "unknown")

        # 确保 member_name 不为空
        if not first_member_name and processed_records:
            first_member_name = processed_records[0].get("member_name", "")
        if not first_member_name:
            first_action = "unknown"

        return {
            "action": first_action,
            "member_name": first_member_name,
            "attribute_type": processed_records[0].get("attribute_type", "basic_info") if processed_records else "basic_info",
            "content": processed_records[0].get("content", user_input) if processed_records else user_input,
            "tool_result": "",
            "response": "",
            "recent_members": recent_members,
            "related_member_name": processed_records[0].get("related_member_name", "") if processed_records else "",
            "records": processed_records,
            "member_genders": member_genders
        }
    except Exception as e:
        # JSON解析失败时，尝试提取第一个 JSON 对象
        print(f"[classify] JSON解析失败: {e}，尝试提取第一个 JSON 对象")
        import re
        # 查找第一个 { 到最后一个 } 之间的内容
        match = re.search(r'\{[^{}]*\}', content)
        if match:
            try:
                result = json.loads(match.group())
                if result.get("member_name"):
                    member_name = result.get("member_name", "")
                    if member_name in pronouns and recent_members:
                        # 根据性别解析代词
                        target_gender = "女" if member_name == "她" else "男"
                        resolved_name = None
                        for rm in recent_members:
                            if member_genders.get(rm) == target_gender:
                                resolved_name = rm
                                break
                        if resolved_name:
                            print(f"[classify] 检测到代词 '{member_name}'，根据性别解析为 '{resolved_name}'")
                            member_name = resolved_name
                        else:
                            print(f"[classify] 检测到代词 '{member_name}'，但无法确定是谁，标记为 confirm")
                            result["action"] = "confirm"
                            result["content"] = f"您说的「{member_name}」是指哪位？"
                            member_name = ""
                    elif member_name in pronouns and not recent_members:
                        print(f"[classify] 检测到代词 '{member_name}'，但 recent_members 为空，标记为 unknown")
                        result["action"] = "unknown"
                        member_name = ""
                    elif member_name and member_name not in pronouns:
                        if member_name not in recent_members:
                            recent_members.insert(0, member_name)
                        recent_members = recent_members[:3]
                    return {
                        "action": result.get("action", "add"),
                        "member_name": member_name,
                        "attribute_type": result.get("attribute_type", "basic_info"),
                        "content": result.get("content", user_input),
                        "tool_result": "",
                        "response": "",
                        "recent_members": recent_members,
                        "related_member_name": result.get("related_member_name", ""),
                        "records": [result]
                    }
            except:
                pass

        # 解析失败，不存储空记录，标记为 unknown
        print(f"[classify] 无法提取有效 JSON，标记为 unknown")
        return {
            "action": "unknown",
            "member_name": "",
            "attribute_type": "basic_info",
            "content": user_input,
            "tool_result": "",
            "response": "",
            "recent_members": recent_members,
            "related_member_name": "",
            "records": []
        }


def add_info(state: FamilyAgentState) -> FamilyAgentState:
    """
    添加信息节点：调用 add_family_info 工具
    支持单条或多条记录（从 records 字段获取）
    如果有 related_member_name，还需要为该成员创建基本记录
    """
    results = []

    # 角色词列表（不创建新成员的词）
    role_words = ["主人", "管家", "老板", "领导", "老师", "同学", "朋友", "同事"]

    # 获取记录列表
    records = state.get("records", [])
    if not records:
        # 向后兼容：如果没有 records，使用单条记录逻辑
        records = [{
            "member_name": state["member_name"],
            "attribute_type": state["attribute_type"],
            "content": state["content"],
            "related_member_name": state.get("related_member_name", "")
        }]

    # 处理每条记录
    for record in records:
        member_name = record.get("member_name", "")
        attribute_type = record.get("attribute_type", "basic_info")
        content = record.get("content", "")
        related_member = record.get("related_member_name", "")

        # 跳过无效记录
        if not member_name or not content:
            print(f"[add_info] 跳过无效记录: member_name={member_name}, content={content}")
            continue

        # 检查 related_member_name 是否是角色描述
        is_role = related_member and any(role in related_member for role in role_words)

        # 如果是角色描述，将角色信息添加到主成员内容中，不创建新成员
        if is_role:
            result = add_family_info._run(
                member_name=member_name,
                attribute_type="relationship",
                content=content
            )
            results.append(result)
            print(f"[add_info] '{related_member}' 是角色描述，已添加到 {member_name} 的关系中")
            continue

        # 如果 related_member_name 是人名（非角色），为主动创建基本记录
        if related_member:
            all_members = chroma_manager.get_all_members()
            if related_member not in all_members:
                result_related = add_family_info._run(
                    member_name=related_member,
                    attribute_type="basic_info",
                    content=f"家庭成员"
                )
                results.append(result_related)
                print(f"[add_info] 已自动创建新成员: {related_member}")

        # 添加主成员信息
        result = add_family_info._run(
            member_name=member_name,
            attribute_type=attribute_type,
            content=content
        )
        results.append(result)

    return {"tool_result": "\n".join(results)}


def update_info(state: FamilyAgentState) -> FamilyAgentState:
    """
    更新信息节点：调用 update_family_info 工具
    """
    result = update_family_info._run(
        member_name=state["member_name"],
        attribute_type=state["attribute_type"],
        old_content=state["content"],
        new_content=state["content"]
    )
    return {"tool_result": result}


def search_info(state: FamilyAgentState) -> FamilyAgentState:
    """
    搜索信息节点：调用 search_family_info 工具
    """
    member_name = state["member_name"]

    # 如果指定了成员姓名，先检查该成员是否存在
    if member_name:
        all_members = chroma_manager.get_all_members()
        if member_name not in all_members:
            return {"tool_result": f"抱歉，知识库中还没有 {member_name} 的记录。请先录入该成员的基本信息。"}

    result = search_family_info._run(
        query_text=state["user_input"],
        member_name=member_name if member_name else None
    )
    return {"tool_result": result}


def get_profile(state: FamilyAgentState) -> FamilyAgentState:
    """
    获取画像节点：调用 get_member_all_info 工具
    """
    if not state["member_name"]:
        return {"tool_result": "请告诉我您想查询哪位家庭成员的画像"}

    result = get_member_all_info._run(member_name=state["member_name"])
    return {"tool_result": result}


def respond(state: FamilyAgentState) -> FamilyAgentState:
    """
    回复节点：使用 LLM 生成最终的自然语言回复
    """
    tool_result = state["tool_result"]
    action = state["action"]
    user_input = state["user_input"]

    if action == "unknown":
        response_text = "抱歉，我不太理解您的意思。您可以告诉我成员姓名和要记录的信息。"
    elif action == "confirm":
        content = state.get("content", "")
        pronoun = "她" if "她" in user_input else "他"
        # 获取 recent_members 中已知性别的成员列表
        recent_members = state.get("recent_members", [])
        member_genders = state.get("member_genders", {})
        candidates = [m for m in recent_members if member_genders.get(m)]
        if candidates:
            names = "、".join(candidates)
            response_text = f"您说的「{pronoun}」是指哪位？{names}？请明确告诉我您想说的是谁。"
        else:
            response_text = f"您说的「{pronoun}」是指哪位？请明确告诉我您想说的是谁。"
    elif action == "aggregate_search":
        prompt = f"""你是家庭管家，根据搜索结果回答用户问题。

搜索结果：
{tool_result}

用户问题：{user_input}

请从搜索结果中找出最符合用户问题的答案。如果搜索结果中没有相关信息，请如实告知用户。
回答要简洁温暖。
"""
        response = llm.invoke(prompt)
        response_text = response.content
    elif action == "count_family":
        members = chroma_manager.get_all_members()
        if members:
            response_text = f"您家有 {len(members)} 口人，分别是：{', '.join(members)}"
        else:
            response_text = "目前还没有录入任何家庭成员的信息哦。"
    elif action == "self_identify":
        member_name = state.get("member_name", "")
        if member_name:
            response_text = f"好的，我记住了，您就是糖糖。以后我会更好地为您服务！"
        else:
            response_text = "好的，我记住了您的话。"
    else:
        prompt = f"""你是家庭管家，根据工具执行结果回复用户。

工具执行结果：
{tool_result}

用户原始输入：{user_input}

请用温暖亲切的语气回复用户，简明扼要地告知执行结果。
如果不是纯确认信息，可以适当补充说明。
"""
        response = llm.invoke(prompt)
        response_text = response.content

    return {"response": response_text}


# =============================================
# 构建 LangGraph
# =============================================

def build_graph():
    """
    构建家庭信息记录 Agent 的 StateGraph
    """
    builder = StateGraph(FamilyAgentState)

    # 添加节点
    builder.add_node("classify", classify)
    builder.add_node("add_info", add_info)
    builder.add_node("update_info", update_info)
    builder.add_node("search_info", search_info)
    builder.add_node("get_profile", get_profile)
    builder.add_node("respond", respond)

    # 设置入口和出口
    builder.add_edge(START, "classify")

    # 分类节点根据 action 结果路由到不同节点
    def route_action(state: FamilyAgentState) -> str:
        action = state.get("action", "unknown")
        if action == "add":
            return "add_info"
        elif action == "update":
            return "update_info"
        elif action == "search":
            return "search_info"
        elif action == "aggregate_search":
            return "search_info"
        elif action == "count_family":
            return "respond"
        elif action == "self_identify":
            return "respond"
        elif action == "profile":
            return "get_profile"
        elif action == "confirm":
            return "respond"
        else:
            return "respond"

    builder.add_conditional_edges(
        "classify",
        route_action,
        {
            "add_info": "add_info",
            "update_info": "update_info",
            "search_info": "search_info",
            "get_profile": "get_profile",
            "respond": "respond"
        }
    )

    # 所有工具节点都连接到回复节点
    builder.add_edge("add_info", "respond")
    builder.add_edge("update_info", "respond")
    builder.add_edge("search_info", "respond")
    builder.add_edge("get_profile", "respond")

    # 回复节点连接到结束
    builder.add_edge("respond", END)

    return builder


# 构建编译后的图
graph = build_graph().compile()