import modules


def test_aq():
    assert ('aq' == modules.process_query('Give me the aq of London,GB')[0])
    assert ('aq' == modules.process_query('aq of Paris,FR')[0])
    assert ('aq' == modules.process_query('What\'s the aq of US')[0])
    assert ('aq' != modules.process_query('How was your day in london')[0])
    assert ('aq' != modules.process_query('Tell me about the aquarium in CH!')[0])
