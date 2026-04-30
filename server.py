from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os
from pathlib import Path

app = FastAPI(title="Canon Platform API")

@app.get("/health")
def health():
    return {"status": "healthy", "service": "canon-platform"}

@app.get("/debug/fs")
def debug_filesystem():
    """Verify persistent volume mount"""
    data_dir = Path("/app/data")
    return {
        "data_dir_exists": data_dir.exists(),
        "data_dir_path": str(data_dir),
        "contents": [str(f) for f in data_dir.iterdir()] if data_dir.exists() else []
    }

@app.get("/debug/db")
def debug_database():
    """Verify database state"""
    db_path = Path("/app/data/canon.db")
    return {
        "db_exists": db_path.exists(),
        "db_path": str(db_path),
        "db_size": db_path.stat().st_size if db_path.exists() else 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
