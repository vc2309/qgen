FROM public.ecr.aws/lambda/python:3.9

COPY requirements.txt ./
RUN python3.9 -m pip install -r requirements.txt -t .

RUN mkdir /tmp/.transformers
ENV TRANSFORMERS_CACHE /tmp/.transformers

COPY app.py ./
COPY checkpoint-11000 /opt/ml/model
ENV MODEL_PATH /opt/ml/model

RUN python -m spacy download en_core_web_sm

CMD ["app.lambda_handler"]
