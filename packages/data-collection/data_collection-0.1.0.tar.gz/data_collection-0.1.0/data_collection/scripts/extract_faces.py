import fire
from data_collection import run_command
import pathlib
import os


def main(input_dir, output_dir):

    raise NotImplementedError
    path = os.path.join(pathlib.Path(__file__).parent.parent, "faceswap/faceswap.py")
    command = f"python3 {path} extract -i {input_dir} -o {output_dir}"
    # print(command)
    run_command(command=command)


if __name__ == "__main__":
    fire.Fire(main)