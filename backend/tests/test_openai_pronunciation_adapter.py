from types import SimpleNamespace

from hsk_api.adapters.openai_pronunciation import OpenAIPronunciationAnalyzer


class FakeTranscriptions:
    def __init__(self) -> None:
        self.kwargs = None

    def create(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(text="")


class FakeCompletions:
    def __init__(self) -> None:
        self.kwargs = None

    def create(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content=(
                            '{"score": 90, "syllables": '
                            '[{"target": "ni", "tone": 3, "status": "good", '
                            '"heard": "ni", "tip_vi": "Giữ thanh 3."}]}'
                        )
                    )
                )
            ]
        )


def test_transcription_is_not_biased_with_the_expected_answer() -> None:
    adapter = OpenAIPronunciationAnalyzer("test-key", "gpt-4o-transcribe", 5)
    transcriptions = FakeTranscriptions()
    adapter.client = SimpleNamespace(
        audio=SimpleNamespace(transcriptions=transcriptions),
    )

    result = adapter.analyze(
        audio=b"silence",
        filename="recording.webm",
        content_type="audio/webm",
        target_text="你好！",
        target_pinyin="Nǐ hǎo!",
    )

    assert "prompt" not in transcriptions.kwargs
    assert result.score == 0
    assert result.verdict == "needs_practice"
    assert [item.target for item in result.syllables] == ["nǐ", "hǎo"]
    assert [item.tone for item in result.syllables] == [3, 3]
    assert "không phải điểm thi" in result.disclaimer_vi


def test_acoustic_assessment_sends_supported_wav_input() -> None:
    adapter = OpenAIPronunciationAnalyzer("test-key", "gpt-4o-transcribe", 5)
    transcriptions = FakeTranscriptions()
    transcriptions.create = lambda **kwargs: SimpleNamespace(text="你")
    completions = FakeCompletions()
    adapter.client = SimpleNamespace(
        audio=SimpleNamespace(transcriptions=transcriptions),
        chat=SimpleNamespace(completions=completions),
    )

    result = adapter.analyze(
        audio=b"RIFF-audio",
        filename="recording.wav",
        content_type="audio/wav",
        target_text="你",
        target_pinyin="nǐ",
    )

    audio_input = completions.kwargs["messages"][1]["content"][1]["input_audio"]
    assert audio_input["format"] == "wav"
    assert result.score == 90
    assert result.syllables[0].tone == 3


def test_acoustic_assessment_skips_unsupported_webm_input() -> None:
    adapter = OpenAIPronunciationAnalyzer("test-key", "gpt-4o-transcribe", 5)
    completions = FakeCompletions()
    adapter.client = SimpleNamespace(
        audio=SimpleNamespace(
            transcriptions=SimpleNamespace(
                create=lambda **kwargs: SimpleNamespace(text="你")
            )
        ),
        chat=SimpleNamespace(completions=completions),
    )

    adapter.analyze(
        audio=b"webm-audio",
        filename="recording.webm",
        content_type="audio/webm",
        target_text="你",
        target_pinyin="nǐ",
    )

    assert completions.kwargs is None
