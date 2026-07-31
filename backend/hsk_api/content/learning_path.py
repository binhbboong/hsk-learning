from hsk_api.models.learning_loop import Checkpoint, LearningPath, MultiActivityLesson


_SEEDS = [
    {
        "title": "Chào hỏi và giới thiệu",
        "goal": "Chào hỏi và nói tên của mình.",
        "dialogue": [
            ("Mai", "你好！", "Nǐ hǎo!", "Xin chào!"),
            ("王明", "你好，我是王明。", "Nǐ hǎo, wǒ shì Wáng Míng.", "Xin chào, tôi là Vương Minh."),
        ],
        "listen": ("你好，我是王明。", "Người nói tên gì?", ["Vương Minh", "Lý Hoa", "Mai"], "Vương Minh"),
        "order": (["我", "是", "学生"], ["我", "是", "学生"], "Tôi là học sinh."),
        "words": [("你", "nǐ", "bạn"), ("好", "hǎo", "tốt")],
    },
    {
        "title": "Hỏi thăm sức khỏe",
        "goal": "Hỏi và trả lời “Bạn khỏe không?”.",
        "dialogue": [
            ("Mai", "你好吗？", "Nǐ hǎo ma?", "Bạn khỏe không?"),
            ("王明", "我很好，谢谢。", "Wǒ hěn hǎo, xièxie.", "Tôi rất khỏe, cảm ơn."),
        ],
        "listen": ("我很好，谢谢。", "Người nói cảm thấy thế nào?", ["Rất khỏe", "Rất mệt", "Đói"], "Rất khỏe"),
        "order": (["你", "好", "吗"], ["你", "好", "吗"], "Bạn khỏe không?"),
        "words": [("吗", "ma", "trợ từ nghi vấn"), ("谢谢", "xièxie", "cảm ơn")],
    },
    {
        "title": "Gia đình của tôi",
        "goal": "Giới thiệu thành viên gia đình.",
        "dialogue": [
            ("王明", "这是我妈妈。", "Zhè shì wǒ māma.", "Đây là mẹ tôi."),
            ("Mai", "她是老师吗？", "Tā shì lǎoshī ma?", "Cô ấy là giáo viên phải không?"),
        ],
        "listen": ("这是我妈妈。", "Người được giới thiệu là ai?", ["Mẹ", "Chị gái", "Giáo viên"], "Mẹ"),
        "order": (["这", "是", "我", "妈妈"], ["这", "是", "我", "妈妈"], "Đây là mẹ tôi."),
        "words": [("这", "zhè", "đây"), ("妈妈", "māma", "mẹ")],
    },
    {
        "title": "Số và tuổi",
        "goal": "Hỏi và nói tuổi.",
        "dialogue": [
            ("Mai", "你几岁？", "Nǐ jǐ suì?", "Bạn mấy tuổi?"),
            ("王明", "我二十岁。", "Wǒ èrshí suì.", "Tôi 20 tuổi."),
        ],
        "listen": ("我二十岁。", "Người nói bao nhiêu tuổi?", ["12", "20", "22"], "20"),
        "order": (["我", "二十", "岁"], ["我", "二十", "岁"], "Tôi 20 tuổi."),
        "words": [("几", "jǐ", "mấy"), ("岁", "suì", "tuổi")],
    },
    {
        "title": "Mua đồ uống",
        "goal": "Gọi một đồ uống đơn giản.",
        "dialogue": [
            ("Mai", "我要一杯茶。", "Wǒ yào yì bēi chá.", "Tôi muốn một cốc trà."),
            ("店员", "好的，谢谢。", "Hǎo de, xièxie.", "Được, cảm ơn."),
        ],
        "listen": ("我要一杯茶。", "Người nói muốn gì?", ["Một cốc trà", "Một cốc nước", "Một bát cơm"], "Một cốc trà"),
        "order": (["我", "要", "一杯", "茶"], ["我", "要", "一杯", "茶"], "Tôi muốn một cốc trà."),
        "words": [("要", "yào", "muốn"), ("茶", "chá", "trà")],
    },
]


