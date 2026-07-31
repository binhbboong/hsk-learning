from hsk_api.models.skills import (
    GrammarLesson,
    ListeningLesson,
    PronunciationLesson,
    SkillCatalog,
)


SKILL_CATALOG = SkillCatalog.model_validate(
    {
        "level": 1,
        "items": [
            {
                "kind": "vocabulary",
                "title": "Từ vựng",
                "goal": "Nhớ 5 từ chào hỏi bằng flip-card.",
                "estimated_minutes": 5,
                "route": "/lesson",
            },
            {
                "kind": "grammar",
                "title": "Ngữ pháp",
                "goal": "Dùng 是 để giới thiệu người và sự vật.",
                "estimated_minutes": 7,
                "route": "/skills/grammar",
            },
            {
                "kind": "listening",
                "title": "Nghe hiểu",
                "goal": "Nhận ra lời chào và câu giới thiệu cơ bản.",
                "estimated_minutes": 5,
                "route": "/skills/listening",
            },
            {
                "kind": "pronunciation",
                "title": "Phát âm",
                "goal": "Luyện thanh 3 trong cụm từ 你好.",
                "estimated_minutes": 6,
                "route": "/skills/pronunciation",
            },
        ],
    }
)


GRAMMAR_LESSON = GrammarLesson.model_validate(
    {
        "id": "hsk1-grammar-shi",
        "level": 1,
        "kind": "grammar",
        "title": "Giới thiệu với 是",
        "goal": "Dùng mẫu A + 是 + B để giới thiệu.",
        "estimated_minutes": 7,
        "pattern": "A + 是 + B",
        "explanation_vi": "是 (shì) nối chủ thể A với danh tính hoặc vai trò B, gần nghĩa “là” trong tiếng Việt.",
        "examples": [
            {"hanzi": "我是学生。", "pinyin": "Wǒ shì xuésheng.", "meaning_vi": "Tôi là học sinh."},
            {"hanzi": "她是老师。", "pinyin": "Tā shì lǎoshī.", "meaning_vi": "Cô ấy là giáo viên."},
        ],
        "questions": [
            {
                "id": "grammar-1",
                "prompt_vi": "Chọn câu đúng cho “Tôi là người Việt Nam”.",
                "options": [
                    {"id": "a", "text": "我是越南人。"},
                    {"id": "b", "text": "我越南人是。"},
                    {"id": "c", "text": "是我越南人。"},
                ],
                "correct_option_id": "a",
                "explanation_vi": "Trật tự đúng là chủ thể 我 + 是 + danh tính 越南人.",
            },
            {
                "id": "grammar-2",
                "prompt_vi": "Chọn từ còn thiếu: 她 ___ 老师。",
                "options": [
                    {"id": "a", "text": "你"},
                    {"id": "b", "text": "是"},
                    {"id": "c", "text": "好"},
                ],
                "correct_option_id": "b",
                "explanation_vi": "是 đứng giữa 她 và 老师 để tạo nghĩa “Cô ấy là giáo viên”.",
            },
        ],
    }
)


LISTENING_LESSON = ListeningLesson.model_validate(
    {
        "id": "hsk1-listening-introduction",
        "level": 1,
        "kind": "listening",
        "title": "Nghe lời chào đầu tiên",
        "goal": "Nhận ra lời chào và tên người nói.",
        "estimated_minutes": 5,
        "utterance_zh": "你好，我是王明。",
        "pinyin": "Nǐ hǎo, wǒ shì Wáng Míng.",
        "meaning_vi": "Xin chào, tôi là Vương Minh.",
        "question_vi": "Người nói tự giới thiệu tên là gì?",
        "options": [
            {"id": "a", "text": "Vương Minh"},
            {"id": "b", "text": "Lý Hoa"},
            {"id": "c", "text": "Trương An"},
        ],
        "correct_option_id": "a",
        "explanation_vi": "Cụm 我是王明 nghĩa là “Tôi là Vương Minh”.",
    }
)


PRONUNCIATION_LESSON = PronunciationLesson.model_validate(
    {
        "id": "hsk1-pronunciation-nihao",
        "level": 1,
        "kind": "pronunciation",
        "title": "Thanh điệu trong 你好",
        "goal": "Nghe và luyện biến điệu của hai thanh 3.",
        "estimated_minutes": 6,
        "hanzi": "你好",
        "pinyin": "nǐ hǎo",
        "meaning_vi": "xin chào",
        "tone_path": ["nǐ: hạ rồi nâng, khi đi trước hǎo đọc gần thanh 2", "hǎo: hạ thấp rồi nâng lên"],
        "common_mistake_vi": "Người Việt thường đọc cả hai âm đều trũng như nhau, khiến cụm từ bị ngắt và thiếu tự nhiên.",
        "correction_tip_vi": "Đọc nǐ ngắn và đi lên như thanh 2, sau đó hạ giọng ở đầu hǎo rồi nâng nhẹ ở cuối.",
    }
)
