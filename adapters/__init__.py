"""
=============================================
输入适配器模块
=============================================

提供多模态输入的适配器：
- FileInputAdapter: 文件导入（JSON/CSV/TXT）
- ImageInputAdapter: 图片识别
- VoiceInputAdapter: 语音转文本
"""

from .base import InputAdapter, InputType
from .file_adapter import FileInputAdapter
from .image_adapter import ImageInputAdapter
from .voice_adapter import VoiceInputAdapter

__all__ = [
    "InputAdapter",
    "InputType",
    "FileInputAdapter",
    "ImageInputAdapter",
    "VoiceInputAdapter",
]
