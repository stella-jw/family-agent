"""
查询 ChromaDB 中的数据
直接运行: python query_db.py
"""

from chroma_manager import ChromaManager


def main():
    cm = ChromaManager()

    # 1. 查看所有家庭成员
    print("=" * 60)
    print("1. 所有家庭成员")
    print("=" * 60)
    members = cm.get_all_members()
    print(f"共 {len(members)} 人: {members}")
    print()

    # 2. 查看所有记录
    print("=" * 60)
    print("2. 所有记录详情")
    print("=" * 60)
    results = cm.collection.get()
    print(f"共 {len(results['documents'])} 条记录")
    for i, doc in enumerate(results['documents']):
        meta = results['metadatas'][i]
        print(f"\n  【记录 {i+1}】")
        print(f"  成员: {meta['member_name']}")
        print(f"  类型: {meta['attribute_type']}")
        print(f" 内容: {doc}")
        print(f"  时间: {meta['timestamp']}")
    print()

    # 3. 语义检索测试
    print("=" * 60)
    print("3. 语义检索测试")
    print("=" * 60)
    test_queries = ["糖糖"]
    for q in test_queries:
        print(f"\n  查询「{q}」:")
        results = cm.search_by_text(q, top_k=5)
        if not results:
            print("    (无结果)")
        for r in results:
            print(f"    → {r['member_name']}: {r['content']}")
    print()


if __name__ == "__main__":
    main()