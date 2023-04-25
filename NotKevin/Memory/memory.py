
class Memory:
    
    def __init__(self):
        pass

    def retreive_recent(self):
        raise NotImplementedError()
    
    def retreive_relevant(self, query):
        raise NotImplementedError()
    
    def store(self, data):
        raise NotImplementedError()

    @property
    def Type(self):
        return self.__type