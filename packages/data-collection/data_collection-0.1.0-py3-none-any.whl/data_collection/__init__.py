import subprocess


class Pipe(object):
    def __init__(self, main, inputs, outputs) -> None:

        self.inputs = inputs
        self.outputs = outputs
        self.main = main




def run_command(command: str):

    command = command.split()

    process = subprocess.Popen(command)

    while True:
        if process.poll() is not None:
            print("Done")
            break