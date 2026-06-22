"""
=============================================
家庭信息记录 Agent - 自动化测试用例集
=============================================

运行方式：
    python test_family_agent.py

测试覆盖：
- 代词解析与性别映射
- 多记录一次性录入
- 否定描述处理（ability vs hobby）
- 家庭成员数量统计
- 聚合搜索（谁XXX）
- 关系描述与性别推理
- 未知意图处理
- 代词确认机制
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from graph import classify, add_info, chroma_manager
from langchain_openai import ChatOpenAI
import config


# =============================================
# 测试辅助函数
# =============================================

def print_test_header(name):
    print(f"\n{'='*60}")
    print(f"测试: {name}")
    print('='*60)


def print_test_result(name, passed, error=None):
    if passed:
        print(f"✅ {name} - 通过")
    else:
        print(f"❌ {name} - 失败: {error}")


class MockState:
    """模拟 LangGraph 状态"""
    def __init__(self, **kwargs):
        self._data = kwargs

    def get(self, key, default=None):
        return self._data.get(key, default)

    def __getitem__(self, key):
        return self._data[key]


# =============================================
# 测试用例
# =============================================

def test_pronoun_resolution_female():
    """测试：代词'她'应解析为女性成员"""
    print_test_header("代词'她'解析为女性成员")

    state = MockState(
        user_input="她今年38岁",
        recent_members=["糖糖", "汪强"],
        member_genders={"糖糖": "女", "汪强": "男"}
    )

    result = classify(state)

    passed = result["member_name"] == "糖糖"
    print_test_result("代词'她'应指向女性成员'糖糖'", passed,
                      f"实际: {result.get('member_name')}")
    return passed


def test_pronoun_resolution_male():
    """测试：代词'他'应解析为男性成员"""
    print_test_header("代词'他'解析为男性成员")

    state = MockState(
        user_input="他今年40岁",
        recent_members=["糖糖", "汪强"],
        member_genders={"糖糖": "女", "汪强": "男"}
    )

    result = classify(state)

    passed = result["member_name"] == "汪强"
    print_test_result("代词'他'应指向男性成员'汪强'", passed,
                      f"实际: {result.get('member_name')}")
    return passed


def test_pronoun_confirm_when_gender_unknown():
    """测试：当无法确定代词性别时应返回 confirm"""
    print_test_header("代词无法确定性别时返回 confirm")

    state = MockState(
        user_input="他爱运动",
        recent_members=["小明", "小红"],  # 性别未知
        member_genders={}
    )

    result = classify(state)

    passed = result["action"] == "confirm"
    print_test_result("性别未知时代词应触发 confirm", passed,
                      f"实际 action: {result.get('action')}")
    return passed


def test_multiple_records_single_input():
    """测试：单次输入多条信息应返回多条记录"""
    print_test_header("单次输入多条信息")

    state = MockState(
        user_input="糖糖今年38岁，职业是软件测试工程师，老公是汪强",
        recent_members=[],
        member_genders={}
    )

    result = classify(state)
    records = result.get("records", [])

    # 应该至少有 3 条记录：年龄、职业、关系
    passed = len(records) >= 3
    print_test_result(f"应返回 >= 3 条记录，实际: {len(records)}", passed)

    # 检查是否包含 relationship 类型
    has_relationship = any(r.get("attribute_type") == "relationship" for r in records)
    print_test_result("应包含 relationship 记录", has_relationship)

    return passed and has_relationship


def test_negation_ability_not_hobby():
    """测试：否定描述应存为 ability 而非 hobby"""
    print_test_header("否定描述存为 ability")

    state = MockState(
        user_input="汪强不太会做饭",
        recent_members=["汪强"],
        member_genders={"汪强": "男"}
    )

    result = classify(state)
    records = result.get("records", [])

    # 查找汪强的记录
    wang_record = next((r for r in records if r.get("member_name") == "汪强"), None)

    passed = wang_record is not None and wang_record.get("attribute_type") == "ability"
    print_test_result("'不太会做饭' 应存为 ability", passed,
                      f"实际 attribute_type: {wang_record.get('attribute_type') if wang_record else 'N/A'}")
    return passed


def test_positive_hobby():
    """测试：肯定描述应存为 hobby"""
    print_test_header("肯定爱好存为 hobby")

    state = MockState(
        user_input="糖糖爱做饭",
        recent_members=["糖糖"],
        member_genders={"糖糖": "女"}
    )

    result = classify(state)
    records = result.get("records", [])

    tang_record = next((r for r in records if r.get("member_name") == "糖糖"), None)

    passed = tang_record is not None and tang_record.get("attribute_type") == "hobby"
    print_test_result("'爱做饭' 应存为 hobby", passed,
                      f"实际 attribute_type: {tang_record.get('attribute_type') if tang_record else 'N/A'}")
    return passed


def test_gender_inference_husband():
    """测试：从'老公是X'推理性别"""
    print_test_header("'老公是X'推理性别")

    state = MockState(
        user_input="糖糖的老公是汪强",
        recent_members=[],
        member_genders={}
    )

    result = classify(state)
    member_genders = result.get("member_genders", {})

    # 糖糖是女性，汪强是男性
    passed = member_genders.get("糖糖") == "女" and member_genders.get("汪强") == "男"
    print_test_result("老公是X → 女(主)，男(X)", passed,
                      f"实际: {member_genders}")
    return passed


def test_gender_inference_wife():
    """测试：从'妻子是X'推理性别"""
    print_test_header("'妻子是X'推理性别")

    state = MockState(
        user_input="汪强的妻子是糖糖",
        recent_members=[],
        member_genders={}
    )

    result = classify(state)
    member_genders = result.get("member_genders", {})

    # 汪强是男性，糖糖是女性
    passed = member_genders.get("汪强") == "男" and member_genders.get("糖糖") == "女"
    print_test_result("妻子是X → 男(主)，女(X)", passed,
                      f"实际: {member_genders}")
    return passed


def test_count_family():
    """测试：'几口人'应返回 count_family action"""
    print_test_header("'几口人'返回 count_family")

    state = MockState(
        user_input="我们家几口人？",
        recent_members=[],
        member_genders={}
    )

    result = classify(state)

    passed = result["action"] == "count_family"
    print_test_result("'几口人'应触发 count_family", passed,
                      f"实际 action: {result.get('action')}")
    return passed


def test_aggregate_search_who():
    """测试：'谁XXX'应返回 aggregate_search action"""
    print_test_header("'谁XXX'返回 aggregate_search")

    state = MockState(
        user_input="我们家谁爱做饭？",
        recent_members=[],
        member_genders={}
    )

    result = classify(state)

    passed = result["action"] == "aggregate_search"
    print_test_result("'谁爱做饭'应触发 aggregate_search", passed,
                      f"实际 action: {result.get('action')}")
    return passed


def test_search_action():
    """测试：普通查询应返回 search action"""
    print_test_header("普通查询返回 search")

    state = MockState(
        user_input="糖糖的生日是哪天？",
        recent_members=["糖糖"],
        member_genders={"糖糖": "女"}
    )

    result = classify(state)

    passed = result["action"] == "search"
    print_test_result("查询生日应触发 search", passed,
                      f"实际 action: {result.get('action')}")
    return passed


def test_add_action():
    """测试：添加信息应返回 add action"""
    print_test_header("添加信息返回 add")

    state = MockState(
        user_input="汪佳齐上二年级，喜欢画画",
        recent_members=[],
        member_genders={}
    )

    result = classify(state)

    passed = result["action"] == "add"
    print_test_result("添加信息应触发 add", passed,
                      f"实际 action: {result.get('action')}")
    return passed


def test_non_family_relationship_no_new_member():
    """测试：非家庭关系词不应创建新成员"""
    print_test_header("非家庭关系不创建新成员")

    state = MockState(
        user_input="糖糖的好朋友是张丽",
        recent_members=["糖糖"],
        member_genders={"糖糖": "女"}
    )

    result = classify(state)
    records = result.get("records", [])

    # 张丽应该是空的 related_member_name
    tang_record = next((r for r in records if r.get("member_name") == "糖糖"), None)

    passed = tang_record is not None and tang_record.get("related_member_name") == ""
    print_test_result("好朋友是张丽 → related_member_name 应为空", passed,
                      f"实际 related_member_name: {tang_record.get('related_member_name') if tang_record else 'N/A'}")
    return passed


def test_family_relationship_create_member():
    """测试：家庭关系词应创建新成员"""
    print_test_header("家庭关系创建新成员")

    state = MockState(
        user_input="她老公是汪强",
        recent_members=["糖糖"],
        member_genders={"糖糖": "女"}
    )

    result = classify(state)
    records = result.get("records", [])

    # 应该有 related_member_name = "汪强"
    tang_record = next((r for r in records if r.get("member_name") == "糖糖"), None)

    passed = tang_record is not None and tang_record.get("related_member_name") == "汪强"
    print_test_result("老公是汪强 → related_member_name 应为'汪强'", passed,
                      f"实际: {tang_record.get('related_member_name') if tang_record else 'N/A'}")
    return passed


# =============================================
# Token 优化相关测试
# =============================================

def test_relevant_examples_loaded_for_count_family():
    """测试：'几口人'应加载统计类示例"""
    print_test_header("'几口人'加载统计类示例")

    from graph import _get_relevant_examples

    examples = _get_relevant_examples("我们家几口人？", max_examples=5)

    passed = len(examples) >= 1
    print_test_result("应加载至少1个相关示例", passed,
                      f"实际: {len(examples)}")
    if examples:
        print(f"  示例: {[e['input'] for e in examples]}")
    return passed


def test_relevant_examples_loaded_for_relationship():
    """测试：'女儿'相关输入应加载关系类示例"""
    print_test_header("'女儿'加载关系类示例")

    from graph import _get_relevant_examples

    examples = _get_relevant_examples("我女儿叫汪佳齐", max_examples=5)

    passed = len(examples) >= 1
    print_test_result("应加载至少1个相关示例", passed,
                      f"实际: {len(examples)}")
    if examples:
        print(f"  示例: {[e['input'] for e in examples]}")
    return passed


def test_relevant_examples_loaded_for_ability():
    """测试：'不太会'相关输入应加载能力类示例"""
    print_test_header("'不太会'加载能力类示例")

    from graph import _get_relevant_examples

    examples = _get_relevant_examples("汪强不太会做饭", max_examples=5)

    passed = len(examples) >= 1
    print_test_result("应加载至少1个相关示例", passed,
                      f"实际: {len(examples)}")
    if examples:
        print(f"  示例: {[e['input'] for e in examples]}")
    return passed


def test_token_optimization_classify():
    """测试：Token 优化后的 classify 仍能正确处理 count_family"""
    print_test_header("Token 优化后 classify 正确处理 count_family")

    state = MockState(
        user_input="请问我们家几口人？",
        recent_members=[],
        member_genders={}
    )

    result = classify(state)

    passed = result["action"] == "count_family"
    print_test_result("'请问我们家几口人？' 应触发 count_family", passed,
                      f"实际 action: {result.get('action')}")
    return passed


def test_token_optimization_aggregate_search():
    """测试：Token 优化后的 classify 仍能正确处理 aggregate_search"""
    print_test_header("Token 优化后 classify 正确处理 aggregate_search")

    state = MockState(
        user_input="我们家谁最爱做饭？",
        recent_members=[],
        member_genders={}
    )

    result = classify(state)

    passed = result["action"] == "aggregate_search"
    print_test_result("'我们家谁最爱做饭？' 应触发 aggregate_search", passed,
                      f"实际 action: {result.get('action')}")
    return passed


# =============================================
# 测试运行器
# =============================================

def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("家庭信息记录 Agent - 测试用例集")
    print("="*60)

    tests = [
        test_pronoun_resolution_female,
        test_pronoun_resolution_male,
        test_pronoun_confirm_when_gender_unknown,
        test_multiple_records_single_input,
        test_negation_ability_not_hobby,
        test_positive_hobby,
        test_gender_inference_husband,
        test_gender_inference_wife,
        test_count_family,
        test_aggregate_search_who,
        test_search_action,
        test_add_action,
        test_non_family_relationship_no_new_member,
        test_family_relationship_create_member,
        # Token 优化相关测试
        test_relevant_examples_loaded_for_count_family,
        test_relevant_examples_loaded_for_relationship,
        test_relevant_examples_loaded_for_ability,
        test_token_optimization_classify,
        test_token_optimization_aggregate_search,
    ]

    results = []
    for test in tests:
        try:
            passed = test()
            results.append(passed)
        except Exception as e:
            print(f"❌ {test.__name__} - 异常: {e}")
            results.append(False)

    # 汇总
    print("\n" + "="*60)
    print("测试汇总")
    print("="*60)
    passed_count = sum(results)
    total_count = len(results)
    print(f"通过: {passed_count}/{total_count}")

    if passed_count == total_count:
        print("🎉 所有测试通过！")
    else:
        print(f"⚠️  有 {total_count - passed_count} 个测试失败")

    return passed_count == total_count


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
