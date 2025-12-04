from crosscompute_macros.text import phrase_count


def test_phrase_count():
    assert phrase_count(1, 'item') == '1 item'
    assert phrase_count(2, 'item') == '2 items'
    assert phrase_count(2, 'foot', 'feet') == '2 feet'


# ruff: noqa: S101
