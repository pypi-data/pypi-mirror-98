import fire
from data_collection import run_command
import pathlib
import os


def main(path_to_video, keep_video=False):

    root = pathlib.Path(path_to_video).stem
    os.mkdir(root)

    command = f"ffmpeg -i {path_to_video} -r 1/1 ./{root}/{root}-%03d.bmp"
    # print(command)
    run_command(command=command)

    if keep_video is False:
        os.remove(path_to_video)


if __name__ == "__main__":
    fire.Fire(main)