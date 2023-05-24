from ..app.app import get_entities, generate_question, generate_multiple_questions, lambda_handler, validate_answer, validate_batch, validate_context, validate_request_body, MAX_CONTEXT_LENGTH, MAX_ANSWER_LENGTH
import pytest

def test_get_entities_valid_entities(sample_sentence_with_entities):
    sentence, expected_entities = sample_sentence_with_entities
    actual_entities = [t.text for t in get_entities(sentence)]
    assert actual_entities == expected_entities

def test_get_entities_no_entities(sample_sentence_no_entities):
    sentence, expected_entities = sample_sentence_no_entities
    actual_entities = [t.text for t in get_entities(sentence)]
    assert actual_entities == expected_entities

def test_validate_context():
    res, _ = validate_context('Something')
    assert res == True
    res, _ = validate_context('')
    assert res == False
    res, _ = validate_context(None)
    assert res == False
    res, _ = validate_context(123)
    assert res == False
    res, _ = validate_context('a'*(MAX_CONTEXT_LENGTH+1))
    assert res == False

def test_validate_answer():
    res, _ = validate_answer('Something')
    assert res == True
    res, _ = validate_answer('')
    assert res == True
    res, _ = validate_answer(None)
    assert res == False
    res, _ = validate_answer(123)
    assert res == False
    res, _ = validate_answer('a'*(MAX_ANSWER_LENGTH+1))
    assert res == False

def test_validate_batch():
    res, _ = validate_batch(None)
    assert res == False
    res, _ = validate_batch(1)
    assert res == False

def test_validate_request_body(valid_request_body_batch, valid_request_body_single, invalid_request_body, invalid_request_body2):
    res, err = validate_request_body(valid_request_body_single)
    assert res == True
    res, err = validate_request_body(valid_request_body_batch)
    assert res == True
    res, err = validate_request_body(invalid_request_body)
    assert res == False
    res, err = validate_request_body(invalid_request_body2)
    assert res == False
    res, err = validate_request_body('sdjs')
    assert res == False

def test_get_multiple_questions_with_entities(sample_sentence_with_entities):
    context, entities = sample_sentence_with_entities
    questions = generate_multiple_questions(context)
    assert len(questions) == len(entities)

def test_get_multiple_questions_no_entities(sample_sentence_no_entities):
    context, _ = sample_sentence_no_entities
    questions = generate_multiple_questions(context)
    assert len(questions) == 1