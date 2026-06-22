"""
=============================================
图片识别适配器
=============================================

支持图片上传和视觉 LLM 识别
"""

import base64
import io
from typing import Optional

from PIL import Image
import httpx

import config
from .base import InputAdapter, InputType


class ImageInputAdapter(InputAdapter):
    """
    图片识别适配器

    使用视觉 LLM 分析图片，识别人物并描述属性
    """

    @property
    def input_type(self) -> InputType:
        return InputType.IMAGE

    def validate_content(self, content: str) -> bool:
        """验证图片内容"""
        # 尝试解码 base64
        try:
            image_data = base64.b64decode(content)
            image = Image.open(io.BytesIO(image_data))

            # 检查格式
            if image.format not in ['JPEG', 'PNG', 'WEBP']:
                raise ValueError(f"不支持的图片格式: {image.format}")

            return True
        except Exception as e:
            raise ValueError(f"图片格式错误: {e}")

    async def process(self, content: str) -> str:
        """
        处理图片内容

        Args:
            content: base64 编码的图片数据

        Returns:
            视觉 LLM 生成的人物描述
        """
        self.validate_content(content)

        # 解码图片
        image_data = base64.b64decode(content)
        image = Image.open(io.BytesIO(image_data))

        # 缩放图片
        image = self._resize_image(image)

        # 调用视觉 LLM
        description = await self._call_vision_llm(image)

        return description

    def _resize_image(self, image: Image.Image) -> Image.Image:
        """缩放图片到最大尺寸"""
        max_size = config.IMAGE_MAX_SIZE  # 2048px

        # 获取最长边
        width, height = image.size
        longest_edge = max(width, height)

        if longest_edge <= max_size:
            return image

        # 计算缩放比例
        ratio = max_size / longest_edge
        new_width = int(width * ratio)
        new_height = int(height * ratio)

        # 缩放
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    async def _call_vision_llm(self, image: Image.Image) -> str:
        """
        调用视觉 LLM 分析图片

        Returns:
            人物描述文本
        """
        model_type = config.VISION_MODEL_TYPE  # minimax_vl / openai_vision

        # 将图片转换为 base64
        buffered = io.BytesIO()
        image.save(buffered, format=image.format or "JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        if model_type == "minimax_vl":
            return await self._call_minimax_vision(img_base64)
        else:
            return await self._call_openai_vision(img_base64)

    async def _call_minimax_vision(self, image_base64: str) -> str:
        """调用 MiniMax 视觉模型"""
        url = f"{config.MINIMAX_BASE_URL}/vision"

        prompt = """请分析这张图片，识别出图片中的人物。

对于每个识别到的人物，请提供：
1. 性别（男/女/不确定）
2. 年龄估计（儿童/青少年/青年/中年/老年）
3. 外貌特征（发型、服装等）
4. 明显的家庭关系（如果有）

请用中文描述。如果图片中没有人物，请说明"未识别到人物"。

输出格式：
照片中有[N]个人物：
1. [描述1]
2. [描述2]
...
"""

        headers = {
            'Authorization': f'Bearer {config.MINIMAX_API_KEY}',
            'Content-Type': 'application/json'
        }

        payload = {
            "model": config.MINIMAX_VISION_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ]
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            result = response.json()

            if 'choices' in result:
                return result['choices'][0]['message']['content']
            else:
                raise ValueError(f"MiniMax Vision API 错误: {result}")

    async def _call_openai_vision(self, image_base64: str) -> str:
        """调用 OpenAI 视觉模型"""
        url = "https://api.openai.com/v1/chat/completions"

        prompt = """请分析这张图片，识别出图片中的人物。

对于每个识别到的人物，请提供：
1. 性别（男/女/不确定）
2. 年龄估计（儿童/青少年/青年/中年/老年）
3. 外貌特征（发型、服装等）
4. 明显的家庭关系（如果有）

请用中文描述。如果图片中没有人物，请说明"未识别到人物"。

输出格式：
照片中有[N]个人物：
1. [描述1]
2. [描述2]
...
"""

        headers = {
            'Authorization': f'Bearer {config.MINIMAX_API_KEY}',
            'Content-Type': 'application/json'
        }

        payload = {
            "model": config.OPENAI_VISION_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ]
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            result = response.json()

            if 'choices' in result:
                return result['choices'][0]['message']['content']
            else:
                raise ValueError(f"OpenAI Vision API 错误: {result}")
