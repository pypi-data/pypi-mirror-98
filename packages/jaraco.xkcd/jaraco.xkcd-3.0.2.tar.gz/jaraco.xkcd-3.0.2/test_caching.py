import pytest
from jaraco import xkcd
from tempora import timing


@pytest.fixture
def fresh_cache(tmpdir, monkeypatch):
    adapter = xkcd.session.get_adapter('http://')
    cache = xkcd.make_cache(tmpdir / 'xkcd')
    monkeypatch.setattr(adapter, 'cache', cache)
    monkeypatch.setattr(adapter.controller, 'cache', cache)


def test_requests_cached(fresh_cache):
    """
    A second pass loading Comics should be substantially faster than the
    first.
    """
    latest = xkcd.Comic.latest()
    last_100_ns = list(range(latest.number, latest.number - 100, -1))

    with timing.Stopwatch() as first_load:
        list(map(xkcd.Comic, last_100_ns))

    with timing.Stopwatch() as second_load:
        list(map(xkcd.Comic, last_100_ns))

    assert second_load.elapsed < first_load.elapsed / 2
