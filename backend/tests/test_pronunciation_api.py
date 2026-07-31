from pathlib import Path
from fastapi.testclient import TestClient
from hsk_api.main import create_app


class FakeAnalyzer:
    def analyze(self, *, audio: bytes, filename: str, content_type: str, target_text: str, target_pinyin: str):
        assert audio == b"fake audio"
        assert target_text == "你好"
        return {
            "verdict": "correct",
            "score": 96,
            "content_score": 100,
            "transcript": "你好",
            "feedback_vi": "AI đã nhận diện đúng câu mẫu.",
            "focus_vi": [],
            "syllables": [
                {
                    "target": "nǐ",
                    "tone": 3,
                    "status": "good",
                    "heard": "nǐ",
                    "tip_vi": "Giữ giọng thấp rồi nhấc nhẹ.",
                },
                {
                    "target": "hǎo",
                    "tone": 3,
                    "status": "good",
                    "heard": "hǎo",
                    "tip_vi": "Nối âm tự nhiên.",
                },
            ],
            "disclaimer_vi": "Phản hồi AI chỉ hỗ trợ luyện tập, không phải điểm thi hay đánh giá của giáo viên.",
        }

class FakeSpeechSynthesizer:
    def synthesize(self, *, text: str, speed: float) -> bytes:
        assert text == "你好！"
        assert speed == 0.82
        return b"fake-mp3"


def authenticated_client(
    tmp_path: Path,
    analyzer=FakeAnalyzer(),
    speech_synthesizer=FakeSpeechSynthesizer(),
):
    client = TestClient(create_app(
        tmp_path / "accounts.sqlite3",
        pronunciation_analyzer=analyzer,
        speech_synthesizer=speech_synthesizer,
    ))
    session = client.post("/api/v1/auth/register", json={
        "display_name": "Mai", "email": "mai@example.com", "password": "matkhau123"
    }).json()
    return client, {"Authorization": f"Bearer {session['token']}"}


def test_analyzes_an_authenticated_recording(tmp_path: Path):
    client, headers = authenticated_client(tmp_path)
    response = client.post(
        "/api/v1/pronunciation/analyze",
        headers=headers,
        data={"target_text": "你好", "target_pinyin": "nǐ hǎo"},
        files={"audio": ("speech.webm", b"fake audio", "audio/webm")},
    )
    assert response.status_code == 200
    assert response.json()["score"] == 96
    assert response.json()["verdict"] == "correct"
    assert response.json()["content_score"] == 100
    assert response.json()["syllables"][0]["tone"] == 3
    assert "không phải điểm thi" in response.json()["disclaimer_vi"]


def test_rejects_unauthenticated_or_unsupported_audio(tmp_path: Path):
    client, headers = authenticated_client(tmp_path)
    assert client.post(
        "/api/v1/pronunciation/analyze",
        data={"target_text": "你好", "target_pinyin": "nǐ hǎo"},
        files={"audio": ("speech.webm", b"fake audio", "audio/webm")},
    ).status_code == 401
    assert client.post(
        "/api/v1/pronunciation/analyze",
        headers=headers,
        data={"target_text": "你好", "target_pinyin": "nǐ hǎo"},
        files={"audio": ("speech.txt", b"fake audio", "text/plain")},
    ).status_code == 415


def test_generates_a_mandarin_sample_for_an_authenticated_learner(tmp_path: Path):
    client, headers = authenticated_client(tmp_path)

    response = client.post(
        "/api/v1/pronunciation/sample",
        headers=headers,
        json={"text": "你好！", "speed": 0.82},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/mpeg"
    assert response.content == b"fake-mp3"
