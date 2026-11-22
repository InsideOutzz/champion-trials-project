from sqlalchemy import inspect, text
from app.database import engine


def migrate():
    inspector = inspect(engine)

    tables = inspector.get_table_names()

    if "crowd_reports" not in tables:
        raise RuntimeError("crowd_reports table not found.")

    if "users" not in tables:
        raise RuntimeError("users table not found.")

    columns = [
        column["name"]
        for column in inspector.get_columns("crowd_reports")
    ]

    if "user_id" in columns:
        print("user_id already exists. No migration needed.")
        return

    with engine.begin() as connection:
        connection.execute(text(
            "ALTER TABLE crowd_reports "
            "ADD COLUMN user_id INTEGER REFERENCES users(id)"
        ))

    print("Migration successful!")
    print("Existing reports have been preserved.")


if __name__ == "__main__":
    migrate()