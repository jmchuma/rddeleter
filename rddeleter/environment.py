"""Variables and functions representing the working environment.

"""


import os
import sys


BASEDIR = ""
RDFIND_RESULTS = ""


def set_env() -> tuple[str, ...]:
    """Sets the environment well be working on.

    To be precise, it sets:
    - the base working directory
    - the location of the rdfind result file

    :return: a tuple with the base directory and the path to the rdfind result
    file. As in (base_dir, result_path)
    """
    global BASEDIR, RDFIND_RESULTS
    # if base dir is not provided assume BASEDIR is cwd
    if len(sys.argv) > 1:
        BASEDIR = sys.argv[1]
    else:
        BASEDIR = os.getcwd()

    # open rdfind result file passed as arg
    # if no file passed as arg ask for file
    if len(sys.argv) > 2:
        RDFIND_RESULTS = f"{BASEDIR}/{sys.argv[2]}"
    else:
        print("Enter rdfind result file.")
        RDFIND_RESULTS = input("Leave empty for rdfind_result.txt: ").strip()
        if RDFIND_RESULTS:
            RDFIND_RESULTS = BASEDIR + "/" + RDFIND_RESULTS
        else:
            RDFIND_RESULTS = BASEDIR + "/rdfind_result.txt"

    return BASEDIR, RDFIND_RESULTS
