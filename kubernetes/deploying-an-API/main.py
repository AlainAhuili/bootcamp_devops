import os
import random
from fastapi import FastAPI
from pydantic import BaseModel

server = FastAPI(title='My API')

@server.get('/status')
async def get_status():
    return {"status": 1}

@server.get('/environment')
async def get_environment():
    # Looks for variables set by Kubernetes ConfigMaps/Secrets
    env_type = os.environ.get('ENVIRONMENT_TYPE', 'unknown')
    return {"environment": env_type}

class Sentence(BaseModel):
    sentence: str = 'hello world'
    language: str = 'en'

class PredictedSentence(Sentence):
    score: float = 0.0

@server.post('/predict', response_model=PredictedSentence)
async def post_sentence(sentence: Sentence):
    return PredictedSentence(
        sentence=sentence.sentence,
        language=sentence.language,
        score=random.uniform(0, 1)
    )
