import fire
from data_collection import run_command


def main(url: str, destination: str):
    """
    Download a youtube video based on a url
    Requires youtube-dl is installed
    pip3 install youtube-dl

    """
    command = f"youtube-dl {url} -o {destination}"
    # print(command)
    run_command(command=command)


if __name__ == "__main__":
    fire.Fire(main)