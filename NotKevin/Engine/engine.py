from .queries import get_chat_completion, get_embeddings
from collections.abc import Iterable
from .prompts import SYSTEM_PROMPT, USER_PROMPT, GET_INSIGHTS_PROMPT, GET_INSIGHTS_SYSTEM_PROMPT

import json

import numpy as np
import tiktoken

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

        self._recentMessages.append({"role":"user", "content":query})
        self._recentMessages.append({"role":"assistant", "content":response})

        return response
 
    def _store(self, query):
        embed = get_embeddings(query)
        self.__memory.store(query, embed)

    def _genRecent(self, as_values = False):
        if as_values:
            return [x['content'] for x in self._genRecent()]
        else:
            return self._recentMessages[-DEFAULT_RECENT_DEPTH:]
    
    def _genContext(self, query, save = True, memory_depth = DEFAULT_MEMORY_DEPTH):
        content, embs = self.__memory.get_memories()

        query_emb = get_embeddings(query)[0]
        similarities = np.dot(embs, query_emb)

        top = np.argsort(similarities)[-memory_depth:]
        mem_prompt = '- '+'\n- '.join(content[top,0])

        return mem_prompt
    
    def _genDeepInsights(self, memory_depth = DEFAULT_MEMORY_DEPTH):
        recent = '/n'.join(self._genRecent(as_values=True))
        embed = get_embeddings(recent)

        insights, insight_embeddings = self.__memory.get_insights()

        if len(insights) == 0:
            self._deepInsights = ''
        else:

            similarities = np.dot(insight_embeddings,embed[0])
            
            top = np.argsort(similarities)[-memory_depth:]
            relevant_insights = '- '+'\n- '.join(insights[top,0])

            summarized_insights_prompt = GET_INSIGHTS_SYSTEM_PROMPT.replace('{name}',self.__memory.Name).replace('{personality}',self.__memory.Personality)

            messages = [{"role":"system","content":summarized_insights_prompt},{"role":"user","content":GET_INSIGHTS_PROMPT.replace('{insights}',relevant_insights)}]
            
            if self.__gpt4:
                response = get_chat_completion(messages, model = 'gpt-4')
            else:
                response = get_chat_completion(messages)

            self._deepInsights = response
    
    def _genResponse(self, query, recentMessages,contextMessages,save = True):

        system_prompt = SYSTEM_PROMPT.replace('{name}',self.__memory.Name) \
                                    .replace('{personality}',self.__memory.Personality) \
                                    .replace('{insights}',self._deepInsights)
        
        user_prompt = USER_PROMPT.replace('{context_messages}',contextMessages) \
                                .replace('{latest_message}',query)
        
        messages = [{"role":"system","content":system_prompt}]+recentMessages+[{"role":"user","content":user_prompt}]

        messages = self._trim_messages(messages, gpt4 = self.__gpt4)
        print(messages)

        if self.__gpt4:
            response = get_chat_completion(messages, model = 'gpt-4')
        else:
            response = get_chat_completion(messages)

        print(f"response: {response}")

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

    def _trim_messages(self, messages, gpt4 = False):
        encoding = tiktoken.get_encoding("cl100k_base")

        message_length = sum(len(encoding.encode(message['content'])) for message in messages)

        print(f"Message length: {message_length}")
        if gpt4:
            if message_length > (8000-1024):
                #Remove some messages
                messages = messages[0]+messages[2:]

                return self._trim_messages(messages, gpt4 = gpt4)
        elif message_length > (4096-1024):
            #Remove some messages
            messages = messages[0]+messages[2:]

            return self._trim_messages(messages, gpt4 = gpt4)
        
        return messages



