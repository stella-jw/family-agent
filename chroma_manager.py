"""
=============================================
ChromaDB 管理模块 -负责知识库的增删改查
=============================================
"""

import os
import uuid
from datetime import datetime
from typing import Optional

import chromadb
import requests

import config


# =============================================
# MiniMax 嵌入函数
# =============================================

class MiniMaxEmbeddingFunction:
    """
    使用 MiniMax Embedding API 进行文本向量化
    MiniMax 的 Embedding API 与 OpenAI 不兼容，需要用 HTTP 直接调用
    """
    def __init__(self):
        self.api_key = config.MINIMAX_API_KEY
        self.model = config.MINIMAX_EMBEDDING_MODEL
        self.dimension = config.EMBEDDING_DIMENSION
        self.url = f"{config.MINIMAX_EMBEDDING_URL}/embeddings"

    def name(self) -> str:
        """返回嵌入函数名称"""
        return "minimax-embedding"

    def __call__(self, input) -> list:
        """批量嵌入"""
        return self.embed(input)

    def embed(self, texts: list) -> list:
        """将文本列表转换为向量列表"""
        response = requests.post(
            self.url,
            headers={
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': self.model,
                'texts': texts,
                'type': 'query'
            }
        )

        result = response.json()

        if 'vectors' in result and result['vectors']:
            return result['vectors']

        raise ValueError(f"Embedding API 返回错误: {result}")

    def embed_query(self, input) -> list:
        """将单个查询文本转换为向量"""
        if isinstance(input, list):
            texts = input
        else:
            texts = [input]
        vectors = self.embed(texts)
        return vectors if vectors else []


# =============================================
# 属性类型常量定义
# =============================================

class AttributeType:
    """属性类型枚举"""
    BASIC_INFO = "basic_info"
    HOBBY = "hobby"
    WORK_EXPERIENCE = "work_experience"
    LIFE_EVENT = "life_event"
    PERSONALITY = "personality"
    RELATIONSHIP = "relationship"


# =============================================
# ChromaDB 管理类
# =============================================

