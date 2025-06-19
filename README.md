# Mini‑TMR Project

A cloud‑native molecule registration system combining AI molecule generation, scoring, and registry with API + dashboard.

## Quickstart (Local, no Docker)

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn api.main:app --reload &
streamlit run dashboard/app.py &
python ingest/generate_and_score.py
```

Open:
- API docs: http://localhost:8000/docs
- Dashboard: http://localhost:8501

## Docker Compose

```bash
docker compose up --build
```

## Environment Variables

- `DATABASE_URL` to point to Postgres (default: sqlite).
- `API_URL` for ingest or dashboard to call backend.