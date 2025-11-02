# MarketPulse

Small full‑stack project that collects market news and stock data, stores them in MongoDB, and serves a frontend (Next.js) that displays the data and performs sentiment analysis using FINBERT.

---

## Repo layout

- `/backend` — FastAPI backend exposing JSON endpoints and reading MongoDB.
- `/frontend` — Next.js + shadcn UI frontend; includes a proxy API route that forwards requests to the backend.
- other scripts for data collection (yfinance, News API, FinBERT analysis) live in the repo root.

