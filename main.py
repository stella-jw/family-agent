"""
=============================================
主入口模块 -命令行交互循环
=============================================

使用 LangGraph 工作流处理家庭信息记录。
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from graph import graph


WELCOME_MESSAGE = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║       欢迎使用「家庭信息记录 Agent」智能管家                      ║
║                                                              ║ 
║        我可以帮您记录、查询和管理家庭成员的各类信息                 ║ 
║        包括基本信息、爱好、经历、重要日期等等                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

📝 示例命令：
   • "汪佳齐的信息：职业是老师"
   • "查询汪佳齐的生日"
   • "其实汪佳齐的生日是6月15日"
   • "帮我总结汪佳齐的人物画像"
   • "退出" - 结束对话

───────────────────────────────────────────────────────────────
"""


GOODBYE_MESSAGE = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        再见！家庭的每一份记忆，我都替您珍藏着。                     ║
║                                                              ║
║👋 祝您生活愉快！                                                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""


def main():
    print(WELCOME_MESSAGE)

    # 验证配置
    errors = config.validate_config()
    if errors:
        print("\n⚠️  配置检查发现问题：")
        for error in errors:
            print(f"   {error}")
        print("\n请参考 .env.example 文件配置环境变量，然后重新运行程序。\n")
        sys.exit(1)

    print("✅ 系统初始化完成！开始与管家对话吧~\n")
    print("=" * 60)

    # 维护对话上下文（用于代词关联）
    # 只存储最近提到的成员列表，避免完整历史带来的 token 消耗
    conversation_context = {
        "recent_members": [],  # 最近提到的成员列表，如 ["糖糖", "汪佳齐"]
        "member_genders": {},  # 成员性别映射，如 {"糖糖": "女", "汪强": "男"}
    }

    while True:
        try:
            user_input = input("\n👤 您：").strip()

            if not user_input:
                continue

            if user_input in ["退出", "再见", "拜拜", "quit", "exit", "bye"]:
                print(f"\n🤖 管家：{GOODBYE_MESSAGE}")
                break

            print("\n🤖 管家：正在处理，请稍候...")

            # 调用 LangGraph 工作流，传入对话上下文
            result = graph.invoke(
                {
                    "user_input": user_input,
                    "recent_members": conversation_context["recent_members"],
                    "member_genders": conversation_context["member_genders"],
                },
                config={"recursion_limit": 50}
            )

            # 更新最近提到的成员列表（最多保留3个）
            if result.get("member_name") and result.get("member_name") not in ["她", "他", "它"]:
                members = conversation_context["recent_members"]
                if result["member_name"] not in members:
                    members.insert(0, result["member_name"])
                if len(members) > 3:
                    members = members[:3]
                conversation_context["recent_members"] = members

            # 更新成员性别映射
            if result.get("member_genders"):
                conversation_context["member_genders"].update(result["member_genders"])

            print(f"\n🤖 管家：{result['response']}")

        except KeyboardInterrupt:
            print(f"\n\n🤖 管家：{GOODBYE_MESSAGE}")
            break
        except Exception as e:
            print(f"\n⚠️ 发生错误：{e}")
            print("请尝试重新输入或重启程序。\n")


if __name__ == "__main__":
    main()