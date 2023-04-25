from .memory import Memory
import os
import numpy as np

class LocalMemory(Memory):
    def __init__(self):
        super().__init__()

        self.__type = "Local"
        self.__text = None
        self.__embeddings = None

        self._setup()
        self._load()

    def retreive_recent(self):
        raise NotImplementedError()
    
    def retreive_relevant(self, query):
        raise NotImplementedError()
    
    def store(self, content, embeddings):
        
        content = np.array(content)
        if len(content.shape) != 2:
            content = content.reshape(-1, 1)

        embeddings = np.array(embeddings)
        if len(embeddings.shape) != 2:
            embeddings = embeddings.reshape(-1, 1536)

        if content.shape[0] != embeddings.shape[0]:
            raise ValueError("Content and Embeddings must be the same length")

        self.__text = np.vstack([self.__text, content])
        self.__embeddings = np.vstack([self.__embeddings, embeddings])
        self._save()
    
    def _load(self):
        self.__embeddings = np.load(".memory/vector.npy").reshape(-1,1536)
        self.__text = np.load(".memory/content.npy").reshape(-1,1)
    
    def _save(self):
        np.save(".memory/vector", self.__embeddings)
        np.save(".memory/content", self.__text)
    
    def _setup(self):
        #Check if .memory exists
        if not os.path.exists(".memory"):
            os.mkdir(".memory")
        
        #check if .memory/vector.np exists
        if not os.path.exists(".memory/vector.npy"):
            vector = np.array([]).reshape(-1,1536)
            np.save(".memory/vector", vector)
        
        #check if .memory/content.np exists
        if not os.path.exists(".memory/content.npy"):
            content = np.array([]).reshape(-1,1)
            np.save(".memory/content", content)
    
    @property
    def Type(self):
        return self.__type