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
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "sk-cp-FZ0T3PMD3ClgnoFrk-jd5b9IpD5MTr9oE6pssiQMrvVAIJ73NMIidHQx1yjHkc4EnRRtBAV7FUEGRMw12zzkwv_raUDELJoga_yf7BDRD6902MtGXlQst-8")

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