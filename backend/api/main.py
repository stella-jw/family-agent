"""
=============================================
FastAPI 应用入口
=============================================

提供 REST API 供前端应用调用 family-agent 功能
"""

import sys
import os

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import config
from graph import graph
from tools import chroma_manager
from adapters import FileInputAdapter, ImageInputAdapter, VoiceInputAdapter, InputType


# =============================================
# 响应模型
# =============================================

class AddRequest(BaseModel):
    """添加信息请求"""
    input_type: str  # text / file / image / voice
    content: str  # 文本内容或 base64 编码的文件内容


class AddResponse(BaseModel):
    """添加信息响应"""
    success: bool
    message: str
    added_count: int = 0
    updated_count: int = 0
    details: list = []


class SearchRequest(BaseModel):
    """搜索请求"""
    query: str
    member_name: Optional[str] = None


class MemberInfo(BaseModel):
    """成员信息"""
    name: str
    count: int


class MembersResponse(BaseModel):
    """成员列表响应"""
    members: list[str]
    total: int


class ProfileResponse(BaseModel):
    """成员档案响应"""
    name: str
    info: list


class DeleteResponse(BaseModel):
    """删除响应"""
    success: bool
    message: str


class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str
    version: str


# =============================================
# 适配器实例
# =============================================

file_adapter = FileInputAdapter()
image_adapter = ImageInputAdapter()
voice_adapter = VoiceInputAdapter()


# =============================================
# Lifespan
# =============================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    print("[API] REST API 服务启动")
    yield
    print("[API] REST API 服务关闭")


# =============================================
# FastAPI 应用
# =============================================

app = FastAPI(
    title="Family Agent API",
    description="家庭信息记录 Agent 的 REST API 接口",
    version="0.1.0",
    lifespan=lifespan
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================
# API 端点
# =============================================

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """健康检查端点"""
    return HealthResponse(status="ok", version="0.1.0")


@app.post("/api/add", response_model=AddResponse)
async def add_member_info(request: AddRequest):
    """
    添加家庭成员信息

    支持文本、文件、图片、语音多种输入方式。
    如果成员已存在，则更新现有记录。
    """
    try:
        content = request.content
        input_type = request.input_type

        # 根据输入类型转换内容
        if input_type == InputType.TEXT.value:
            text_content = content
        elif input_type == InputType.FILE.value:
            text_content = file_adapter.process(content)
        elif input_type == InputType.IMAGE.value:
            text_content = await image_adapter.process(content)
        elif input_type == InputType.VOICE.value:
            text_content = voice_adapter.process(content)
        else:
            raise HTTPException(status_code=400, detail=f"不支持的输入类型: {input_type}")

        # 调用 graph 处理
        result = graph.invoke({
            "user_input": text_content,
            "recent_members": [],
            "member_genders": {},
        })

        # 解析结果
        response_text = result.get("response", "")
        action = result.get("action", "")

        # 统计添加和更新的数量（从 classify 结果推断）
        records = result.get("records", [])
        added_count = 0
        updated_count = 0
        details = []

        for record in records:
            member_name = record.get("member_name", "")
            record_action = record.get("action", action)

            if member_name:
                all_members = chroma_manager.get_all_members()
                if member_name in all_members:
                    updated_count += 1
                    details.append({"name": member_name, "action": "updated"})
                else:
                    added_count += 1
                    details.append({"name": member_name, "action": "added"})

        # 如果没有记录，根据 action 判断
        if not details:
            if action in ["add", "update", "search"]:
                details.append({"name": "", "action": action})

        return AddResponse(
            success=True,
            message=response_text or "信息处理完成",
            added_count=added_count,
            updated_count=updated_count,
            details=details
        )

    except Exception as e:
        print(f"[API] /api/add 错误: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/search")
async def search_member_info(request: SearchRequest):
    """搜索家庭成员信息"""
    try:
        result = chroma_manager.search_by_text(
            query_text=request.query,
            member_name=request.member_name
        )

        return {
            "success": True,
            "results": result,
            "count": len(result)
        }

    except Exception as e:
        print(f"[API] /api/search 错误: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/profile/{name}")
async def get_member_profile(name: str):
    """获取成员完整档案"""
    try:
        all_members = chroma_manager.get_all_members()
        if name not in all_members:
            raise HTTPException(status_code=404, detail=f"未找到成员: {name}")

        info = chroma_manager.get_all_member_info(name)

        return ProfileResponse(
            name=name,
            info=info
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"[API] /api/profile 错误: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/members", response_model=MembersResponse)
async def list_members():
    """列出所有成员"""
    try:
        members = chroma_manager.get_all_members()

        return MembersResponse(
            members=members,
            total=len(members)
        )

    except Exception as e:
        print(f"[API] /api/members 错误: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/member/{name}", response_model=DeleteResponse)
async def delete_member(name: str):
    """删除成员"""
    try:
        all_members = chroma_manager.get_all_members()
        if name not in all_members:
            raise HTTPException(status_code=404, detail=f"未找到成员: {name}")

        deleted_count = chroma_manager.delete_member_info(name)

        return DeleteResponse(
            success=True,
            message=f"已删除 {name}，共删除 {deleted_count} 条记录"
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"[API] /api/member/{name} 错误: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =============================================
# 启动命令
# =============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.api.main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True
    )
