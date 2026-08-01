from hsk_api.models.topic_vocabulary import (
    TopicRecommendation,
    TopicVocabularySession,
)


TOPICS = [
    ("greetings", "Chào hỏi", "Chào hỏi và làm quen trong các cuộc gặp hằng ngày."),
    ("family", "Gia đình", "Giới thiệu người thân và nói về gia đình."),
    ("food", "Ăn uống", "Gọi món và nói về đồ ăn, thức uống quen thuộc."),
    ("travel", "Du lịch", "Hỏi đường và di chuyển trong chuyến đi."),
    ("shopping", "Mua sắm", "Hỏi giá, số lượng và chọn món đồ cần mua."),
    ("school", "Trường học", "Từ vựng dùng trong lớp học và học tập."),
    ("work", "Công việc", "Giao tiếp cơ bản tại nơi làm việc."),
    ("time", "Thời gian", "Nói về ngày, giờ và lịch sinh hoạt hằng ngày."),
    ("numbers", "Số đếm", "Đếm, hỏi số lượng và dùng số trong tình huống cơ bản."),
]


CURATED_WORDS: dict[str, list[tuple[str, str, str, str, str, str]]] = {
    "greetings": [
        ("你好", "nǐ hǎo", "NHĨ HẢO", "xin chào", "你好，我叫安。", "Xin chào, tôi tên An."),
        ("再见", "zài jiàn", "TÁI KIẾN", "tạm biệt", "老师，再见！", "Tạm biệt thầy/cô!"),
        ("谢谢", "xièxie", "TẠ TẠ", "cảm ơn", "谢谢你的帮助。", "Cảm ơn bạn đã giúp đỡ."),
        ("不客气", "bú kèqi", "BẤT KHÁCH KHÍ", "không có gì", "不客气，我们是朋友。", "Không có gì, chúng ta là bạn."),
        ("请", "qǐng", "THỈNH", "mời; xin vui lòng", "请坐。", "Mời ngồi."),
        ("对不起", "duìbuqǐ", "ĐỐI BẤT KHỞI", "xin lỗi", "对不起，我来晚了。", "Xin lỗi, tôi đến muộn."),
        ("没关系", "méi guānxi", "MỘT QUAN HỆ", "không sao", "没关系，下次见。", "Không sao, lần sau gặp nhé."),
        ("名字", "míngzi", "DANH TỰ", "tên", "你叫什么名字？", "Bạn tên là gì?"),
        ("认识", "rènshi", "NHẬN THỨC", "quen; biết", "很高兴认识你。", "Rất vui được biết bạn."),
        ("朋友", "péngyou", "BẰNG HỮU", "bạn bè", "他是我的朋友。", "Anh ấy là bạn của tôi."),
    ],
    "family": [
        ("家", "jiā", "GIA", "nhà; gia đình", "我家有四个人。", "Nhà tôi có bốn người."),
        ("爸爸", "bàba", "BA BA", "bố", "我爸爸是医生。", "Bố tôi là bác sĩ."),
        ("妈妈", "māma", "MA MA", "mẹ", "妈妈在家。", "Mẹ đang ở nhà."),
        ("哥哥", "gēge", "CA CA", "anh trai", "我哥哥二十岁。", "Anh trai tôi hai mươi tuổi."),
        ("姐姐", "jiějie", "TỶ TỶ", "chị gái", "姐姐喜欢看书。", "Chị gái thích đọc sách."),
        ("弟弟", "dìdi", "ĐỆ ĐỆ", "em trai", "弟弟是学生。", "Em trai là học sinh."),
        ("妹妹", "mèimei", "MUỘI MUỘI", "em gái", "妹妹很可爱。", "Em gái rất đáng yêu."),
        ("儿子", "érzi", "NHI TỬ", "con trai", "他有一个儿子。", "Anh ấy có một con trai."),
        ("女儿", "nǚ'ér", "NỮ NHI", "con gái", "她女儿五岁。", "Con gái cô ấy năm tuổi."),
        ("爱", "ài", "ÁI", "yêu", "我爱我的家。", "Tôi yêu gia đình mình."),
    ],
    "food": [
        ("吃", "chī", "CẬT", "ăn", "我想吃米饭。", "Tôi muốn ăn cơm."),
        ("喝", "hē", "HÁT", "uống", "你喝茶吗？", "Bạn uống trà không?"),
        ("米饭", "mǐfàn", "MỄ PHẠN", "cơm", "米饭很好吃。", "Cơm rất ngon."),
        ("面条", "miàntiáo", "MIẾN ĐIỀU", "mì sợi", "我要一碗面条。", "Tôi muốn một bát mì."),
        ("水", "shuǐ", "THỦY", "nước", "请给我一杯水。", "Cho tôi một cốc nước."),
        ("茶", "chá", "TRÀ", "trà", "爸爸喜欢喝茶。", "Bố thích uống trà."),
        ("苹果", "píngguǒ", "BÌNH QUẢ", "táo", "这个苹果很甜。", "Quả táo này rất ngọt."),
        ("菜", "cài", "THÁI", "món ăn; rau", "这个菜不辣。", "Món này không cay."),
        ("好吃", "hǎochī", "HẢO CẬT", "ngon", "中国菜很好吃。", "Món Trung Quốc rất ngon."),
        ("买单", "mǎidān", "MÃI ĐƠN", "tính tiền", "服务员，买单。", "Nhân viên ơi, tính tiền."),
    ],
    "travel": [
        ("去", "qù", "KHỨ", "đi", "我去北京。", "Tôi đi Bắc Kinh."),
        ("来", "lái", "LAI", "đến", "你什么时候来？", "Khi nào bạn đến?"),
        ("车站", "chēzhàn", "XA TRẠM", "nhà ga", "车站在哪儿？", "Nhà ga ở đâu?"),
        ("飞机", "fēijī", "PHI CƠ", "máy bay", "飞机十点起飞。", "Máy bay cất cánh lúc mười giờ."),
        ("火车", "huǒchē", "HỎA XA", "tàu hỏa", "我坐火车去。", "Tôi đi bằng tàu hỏa."),
        ("出租车", "chūzūchē", "XUẤT TÔ XA", "taxi", "我们坐出租车吧。", "Chúng ta đi taxi nhé."),
        ("酒店", "jiǔdiàn", "TỬU ĐIẾM", "khách sạn", "酒店离这儿不远。", "Khách sạn không xa đây."),
        ("左边", "zuǒbian", "TẢ BIÊN", "bên trái", "银行在左边。", "Ngân hàng ở bên trái."),
        ("右边", "yòubian", "HỮU BIÊN", "bên phải", "商店在右边。", "Cửa hàng ở bên phải."),
        ("地图", "dìtú", "ĐỊA ĐỒ", "bản đồ", "我看一下地图。", "Tôi xem bản đồ một chút."),
    ],
    "shopping": [
        ("买", "mǎi", "MÃI", "mua", "我想买衣服。", "Tôi muốn mua quần áo."),
        ("卖", "mài", "MẠI", "bán", "这里卖水果。", "Ở đây bán hoa quả."),
        ("多少钱", "duōshao qián", "ĐA THIỂU TIỀN", "bao nhiêu tiền", "这个多少钱？", "Cái này bao nhiêu tiền?"),
        ("贵", "guì", "QUÝ", "đắt", "这件衣服太贵了。", "Bộ quần áo này đắt quá."),
        ("便宜", "piányi", "TIỆN NGHI", "rẻ", "那个比较便宜。", "Cái kia rẻ hơn."),
        ("衣服", "yīfu", "Y PHỤC", "quần áo", "这件衣服很好看。", "Bộ quần áo này rất đẹp."),
        ("大", "dà", "ĐẠI", "to", "有大一点的吗？", "Có cái lớn hơn một chút không?"),
        ("小", "xiǎo", "TIỂU", "nhỏ", "这个太小了。", "Cái này nhỏ quá."),
        ("颜色", "yánsè", "NHAN SẮC", "màu sắc", "你喜欢什么颜色？", "Bạn thích màu gì?"),
        ("可以", "kěyǐ", "KHẢ DĨ", "có thể; được", "可以便宜一点吗？", "Có thể rẻ hơn một chút không?"),
    ],
    "school": [
        ("学校", "xuéxiào", "HỌC HIỆU", "trường học", "我的学校很大。", "Trường của tôi rất lớn."),
        ("老师", "lǎoshī", "LÃO SƯ", "giáo viên", "王老师教汉语。", "Thầy Vương dạy tiếng Trung."),
        ("学生", "xuésheng", "HỌC SINH", "học sinh", "我是学生。", "Tôi là học sinh."),
        ("同学", "tóngxué", "ĐỒNG HỌC", "bạn học", "她是我的同学。", "Cô ấy là bạn học của tôi."),
        ("书", "shū", "THƯ", "sách", "桌子上有一本书。", "Trên bàn có một quyển sách."),
        ("汉语", "Hànyǔ", "HÁN NGỮ", "tiếng Trung", "我学习汉语。", "Tôi học tiếng Trung."),
        ("写", "xiě", "TẢ", "viết", "请写你的名字。", "Hãy viết tên của bạn."),
        ("读", "dú", "ĐỘC", "đọc", "我们一起读课文。", "Chúng ta cùng đọc bài khóa."),
        ("问题", "wèntí", "VẤN ĐỀ", "câu hỏi; vấn đề", "我有一个问题。", "Tôi có một câu hỏi."),
        ("考试", "kǎoshì", "KHẢO THÍ", "kỳ thi", "明天有考试。", "Ngày mai có kỳ thi."),
    ],
    "work": [
        ("工作", "gōngzuò", "CÔNG TÁC", "công việc; làm việc", "我在公司工作。", "Tôi làm việc ở công ty."),
        ("公司", "gōngsī", "CÔNG TY", "công ty", "公司离家很近。", "Công ty rất gần nhà."),
        ("同事", "tóngshì", "ĐỒNG SỰ", "đồng nghiệp", "他是我的同事。", "Anh ấy là đồng nghiệp của tôi."),
        ("经理", "jīnglǐ", "KINH LÝ", "quản lý", "经理现在很忙。", "Quản lý hiện đang rất bận."),
        ("开会", "kāihuì", "KHAI HỘI", "họp", "我们下午开会。", "Chiều nay chúng tôi họp."),
        ("电脑", "diànnǎo", "ĐIỆN NÃO", "máy tính", "我的电脑在桌上。", "Máy tính của tôi ở trên bàn."),
        ("电话", "diànhuà", "ĐIỆN THOẠI", "điện thoại", "请给我打电话。", "Hãy gọi điện cho tôi."),
        ("忙", "máng", "MANG", "bận", "今天工作很忙。", "Hôm nay công việc rất bận."),
        ("休息", "xiūxi", "HƯU TỨC", "nghỉ ngơi", "中午休息一个小时。", "Buổi trưa nghỉ một tiếng."),
        ("时间", "shíjiān", "THỜI GIAN", "thời gian", "你有时间吗？", "Bạn có thời gian không?"),
    ],
    "time": [
        ("今天", "jīntiān", "KIM THIÊN", "hôm nay", "今天天气很好。", "Hôm nay thời tiết rất đẹp."),
        ("明天", "míngtiān", "MINH THIÊN", "ngày mai", "明天我去学校。", "Ngày mai tôi đi học."),
        ("昨天", "zuótiān", "TẠC THIÊN", "hôm qua", "昨天我在家。", "Hôm qua tôi ở nhà."),
        ("现在", "xiànzài", "HIỆN TẠI", "bây giờ", "现在几点？", "Bây giờ là mấy giờ?"),
        ("点", "diǎn", "ĐIỂM", "giờ", "现在八点。", "Bây giờ là tám giờ."),
        ("分钟", "fēnzhōng", "PHÂN CHUNG", "phút", "请等五分钟。", "Vui lòng đợi năm phút."),
        ("上午", "shàngwǔ", "THƯỢNG NGỌ", "buổi sáng", "我上午学习汉语。", "Buổi sáng tôi học tiếng Trung."),
        ("下午", "xiàwǔ", "HẠ NGỌ", "buổi chiều", "下午三点见。", "Gặp lúc ba giờ chiều."),
        ("晚上", "wǎnshang", "VÃN THƯỢNG", "buổi tối", "晚上我看书。", "Buổi tối tôi đọc sách."),
        ("星期", "xīngqī", "TINH KỲ", "tuần; thứ", "今天星期几？", "Hôm nay là thứ mấy?"),
    ],
    "numbers": [
        ("一", "yī", "NHẤT", "một", "我有一个朋友。", "Tôi có một người bạn."),
        ("二", "èr", "NHỊ", "hai", "桌上有两本书。", "Trên bàn có hai quyển sách."),
        ("三", "sān", "TAM", "ba", "我买三个苹果。", "Tôi mua ba quả táo."),
        ("四", "sì", "TỨ", "bốn", "我家有四个人。", "Nhà tôi có bốn người."),
        ("五", "wǔ", "NGŨ", "năm", "妹妹五岁。", "Em gái năm tuổi."),
        ("六", "liù", "LỤC", "sáu", "现在六点。", "Bây giờ là sáu giờ."),
        ("七", "qī", "THẤT", "bảy", "一个星期有七天。", "Một tuần có bảy ngày."),
        ("八", "bā", "BÁT", "tám", "我们八点上课。", "Chúng tôi học lúc tám giờ."),
        ("九", "jiǔ", "CỬU", "chín", "他九岁。", "Cậu ấy chín tuổi."),
        ("十", "shí", "THẬP", "mười", "这本书十块钱。", "Quyển sách này mười tệ."),
    ],
}


