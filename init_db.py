import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("/app/data/canon.db")

def init_database(db_path=DB_PATH):
    """Initialize the Canon Platform database with all required tables"""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Table 1: projects
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            owner TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    
    # Table 2: canon_entities
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS canon_entities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            name TEXT NOT NULL,
            summary TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
    """)
    
    # Table 3: canon_assertions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS canon_assertions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            entity_id INTEGER NOT NULL,
            assertion_text TEXT NOT NULL,
            scope_label TEXT,
            scope_value TEXT,
            is_invariant INTEGER DEFAULT 0,
            status TEXT DEFAULT 'approved',
            source_ref TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            created_by TEXT,
            parent_assertion_id INTEGER,
            FOREIGN KEY (project_id) REFERENCES projects (id),
            FOREIGN KEY (entity_id) REFERENCES canon_entities (id),
            FOREIGN KEY (parent_assertion_id) REFERENCES canon_assertions (id)
        )
    """)
    
    # Table 4: assertion_history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assertion_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assertion_id INTEGER NOT NULL,
            prior_state TEXT NOT NULL,
            changed_at TEXT NOT NULL DEFAULT (datetime('now')),
            changed_by TEXT,
            FOREIGN KEY (assertion_id) REFERENCES canon_assertions (id)
        )
    """)
    
    # Table 5: relations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS relations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            from_entity INTEGER NOT NULL,
            to_entity INTEGER NOT NULL,
            relation_type TEXT NOT NULL,
            scope_label TEXT,
            scope_value TEXT,
            FOREIGN KEY (project_id) REFERENCES projects (id),
            FOREIGN KEY (from_entity) REFERENCES canon_entities (id),
            FOREIGN KEY (to_entity) REFERENCES canon_entities (id)
        )
    """)
    
    # Table 6: config
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            key TEXT NOT NULL,
            value TEXT,
            FOREIGN KEY (project_id) REFERENCES projects (id),
            UNIQUE (project_id, key)
        )
    """)
    
    conn.commit()
    conn.close()
    
    print(f"Database initialized successfully at {db_path}")
    return True

if __name__ == "__main__":
    # For local testing, use a local path
    local_db = Path("canon_local.db")
    init_database(local_db)
    
    # Verify tables were created
    conn = sqlite3.connect(local_db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"\nTables created: {[t[0] for t in tables]}")
    conn.close()
