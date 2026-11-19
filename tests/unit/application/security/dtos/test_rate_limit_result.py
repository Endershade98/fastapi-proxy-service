# tests/unit/application/security/dtos/test_rate_limit_result.py

from app.application.security.dtos.rate_limit_result import RateLimitResult


def test_rate_limit_result():
    result = RateLimitResult(
        allowed=True,
        limit=100,
        remaining=99,
        retry_after_seconds=0,
        window_seconds=60,
    )

    assert result.allowed is True
    assert result.limit == 100
    assert result.remaining == 99
    assert result.retry_after_seconds == 0
    assert result.window_seconds == 60


def test_rate_limit_result_is_immutable():
    result = RateLimitResult(
        allowed=True,
        limit=100,
        remaining=99,
        retry_after_seconds=0,
        window_seconds=60,
    )

    try:
        result.allowed = False
    except AttributeError:
        pass
    else:
        raise AssertionError("RateLimitResult must be immutable")