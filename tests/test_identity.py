from erasmus.population import population


def test_scalar():
    p = population(None)
    assert(p)