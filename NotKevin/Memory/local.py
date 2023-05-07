from .memory import Memory
import os
import numpy as np

HOME = os.path.expanduser('~')

class LocalMemory(Memory):
    def __init__(self, sub_directory = 'NotKevin'):
        super().__init__()

        self.__type = "Local"
        self.__sub_directory = sub_directory
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
        self.__embeddings = np.load(f"{HOME}/.memory/{self.__sub_directory}/vector.npy").reshape(-1,1536)
        self.__text = np.load(f"{HOME}/.memory/{self.__sub_directory}/content.npy").reshape(-1,1)
    
    def _save(self):
        np.save(f"{HOME}/.memory/{self.__sub_directory}/vector", self.__embeddings)
        np.save(f"{HOME}/.memory/{self.__sub_directory}/content", self.__text)
    
    def _setup(self):
        #Check if .memory exists
        if not os.path.exists(f"{HOME}/.memory"):
            os.mkdir(f"{HOME}/.memory")

        if not os.path.exists(f"{HOME}/.memory/{self.__sub_directory}"):
            os.mkdir(f"{HOME}/.memory/{self.__sub_directory}")
        
        #check if .memory/vector.np exists
        if not os.path.exists(f"{HOME}/.memory/{self.__sub_directory}/vector.npy"):
            vector = np.array([]).reshape(-1,1536)
            np.save(f"{HOME}/.memory/{self.__sub_directory}/vector", vector)
        
        #check if .memory/content.np exists
        if not os.path.exists(f"{HOME}/.memory/{self.__sub_directory}/content.npy"):
            content = np.array([]).reshape(-1,1)
            np.save(f"{HOME}/.memory/{self.__sub_directory}/content", content)

    def get_memories(self):
        idx = [x[0][:3]!='[IN' for x in self.Content]
        return self.Content[idx], self.Embeddings[idx]
        return self.Content, self.Embeddings
    
    def clear(self, save = False):
        self.__text = np.array([]).reshape(-1,1)
        self.__embeddings = np.array([]).reshape(-1,1536)
        if save:
            self._save()
    
    @property
    def Type(self):
        return self.__type
    
    @property
    def Embeddings(self):
        return self.__embeddings

    @property
    def Content(self):
        return self.__text