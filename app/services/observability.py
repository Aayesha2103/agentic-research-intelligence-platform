import os
import time

from dotenv import load_dotenv
from langfuse import get_client

load_dotenv()


def is_langfuse_available() -> bool:
    """Return True when Langfuse credentials are configured."""
    return bool(
        os.getenv("LANGFUSE_PUBLIC_KEY")
        and os.getenv("LANGFUSE_SECRET_KEY")
    )


def start_trace(name: str):
    """Create a Langfuse trace when observability is configured."""
    if not is_langfuse_available():
        return None

    client = get_client()

    return client.trace(
        name=name,
    )


def flush_langfuse() -> None:
    """Send pending Langfuse events."""
    if not is_langfuse_available():
        return

    client = get_client()
    client.flush()


def measure_latency(start_time: float) -> float:
    """Calculate elapsed time in seconds."""
    return round(
        time.perf_counter() - start_time,
        2,
    )