import openai
import os

DEFAULT_EMBEDDING_MODEL = 'text-embedding-ada-002'
DEFAULT_COMPLETION_MODEL = 'text-davinci-003'
DEFAULT_TEMPERATURE = 0
DEFAULT_MAX_TOKENS = 1024
DEFAULT_EMBEDDING_CHUNK = 1000

openai.api_key = os.getenv('OPENAI_API_KEY')

def get_embeddings(docs, model = DEFAULT_EMBEDDING_MODEL, chunk = DEFAULT_EMBEDDING_CHUNK):

    embeddings = []
    if len(docs) > chunk:
        for i in range(0, len(docs), chunk):
            response = get_embeddings(docs[i:i+chunk])
            embeddings.extend(response)          
    else:
        response = openai.Embedding.create(model=model, input = docs) 
        embeddings = [doc['embedding'] for doc in response['data']]

    return embeddings

def get_completion(input, model = DEFAULT_COMPLETION_MODEL, max_tokens = DEFAULT_MAX_TOKENS, temperature = DEFAULT_TEMPERATURE):
    response = openai.Completion.create(
        model=model,
        prompt=input,
        max_tokens=max_tokens,
        temperature=temperature,
        )
    
    return response['choices'][0]['text']
