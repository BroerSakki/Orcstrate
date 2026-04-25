import os
import subprocess
from collections import deque

class CommandRunner:
    def __init__(self):
        self.processes = []
        self.queue = deque()

    # Sanitize environment
    # ---
    def clean_env(self):
        env = os.environ.copy()

        for key in [
            "GTK_PATH",
            "GIO_MODULE_DIR",
            "LOCPATH",
            "LD_PRELOAD",
            "GTK_MODULES",
        ]:
            env.pop(key, None)

        return env
    # ---

    # Execution contexts
    # ---
    def run_internal(self, cmd):
        print(f"[INTERNAL] {cmd}")

        process = subprocess.Popen(cmd, shell=True)
        process.wait()

        if process.returncode != 0:
            print(f"[ERROR] Command failed: {cmd}")

        return process

    def run_external(self, cmd, keep_open=True):
        print(f"[EXTERNAL] {cmd}")
    
        if keep_open:
            full_cmd = f"{cmd}; echo '\\n[Process finished]'; exec bash"
        else:
            full_cmd = cmd
    
        process = subprocess.Popen(
            ["xfce4-terminal", "-e", f'bash -c "{full_cmd}"'],
            env=self.clean_env()
        )
    
        self.processes.append(process)
        return process
    #---

    # Main runner
    # ---
    def run_queue(self):
        while self.queue:

            cmd = self.queue.popleft()

            if cmd.external:
                self.run_external(cmd.command, keep_open=cmd.keep_open)
            else:
                self.run_internal(cmd.command)    
    # ---

    # Queue management
    # ---
    def add_to_queue(self, command):
        self.queue.append(command)

    def clear_queue(self):
        self.queue.clear()

    def load_commands(self, commands):
        self.clear_queue()
        for cmd in commands:
            self.add_to_queue(cmd)
    # ---