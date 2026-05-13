import gi
gi.require_version('Vte', '3.91')
import os
import subprocess
import platform
import threading
import time
from collections import deque
from models.command import Command
from gi.repository import GLib
from gi.repository import Vte

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
    def run_internal(self, cmd: str, terminal):
        print(f"\n[INTERNAL] {cmd}")

        loop = GLib.MainLoop()
        return_code = None

        def on_child_exited(term, exit_status):
            nonlocal return_code
            return_code = exit_status
            loop.quit()

        handler_id = terminal.connect("child-exited", on_child_exited)

        shell_bin = os.environ.get("SHELL", "/bin/sh")
        argv = [shell_bin, "-c", cmd, None]
        working_dir = os.environ.get("HOME", "/")

        terminal.spawn_async(
            Vte.PtyFlags.DEFAULT,
            working_dir,
            argv,
            None,
            GLib.SpawnFlags.DEFAULT,
            None, None,
            -1,
            None,
            None,
            None
        )

        loop.run()

        terminal.disconnect(handler_id)

        if return_code != 0:
            print(f"\n[ERROR] Command failed: {cmd}")

        return return_code

    def run_external(self, cmd:str, keep_open:bool=True):
        print(f"\n[EXTERNAL] {cmd}")

        os_name = platform.system()

        if keep_open:
            full_cmd:str = f"{cmd}; echo '\n[Process finished]'; exec bash"
        else:
            full_cmd:str = cmd

        if os_name == "Windows":
            print("\n[INFO] Mintty Terminal")
            terminal = "mintty"
            terminal_args = ["-e", "bash", "-c", full_cmd]
        else:
            print("\n[INFO] XFCE Terminal")
            terminal = "xfce4-terminal"
            terminal_args = ["-e", f'bash -c "{full_cmd}"']

        print(f"\n[INFO] Running {[terminal] + terminal_args}")
        process = subprocess.Popen(
            [terminal] + terminal_args,
            env=self.clean_env(),
        )

        self.processes.append(process)
        return process
    #---

    def clear_vte_terminal(self, terminal):
        terminal.reset(True, True)

    # Main runner
    # ---
    def run_queue(self, terminal):
        if self._running:
            print("\n[INFO] Already running")
            return
        else:
            print("\n[INFO] Starting worker")

        self._running = True

        self.clear_vte_terminal(terminal)
        thread = threading.Thread(target=self._run_worker, args=(terminal,))
        thread.daemon = True
        thread.start()
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
    def _run_worker(self, terminal):
        if self._running:
            print("\n[INFO] Worker started")
        else:
            print("\n[INFO] Worker disconnected")

        while self._running:

            while self._paused:
                time.sleep(0.1)

            if not self.queue:
                time.sleep(0.1)
                continue

            cmd:Command = self.queue.popleft()

            if cmd.external:
                self.run_external(cmd.command, keep_open=cmd.keep_open)
            else:
                self.run_internal(cmd.command, terminal)

            print()

        print("\n[INFO] Worker stopped")
    # ---

    # Runtime management
    # ---
    def pause(self):
        print("\n[INFO] Pausing worker")
        self._paused = True

    def resume(self):
        print("\n[INFO] Resuming worker")
        self._paused = False

    def stop(self):
        print("\n[INFO] Stopping worker")
        self._running = False

    def wait_until_done(self, manual: bool = False):
        if manual:
            input()
            self.stop()
            self._run_worker()
        else:
            while self._running or self.queue:
                time.sleep(0.1)
    # ---