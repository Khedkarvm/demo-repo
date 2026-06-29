import json
from sqlalchemy import create_engine, inspect

DB_URL = "postgresql+psycopg2://postgres:9767@localhost:5433/northwind"
engine = create_engine(DB_URL)
inspector = inspect(engine)

metadata = {}

for table in inspector.get_table_names():
    metadata[table] = {
        col["name"]: str(col["type"])
        for col in inspector.get_columns(table)
    }

with open("northwind_schema.json", "w") as f:
    json.dump(metadata, f, indent=2)

print("Schema saved to northwind_schema.json")
