"""Variables and functions representing the working environment.

"""


import os
import sys


RD_BASEDIR = ""
RD_RESULTS = ""


def set_env() -> tuple[str, ...]:
    """Sets the environment well be working on.

    To be precise, it sets:
    - the base working directory
    - the location of the rdfind result file

    :return: a tuple with the base directory and the path to the rdfind result
    file. As in (base_dir, result_path)
    """
    global RD_BASEDIR, RD_RESULTS
    # if base dir is not provided assume BASEDIR is cwd
    if len(sys.argv) > 1:
        RD_BASEDIR = sys.argv[1]
    else:
        RD_BASEDIR = os.getcwd()

    # open rdfind result file passed as arg
    # if no file passed as arg ask for file
    if len(sys.argv) > 2:
        RD_RESULTS = f"{RD_BASEDIR}/{sys.argv[2]}"
    else:
        print("Enter rdfind result file.")
        RD_RESULTS = input("Leave empty for rdfind_result.txt: ").strip()
        if RD_RESULTS:
            RD_RESULTS = f"{RD_BASEDIR}/{RD_RESULTS}"
        else:
            RD_RESULTS = f"{RD_BASEDIR}/rdfind_result.txt"

    return RD_BASEDIR, RD_RESULTS
