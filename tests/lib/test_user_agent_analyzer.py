import pytest

from app.lib.user_agent_analyzer import is_browser_supported


@pytest.mark.parametrize(
    ('input', 'output'),
    [
        (
            # Old Chrome version
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.104 Safari/537.36',
            False,
        ),
        (
            # Old Firefox version
            'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/78.0',
            False,
        ),
        (
            'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
            True,
        ),
        (
            'Unknown-User-Agent',
            True,
        ),
        (
            '',
            True,
        ),
    ],
)
def test_is_browser_supported(input, output):
    assert is_browser_supported(input) == output