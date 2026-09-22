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
    """Start a Langfuse observation when credentials are configured."""

    if not is_langfuse_available():
        return None

    try:
        client = get_client()

        return client.start_as_current_observation(
            name=name,
            as_type="span",
        )

    except Exception as error:
        print(
            f"Langfuse trace start skipped: {error}"
        )
        return None


def end_trace(
    trace,
    elapsed: float,
) -> None:
    """Record latency and close the Langfuse observation."""

    if trace is None:
        return

    try:
        trace.update(
            metadata={
                "latency_seconds": elapsed,
            }
        )

        trace.end()

    except Exception as error:
        print(
            f"Langfuse trace end skipped: {error}"
        )


def flush_langfuse() -> None:
    """Send pending Langfuse events."""

    if not is_langfuse_available():
        return

    try:
        client = get_client()
        client.flush()

    except Exception as error:
        print(
            f"Langfuse flush skipped: {error}"
        )


def measure_latency(
    start_time: float,
) -> float:
    """Calculate elapsed time in seconds."""

    return round(
        time.perf_counter() - start_time,
        2,
    )