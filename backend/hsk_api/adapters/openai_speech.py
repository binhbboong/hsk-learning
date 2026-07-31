from hsk_api.adapters.openai_client import create_openai_client


class OpenAISpeechSynthesizer:
    def __init__(self, api_key: str, model: str, voice: str, timeout: float) -> None:
        self.client = create_openai_client(api_key, timeout)
        self.model = model
        self.voice = voice

    def synthesize(self, *, text: str, speed: float) -> bytes:
        response = self.client.audio.speech.create(
            model=self.model,
            voice=self.voice,
            input=text,
            instructions="Nói tiếng Phổ thông chuẩn, rõ từng âm tiết và tự nhiên cho người mới học tiếng Trung.",
            response_format="mp3",
            speed=speed,
        )
        return response.content
