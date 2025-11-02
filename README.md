# MarketPulse

Small full‑stack project that collects market news and stock data, stores them in MongoDB, and serves a frontend (Next.js) that displays the data and performs sentiment analysis.

---

## Repo layout

- `/backend` — FastAPI backend exposing JSON endpoints and reading MongoDB.
- `/frontend` — Next.js + shadcn UI frontend; includes a proxy API route that forwards requests to the backend.
- other scripts for data collection (yfinance, News API, FinBERT analysis) live in the repo root.

---

## Requirements (macOS)

- Python 3.10+ (3.11 / 3.12 / 3.13 tested)
- Node.js 18+ and npm (or pnpm/yarn)
- MongoDB instance (Atlas or local)
- (Optional) Hugging Face token if using private models

---

## Environment variables

Create a `.env` (backend) and `.env.local` (frontend) with at least:

Backend (`/Users/tudornitu/marketpulse/.env`)

```
MONGODB_URI=mongodb+srv://<user>:<pass>@cluster.example.mongodb.net/?retryWrites=true&w=majority
NEWS_API_KEY=your_news_api_key_here
HF_TOKEN=your_hf_token_if_needed
```

Frontend (`/Users/tudornitu/marketpulse/frontend/.env.local`)

```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000   # optional if using direct calls
```

Do not commit `.env` files with secrets.

---

## Backend — FastAPI

1. Create & activate venv (recommended)

```bash
cd /Users/tudornitu/marketpulse
python -m venv .venv-backend
source .venv-backend/bin/activate
```

2. Install dependencies

```bash
pip install -U pip
pip install fastapi uvicorn pymongo python-dotenv certifi
```

3. Run the backend:

```bash
uvicorn backend.main:app --reload --port 8000
```

Endpoints

- GET /api/news?limit=50&skip=0 — list news (sorted by date desc)
- GET /api/news/{id} — get single article
- GET /api/stocks?symbol=AAPL&limit=100 — list stock rows

Notes

- Backend converts ObjectId -> string and datetimes -> ISO strings.
- CORS is configured to allow `http://localhost:3000` by default.

---

## Frontend — Next.js

1. Install deps

```bash
cd /Users/tudornitu/marketpulse/frontend
npm install
# if you hit peer dependency conflicts, use:
# npm install --legacy-peer-deps
```

2. Start dev server

```bash
npm run dev
# Open http://localhost:3000
```

Integration options

- Proxy (recommended): The Next API route at `/app/api/news/route.ts` forwards requests to the backend. Call `/api/news` from client code.
- Direct: Call FastAPI directly from client (ensure backend CORS allows your origin and set NEXT_PUBLIC_BACKEND_URL).

Example client fetch helper

```js
// frontend/src/lib/api.ts
export async function fetchNews(limit = 50) {
  const res = await fetch(`/api/news?limit=${limit}`);
  if (!res.ok) throw new Error("Failed to fetch news");
  return res.json();
}
```

---

## Sentiment analysis (FinBERT)

- Script(s) use transformers and a FinBERT model. If you use a private HF model set `HF_TOKEN` in backend `.env`.
- Typical dependencies: `transformers`, `torch`, `numpy`, `pandas`, `tqdm`.
- Sentiment tasks usually run offline (batch update DB documents with sentiment fields).

---

## Common issues & troubleshooting

- ModuleNotFoundError: No module named 'bson'  
  Install `pymongo` in the same environment running uvicorn:

  ```
  pip install pymongo
  ```

- npm ERESOLVE dependency errors  
  Either remove/replace the incompatible dependency (e.g. `vaul`) in `frontend/package.json`, or install with:

  ```
  npm install --legacy-peer-deps
  ```

- CSV encoding problems when importing data  
  Use `encoding='utf-8'` with a fallback to `latin-1`, or detect encoding with `chardet`.

- MongoDB documents must have string keys  
  Ensure pandas DataFrame columns are flattened (no tuple column names) and Timestamps converted to datetimes before inserting into MongoDB.

---

## Development workflow

1. Start MongoDB (Atlas or local).
2. Start backend:
   ```
   source .venv-backend/bin/activate
   uvicorn backend.main:app --reload --port 8000
   ```
3. Start frontend:
   ```
   cd frontend
   npm run dev
   ```
4. Open browser: http://localhost:3000

---

## Contributing

- Open issues for bugs or feature requests.
- Follow standard GitHub flow: branch -> PR -> review -> merge.

---

## License

Add a LICENSE file suitable for the project (e.g., MIT).

---

If you want, apply this README to the repository or tell me which sections to expand (deployment, tests, CI, sample requests).// filepath: /Users/tudornitu/marketpulse/README.md

