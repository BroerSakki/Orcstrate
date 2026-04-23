class Command:
    def __init__(self, command, external=False, name=None):
        self.command = command
        self.external = external
        self.name = name or command