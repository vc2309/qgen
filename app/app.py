import torch
from transformers import AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq, Seq2SeqTrainingArguments, Seq2SeqTrainer
from transformers import AutoTokenizer
import spacy
import logging
import json

print("Loading model...")
model_path = '/opt/ml/model'
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
model_checkpoint = "t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
print("Model load complete.")

def run_model(input_string, model, tokenizer, device, **generator_args):
    input_ids = tokenizer.encode(input_string, return_tensors="pt").to(torch.device(device))
    res = model.generate(
        input_ids, **generator_args)
    output = tokenizer.batch_decode(res, skip_special_tokens=True)
    return output

def get_entities(text):
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

def lambda_handler(event, context):
    print(f"Function Invoked. Event : {event}")
    body = json.loads(event.get('body'))
    try:
        ans = body.get("ans")
        cnt = body.get("cnt")
        questions =  generate_question(cnt, ans)
        response_body = {
            "questions" : questions
        }

        return {
            "statusCode" : 200,
            "body" : json.dumps(response_body),
            "headers" : {
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        error_body = {
            "error" : f"Excpetion occured while generating questions : {e}"
        }
        return {
            "status" : 500,
            "body" : json.dumps(error_body),
            "headers" : {
                'Content-Type': 'application/json'
            }   
        }