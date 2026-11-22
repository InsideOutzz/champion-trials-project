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