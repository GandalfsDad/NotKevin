from .queries import get_chat_completion, get_embeddings
from collections.abc import Iterable
from .prompts import USER_PROMPT, SYSTEM_PROMPT, GET_INSIGHTS_PROMPT, GET_INSIGHTS_SYSTEM_PROMPT

import json

import numpy as np

DEFAULT_MEMORY_DEPTH = 25
DEFAULT_RECENT_DEPTH = 10
DEFAULT_INSIGHT_FREQUENCY = 5

class Engine:

    def __init__(self, memory, gpt4 = False):
        self.__memory = memory
        self._recentMessages = []

        self.__gpt4 = gpt4

        self.__queryCount = 0
        self._deepInsights = ''
        self._genDeepInsights()

    def get_embeddings(self, query, save = True):

        if query is not Iterable:
            query = [query]
        
        embeddings = get_embeddings(query)

        for q, e in zip(query, embeddings):
            self.__memory.store(q, e)

        if save:
            self.__memory.save()

    def generate(self, query, save = True):
        query = f"[ME] {query}"

        self.__queryCount +=1
        if self.__queryCount % DEFAULT_INSIGHT_FREQUENCY == 0:
            self._genDeepInsights()
    
        recent = self._genRecent()
        context = self._genContext(query)

        if save:
            self._store(query)
        
        response = self._genResponse(query, recent, context, save = save)

        self._recentMessages.append(query)
        self._recentMessages.append(response)

        return response
 
    def _store(self, query):
        embed = get_embeddings(query)
        self.__memory.store(query, embed)

    def _genRecent(self):
        return '\n'.join(self._recentMessages[-DEFAULT_RECENT_DEPTH:])
    
    def _genContext(self, query, save = True, memory_depth = DEFAULT_MEMORY_DEPTH):
        content, embs = self.__memory.get_memories()

        query_emb = get_embeddings(query)[0]
        similarities = np.dot(embs, query_emb)

        top = np.argsort(similarities)[-memory_depth:]
        mem_prompt = '- '+'\n- '.join(content[top,0])

        return mem_prompt
    
    def _genDeepInsights(self, memory_depth = DEFAULT_MEMORY_DEPTH):
        recent = '/n'.join(self._recentMessages[-DEFAULT_RECENT_DEPTH:])
        embed = get_embeddings(recent)

        insights, insight_embeddings = self.__memory.get_insights()
        similarities = np.dot(insight_embeddings,embed[0])
        
        top = np.argsort(similarities)[-memory_depth:]
        relevant_insights = '- '+'\n- '.join(insights[top,0])

        summarized_insights_prompt = GET_INSIGHTS_SYSTEM_PROMPT.replace('{name}',self.__memory.Name).replace('{personality}',self.__memory.Personality).replace('{insights}',relevant_insights)

        if self.__gpt4:
            response = get_chat_completion(GET_INSIGHTS_PROMPT, summarized_insights_prompt, model = 'gpt4')
        else:
            response = get_chat_completion(GET_INSIGHTS_PROMPT, summarized_insights_prompt)
            
        self._deepInsights = response
    
    def _genResponse(self, query, recentMessages,contextMessages,save = True):
        
        prompt = USER_PROMPT.format(recent_messages = recentMessages, context_messages = contextMessages, query = query)

        system_prompt = SYSTEM_PROMPT.replace('{name}',self.__memory.Name).replace('{personality}',self.__memory.Personality).replace('{insights}',self._deepInsights)
        
        if self.__gpt4:
            response = get_chat_completion(prompt, system_prompt, model = 'gpt4')
        else:
            response = get_chat_completion(prompt, system_prompt)

        response = json.loads(response)
        if "[INSIGHT]" in response:
            if save and (len(response['[INSIGHT]']) > 0):
                self._store(f"[INSIGHT] {response['[INSIGHT]']}")

        if "[RESPONSE]" in response:
            _response = f"[{self.__memory.Name}] {response['[RESPONSE]']}"
            if save:
                self._store(_response)
            return _response
        else:
            raise ValueError("Response not found")


