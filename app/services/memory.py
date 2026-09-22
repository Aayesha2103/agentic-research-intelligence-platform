import json
import os

import redis
from dotenv import load_dotenv

load_dotenv()


def get_redis_client():
    redis_url = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379",
    )

    return redis.from_url(
        redis_url,
        decode_responses=True,
    )


def is_memory_available() -> bool:
    try:
        client = get_redis_client()
        return bool(client.ping())
    except Exception:
        return False


def save_research_result(
    question: str,
    report: str,
) -> bool:
    try:
        client = get_redis_client()

        key = (
            "research:"
            + question.strip().lower()
        )

        data = {
            "question": question,
            "report": report,
        }

        client.set(
            key,
            json.dumps(data),
            ex=60 * 60 * 24 * 7,
        )

        return True

    except Exception as error:
        print(
            f"Redis save skipped: {error}"
        )
        return False


def get_previous_research(
    question: str,
) -> dict | None:
    try:
        client = get_redis_client()

        key = (
            "research:"
            + question.strip().lower()
        )

        value = client.get(key)

        if not value:
            return None

        return json.loads(value)

    except Exception as error:
        print(
            f"Redis read skipped: {error}"
        )
        return None