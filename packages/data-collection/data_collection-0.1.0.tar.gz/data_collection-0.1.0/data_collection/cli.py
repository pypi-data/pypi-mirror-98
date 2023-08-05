import os
import pathlib
import importlib
import fire
import sys


def main(script_name=None):
    
    # del fire.__cached__
    scripts = os.path.join(pathlib.Path(__file__).parent, "scripts")

    available_scripts = [pathlib.Path(script).stem for script in os.listdir(scripts)]

    if script_name == None:
        print(f"\nNo script name given. These are the available options:\n")
        for _ in available_scripts:
            if _ != "__pycache__":
                print(_)
        sys.exit(print(""))

    for script in available_scripts:

        if script_name == script:

            mod = importlib.import_module(f"data_collection.scripts.{script_name}")
            sys.argv.pop(0)
            fire.Fire(mod.main, name=script_name)
            sys.exit()

    print(
        f'\nScript "{script_name}" doesn\'t exist. These are the available options:\n'
    )
    for _ in available_scripts:
        if _ != "__pycache__":
            print(_)
    sys.exit(print(""))


def fire_main():
    fire.Fire(main)