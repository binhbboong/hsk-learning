# HSK Learning

## Tài khoản người học

Mở [http://127.0.0.1:4204/auth](http://127.0.0.1:4204/auth) để đăng ký hoặc đăng nhập. Mỗi tài
khoản có tiến độ, chuỗi ngày, lịch ôn, câu sai và sổ từ riêng. Dữ liệu tài khoản local được lưu
trong `backend/data/hsk_learning.sqlite3`; không commit file database này.

Website học HSK 1-6 cho người Việt, bắt đầu bằng bốn dạng bài HSK 1: từ vựng flip-card,
ngữ pháp tương tác, nghe hiểu và luyện phát âm có ghi/nghe lại cục bộ. Frontend dùng Angular,
API dùng FastAPI. Khi có OpenAI API key, backend có thể tạo bài từ vựng theo schema; nếu
thiếu key hoặc dịch vụ lỗi, hệ thống tự dùng bài HSK 1 mặc định.

## Cấu trúc

- `frontend/`: Angular 21 SPA, unit tests bằng Vitest và E2E bằng Playwright.
- `backend/`: FastAPI, vocabulary/skill lesson contracts, OpenAI adapter và fallback đã kiểm soát.
- `docs/`: Vision, PRD, persona, UX, specification, plan, tasks, ADR và architecture.

## Yêu cầu môi trường

- Node.js `^20.19.0`, `^22.12.0` hoặc `^24.0.0` (project hiện được kiểm chứng với Node
  22.14).
- npm 10+.
- Python 3.12.

## Chạy local

### 1. Chạy FastAPI

Mở terminal thứ nhất tại repository:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[test]"
python -m uvicorn app:app --reload --port 8000
```

Kiểm tra API tại `http://localhost:8000/api/health` và tài liệu API tại
`http://localhost:8000/api/docs`.

Không cần API key để chạy local. Backend sẽ trả bài fallback hoàn chỉnh.

### 2. Chạy Angular

Mở terminal thứ hai:

```powershell
cd frontend
npm ci
npm start
```

Mở `http://localhost:4200`. Angular development server chuyển tiếp `/api` sang FastAPI ở
port 8000.

## Bật bài học AI

Sao chép `.env.example` thành `backend/.env`, sau đó điền:

```dotenv
OPENAI_API_KEY=your-server-side-key
OPENAI_MODEL=gpt-5.6
OPENAI_TIMEOUT_SECONDS=15
ALLOWED_ORIGINS=http://localhost:4200
```

Không dùng tiền tố public cho API key và không đặt key trong `frontend/`. File `.env` đã
được gitignore.

## Kiểm thử

Backend:

```powershell
cd backend
python -m pytest
```

Frontend unit tests và production build:

```powershell
cd frontend
npm test -- --watch=false
npm run build
```

E2E tự chạy FastAPI ở port 8010 và Angular ở port 4200:

```powershell
cd frontend
$env:PYTHON = (Resolve-Path '..\backend\.venv\Scripts\python.exe')
npm run e2e
```

## Deploy lên Vercel

Repository dùng hai Vercel project từ cùng một monorepo để frontend và backend build độc lập.

### Backend project

1. Import repository vào Vercel.
2. Chọn Root Directory là `backend`.
3. Vercel tự nhận FastAPI từ `backend/app.py`; Python được pin ở 3.12.
4. Thêm các environment variables phía server:
   - `OPENAI_API_KEY` (tùy chọn; không có thì dùng fallback).
   - `OPENAI_MODEL` (mặc định `gpt-5.6`).
   - `OPENAI_TIMEOUT_SECONDS` (mặc định `15`).
   - `ALLOWED_ORIGINS` (URL frontend, nhiều URL ngăn cách bằng dấu phẩy).
5. Deploy và kiểm tra `https://<backend-domain>/api/health`.

### Frontend project

1. Import cùng repository thành project thứ hai.
2. Chọn Root Directory là `frontend` và Framework Preset là Angular.
3. Thêm environment variable công khai:
   - `API_BASE_URL=https://<backend-domain>` (không có dấu `/` cuối).
4. Deploy. `frontend/vercel.json` giữ các route `/lesson`, `/study` và `/results` hoạt động
   sau khi refresh.
5. Cập nhật `ALLOWED_ORIGINS` của backend bằng domain frontend thực tế và redeploy backend.

Với preview deployments, thêm từng frontend preview origin cần dùng vào `ALLOWED_ORIGINS`.
Không đặt wildcard origin khi bật dữ liệu người dùng hoặc authentication trong tương lai.

## Tài liệu nguồn chính thức

- Angular version compatibility: https://angular.dev/reference/versions
- Angular deployment: https://angular.dev/tools/cli/deployment
- FastAPI deployment: https://fastapi.tiangolo.com/deployment/
- FastAPI on Vercel: https://vercel.com/docs/frameworks/backend/fastapi
- Vercel monorepos: https://vercel.com/docs/monorepos
- Vercel SPA rewrites: https://vercel.com/kb/guide/why-is-my-deployed-project-giving-404
- OpenAI structured outputs: https://developers.openai.com/api/docs/guides/structured-outputs
