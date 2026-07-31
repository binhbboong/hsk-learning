import base64
import json
import re
from difflib import SequenceMatcher

from hsk_api.adapters.openai_client import create_openai_client
from hsk_api.models.pronunciation import PronunciationResult, SyllableFeedback


DISCLAIMER = (
    "Phản hồi AI chỉ hỗ trợ luyện tập, không phải điểm thi hay đánh giá của giáo viên."
)
TONE_MARKS = {
    **dict.fromkeys("āēīōūǖ", 1),
    **dict.fromkeys("áéíóúǘ", 2),
    **dict.fromkeys("ǎěǐǒǔǚ", 3),
    **dict.fromkeys("àèìòùǜ", 4),
}


class OpenAIPronunciationAnalyzer:
    def __init__(
        self,
        api_key: str,
        model: str,
        timeout: float,
        audio_model: str = "gpt-audio",
    ) -> None:
        self.client = create_openai_client(api_key, timeout)
        self.model = model
        self.audio_model = audio_model

    def analyze(
        self,
        *,
        audio: bytes,
        filename: str,
        content_type: str,
        target_text: str,
        target_pinyin: str,
    ) -> PronunciationResult:
        transcription = self.client.audio.transcriptions.create(
            model=self.model,
            file=(filename, audio, content_type),
            language="zh",
        )
        transcript = transcription.text.strip()
        expected, actual = self._normalize(target_text), self._normalize(transcript)
        content_score = round(
            (SequenceMatcher(None, expected, actual).ratio() if expected else 0) * 100
        )
        content_correct = content_score >= 85
        syllables = self._fallback_syllables(
            target_pinyin,
            correct=content_correct and bool(actual),
        )
        if not actual:
            return PronunciationResult(
                verdict="needs_practice",
                score=0,
                content_score=0,
                transcript="",
                feedback_vi=(
                    "AI không nhận diện được lời nói trong bản thu. "
                    "Hãy kiểm tra microphone và nói rõ hơn."
                ),
                focus_vi=[f"Đọc lại: {target_pinyin}"],
                syllables=syllables,
                disclaimer_vi=DISCLAIMER,
            )

        acoustic = self._audio_assessment(
            audio=audio,
            content_type=content_type,
            target_text=target_text,
            target_pinyin=target_pinyin,
        )
        overall_score = content_score
        if acoustic is not None:
            overall_score = max(0, min(100, int(acoustic.get("score", content_score))))
            try:
                parsed = [
                    SyllableFeedback.model_validate(item)
                    for item in acoustic.get("syllables", [])
                ]
                if parsed:
                    syllables = parsed
            except (TypeError, ValueError):
                pass

        correct = content_correct and overall_score >= 85
        return PronunciationResult(
            verdict="correct" if correct else "needs_practice",
            score=overall_score,
            content_score=content_score,
            transcript=transcript,
            feedback_vi=(
                "AI đã nhận diện đúng nội dung câu mẫu. Xem từng âm tiết bên dưới "
                "và nghe lại để đối chiếu thanh điệu."
                if content_correct
                else "AI chưa nhận diện trọn vẹn câu mẫu. Hãy nghe mẫu, nói chậm "
                "và rõ từng âm tiết rồi thử lại."
            ),
            focus_vi=[] if correct else [f"Luyện lại: {target_pinyin}"],
            syllables=syllables,
            disclaimer_vi=DISCLAIMER,
        )

    @staticmethod
    def _normalize(value: str) -> str:
        return re.sub(r"[\W_]+", "", value, flags=re.UNICODE).casefold()

    def _audio_assessment(
        self,
        *,
        audio: bytes,
        content_type: str,
        target_text: str,
        target_pinyin: str,
    ) -> dict | None:
        chat = getattr(self.client, "chat", None)
        if chat is None:
            return None
        audio_format = {
            "audio/mpeg": "mp3",
            "audio/wav": "wav",
            "audio/x-wav": "wav",
        }.get(content_type)
        if audio_format is None:
            return None
        schema_instruction = (
            '{"score": 0, "syllables": [{"target": "nǐ", "tone": 3, '
            '"status": "good|review|uncertain", "heard": "", "tip_vi": ""}]}'
        )
        try:
            response = chat.completions.create(
                model=self.audio_model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Bạn phân tích phát âm tiếng Trung cho người Việt. "
                            "Chỉ trả JSON hợp lệ, không markdown."
                        ),
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    f"Câu đích: {target_text}; pinyin: {target_pinyin}. "
                                    f"Trả đúng dạng {schema_instruction}. Mỗi âm tiết đích "
                                    "có một mục. Dùng uncertain nếu âm thanh không đủ rõ. "
                                    "Mẹo sửa phải cụ thể bằng tiếng Việt."
                                ),
                            },
                            {
                                "type": "input_audio",
                                "input_audio": {
                                    "data": base64.b64encode(audio).decode("ascii"),
                                    "format": audio_format,
                                },
                            },
                        ],
                    },
                ],
            )
            content = response.choices[0].message.content or ""
            cleaned = content.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.removeprefix("```json").removeprefix("```")
                cleaned = cleaned.removesuffix("```").strip()
            return json.loads(cleaned)
        except Exception:
            return None

    @staticmethod
    def _fallback_syllables(
        target_pinyin: str,
        *,
        correct: bool,
    ) -> list[SyllableFeedback]:
        tokens = re.findall(
            r"[A-Za-züÜāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]+[1-4]?",
            target_pinyin,
        )
        result: list[SyllableFeedback] = []
        for raw in tokens:
            numbered_tone = int(raw[-1]) if raw[-1:].isdigit() else 0
            tone = numbered_tone or next(
                (
                    TONE_MARKS[char.casefold()]
                    for char in raw
                    if char.casefold() in TONE_MARKS
                ),
                0,
            )
            target = raw.casefold().rstrip("1234")
            result.append(
                SyllableFeedback(
                    target=target,
                    tone=tone,
                    status="good" if correct else "uncertain",
                    heard="",
                    tip_vi=(
                        f"Giữ đường nét thanh {tone} và nghe mẫu để tự đối chiếu."
                        if tone
                        else "Đọc chậm, rõ phần đầu và vần của âm tiết."
                    ),
                )
            )
        return result
