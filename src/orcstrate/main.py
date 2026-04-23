from core.runner import CommandRunner
from core.command import Command

runner = CommandRunner()
commands = [
    Command("echo '=== START ==='"),

    # Quick internal
    Command("echo 'Running internal command 1'"),

    # External long-running (you should see a new terminal)
    Command("sleep 5", external=True),

    # Internal after external (should NOT wait for it)
    Command("echo 'Back to internal flow'"),

    # Another external
    Command("ping -c 4 google.com", external=True),

    # Simulate work
    Command("sleep 2"),

    # Failure case
    Command("ls /this/does/not/exist"),

    # Final
    Command("echo '=== END ==='")
]

runner.run_all(commands)
