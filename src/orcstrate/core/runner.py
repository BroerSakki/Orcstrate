import os
import subprocess
import threading
import time
from collections import deque
from core.command import Command

class CommandRunner:
    # Constructer
    # ---
    def __init__(self):
        self.processes = []
        self.queue: deque[Command] = deque()

        self._running = False
        self._paused = False
    # ---

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
    def run_internal(self, cmd: str):
        print(f"[INTERNAL] {cmd}")

        process:subprocess.Popen = subprocess.Popen(cmd, shell=True)
        process.wait()

        if process.returncode != 0:
            print(f"[ERROR] Command failed: {cmd}")

        return process

    def run_external(self, cmd:str, keep_open:bool=True):
        print(f"[EXTERNAL] {cmd}")
    
        if keep_open:
            full_cmd:str = f"{cmd}; echo '\n[Process finished]'; exec bash"
        else:
            full_cmd:str = cmd
    
        process:subprocess.Popen = subprocess.Popen(
            ["xfce4-terminal", "-e", f'bash -c "{full_cmd}"'],
            env=self.clean_env()
        )
    
        self.processes.append(process)
        return process
    #---

    # Main runner
    # ---
    def run_queue(self, manual:bool = False):
        if self._running:
            print("[INFO] Already running")
            return
        else:
            print("[INFO] Starting worker")
            if manual:
                print("[INFO] Press Enter to stop...\n")

        self._running = True


        thread = threading.Thread(target=self._run_worker)
        thread.daemon = True
        thread.start()
        self.wait_until_done(manual)
    # ---

    # Queue management
    # ---
    def add_to_queue(self, command: Command):
        self.queue.append(command)

    def clear_queue(self):
        self.queue.clear()

    def queue_size(self) -> int:
        return len(self.queue)

    def peek_queue(self) -> deque[Command]:
        return list(self.queue)

    def load_commands(self, commands: list[Command]):
        self.clear_queue()
        for cmd in commands:
            self.add_to_queue(cmd)
    # ---

    # Worker management
    # ---
    def _run_worker(self):
        print("[INFO] Worker started")
        while self._running:

            while self._paused:
                time.sleep(0.1)

            if not self.queue:
                time.sleep(0.1)
                continue

            cmd = self.queue.popleft()

            if cmd.external:
                self.run_external(cmd.command, keep_open=cmd.keep_open)
            else:
                self.run_internal(cmd.command)

        print("[INFO] Worker stopped")
    # ---

    # Runtime management
    # ---
    def pause(self):
        print("[INFO] Pausing worker")
        self._paused = True

    def resume(self):
        print("[INFO] Resuming worker")
        self._paused = False

    def stop(self):
        print("[INFO] Stopping worker")
        self._running = False

    def wait_until_done(self, manual: bool = False):
        if manual:
            input()
            self.stop()
        else:
            while self._running or self.queue:
                time.sleep(0.1)
    # ---