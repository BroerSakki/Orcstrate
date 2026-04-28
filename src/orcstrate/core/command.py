class Command:
    def __init__(self, command:str, external:bool=False, keep_open:bool=True, name:str=None):
        self.command:str = command
        self.external:bool = external
        self.keep_open:bool = keep_open
        self.name:str = name or command