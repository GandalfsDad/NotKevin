from ..Memory import LocalMemory, Memory
from ..Engine import Engine
from colorama import init, Fore, Style, Back

DEFAULT_MEMORY = 'Local'
DEFULT_AUTOSAVE = True

class Agent:

    def __init__(self, name = "NotKevin", memory = DEFAULT_MEMORY, autosave = DEFULT_AUTOSAVE):
        self.__name = name
        self.__memory = self._initiate_memory(memory)
        self.__engine = Engine(self.__memory)
        self.__autosave = autosave
        

        init(autoreset=True)

    def _initiate_memory(self, memory):
        if memory is  Memory:
            return memory

        if memory == 'Local':
            lm = LocalMemory(sub_directory=self.__name)

            if  not lm.HasPersonality:
                query = input(Fore.RED+"Before we kick off. Please provide a summary of my personality \n" + Fore.WHITE)
                lm.save_personality(query)

            return lm
        else:
            raise NotImplementedError()
        
    def clear_memory(self, save = False):
        self.__memory.clear(save=save)

        if  not self.__memory.HasPersonality:
                query = input(Fore.RED+"Before we kick off. Please provide a summary of my personality \n" + Fore.WHITE)
                self.__memory.save_personality(query)

    def run(self):
        print(self.format_response(f"Hello I am {self.__name}, what can I do for you today?"))
        while True:
            query = input(Fore.RED+"[YOU] " + Fore.WHITE)

            if query.lower().strip() in  ("exit","exit()","end","die","quit","q"):
                break   

            response = self.__engine.generate(query, save = self.__autosave)
            print(self.format_response(response))
    
    def format_response(self, response):
       loc = response.find("]")+1
       if loc <= 0:
            return(Fore.GREEN+f"[{self.__name}] "+Fore.CYAN+response)
       else:
            return(Fore.GREEN+f"[{self.__name}] "+Fore.CYAN+response[loc:])