from ..Memory import LocalMemory, Memory
from ..Engine import Engine

DEFAULT_MEMORY = 'Local'
DEFULT_AUTOSAVE = True

class Agent:

    def __init__(self, name = "Not Kevin", memory = DEFAULT_MEMORY, autosave = DEFULT_AUTOSAVE):
        self.__memory = self._initiate_memory(memory)
        self.__engine = Engine()
        self.__autosave = autosave

    def _initiate_memory(self, memory):
        if memory is  Memory:
            return memory

        if memory == 'Local':
            return LocalMemory()
        else:
            raise NotImplementedError()