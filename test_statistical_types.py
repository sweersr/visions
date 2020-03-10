import pytest

from visions_statistical import series_nominal2, visions_nominal


@pytest.mark.parametrize("series,type",[
    (series_nominal2, visions_nominal),
    (series_nominal2, visions_nominal),
    (series_nominal2, visions_nominal),
])
def test_contains(series, type):
    assert series in type

