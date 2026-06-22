"""
=============================================
家庭成员服务层
=============================================

处理家庭成员信息的添加、更新、查询等业务逻辑
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Optional
from tools import chroma_manager


class FamilyMemberService:
    """
    家庭成员服务

    提供智能合并的添加逻辑：
    - 如果成员已存在，则更新现有记录
    - 如果成员不存在，则添加新记录
    """

    def __init__(self):
        self.chroma = chroma_manager

    def add_or_update_member(self, member_name: str, attribute_type: str, content: str) -> dict:
        """
        添加或更新成员信息

        Args:
            member_name: 成员姓名
            attribute_type: 属性类型
            content: 属性内容

        Returns:
            dict: {
                "action": "added" | "updated",
                "message": str
            }
        """
        all_members = self.chroma.get_all_members()

        if member_name in all_members:
            # 成员已存在，执行更新
            self.chroma.update_member_info(
                member_name=member_name,
                attribute_type=attribute_type,
                old_content=content,
                new_content=content
            )
            return {
                "action": "updated",
                "message": f"已更新 {member_name} 的信息"
            }
        else:
            # 成员不存在，执行添加
            self.chroma.add_member_info(
                member_name=member_name,
                attribute_type=attribute_type,
                content=content
            )
            return {
                "action": "added",
                "message": f"已添加 {member_name} 的信息"
            }

    def add_or_update_from_text(self, text_content: str) -> dict:
        """
        从文本内容添加或更新成员信息

        解析文本中的成员信息，然后逐条添加/更新

        Args:
            text_content: 自然语言文本，如 "林月是中学老师"

        Returns:
            dict: {
                "added_count": int,
                "updated_count": int,
                "details": list,
                "message": str
            }
        """
        # TODO: 使用 LLM 解析文本，提取成员和属性信息
        # 目前简化处理，直接添加

        # 这里需要调用 graph 的 classify 来解析文本
        # 但为了避免循环依赖，我们在 API 层处理

        pass

    def get_member_info(self, member_name: str) -> dict:
        """
        获取成员详细信息

        Args:
            member_name: 成员姓名

        Returns:
            dict: 成员信息
        """
        all_members = self.chroma.get_all_members()

        if member_name not in all_members:
            return None

        info = self.chroma.get_all_member_info(member_name)

        return {
            "name": member_name,
            "info": info,
            "total": len(info)
        }

    def list_all_members(self) -> dict:
        """
        列出所有成员

        Returns:
            dict: {
                "members": list,
                "total": int
            }
        """
        members = self.chroma.get_all_members()

        return {
            "members": members,
            "total": len(members)
        }

    def delete_member(self, member_name: str) -> dict:
        """
        删除成员

        Args:
            member_name: 成员姓名

        Returns:
            dict: {
                "success": bool,
                "message": str
            }
        """
        all_members = self.chroma.get_all_members()

        if member_name not in all_members:
            return {
                "success": False,
                "message": f"未找到成员: {member_name}"
            }

        deleted_count = self.chroma.delete_member_info(member_name)

        return {
            "success": True,
            "message": f"已删除 {member_name}，共删除 {deleted_count} 条记录"
        }


# 全局单例
family_service = FamilyMemberService()
