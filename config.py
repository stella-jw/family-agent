"""
=============================================
配置模块 -集中管理所有配置项
=============================================
"""

import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()


# =============================================
# MiniMax API 配置
# =============================================

# MiniMax API Key（必需）
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "")

# MiniMax API 基础地址
MINIMAX_BASE_URL = os.getenv("MINIMAX_BASE_URL", "https://api.minimaxi.com/v1")

# 使用的模型名称
MINIMAX_MODEL_NAME = os.getenv("MINIMAX_MODEL_NAME", "minimax-text-01")


# =============================================
# 嵌入模型配置（MiniMax Embedding API）
# =============================================

# MiniMax Embedding API 模型名称
MINIMAX_EMBEDDING_MODEL = "embo-01"

# MiniMax Embedding API 地址（与文本API不同）
MINIMAX_EMBEDDING_URL = "https://api.minimax.chat/v1"

# 嵌入模型的向量维度（embo-01 为 1024维）
EMBEDDING_DIMENSION = 1024


# =============================================
# ChromaDB 配置
# =============================================

# ChromaDB 持久化存储路径
CHROMA_DB_PATH = "./data/chroma_db"

# Collection 名称
CHROMA_COLLECTION_NAME = "family_knowledge"


# =============================================
# REST API 服务器配置
# =============================================

# API 服务器地址
API_HOST = os.getenv("API_HOST", "0.0.0.0")

# API 服务器端口
API_PORT = int(os.getenv("API_PORT", "8000"))

# CORS 允许的 origins（逗号分隔）
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# API 密钥（可选，用于简单认证）
API_KEY = os.getenv("API_KEY", "")


# =============================================
# 视觉模型配置（用于图片识别）
# =============================================

# 视觉模型类型：minimax_vl / openai_vision
VISION_MODEL_TYPE = os.getenv("VISION_MODEL_TYPE", "minimax_vl")

# MiniMax 视觉模型名称
MINIMAX_VISION_MODEL = os.getenv("MINIMAX_VISION_MODEL", "Minimaxvision-v2")

# OpenAI 视觉模型名称（如使用）
OPENAI_VISION_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4o")

# 图片最大尺寸（像素，最长边）
IMAGE_MAX_SIZE = int(os.getenv("IMAGE_MAX_SIZE", "2048"))


# =============================================
# STT 语音识别配置
# =============================================

# STT 服务类型：minimax_stt / whisper
STT_SERVICE_TYPE = os.getenv("STT_SERVICE_TYPE", "minimax_stt")

# MiniMax T2A API（语音合成）的 URL
MINIMAX_STT_URL = os.getenv("MINIMAX_STT_URL", "https://api.minimaxi.com/v1")

# Whisper API URL（如使用）
WHISPER_API_URL = os.getenv("WHISPER_API_URL", "https://api.openai.com/v1/audio/transcriptions")

# 音频最大时长（秒）
AUDIO_MAX_DURATION = int(os.getenv("AUDIO_MAX_DURATION", "30"))


# =============================================
# 文件导入配置
# =============================================

# 允许的文件类型
ALLOWED_FILE_TYPES = [".json", ".csv", ".txt"]

# 文件最大大小（字节）
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", str(10 * 1024 * 1024)))  # 10MB


# =============================================
<<<<<<< HEAD
=======
# LangSmith 配置（用于调试追踪）
# =============================================

# 是否启用 LangSmith 追踪
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"

# LangSmith API Key（从 https://smith.langchain.com 获取）
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "")

# LangSmith Project 名称
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "family-agent")

# 启用 LangSmith 追踪
if LANGSMITH_TRACING and LANGSMITH_API_KEY:
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
    os.environ["LANGSMITH_PROJECT"] = LANGSMITH_PROJECT


# =============================================
>>>>>>> fbb280c (fix: remove hardcoded secrets from config.py)
# 验证配置
# =============================================

def validate_config():
    """
    验证必要的配置项是否已填写
    """
    errors = []

    if not MINIMAX_API_KEY:
        errors.append("错误：未设置 MINIMAX_API_KEY 环境变量，请参考 .env.example 文件配置")

    if not MINIMAX_API_KEY.startswith("sk"):
        errors.append("警告：MINIMAX_API_KEY 可能格式不正确，应该以 'sk' 开头")

    return errors