# MarketPulse

Small full‑stack project that collects market news and stock data, stores them in MongoDB, and serves a frontend (Next.js) that displays the data and performs sentiment analysis.

---

## Repo layout

- `/backend` — FastAPI backend exposing JSON endpoints and reading MongoDB.
- `/frontend` — Next.js + shadcn UI frontend; includes a proxy API route that forwards requests to the backend.
- other scripts for data collection (yfinance, News API, FinBERT analysis) live in the repo root.

---

## Requirements (macOS)

- Python 3.10+ (3.11 / 3.12 / 3.13 tested)
- Node.js 18+ and npm (or pnpm/yarn)
- MongoDB instance (Atlas or local)
- (Optional) Hugging Face token if using private models

---

## Environment variables

Create a `.env` (backend) and `.env.local` (frontend) with at least:

Backend (`/Users/tudornitu/marketpulse/.env`)

```
MONGODB_URI=mongodb+srv://<user>:<pass>@cluster.example.mongodb.net/?retryWrites=true&w=majority
NEWS_API_KEY=your_news_api_key_here
HF_TOKEN=your_hf_token_if_needed
```

Frontend (`/Users/tudornitu/marketpulse/frontend/.env.local`)

```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000   # optional if using direct calls
```

Do not commit `.env` files with secrets.

---

## Backend — FastAPI

1. Create & activate venv (recommended)

```bash
cd /Users/tudornitu/marketpulse
python -m venv .venv-backend
source .venv-backend/bin/activate
```

2. Install dependencies

```bash
pip install -U pip
pip install fastapi uvicorn pymongo python-dotenv certifi
```

3. Run the backend:

```bash
uvicorn backend.main:app --reload --port 8000
```

Endpoints

- GET /api/news?limit=50&skip=0 — list news (sorted by date desc)
- GET /api/news/{id} — get single article
- GET /api/stocks?symbol=AAPL&limit=100 — list stock rows

Notes

- Backend converts ObjectId -> string and datetimes -> ISO strings.
- CORS is configured to allow `http://localhost:3000` by default.

---

## Frontend — Next.js

1. Install deps

```bash
cd /Users/tudornitu/marketpulse/frontend
npm install
# if you hit peer dependency conflicts, use:
# npm install --legacy-peer-deps
```

2. Start dev server

```bash
npm run dev
# Open http://localhost:3000
```

Integration options

- Proxy (recommended): The Next API route at `/app/api/news/route.ts` forwards requests to the backend. Call `/api/news` from client code.
- Direct: Call FastAPI directly from client (ensure backend CORS allows your origin and set NEXT_PUBLIC_BACKEND_URL).

Example client fetch helper

```js
// frontend/src/lib/api.ts
export async function fetchNews(limit = 50) {
  const res = await fetch(`/api/news?limit=${limit}`);
  if (!res.ok) throw new Error("Failed to fetch news");
  return res.json();
}
```

---

## Sentiment analysis (FinBERT)

- Script(s) use transformers and a FinBERT model. If you use a private HF model set `HF_TOKEN` in backend `.env`.
- Typical dependencies: `transformers`, `torch`, `numpy`, `pandas`, `tqdm`.
- Sentiment tasks usually run offline (batch update DB documents with sentiment fields).

---

## Common issues & troubleshooting

- ModuleNotFoundError: No module named 'bson'  
  Install `pymongo` in the same environment running uvicorn:

  ```
  pip install pymongo
  ```

- npm ERESOLVE dependency errors  
  Either remove/replace the incompatible dependency (e.g. `vaul`) in `frontend/package.json`, or install with:

  ```
  npm install --legacy-peer-deps
  ```

- CSV encoding problems when importing data  
  Use `encoding='utf-8'` with a fallback to `latin-1`, or detect encoding with `chardet`.

- MongoDB documents must have string keys  
  Ensure pandas DataFrame columns are flattened (no tuple column names) and Timestamps converted to datetimes before inserting into MongoDB.

---

## Development workflow

1. Start MongoDB (Atlas or local).
2. Start backend:
   ```
   source .venv-backend/bin/activate
   uvicorn backend.main:app --reload --port 8000
   ```
3. Start frontend:
   ```
   cd frontend
   npm run dev
   ```
4. Open browser: http://localhost:3000

---

## Contributing

- Open issues for bugs or feature requests.
- Follow standard GitHub flow: branch -> PR -> review -> merge.

---

## License

Add a LICENSE file suitable for the project (e.g., MIT).

---

If you want, apply this README to the repository or tell me which sections to expand (deployment, tests, CI, sample requests).
