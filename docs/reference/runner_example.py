import subprocess
import threading
from typing import List, Callable, Optional
from.command import Command

class CommandRunner:
    def __init__(self):
        self.processes = []

    # -------------------------
    # Public API
    # -------------------------

    def run_sequential(
        self,
        commands: List[str],
        on_output: Optional[Callable[[str], None]] = None,
        on_complete: Optional[Callable[[], None]] = None,
    ):
        thread = threading.Thread(
            target=self._run_sequential_worker,
            args=(commands, on_output, on_complete),
            daemon=True,
        )
        thread.start()

    def run_parallel(
        self,
        commands: List[str],
        on_output: Optional[Callable[[str], None]] = None,
        on_complete: Optional[Callable[[], None]] = None,
    ):
        thread = threading.Thread(
            target=self._run_parallel_worker,
            args=(commands, on_output, on_complete),
            daemon=True,
        )
        thread.start()

    def terminate_all(self):
        for process in self.processes:
            if process.poll() is None:
                process.terminate()

    # -------------------------
    # Internal workers
    # -------------------------

    def _run_sequential_worker(self, commands, on_output, on_complete):
        for cmd in commands:
            if on_output:
                on_output(f"\n[RUNNING] {cmd}\n")

            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )

            self.processes.append(process)

            for line in process.stdout:
                if on_output:
                    on_output(line)

            process.wait()

        if on_complete:
            on_complete()

    def _run_parallel_worker(self, commands, on_output, on_complete):
        threads = []

        for cmd in commands:
            t = threading.Thread(
                target=self._run_single_command,
                args=(cmd, on_output),
                daemon=True,
            )
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        if on_complete:
            on_complete()

    def _run_single_command(self, cmd, on_output):
        if on_output:
            on_output(f"\n[RUNNING] {cmd}\n")

        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        self.processes.append(process)

        for line in process.stdout:
            if on_output:
                on_output(line)

        process.wait()