def curated_recommendations(level: int) -> list[TopicRecommendation]:
    return [
        TopicRecommendation(
            id=topic_id,
            name_vi=name,
            description_vi=description,
            reason_vi=f"Bộ từ đã kiểm duyệt, phù hợp để củng cố nền tảng HSK {level}.",
            level=level,
        )
        for topic_id, name, description in TOPICS
    ]


def curated_session(topic_id: str, level: int, topic_name_vi: str | None = None) -> TopicVocabularySession:
    selected_id = topic_id if topic_id in CURATED_WORDS else "greetings"
    name = topic_name_vi or next(item[1] for item in TOPICS if item[0] == selected_id)
    words = [
        {
            "id": f"word:{hanzi}",
            "hanzi": hanzi,
            "pinyin": pinyin,
            "sino_vietnamese": sino_vietnamese,
            "meaning_vi": meaning_vi,
            "example_zh": example_zh,
            "example_vi": example_vi,
            "is_extension": False,
        }
        for hanzi, pinyin, sino_vietnamese, meaning_vi, example_zh, example_vi in CURATED_WORDS[selected_id]
    ]
    return TopicVocabularySession(
        id=f"{topic_id}-session-1",
        topic_id=topic_id,
        topic_name_vi=name,
        level=level,
        source="curated",
        words=words,
    )
