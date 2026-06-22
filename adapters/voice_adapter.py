"""
=============================================
语音输入适配器
=============================================

支持音频录制和 STT 语音转文本
"""

import base64
import io
import httpx

import config
from .base import InputAdapter, InputType


class VoiceInputAdapter(InputAdapter):
    """
    语音输入适配器

    使用 STT 服务将语音转换为文本
    """

    @property
    def input_type(self) -> InputType:
        return InputType.VOICE

    def validate_content(self, content: str) -> bool:
        """验证音频内容"""
        try:
            audio_data = base64.b64decode(content)
            # 检查音频数据大小（简单验证）
            if len(audio_data) < 100:
                raise ValueError("音频数据过小")
            return True
        except Exception as e:
            raise ValueError(f"音频格式错误: {e}")

    def process(self, content: str) -> str:
        """
        处理语音内容

        Args:
            content: base64 编码的音频数据

        Returns:
            STT 转录的文本
        """
        self.validate_content(content)

        audio_data = base64.b64decode(content)

        # 根据 STT 服务类型调用
        stt_type = config.STT_SERVICE_TYPE  # minimax_stt / whisper

        if stt_type == "minimax_stt":
            return self._call_minimax_stt(audio_data)
        else:
            return self._call_whisper(audio_data)

    def _call_minimax_stt(self, audio_data: bytes) -> str:
        """调用 MiniMax STT 服务"""
        url = f"{config.MINIMAX_STT_URL}/audio/transcriptions"

        headers = {
            'Authorization': f'Bearer {config.MINIMAX_API_KEY}'
        }

        files = {
            'file': ('audio.wav', io.BytesIO(audio_data), 'audio/wav')
        }

        data = {
            'model': 'speech-01'
        }

        try:
            response = httpx.post(url, headers=headers, files=files, data=data, timeout=30.0)
            result = response.json()

            if 'text' in result:
                return result['text']
            else:
                raise ValueError(f"MiniMax STT API 错误: {result}")
        except Exception as e:
            raise ValueError(f"STT 调用失败: {e}")

    def _call_whisper(self, audio_data: bytes) -> str:
        """调用 Whisper API"""
        url = config.WHISPER_API_URL or "https://api.openai.com/v1/audio/transcriptions"

        headers = {
            'Authorization': f'Bearer {config.MINIMAX_API_KEY}'
        }

        files = {
            'file': ('audio.wav', io.BytesIO(audio_data), 'audio/wav')
        }

        data = {
            'model': 'whisper-1',
            'language': 'zh'
        }

        try:
            response = httpx.post(url, headers=headers, files=files, data=data, timeout=30.0)
            result = response.json()

            if 'text' in result:
                return result['text']
            else:
                raise ValueError(f"Whisper API 错误: {result}")
        except Exception as e:
            raise ValueError(f"STT 调用失败: {e}")
