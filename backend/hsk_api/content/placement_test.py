from dataclasses import dataclass

from hsk_api.models.placement import PlacementOption, PlacementSkill


@dataclass(frozen=True)
class PlacementQuestionDefinition:
    id: str
    skill: PlacementSkill
    level: int
    prompt_vi: str
    options: tuple[PlacementOption, ...] = ()
    correct_option_id: str | None = None
    audio_text: str | None = None
    target_text: str | None = None
    target_pinyin: str | None = None


def _options(question_id: str, values: tuple[str, str, str, str]) -> tuple[PlacementOption, ...]:
    return tuple(
        PlacementOption(id=f"{question_id}-{letter}", text=value)
        for letter, value in zip("abcd", values)
    )


_VOCABULARY = [
    (1, "你", ("bạn", "tôi", "anh ấy", "chúng tôi"), 0),
    (2, "一起", ("một mình", "cùng nhau", "đã từng", "ngay lập tức"), 1),
    (3, "已经", ("đang", "sắp", "đã", "thường"), 2),
    (4, "顺利", ("thuận lợi", "đột ngột", "nghiêm túc", "náo nhiệt"), 0),
    (5, "承担", ("từ chối", "gánh vác", "thảo luận", "miêu tả"), 1),
    (6, "潜移默化", ("thay đổi âm thầm", "công khai phản đối", "nhanh chóng kết thúc", "lặp lại máy móc"), 0),
]

_GRAMMAR = [
    (1, "Chọn câu đúng: Tôi là học sinh.", ("我是学生。", "我学生是。", "是我学生。", "学生我是。"), 0),
    (2, "Điền từ: 我___北京工作。", ("把", "在", "被", "过"), 1),
    (3, "Điền từ: 他___吃完饭，就去上班了。", ("一", "把", "虽然", "除了"), 0),
    (4, "Chọn liên từ đúng: ___下雨，比赛___继续进行。", ("因为…所以…", "虽然…但是…", "不但…而且…", "只要…就…"), 1),
    (5, "Điền từ: 这个问题值得我们认真___。", ("考虑", "考虑了", "被考虑", "把考虑"), 0),
    (6, "Chọn cách diễn đạt tự nhiên nhất.", ("与其等待机会，不如主动创造机会。", "与其等待机会，所以主动创造机会。", "虽然等待机会，就主动创造机会。", "不仅等待机会，但是主动创造机会。"), 0),
]

_LISTENING = [
    (1, "Người nói đang chào ai?", "你好！", ("Một người", "Một món ăn", "Một địa điểm", "Một con số"), 0),
    (2, "Hai người sẽ làm gì?", "我们一起去吃饭吧。", ("Đi học", "Đi ăn", "Đi ngủ", "Đi mua sách"), 1),
    (3, "Việc gì đã xảy ra?", "火车已经到了。", ("Tàu đã đến", "Tàu sắp đi", "Vé đã hết", "Ga đóng cửa"), 0),
    (4, "Vì sao cô ấy vui?", "她通过了考试，所以特别高兴。", ("Được nghỉ", "Gặp bạn", "Thi đỗ", "Mua quà"), 2),
    (5, "Người nói nhấn mạnh điều gì?", "这项工作不仅需要耐心，还需要丰富的经验。", ("Chỉ cần nhanh", "Cần kiên nhẫn và kinh nghiệm", "Không cần kinh nghiệm", "Nên đổi công việc"), 1),
    (6, "Quan điểm chính là gì?", "科技带来便利的同时，也促使我们重新审视人与人之间的关系。", ("Công nghệ chỉ có hại", "Quan hệ con người không đổi", "Cần nhìn lại quan hệ khi công nghệ phát triển", "Nên ngừng dùng công nghệ"), 2),
]

_PRONUNCIATION = [
    (1, "你好。", "nǐ hǎo"),
    (2, "我想喝一杯茶。", "wǒ xiǎng hē yì bēi chá"),
    (3, "请问，地铁站怎么走？", "qǐngwèn, dìtiězhàn zěnme zǒu"),
    (4, "虽然下雨，但是我们还是出发了。", "suīrán xiàyǔ, dànshì wǒmen háishi chūfā le"),
    (5, "有效的沟通能够避免不必要的误会。", "yǒuxiào de gōutōng nénggòu bìmiǎn bù bìyào de wùhuì"),
    (6, "面对错综复杂的局面，他依然从容不迫。", "miànduì cuòzōng fùzá de júmiàn, tā yīrán cóngróng búpò"),
]

_VOCABULARY_ALT = [
    (1, "谢谢", ("xin lỗi", "cảm ơn", "tạm biệt", "không sao"), 1),
    (2, "附近", ("ở giữa", "gần đây", "bên trong", "phía trên"), 1),
    (3, "决定", ("quyết định", "do dự", "phản đối", "quên"), 0),
    (4, "适应", ("thích nghi", "từ bỏ", "tiết kiệm", "so sánh"), 0),
    (5, "缓解", ("làm dịu", "tăng tốc", "bác bỏ", "che giấu"), 0),
    (6, "无可厚非", ("không đáng trách", "không thể hiểu", "không có căn cứ", "không cần thiết"), 0),
]

_GRAMMAR_ALT = [
    (1, "Điền từ: 这是___书。", ("我", "我的", "我是", "我在"), 1),
    (2, "Điền từ: 我学中文学___两年。", ("着", "过", "了", "的"), 2),
    (3, "Điền từ: 你___认真，就一定能学好。", ("只要", "虽然", "除了", "不但"), 0),
    (4, "Chọn câu dùng 把 đúng.", ("我把作业做完了。", "我作业把做完了。", "把我做完了作业。", "我做把作业完了。"), 0),
    (5, "Điền từ: 无论多忙，他___坚持锻炼。", ("才", "却", "都", "又"), 2),
    (6, "Chọn cách diễn đạt tự nhiên nhất.", ("这个方案尚有值得商榷之处。", "这个方案尚有商榷得值得之处。", "这个方案把值得商榷之处。", "这个方案被尚有商榷。"), 0),
]

