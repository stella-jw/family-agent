"""
=============================================
REST API 文件上传测试

启动 API 服务器后运行此脚本测试文件上传功能

启动命令：
    python backend/api/main.py

测试命令：
    python test_api_file_upload.py
=============================================
"""

import requests
import json

API_BASE = "http://localhost:8000"


def test_health():
    """测试健康检查"""
    resp = requests.get(f"{API_BASE}/api/health")
    print(f"GET /api/health -> {resp.status_code}")
    print(f"  {resp.json()}")
    return resp.status_code == 200


def test_text_add():
    """测试文本添加"""
    resp = requests.post(f"{API_BASE}/api/add", json={
        "input_type": "text",
        "content": "糖糖今年38岁，职业是软件测试工程师"
    })
    print(f"\nPOST /api/add (text) -> {resp.status_code}")
    print(f"  {json.dumps(resp.json(), ensure_ascii=False, indent=2)}")
    return resp.status_code == 200


def test_json_upload():
    """测试 JSON 文件上传"""
    json_content = json.dumps([
        {"name": "汪强", "age": "40", "job": "工程师"},
        {"name": "汪佳齐", "age": "8", "grade": "二年级"}
    ], ensure_ascii=False)

    resp = requests.post(f"{API_BASE}/api/add", json={
        "input_type": "file",
        "content": json_content
    })
    print(f"\nPOST /api/add (JSON) -> {resp.status_code}")
    print(f"  {json.dumps(resp.json(), ensure_ascii=False, indent=2)}")
    return resp.status_code == 200


def test_csv_upload():
    """测试 CSV 文件上传"""
    csv_content = """name,age,job
汪强,40,工程师
糖糖,38,软件测试工程师"""

    resp = requests.post(f"{API_BASE}/api/add", json={
        "input_type": "file",
        "content": csv_content
    })
    print(f"\nPOST /api/add (CSV) -> {resp.status_code}")
    print(f"  {json.dumps(resp.json(), ensure_ascii=False, indent=2)}")
    return resp.status_code == 200


def test_txt_upload():
    """测试 TXT 文件上传"""
    txt_content = """糖糖今年38岁，职业是软件测试工程师。
她老公是汪强，是一名工程师。
他们有个女儿叫汪佳齐，今年8岁，上二年级。
汪佳齐喜欢画画和跳舞。"""

    resp = requests.post(f"{API_BASE}/api/add", json={
        "input_type": "file",
        "content": txt_content
    })
    print(f"\nPOST /api/add (TXT) -> {resp.status_code}")
    print(f"  {json.dumps(resp.json(), ensure_ascii=False, indent=2)}")
    return resp.status_code == 200


def test_members_list():
    """测试成员列表"""
    resp = requests.get(f"{API_BASE}/api/members")
    print(f"\nGET /api/members -> {resp.status_code}")
    print(f"  {json.dumps(resp.json(), ensure_ascii=False, indent=2)}")
    return resp.status_code == 200


def test_search():
    """测试搜索"""
    resp = requests.post(f"{API_BASE}/api/search", json={
        "query": "糖糖",
        "member_name": None
    })
    print(f"\nPOST /api/search -> {resp.status_code}")
    print(f"  {json.dumps(resp.json(), ensure_ascii=False, indent=2)}")
    return resp.status_code == 200


def test_profile():
    """测试档案查询"""
    resp = requests.get(f"{API_BASE}/api/profile/糖糖")
    print(f"\nGET /api/profile/糖糖 -> {resp.status_code}")
    print(f"  {json.dumps(resp.json(), ensure_ascii=False, indent=2)}")
    return resp.status_code == 200


def run_all_tests():
    print("=" * 60)
    print("REST API 文件上传测试")
    print("=" * 60)

    # 先检查 API 是否可用
    if not test_health():
        print("\n❌ API 服务未启动，请先运行：")
        print("   python backend/api/main.py")
        return False

    # 测试各种文件类型上传
    print("\n" + "=" * 60)
    print("测试文件上传")
    print("=" * 60)

    test_json_upload()
    test_csv_upload()
    test_txt_upload()

    # 测试常规 API
    print("\n" + "=" * 60)
    print("测试常规 API")
    print("=" * 60)

    test_text_add()
    test_members_list()
    test_search()
    test_profile()

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    return True


if __name__ == "__main__":
    run_all_tests()
