import os

from dotenv import load_dotenv
import psycopg


load_dotenv()


def get_database_connection():
    """
    Creates and returns a PostgreSQL connection
    to the Supabase database.
    """

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError(
            "DATABASE_URL is not configured."
        )

    return psycopg.connect(database_url)