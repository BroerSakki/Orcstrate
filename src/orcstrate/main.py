from core.runner import CommandRunner
from models.command import Command
from app import App
import time

runner = CommandRunner()
commands = [
    Command("echo '=== START ==='"),
    Command("echo 'Running internal command 1'"),
    Command("sleep 5", external=True),
    Command("echo 'Back to internal flow'"),
    Command("ping -c 4 google.com", external=True, keep_open=False),
    Command("sleep 2"),
    Command("ls /this/does/not/exist"),
    Command("echo '=== END ==='")
]


app = App(commands)
app.run()