import time
from typing import Callable, Any


def retry(
    operation: Callable[[], Any],
    attempts: int = 3,
    delay: float = 2.0,
) -> Any:
    """
    Executes an operation and retries temporary failures.

    Quota and permission errors are not retried because
    repeating the same request cannot resolve them.
    """

    last_error = None

    for attempt in range(1, attempts + 1):

        try:
            return operation()

        except Exception as error:

            last_error = error

            error_message = str(error).lower()

            # ------------------------------------------
            # Do not retry quota / permission errors
            # ------------------------------------------

            non_retryable_messages = [
                "usage limit",
                "quota",
                "forbidden",
                "plan's set usage limit",
                "upgrade your plan",
            ]

            if any(
                message in error_message
                for message in non_retryable_messages
            ):

                print(
                    "Non-retryable error detected:"
                )

                print(error)

                raise

            # ------------------------------------------
            # Retry temporary failures
            # ------------------------------------------

            print(
                f"Attempt {attempt}/{attempts} failed: "
                f"{error}"
            )

            if attempt < attempts:
                time.sleep(delay)

    raise last_error