class Command:
    def __init__(self, command, external=False, keep_open=True, name=None):
        self.command = command
        self.external = external
        self.keep_open = keep_open
        self.name = name or command