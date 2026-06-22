"""
=============================================
输入适配器基类
=============================================
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any


class InputType(str, Enum):
    """输入类型枚举"""
    TEXT = "text"
    FILE = "file"
    IMAGE = "image"
    VOICE = "voice"


class InputAdapter(ABC):
    """
    输入适配器抽象基类

    所有输入适配器必须实现 process 方法，
    将各自的输入类型转换为文本，交给 graph 处理。
    """

    @property
    @abstractmethod
    def input_type(self) -> InputType:
        """返回适配器处理的输入类型"""
        pass

    @abstractmethod
    def process(self, content: Any) -> str:
        """
        处理输入内容，返回文本描述

        Args:
            content: 输入内容（类型取决于具体适配器）

        Returns:
            str: 处理后的文本描述，可直接传给 graph
        """
        pass

    def validate_content(self, content: Any) -> bool:
        """
        验证输入内容是否合法

        Args:
            content: 输入内容

        Returns:
            bool: 是否合法
        """
        return True
