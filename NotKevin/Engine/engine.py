from .queries import get_completion, get_embeddings
from collections.abc import Iterable
from .prompts import REMEMBER_PROMPT, QUERY_TYPE_PROMPT, RECALL_PROMPT, RESPONSE_PROMPT
from .enum import ResponseType
from datetime import datetime

import numpy as np

DEFAULT_MEMORY_DEPTH = 25

class Engine:

    def __init__(self, memory):
        self.__memory = memory

    def get_embeddings(self, query, autoSave = False):

        if query is not Iterable:
            query = [query]
        
        embeddings = get_embeddings(query)

        for q, e in zip(query, embeddings):
            self.__memory.store(q, e)

        if autoSave:
            self.__memory.save()

    def _generate(self, query, save = False):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Received query: {query}")

        if save:
            user_input = f"[USERINPUT][{ts}] {query}"
            self._store(user_input, ts)

        responseType = self._get_response_type(query)

        print(f"Response type is: {responseType}")

        if responseType == ResponseType.MEMORY:
            return self._remember(query, ts, save=save)
        elif responseType == ResponseType.RECALL:
            return self._recall(query, ts, save=save)
        elif responseType == ResponseType.RESPONSE:
            return self._respond(query, ts, save=save)
        else:
            raise ValueError("Invalid Response Type")

    def _remember(self, query, ts, save = False):
        mem = get_completion(REMEMBER_PROMPT.format(user_input=query, timestamp=ts)).strip()
        if save:
            self._store(mem, ts)

        return mem
    
    def _store(self, query, ts):
        embed = get_embeddings(query)
        self.__memory.store(query, embed)
    
    def _recall(self, query, ts, save = False, memory_depth = DEFAULT_MEMORY_DEPTH):
        content, embs = self.__memory.get_memories()

        query_emb = get_embeddings(query)[0]
        similarities = np.dot(embs, query_emb)

        top = np.argsort(similarities)[-memory_depth:]
        mem_prompt = '- '+'\n- '.join(content[top,0])

        recall =  get_completion(RECALL_PROMPT.format(user_input=query, memory_input=mem_prompt))
        recall = f"[RECALL][{ts}] {recall}"

        recall_emb = get_embeddings(recall)
        self.__memory.store(recall, recall_emb)

        return recall
    
    def _respond(self, query, ts, save = False):
        response =  get_completion(RESPONSE_PROMPT.format(user_input=query))

        response = f"[RESPONSE][{ts}] {response}"
        response_emb = get_embeddings(response)
        self.__memory.store(response, response_emb)

        return response
    
    def _get_response_type(self, query):
        responseType = get_completion(QUERY_TYPE_PROMPT.format(user_input=query),stop = [']','\n', ' ']).strip()
        print(f"Response type response is: {responseType}")

        if responseType in ['[MEMORY]', 'MEMORY']:
            return ResponseType.MEMORY
        elif responseType in ['[RESPONSE]', 'RESPONSE']:
            return ResponseType.RESPONSE
        elif responseType in ['[RECALL]', 'RECALL']:
            return ResponseType.RECALL
        else:
            raise ValueError("Invalid Response Type")