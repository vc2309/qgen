import torch
from transformers import AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq, Seq2SeqTrainingArguments, Seq2SeqTrainer
from transformers import AutoTokenizer
import spacy
import logging
import json
import os
from typing import Tuple, Optional, List
Token = spacy.tokens.span.Span

print("Loading model...")
model_path = os.getenv("MODEL_PATH")
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
model_checkpoint = "t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
MAX_CONTEXT_LENGTH = 2500
MAX_ANSWER_LENGTH = 150
print("Model load complete.")

def run_model(input_string, model, tokenizer, device, **generator_args):
    input_ids = tokenizer.encode(input_string, return_tensors="pt").to(torch.device(device))
    res = model.generate(
        input_ids, **generator_args)
    output = tokenizer.batch_decode(res, skip_special_tokens=True)
    return output

def get_entities(text : str) -> List[Token]:
    seen = set()
    entities = []
    spacy_nlp = spacy.load('en_core_web_sm')
    for entity in spacy_nlp(text).ents:
        if entity.text not in seen:
            seen.add(entity.text)
            entities.append(entity)
    return sorted(entities, key=lambda e: e.text)


def generate_question(context, answer):
    return run_model(f"generate question: {answer} context: {context}", model, tokenizer, 'cpu', max_length=50)

def generate_multiple_questions(context : str) -> List[str]:
    entities = [t.text for t in get_entities(context)]
    entities = entities if entities else entities+[''] #We can provide a basic response in case no entities are found
    questions = []
    for entity in entities:
        question = generate_question(context=context, answer=entity)
        if question:
            questions.append(question[0])
    return questions

def validate_context(cnt : str) -> Tuple[bool, str]:
    if not cnt:
        return False, 'Context cannot be empty.'
    if type(cnt) != str:
        return False, 'Context must be a string.'
    if len(cnt) > MAX_CONTEXT_LENGTH:
        return False, "Maximum context length is 2500 characters."
    
    return True, ''

def validate_answer(ans : str) -> Tuple[bool, str]:
    if type(ans) != str:
        return False, 'Answer must be a string'
    if len(ans) > MAX_ANSWER_LENGTH:
        return False, "Maximum answer length is 150 characters."
    return True, ''

def validate_batch(batch : bool) -> Tuple[bool, str]:
    if type(batch) != bool:
        return False, "Batch must be a boolean."
    return True, ''    

def validate_request_body(body : str) -> Tuple[bool, str]:
    body_dict = {}
    try:
        body_dict = json.loads(body)
    except Exception as e:
        return False, f'Malformed request body. Exception ocurred : {e}'
    
    cnt, ans, batch = body_dict.get('cnt'), body_dict.get('ans'), body_dict.get('batch')
    if not ans and not batch:
        return False, 'No answer provided for a single-mode query.'
    
    res, err = validate_context(cnt)
    if not res:
        return False, err
    if ans:
        res, err = validate_answer(ans)
        if not res:
            return False, err
    res, err = validate_batch(batch)
    if not res:
        return False, err
    return True, ''

def create_response(response_body : dict, status_code : int) -> dict:
    return {
            "statusCode" : status_code,
            "body" : json.dumps(response_body),
            "headers" : {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': '*',
                'Accept' : '*/*'
            }
    }

def lambda_handler(event, context):
    print(f"Function Invoked. Event : {event}")
    body = event.get('body')
    res, err = validate_request_body(body)
    response_body, status_code = {}, 200
    if not res:
        print(f"Invalid request body. err {err}")
        response_body = {"error" : err}
        status_code = 400
    else:
        body = json.loads(body)
        try:
            ans = body.get("ans")
            cnt = body.get("cnt")
            batch = body.get("batch")
            if batch == True:
                questions = generate_multiple_questions(cnt)
            else:
                questions =  generate_question(cnt, ans)
            
            response_body = {
                "questions" : questions
            }
            status_code = 200
        except Exception as e:
            response_body = {
                "error" : f"Exception occured while generating questions : {e}"
            }
            status_code = 500
    response = create_response(response_body, status_code)
    print(response)
    return response