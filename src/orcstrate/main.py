from core.runner import CommandRunner
from models.command import Command
import time
from app import App
from ui.window import MainWindow

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

print("[INFO] Press Enter to stop...\n")

runner.add_to_queue(Command("echo thingymajiggle"))
#runner.run_queue()


time.sleep(1)

runner.add_to_queue(Command("echo added later"))

#runner.wait_until_done(True)

app = App(runner.queue)
app.run()