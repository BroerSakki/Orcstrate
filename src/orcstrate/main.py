from core.runner import CommandRunner
from core.command import Command

runner = CommandRunner()
commands = [
    Command("echo '=== START ==='"),
    Command("echo 'Running internal command 1'"),
    Command("sleep 5", external=True),
    Command("echo 'Back to internal flow'"),
    Command("ping -c 4 google.com", external=True),
    Command("sleep 2"),
    Command("ls /this/does/not/exist"),
    Command("echo '=== END ==='")
]

runner.load_commands(commands)
runner.run_queue()