_LISTENING_ALT = [
    (1, "Người nói muốn uống gì?", "我想喝水。", ("Nước", "Trà", "Cà phê", "Sữa"), 0),
    (2, "Cuộc hẹn vào lúc nào?", "我们下午三点见。", ("8 giờ sáng", "12 giờ trưa", "3 giờ chiều", "7 giờ tối"), 2),
    (3, "Tại sao anh ấy đến muộn?", "因为路上堵车，他迟到了。", ("Quên giờ", "Tắc đường", "Trời mưa", "Xe hỏng"), 1),
    (4, "Người phụ nữ đề nghị điều gì?", "要不我们先休息一下，再继续讨论吧。", ("Dừng hẳn", "Nghỉ rồi thảo luận tiếp", "Đổi chủ đề", "Về nhà ngay"), 1),
    (5, "Kết luận của người nói là gì?", "尽管准备时间有限，我们还是按时完成了任务。", ("Nhiệm vụ bị hủy", "Cần thêm thời gian", "Đã hoàn thành đúng hạn", "Chưa bắt đầu"), 2),
    (6, "Thái độ của người nói là gì?", "这项改革虽非尽善尽美，却不失为一次有益的尝试。", ("Phủ nhận hoàn toàn", "Ủng hộ có dè dặt", "Không quan tâm", "Muốn dừng ngay"), 1),
]

_PRONUNCIATION_ALT = [
    (1, "谢谢你。", "xièxie nǐ"),
    (2, "今天天气很好。", "jīntiān tiānqì hěn hǎo"),
    (3, "我已经吃过早饭了。", "wǒ yǐjīng chīguo zǎofàn le"),
    (4, "只要坚持练习，就会有进步。", "zhǐyào jiānchí liànxí, jiù huì yǒu jìnbù"),
    (5, "这个决定充分考虑了大家的意见。", "zhège juédìng chōngfèn kǎolǜ le dàjiā de yìjiàn"),
    (6, "在瞬息万变的环境中，保持判断力尤为重要。", "zài shùnxī wànbiàn de huánjìng zhōng, bǎochí pànduànlì yóuwéi zhòngyào"),
]


def _build_bank() -> tuple[PlacementQuestionDefinition, ...]:
    questions: list[PlacementQuestionDefinition] = []
    for level, hanzi, values, correct_index in _VOCABULARY:
        question_id = f"vocabulary-hsk{level}"
        options = _options(question_id, values)
        questions.append(PlacementQuestionDefinition(
            id=question_id, skill="vocabulary", level=level,
            prompt_vi=f'Chọn nghĩa đúng của “{hanzi}”.', options=options,
            correct_option_id=options[correct_index].id,
        ))
    for level, prompt, values, correct_index in _GRAMMAR:
        question_id = f"grammar-hsk{level}"
        options = _options(question_id, values)
        questions.append(PlacementQuestionDefinition(
            id=question_id, skill="grammar", level=level, prompt_vi=prompt,
            options=options, correct_option_id=options[correct_index].id,
        ))
    for level, prompt, audio, values, correct_index in _LISTENING:
        question_id = f"listening-hsk{level}"
        options = _options(question_id, values)
        questions.append(PlacementQuestionDefinition(
            id=question_id, skill="listening", level=level, prompt_vi=prompt,
            options=options, correct_option_id=options[correct_index].id,
            audio_text=audio,
        ))
    for level, target, pinyin in _PRONUNCIATION:
        questions.append(PlacementQuestionDefinition(
            id=f"pronunciation-hsk{level}", skill="pronunciation", level=level,
            prompt_vi="Đọc rõ câu sau.", target_text=target, target_pinyin=pinyin,
        ))
    for level, hanzi, values, correct_index in _VOCABULARY_ALT:
        question_id = f"vocabulary-hsk{level}-b"
        options = _options(question_id, values)
        questions.append(PlacementQuestionDefinition(
            id=question_id, skill="vocabulary", level=level,
            prompt_vi=f'Chọn nghĩa đúng của “{hanzi}”.', options=options,
            correct_option_id=options[correct_index].id,
        ))
    for level, prompt, values, correct_index in _GRAMMAR_ALT:
        question_id = f"grammar-hsk{level}-b"
        options = _options(question_id, values)
        questions.append(PlacementQuestionDefinition(
            id=question_id, skill="grammar", level=level, prompt_vi=prompt,
            options=options, correct_option_id=options[correct_index].id,
        ))
    for level, prompt, audio, values, correct_index in _LISTENING_ALT:
        question_id = f"listening-hsk{level}-b"
        options = _options(question_id, values)
        questions.append(PlacementQuestionDefinition(
            id=question_id, skill="listening", level=level, prompt_vi=prompt,
            options=options, correct_option_id=options[correct_index].id, audio_text=audio,
        ))
    for level, target, pinyin in _PRONUNCIATION_ALT:
        questions.append(PlacementQuestionDefinition(
            id=f"pronunciation-hsk{level}-b", skill="pronunciation", level=level,
            prompt_vi="Đọc rõ câu sau.", target_text=target, target_pinyin=pinyin,
        ))
    return tuple(questions)


PLACEMENT_QUESTION_BANK = _build_bank()


def placement_question(question_id: str) -> PlacementQuestionDefinition | None:
    return next((item for item in PLACEMENT_QUESTION_BANK if item.id == question_id), None)
