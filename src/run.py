import os
import subprocess
import threading

class run_api:
    def setup(self):
        os.environ["PYTHONUNBUFFERED"] = "1"

        node = subprocess.Popen(
            ["node", "rest_engine/dist/src/server.js"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        python = subprocess.Popen(
            ["python", "./main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        threading.Thread(target=self.read_output, args=(node, "Neon")).start()
        threading.Thread(target=self.read_output, args=(python, "Astra")).start()

    def read_output(self, process, process_name):
        for line in iter(process.stdout.readline, b''):
            if line:
                print(f"[{process_name} I/O] {line.decode().strip()}")
        for line in iter(process.stderr.readline, b''):
            if line:
                print(f"[{process_name} Error] {line.decode().strip()}")


run_api().setup()

