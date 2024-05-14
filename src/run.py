import os
import subprocess
import threading


class run_api:
    def setup(self):
        os.environ["PYTHONUNBUFFERED"] = "1"

        node = subprocess.Popen(
            ["node", "api/dist/src/server.js"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        python = subprocess.Popen(
            ["python", "./main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        threading.Thread(target=self.read_output, args=(node, "Ares API")).start()
        threading.Thread(target=self.read_output, args=(python, "AstraNet")).start()

    def read_output(self, process, process_name):
        for line in iter(process.stdout.readline, b""):
            print(f"[{process_name} I/O] {line.decode()}")
        for line in iter(process.stderr.readline, b""):
            print(f"[{process_name} Error] {line.decode()}")


run_api().setup()
