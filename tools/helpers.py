import os, sys

GENERATED_FOLDER = "generated"
OUT_FOLDER = "out"


def init_folders():
    create_folder(OUT_FOLDER)
    create_folder(GENERATED_FOLDER)

def create_folder(name):
    root = os.path.abspath(".")
    path = f"{root}/{name}"
    if (not os.path.exists(path)):
        os.mkdir(path)

def get_arg():
    return open(sys.argv[1]).read()

def get_program_name():
    return os.path.basename(sys.argv[1]).split(".")[0]
