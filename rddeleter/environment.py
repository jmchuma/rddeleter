"""Variables and functions representing the working environment.

"""


import os


LAUNCH_DIR = ""
RD_BASEDIR = ""
RD_RESULTS = ""


def set_env(results_path: str) -> tuple[str, ...]:
    """Sets the environment well be working on.

    To be precise, it sets:
    - the base working directory
    - the location of the rdfind result file

    :param results_path: path (absolute or relative to current working directory)
    to the rdfind result file.
    :return: a tuple with the base directory and the path to the rdfind result
    file. As in (base_dir, result_path)
    """
    global LAUNCH_DIR
    global RD_BASEDIR
    global RD_RESULTS

    RD_RESULTS = os.path.abspath(results_path)
    RD_BASEDIR = os.path.dirname(RD_RESULTS)

    # move to the directory where the result file is located
    # since the paths will be relative to that directory
    LAUNCH_DIR = os.getcwd()
    if LAUNCH_DIR != RD_BASEDIR:
        os.chdir(RD_BASEDIR)

    return RD_BASEDIR, RD_RESULTS
