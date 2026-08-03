from hsk_api.adapters.openai_speech import OpenAISpeechSynthesizer


class FakeSpeechEndpoint:
    def __init__(self) -> None:
        self.request: dict | None = None

    def create(self, **kwargs):
        self.request = kwargs
        return type("SpeechResponse", (), {"content": b"mp3"})()


class FakeClient:
    def __init__(self) -> None:
        endpoint = FakeSpeechEndpoint()
        self.audio = type("Audio", (), {"speech": endpoint})()


def test_tts_1_hd_uses_the_speech_endpoint_without_unsupported_instructions() -> None:
    synthesizer = OpenAISpeechSynthesizer(
        api_key="test-key",
        model="tts-1-hd",
        voice="coral",
        timeout=15,
    )
    synthesizer.client = FakeClient()

    content = synthesizer.synthesize(text="你好", speed=0.82)

    assert content == b"mp3"
    assert synthesizer.client.audio.speech.request == {
        "model": "tts-1-hd",
        "voice": "coral",
        "input": "你好",
        "response_format": "mp3",
        "speed": 0.82,
    }