class ChromaManager:
    """
    ChromaDB 管理类

    负责与 ChromaDB 向量数据库的交互，
    实现家庭成员信息的存储、更新、删除和检索功能。
    """

    def __init__(self):
        """
        初始化 ChromaDB 客户端和 Collection
        """
        # 确保数据目录存在
        os.makedirs(config.CHROMA_DB_PATH, exist_ok=True)

        # 初始化 MiniMax 嵌入函数
        print("[ChromaManager] 初始化 MiniMax Embedding API...")
        self.embedding_function = MiniMaxEmbeddingFunction()
        print(f"[ChromaManager] 使用模型: {self.embedding_function.model}")

        # 初始化 ChromaDB 客户端（持久化存储）
        self.client = chromadb.PersistentClient(
            path=config.CHROMA_DB_PATH
        )

        # 获取或创建 Collection（使用 MiniMax 嵌入函数）
        self.collection = self.client.get_or_create_collection(
            name=config.CHROMA_COLLECTION_NAME,
            embedding_function=self.embedding_function,
            metadata={"description": "家庭成员信息知识库"}
        )

        print(f"[ChromaManager] 已连接到 ChromaDB，Collection: {config.CHROMA_COLLECTION_NAME}")

    def add_member_info(
        self,
        member_name: str,
        attribute_type: str,
        content: str,
        metadata: Optional[dict] = None
    ) -> str:
        """
        添加家庭成员信息到知识库
        """
        record_id = str(uuid.uuid4())

        meta = {
            "member_name": member_name,
            "attribute_type": attribute_type,
            "content": content,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        if metadata:
            meta.update(metadata)

        self.collection.add(
            ids=[record_id],
            documents=[content],
            metadatas=[meta]
        )

        print(f"[ChromaManager] 新增记录: {member_name} - {attribute_type}")
        return record_id

    def update_member_info(
        self,
        member_name: str,
        attribute_type: str,
        old_content: str,
        new_content: str
    ) -> bool:
        """
        更新家庭成员信息
        改进：先查 member_name 的所有记录，再用 attribute_type 过滤
        """
        # ChromaDB 1.5+ where clause 必须使用操作符语法
        def make_eq_clause(field, value):
            return {field: {"$eq": value}}

        # 先尝试精确匹配 content
        where_clause = {
            "$and": [
                make_eq_clause("member_name", member_name),
                make_eq_clause("attribute_type", attribute_type),
                make_eq_clause("content", old_content)
            ]
        }
        results = self.collection.get(where=where_clause)

        # 如果精确匹配没找到，尝试只按 member_name + attribute_type
        if not results["ids"]:
            where_clause = {
                "$and": [
                    make_eq_clause("member_name", member_name),
                    make_eq_clause("attribute_type", attribute_type)
                ]
            }
            results = self.collection.get(where=where_clause)

        # 如果还没找到，只按 member_name
        if not results["ids"]:
            where_clause = make_eq_clause("member_name", member_name)
            results = self.collection.get(where=where_clause)
            # 过滤出相同 attribute_type 的记录
            if results["ids"]:
                filtered_ids = []
                for i, meta in enumerate(results["metadatas"]):
                    if meta["attribute_type"] == attribute_type:
                        filtered_ids.append(results["ids"][i])
                results["ids"] = filtered_ids

        if not results["ids"]:
            print(f"[ChromaManager] 未找到要更新的记录")
            return False

        # 删除旧记录，添加新内容
        self.collection.delete(ids=results["ids"])
        self.add_member_info(member_name, attribute_type, new_content)

        print(f"[ChromaManager] 更新记录: {member_name} - {attribute_type}")
        return True

    def delete_member_info(self, member_name: str, attribute_type: Optional[str] = None) -> int:
        """
        删除家庭成员信息
        """
        where_filter = {"member_name": member_name, "attribute_type": attribute_type} if attribute_type else {"member_name": member_name}

        results = self.collection.get(where=where_filter)

        if not results["ids"]:
            print(f"[ChromaManager] 未找到要删除的记录: {member_name}")
            return 0

        self.collection.delete(ids=results["ids"])
        print(f"[ChromaManager] 删除记录: {member_name}")
        return len(results["ids"])

    def search_by_text(
        self,
        query_text: str,
        member_name: Optional[str] = None,
        top_k: int = 10
    ) -> list:
        """
        根据文本在知识库中检索相关信息
        """
        where_filter = {"member_name": member_name} if member_name else None

        results = self.collection.query(
            query_texts=[query_text],
            n_results=top_k,
            where=where_filter
        )

        formatted_results = []
        if results["documents"] and len(results["documents"]) > 0:
            for i, doc in enumerate(results["documents"][0]):
                formatted_results.append({
                    "content": doc,
                    "member_name": results["metadatas"][0][i]["member_name"],
                    "attribute_type": results["metadatas"][0][i]["attribute_type"],
                    "timestamp": results["metadatas"][0][i]["timestamp"]
                })

        print(f"[ChromaManager] 检索到 {len(formatted_results)} 条相关记录")
        return formatted_results

    def get_all_member_info(self, member_name: str) -> list:
        """
        获取某个成员的所有信息
        """
        results = self.collection.get(
            where={"member_name": member_name}
        )

        all_info = []
        if results["documents"]:
            for i, doc in enumerate(results["documents"]):
                all_info.append({
                    "content": doc,
                    "attribute_type": results["metadatas"][i]["attribute_type"],
                    "timestamp": results["metadatas"][i]["timestamp"]
                })

        print(f"[ChromaManager] 获取成员 {member_name} 的 {len(all_info)} 条记录")
        return all_info

    def get_all_members(self) -> list:
        """
        获取所有家庭成员的姓名列表
        """
        results = self.collection.get()

        members = set()
        if results["metadatas"]:
            for meta in results["metadatas"]:
                members.add(meta["member_name"])

        return list(members)

    def get_member_count(self) -> int:
        """
        获取记录总数
        """
        results = self.collection.get()
        return len(results["documents"]) if results["documents"] else 0