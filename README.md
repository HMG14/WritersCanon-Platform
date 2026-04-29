# Canon Platform

A canon governance system for multi-season storytelling projects.

## Tech Stack

- FastAPI
- SQLite (persistent volume)
- Railway deployment

## Local Development

```bash
pip install -r requirements.txt
python server.py
```

## Endpoints

- GET /health - Health check
- GET /debug/fs - Verify volume mount
- GET /debug/db - Verify database state
