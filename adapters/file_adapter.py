"""
=============================================
文件输入适配器
=============================================

支持 JSON、CSV、TXT 文件的解析
"""

import json
import csv
import io
from typing import Optional

import config
from .base import InputAdapter, InputType


class FileInputAdapter(InputAdapter):
    """
    文件输入适配器

    支持解析：
    - JSON: 数组格式或 {"members": [...]} 嵌套格式
    - CSV: 带表头的表格数据
    - TXT: 自由文本，直接传给 classify 处理
    """

    def __init__(self):
        self.max_file_size = config.MAX_FILE_SIZE  # 10MB
        self.allowed_types = config.ALLOWED_FILE_TYPES  # .json, .csv, .txt

    @property
    def input_type(self) -> InputType:
        return InputType.FILE

    def validate_content(self, content: str) -> bool:
        """验证文件内容"""
        # 检查文件大小
        if len(content.encode('utf-8')) > self.max_file_size:
            raise ValueError(f"文件过大，最大支持 {self.max_file_size // (1024*1024)}MB")

        return True

    def process(self, content: str, filename: Optional[str] = None) -> str:
        """
        处理文件内容

        Args:
            content: 文件内容（字符串）
            filename: 文件名（用于检测文件类型）

        Returns:
            解析后的文本描述
        """
        self.validate_content(content)

        # 根据文件扩展名判断类型
        file_type = self._detect_file_type(content, filename)

        if file_type == "json":
            return self._parse_json(content)
        elif file_type == "csv":
            return self._parse_csv(content)
        elif file_type == "txt":
            return self._parse_txt(content)
        else:
            raise ValueError(f"不支持的文件类型: {file_type}")

    def _detect_file_type(self, content: str, filename: Optional[str] = None) -> str:
        """检测文件类型"""
        # 优先根据文件名判断
        if filename:
            ext = filename.lower().split('.')[-1]
            if ext in ['json', 'csv', 'txt']:
                return ext

        # 尝试根据内容判断
        content_stripped = content.strip()

        # JSON 通常以 { 或 [ 开头
        if content_stripped.startswith('{') or content_stripped.startswith('['):
            return "json"

        # CSV 通常有逗号分隔
        if ',' in content_stripped.split('\n')[0] if '\n' in content_stripped else content_stripped:
            return "csv"

        # 默认当作 TXT
        return "txt"

    def _detect_encoding(self, content: bytes) -> str:
        """检测文件编码"""
        # 尝试 UTF-8
        try:
            content.decode('utf-8')
            return 'utf-8'
        except UnicodeDecodeError:
            pass

        # 尝试 GBK
        try:
            content.decode('gbk')
            return 'gbk'
        except UnicodeDecodeError:
            pass

        # 尝试 GB2312
        try:
            content.decode('gb2312')
            return 'gb2312'
        except UnicodeDecodeError:
            pass

        # 默认 UTF-8
        return 'utf-8'

    def _parse_json(self, content: str) -> str:
        """解析 JSON 文件"""
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 解析失败: {e}")

        # 转换为文本描述
        result_parts = []

        # 处理数组格式
        if isinstance(data, list):
            members = data
        # 处理嵌套格式 {"members": [...]}
        elif isinstance(data, dict) and "members" in data:
            members = data["members"]
        else:
            members = [data]

        for member in members:
            if not isinstance(member, dict):
                continue

            name = member.get("name", "")
            if not name:
                continue

            # 收集所有属性
            attrs = []
            for key, value in member.items():
                if key == "name":
                    continue
                if value:
                    attrs.append(f"{key}是{value}")

            if attrs:
                result_parts.append(f"{name}的{'，'.join(attrs)}")
            else:
                result_parts.append(f"{name}")

        return "；".join(result_parts) if result_parts else content

    def _parse_csv(self, content: str) -> str:
        """解析 CSV 文件"""
        result_parts = []

        # 尝试不同编码
        lines = content.split('\n')

        # 解析 CSV
        reader = csv.DictReader(io.StringIO(content))
        headers = reader.fieldnames or []

        for row in reader:
            name = row.get('name', row.get('姓名', ''))
            if not name:
                continue

            attrs = []
            for header in headers:
                if header.lower() in ['name', '姓名']:
                    continue
                value = row.get(header, '').strip()
                if value:
                    attrs.append(f"{header}是{value}")

            if attrs:
                result_parts.append(f"{name}的{'，'.join(attrs)}")
            else:
                result_parts.append(f"{name}")

        return "；".join(result_parts) if result_parts else content

    def _parse_txt(self, content: str) -> str:
        """解析 TXT 文件，直接返回内容"""
        return content.strip()

    def detect_input_mode(self, content: str, filename: Optional[str] = None) -> str:
        """
        检测输入模式（兼容旧接口）

        Returns:
            "json", "csv", 或 "txt"
        """
        return self._detect_file_type(content, filename)
