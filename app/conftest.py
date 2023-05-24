import pytest
import json

@pytest.fixture()
def sample_sentence_with_entities():
    sentence = """Arsenal Football Club is an English professional football club based in Islington, London. Arsenal play in the Premier League, the top flight of English football."""
    entities = ["Arsenal Football Club", "English", "Islington", "London", "the Premier League"]
    return sentence, entities

@pytest.fixture()
def sample_sentence_no_entities():
    sentence = "Let's go for a walk."
    entities = []
    return sentence, entities

@pytest.fixture()
def valid_request_body_batch():
    body = {
        "ans" : '',
        "cnt" : 'Some text',
        "batch" : True
    }
    return json.dumps(body)

@pytest.fixture()
def valid_request_body_single():
    body = {
        "ans" : 'hello',
        "cnt" : 'Some text',
        "batch" : False
    }
    return json.dumps(body)

@pytest.fixture()
def invalid_request_body():
    body = {
        "ans" : '',
        "cnt" : 'Some text',
        "batch" : False
    }
    return json.dumps(body)

@pytest.fixture()
def invalid_request_body2():
    body = {
        "ans" : 'hello',
        "cnt" : 'Some text'
    }
    return json.dumps(body)