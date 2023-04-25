from ..Memory import LocalMemory, Memory
from ..Engine import Engine

DEFAULT_MEMORY = 'Local'
DEFULT_AUTOSAVE = False

class Agent:

    def __init__(self, name = "Not Kevin", memory = DEFAULT_MEMORY, autosave = DEFULT_AUTOSAVE):
        self.__memory = self._initiate_memory(memory)
        self.__engine = Engine(self.__memory)
        self.__autosave = autosave
        self.name = name

    def _initiate_memory(self, memory):
        if memory is  Memory:
            return memory

        if memory == 'Local':
            return LocalMemory()
        else:
            raise NotImplementedError()
        
    def run(self):
        print(f"[{self.name}]Hello I am Kevin, what can I do for you today?")
        while True:
            query = input("[YOU] ")
            response = self.__engine._generate(query, save = self.__autosave)
            print(f"[{self.name}] {response}")