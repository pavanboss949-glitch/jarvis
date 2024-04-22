import modules

def test_synonym():
    # Tests for correctly identifying queries that should return synonyms
    assert ('synonym' == modules.process_query('synonyms for happy')[0])
    assert ('synonym' == modules.process_query('give me synonyms of joy')[0])
    assert ('synonym' == modules.process_query('other words for sad')[0])

    # Tests to ensure non-synonym queries are not mistaken
    assert ('synonym' != modules.process_query('define happiness')[0])
    assert ('synonym' != modules.process_query('something random')[0])

    # Specific test cases to check if the synonyms returned are accurate
    # These tests check for specific synonyms being included in the results
    intent, synonyms = modules.process_query('synonyms for love')
    assert ('synonym' == intent)
    assert 'affection' in synonyms
    assert 'devotion' in synonyms

    intent, synonyms = modules.process_query('synonyms for strong')
    assert ('synonym' == intent)
    assert 'powerful' in synonyms
    assert 'sturdy' in synonyms

    # Test for a word with no synonyms
    intent, synonyms = modules.process_query('synonyms for qwertyuiop')
    assert ('synonym' == intent)
    assert synonyms == "No synonyms found."


