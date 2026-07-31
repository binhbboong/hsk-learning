from hsk_api.models.lesson import Lesson


DEFAULT_HSK1_LESSON = Lesson.model_validate(
    {
        "id": "hsk1-chao-hoi",
        "level": 1,
        "title": "Chào hỏi đầu tiên",
        "goal": "Nhận biết và sử dụng 5 từ HSK 1 quen thuộc trong giao tiếp cơ bản.",
        "estimated_minutes": 5,
        "cards": [
            {
                "id": "ni",
                "hanzi": "你",
                "pinyin": "nǐ",
                "sino_vietnamese": "nhĩ",
                "meaning_vi": "bạn",
                "example_zh": "你好！",
                "example_vi": "Xin chào bạn!",
            },
            {
                "id": "hao",
                "hanzi": "好",
                "pinyin": "hǎo",
                "sino_vietnamese": "hảo",
                "meaning_vi": "tốt, khỏe",
                "example_zh": "我很好。",
                "example_vi": "Tôi rất khỏe.",
            },
            {
                "id": "wo",
                "hanzi": "我",
                "pinyin": "wǒ",
                "sino_vietnamese": "ngã",
                "meaning_vi": "tôi",
                "example_zh": "我是学生。",
                "example_vi": "Tôi là học sinh.",
            },
            {
                "id": "shi",
                "hanzi": "是",
                "pinyin": "shì",
                "sino_vietnamese": "thị",
                "meaning_vi": "là",
                "example_zh": "她是老师。",
                "example_vi": "Cô ấy là giáo viên.",
            },
            {
                "id": "xiexie",
                "hanzi": "谢谢",
                "pinyin": "xièxie",
                "sino_vietnamese": "tạ tạ",
                "meaning_vi": "cảm ơn",
                "example_zh": "谢谢你。",
                "example_vi": "Cảm ơn bạn.",
            },
        ],
    }
)