def _lesson(number: int, seed: dict) -> MultiActivityLesson:
    lesson_id = f"hsk1-lesson-{number}"
    options = [
        {"id": chr(97 + index), "text": text}
        for index, text in enumerate(seed["listen"][2])
    ]
    correct_id = next(option["id"] for option in options if option["text"] == seed["listen"][3])
    return MultiActivityLesson.model_validate(
        {
            "id": lesson_id,
            "number": number,
            "level": 1,
            "title": seed["title"],
            "goal": seed["goal"],
            "estimated_minutes": 10,
            "dialogue": [
                {
                    "id": f"{lesson_id}-line-{index}",
                    "speaker": speaker,
                    "hanzi": hanzi,
                    "audio_text": hanzi,
                    "pinyin": pinyin,
                    "translation_vi": translation,
                }
                for index, (speaker, hanzi, pinyin, translation) in enumerate(seed["dialogue"], 1)
            ],
            "listening": {
                "id": f"{lesson_id}-listening",
                "audio_text": seed["listen"][0],
                "prompt_vi": seed["listen"][1],
                "options": options,
                "correct_option_id": correct_id,
                "transcript_zh": seed["listen"][0],
                "pinyin": seed["dialogue"][1][2],
                "translation_vi": seed["dialogue"][1][3],
                "explanation_vi": f"Đáp án đúng là {seed['listen'][3]}.",
            },
            "sentence_order": {
                "id": f"{lesson_id}-order",
                "prompt_vi": "Sắp xếp thành câu đúng.",
                "tokens": list(reversed(seed["order"][0])),
                "correct_tokens": seed["order"][1],
                "pinyin": " / ".join(seed["order"][1]),
                "translation_vi": seed["order"][2],
                "explanation_vi": "Đặt chủ thể trước, sau đó là động từ và phần bổ sung.",
            },
            "vocabulary": [
                {
                    "id": f"{lesson_id}-word-{index}",
                    "hanzi": hanzi,
                    "pinyin": pinyin,
                    "meaning_vi": meaning,
                }
                for index, (hanzi, pinyin, meaning) in enumerate(seed["words"], 1)
            ],
            "pronunciation_text": seed["dialogue"][0][1],
        }
    )


LESSONS = [_lesson(index, seed) for index, seed in enumerate(_SEEDS, 1)]
PATH = LearningPath(
    level=1,
    lessons=[lesson.model_dump(include={"id", "number", "title", "goal", "estimated_minutes"}) for lesson in LESSONS],
)
CHECKPOINT = Checkpoint.model_validate(
    {
        "id": "hsk1-checkpoint-1-5",
        "title": "Checkpoint Bài 1-5",
        "lesson_ids": [lesson.id for lesson in LESSONS],
        "questions": [
            {
                "id": "checkpoint-listening",
                "kind": "listening",
                "prompt_vi": "Người nói muốn gì?",
                "audio_text": "我要一杯茶。",
                "options": [
                    {"id": "a", "text": "Một cốc trà"},
                    {"id": "b", "text": "Một cốc nước"},
                ],
                "correct_answer": "a",
                "explanation_vi": "茶 nghĩa là trà.",
            },
            {
                "id": "checkpoint-vocabulary",
                "kind": "vocabulary",
                "prompt_vi": "谢谢 nghĩa là gì?",
                "options": [
                    {"id": "a", "text": "Xin chào"},
                    {"id": "b", "text": "Cảm ơn"},
                ],
                "correct_answer": "b",
                "explanation_vi": "谢谢 (xièxie) nghĩa là cảm ơn.",
            },
            {
                "id": "checkpoint-order",
                "kind": "sentence-order",
                "prompt_vi": "Sắp xếp câu “Tôi là học sinh”.",
                "tokens": ["学生", "是", "我"],
                "correct_answer": "我|是|学生",
                "explanation_vi": "Trật tự là chủ thể 我 + 是 + danh từ 学生.",
            },
        ],
    }
)
