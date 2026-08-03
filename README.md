# HSK Learning

Nền tảng học HSK 1–6 dành cho người Việt. Người học có thể bắt đầu HSK 1 ngay hoặc làm bài
kiểm tra đầu vào tùy chọn, sau đó học theo lộ trình mỗi ngày gồm 5 bài và tiếp tục ngày kế tiếp
sau khi hoàn thành checkpoint.

## Production

- Website: [frontend-three-theta-34.vercel.app](https://frontend-three-theta-34.vercel.app)
- API: [hsk-learning-api.vercel.app](https://hsk-learning-api.vercel.app/api/health)
- API docs: [hsk-learning-api.vercel.app/api/docs](https://hsk-learning-api.vercel.app/api/docs)
- Database: Neon PostgreSQL Free, Singapore (`sin1`)

## Tính năng hiện có

- Lộ trình AI tăng dần từ HSK 1 đến HSK 6, mỗi ngày 5 bài và một checkpoint.
- Kiểm tra đầu vào thích ứng 20 câu về từ vựng, ngữ pháp, nghe và phát âm; đề xuất HSK 1–6,
  lưu lượt đang làm và cho phép thi lại sau 30 ngày mà không ảnh hưởng tiến độ.
- Hội thoại có âm thanh từng câu; bật/tắt Pinyin và bản dịch tiếng Việt.
- Flashcard và ôn tập ngắt quãng bằng câu hỏi 4 đáp án.
- Bài nghe chọn đáp án và sắp xếp từ thành câu.
- Thu âm, nghe lại và phân tích phát âm AI theo âm tiết/thanh điệu.
- Sổ từ cá nhân, ôn câu sai và theo dõi tiến độ từng bài.
- Chuỗi ngày học, hoạt động 7 ngày, tỷ lệ ghi nhớ 30 ngày và gợi ý học tiếp.
- Tài khoản riêng, đồng bộ tiến độ trên server và phiên đăng nhập có thể thu hồi.
- Kiểm tra chất lượng, phát hiện nội dung AI trùng lặp và giới hạn chi phí theo ngày.
- Trang quản trị để xem usage, sửa, duyệt hoặc từ chối bài AI.

## Kiến trúc

| Thành phần | Công nghệ | Trách nhiệm |
|---|---|---|
| Frontend | Angular 21, TypeScript, SCSS | Giao diện học, ôn tập, analytics và quản trị |
| Backend | FastAPI, Python 3.12 | API, xác thực, lộ trình, AI và kiểm tra chất lượng |
| Production database | Neon PostgreSQL | Tài khoản, session, tiến độ, lộ trình và AI usage |
| Local/test database | SQLite | Chạy local và kiểm thử không cần dịch vụ ngoài |
| AI | OpenAI API | Sinh lộ trình, chuyển giọng nói, phát âm và audio mẫu |
| Hosting | Hai Vercel projects | Deploy frontend/backend độc lập |

```text
frontend/   Angular SPA
backend/    FastAPI application và tests
docs/       Vision, PRD, specs, ADR, UX và architecture
```

## Yêu cầu môi trường

- Node.js `^20.19.0`, `^22.12.0` hoặc `^24.0.0`.
- npm 10+.
- Python 3.12.

## Chạy local

### 1. Cấu hình backend

```powershell
Copy-Item .env.example backend/.env
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[test]"
```

Có thể để trống `OPENAI_API_KEY`; hệ thống vẫn chạy với nội dung fallback. Khi không có
`DATABASE_URL`, backend tự dùng `backend/data/hsk_learning.sqlite3`.

### 2. Chạy FastAPI

```powershell
cd backend
.\.venv\Scripts\python.exe -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

- Health: [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)
- API docs: [http://127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs)

### 3. Chạy Angular

Mở terminal khác:

```powershell
cd frontend
npm ci
npm start -- --host 127.0.0.1 --port 4200
```

Mở [http://127.0.0.1:4200/auth](http://127.0.0.1:4200/auth). Proxy Angular chuyển `/api`
tới backend tại port 8000.

## Biến môi trường

Các biến backend nằm trong `backend/.env`; không đặt API key trong frontend.

| Biến | Bắt buộc | Mô tả |
|---|---:|---|
| `OPENAI_API_KEY` | Không | API key phía server; thiếu key sẽ dùng fallback |
| `OPENAI_MODEL` | Không | Model tạo nội dung AI dạng văn bản (mặc định `gpt-4.1-mini`) |
| `OPENAI_TRANSCRIPTION_MODEL` | Không | Chuyển giọng nói tiếng Trung thành văn bản |
| `OPENAI_AUDIO_MODEL` | Không | Phân tích âm thanh/phát âm |
| `OPENAI_SPEECH_MODEL` | Không | Sinh audio mẫu (mặc định `tts-1-hd`; giọng thiết bị chỉ dùng khi API lỗi) |
| `OPENAI_DAILY_PATH_TIMEOUT_SECONDS` | Không | Timeout khi tạo lộ trình |
| `AI_ACCOUNT_DAILY_LIMIT` | Không | Giới hạn lượt tạo AI mỗi tài khoản/ngày |
| `AI_SYSTEM_DAILY_LIMIT` | Không | Giới hạn lượt tạo AI toàn hệ thống/ngày |
| `ADMIN_EMAILS` | Không | Danh sách email admin, ngăn cách bằng dấu phẩy |
| `ALLOWED_ORIGINS` | Có ở production | Danh sách frontend origin được phép gọi API |
| `DATABASE_URL` | Có ở production | PostgreSQL pooled connection string |
| `API_BASE_URL` | Có khi build frontend | URL backend, không có dấu `/` cuối |
| `TELEGRAM_BOT_TOKEN` | Có khi bật nhắc | Token bot từ `@BotFather` |
| `TELEGRAM_CHAT_ID` | Có khi bật nhắc | Chat ID nhận thông báo |
| `TELEGRAM_ACCOUNT_EMAIL` | Có khi bật nhắc | Email tài khoản học được theo dõi |
| `TELEGRAM_TIMEZONE` | Không | Múi giờ nhắc, mặc định `Asia/Ho_Chi_Minh` |
| `CRON_SECRET` | Có khi bật nhắc | Khóa bảo vệ endpoint cron; GitHub Actions gửi qua Bearer token |

Ví dụ cấp quyền quản trị:

```dotenv
ADMIN_EMAILS=binhqd@vnpt.vn
```

Tài khoản phải đăng xuất và đăng nhập lại sau khi email được thêm vào danh sách admin.

### Bật bot Telegram nhắc tiến độ

1. Tạo bot với `@BotFather`, lưu token vào `TELEGRAM_BOT_TOKEN`.
2. Gửi một tin nhắn cho bot, gọi
   `https://api.telegram.org/bot<TOKEN>/getUpdates`, rồi lấy `message.chat.id` làm
   `TELEGRAM_CHAT_ID`.
3. Đặt `TELEGRAM_ACCOUNT_EMAIL` bằng email tài khoản HSK Learning cần theo dõi và tạo
   một `CRON_SECRET` ngẫu nhiên, dài.
4. Thêm cùng giá trị `CRON_SECRET` vào GitHub Actions secret của repository và deploy lại
   backend. Workflow gọi endpoint mỗi giờ từ 18:00–23:00 theo giờ Việt Nam, lặp lại khi
   Ngày hiện tại chưa hoàn thành.

Bot gửi thông báo hoàn thành ngay khi Ngày hiện tại chuyển sang đủ 5 bài, phiên từ vựng
theo chủ đề và checkpoint. Lỗi kết nối Telegram không chặn việc lưu tiến độ học.

## Kiểm thử

Backend:

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -q
```

PostgreSQL integration test dùng `TEST_POSTGRES_URL` trỏ tới database test riêng:

```powershell
$env:TEST_POSTGRES_URL='postgresql://user:password@127.0.0.1:5432/hsk_test'
.\.venv\Scripts\python.exe -m pytest -q tests/test_postgres_repository.py
```

Frontend:

```powershell
cd frontend
npx ng test --watch=false
npm run build
```

E2E:

```powershell
cd frontend
$env:PYTHON = (Resolve-Path '..\backend\.venv\Scripts\python.exe')
npm run e2e
```

Kết quả xác minh gần nhất: 52 backend tests và 71 frontend tests đạt; Angular production build
thành công.

## Deploy Vercel

Repository dùng hai Vercel projects trong cùng monorepo.

### Backend — `hsk-learning-api`

1. Root Directory: `backend`.
2. Framework Preset: FastAPI.
3. Kết nối Neon PostgreSQL Marketplace với environment production.
4. Cấu hình `OPENAI_API_KEY`, `ADMIN_EMAILS` và `ALLOWED_ORIGINS`.
5. `backend/vercel.json` đặt FastAPI Function tại `sin1`, gần Neon database.
6. Deploy và kiểm tra `/api/health`.

```powershell
cd backend
npx vercel --prod
```

### Frontend — `frontend`

1. Root Directory: `frontend`.
2. Framework Preset: Angular.
3. Đặt `API_BASE_URL=https://hsk-learning-api.vercel.app`.
4. Deploy frontend.
5. Đưa domain frontend vào `ALLOWED_ORIGINS` của backend và redeploy backend.

```powershell
cd frontend
npx vercel --prod
```

Không dùng SQLite hoặc `/tmp` để lưu tài khoản production. Không dùng wildcard CORS khi website
có xác thực người dùng.

## Tài liệu dự án

- [Product Vision](docs/business/Vision.md)
- [PRD](docs/business/PRD.md)
- [Architecture](docs/architecture/Architecture.md)
- [ADR index](docs/adr/DECISIONS.md)
- [PostgreSQL production ADR](docs/adr/2026-07-31-postgresql-production-persistence.md)
- [Learning intelligence specification](docs/specs/learning-intelligence-operations/Specification.md)

## Tài liệu tham khảo

- [Angular deployment](https://angular.dev/tools/cli/deployment)
- [FastAPI deployment](https://fastapi.tiangolo.com/deployment/)
- [FastAPI on Vercel](https://vercel.com/docs/frameworks/backend/fastapi)
- [Vercel monorepos](https://vercel.com/docs/monorepos)
- [Vercel Function regions](https://vercel.com/docs/functions/configuring-functions/region)
- [PostgreSQL on Vercel](https://vercel.com/docs/postgres)
- [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
