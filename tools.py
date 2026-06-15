"""
=============================================
工具模块 -定义家庭信息记录 Agent 的工具函数
=============================================
"""

from typing import Optional

from chroma_manager import ChromaManager


# =============================================
# 初始化全局组件
# =============================================

# 初始化 ChromaDB 管理器（全局单例）
chroma_manager = ChromaManager()


# =============================================
# 工具类（兼容 graph.py 的调用方式）
# =============================================

class AddFamilyInfoTool:
    """添加家庭成员信息工具"""
    name: str = "添加家庭成员信息"

    def _run(self, member_name: str, attribute_type: str, content: str, extra_info: Optional[str] = None) -> str:
        metadata = {}
        if extra_info:
            metadata["extra_info"] = extra_info

        record_id = chroma_manager.add_member_info(
            member_name=member_name,
            attribute_type=attribute_type,
            content=content,
            metadata=metadata
        )
        return f"已成功将「{member_name}」的「{attribute_type}」信息添加到知识库，ID: {record_id}"


class UpdateFamilyInfoTool:
    """更新家庭成员信息工具"""
    name: str = "更新家庭成员信息"

    def _run(self, member_name: str, attribute_type: str, old_content: str, new_content: str) -> str:
        success = chroma_manager.update_member_info(
            member_name=member_name,
            attribute_type=attribute_type,
            old_content=old_content,
            new_content=new_content
        )
        if success:
            return f"已成功更新「{member_name}」的「{attribute_type}」信息"
        else:
            return f"更新失败：未找到「{member_name}」的「{old_content}」记录"


class SearchFamilyInfoTool:
    """检索家庭成员信息工具"""
    name: str = "检索家庭成员信息"

    def _run(self, query_text: str, member_name: Optional[str] = None, top_k: int = 10) -> str:
        results = chroma_manager.search_by_text(
            query_text=query_text,
            member_name=member_name,
            top_k=top_k
        )
        if not results:
            return "未找到相关记录"

        formatted = []
        for i, r in enumerate(results, 1):
            formatted.append(
                f"【{i}】{r['member_name']} - {r['attribute_type']}\n"
                f"    内容：{r['content']}\n"
                f"    时间：{r['timestamp']}"
            )
        return "\n".join(formatted)


class GetMemberAllInfoTool:
    """获取成员全部信息工具"""
    name: str = "获取成员全部信息"

    def _run(self, member_name: str) -> str:
        results = chroma_manager.get_all_member_info(member_name)
        if not results:
            return f"知识库中没有「{member_name}」的记录"

        by_type = {}
        for r in results:
            attr_type = r["attribute_type"]
            if attr_type not in by_type:
                by_type[attr_type] = []
            by_type[attr_type].append(r["content"])

        formatted = [f"【{member_name}】的信息汇总："]
        for attr_type, contents in by_type.items():
            formatted.append(f"\n  [{attr_type}]:")
            for c in contents:
                formatted.append(f"    - {c}")
        return "\n".join(formatted)


class DeleteFamilyInfoTool:
    """删除家庭成员信息工具"""
    name: str = "删除家庭成员信息"

    def _run(self, member_name: str, attribute_type: Optional[str] = None) -> str:
        count = chroma_manager.delete_member_info(member_name, attribute_type)
        if count > 0:
            attr_desc = attribute_type if attribute_type else "全部属性"
            return f"已删除「{member_name}」的 {count} 条「{attr_desc}」记录"
        else:
            return f"删除失败：未找到「{member_name}」的相关记录"


class GetAllMembersTool:
    """获取所有成员姓名工具"""
    name: str = "获取所有成员姓名"

    def _run(self) -> str:
        members = chroma_manager.get_all_members()
        if not members:
            return "知识库中还没有任何家庭成员的信息"
        return "、".join(members)


# =============================================
# 创建工具实例
# =============================================

add_family_info = AddFamilyInfoTool()
update_family_info = UpdateFamilyInfoTool()
search_family_info = SearchFamilyInfoTool()
get_member_all_info = GetMemberAllInfoTool()
delete_family_info = DeleteFamilyInfoTool()
get_all_members = GetAllMembersTool()