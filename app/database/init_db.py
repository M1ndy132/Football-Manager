from app.database.models import Base
from app.database.session import engine


def init_db():
    """Initialize the database by creating all tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

    # Verify tables were created
    from sqlalchemy import inspect

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("📊 Tables in database:", tables)

    return tables


# This allows the function to be imported
if __name__ == "__main__":
    # Add path for direct execution
    import sys
    import os

    sys.path.insert(
        0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
    init_db()
