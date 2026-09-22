from app.utils.retry import retry


def test_retry():

    attempts = []

    def operation():

        attempts.append(1)

        if len(attempts) < 3:
            raise ValueError("Temporary failure")

        return "success"

    result = retry(
        operation,
        attempts=3,
        delay=0
    )

    assert result == "success"
    assert len(attempts) == 3

    print()
    print("Retry test successful.")
    print("Attempts:", len(attempts))