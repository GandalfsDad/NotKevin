from ..Memory import LocalMemory, Memory
from ..Engine import Engine
from colorama import init, Fore, Style, Back

DEFAULT_MEMORY = 'Local'
DEFULT_AUTOSAVE = True

class Agent:

    def __init__(self, name = "Not Kevin", memory = DEFAULT_MEMORY, autosave = DEFULT_AUTOSAVE):
        self.__memory = self._initiate_memory(memory)
        self.__engine = Engine(self.__memory)
        self.__autosave = autosave
        self.name = name

        init(autoreset=True)

    def _initiate_memory(self, memory):
        if memory is  Memory:
            return memory

        if memory == 'Local':
            return LocalMemory()
        else:
            raise NotImplementedError()
        
    def clear_memory(self, save = False):
        self.__memory.clear(save=save)
        
    def run(self):
        print(self.format_response("Hello I am Kevin, what can I do for you today?"))
        while True:
            query = input(Fore.RED+"[YOU] " + Fore.WHITE)

            if query.lower().strip() in  ("exit","exit()","end","die","quit","q"):
                break   

            response = self.__engine.generate(query, save = self.__autosave)
            print(self.format_response(response))
    
    def format_response(self, response):
       loc = response.find("]")+1
       if loc <= 0:
            return(Fore.GREEN+f"[{self.name}] "+Fore.CYAN+response)
       else:
            return(Fore.GREEN+f"[{self.name}] "+Fore.CYAN+response[loc:])