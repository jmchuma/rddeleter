"""Parses rdfind result file.

Arguments [directory] [result_file]
If directory is not provided it assumes the current working directory as the
base working.
If result_file is not provided it ask for it and if it's not provided assumes
rdfind_result.txt in the base directory.
"""


import os
import sys


def main():
    """
    """
    BASEDIR, RDFIND_RESULTS = set_env()

    with open(RDFIND_RESULTS, "r") as file_in:
        block = []

        for line in file_in:
            line = line.lstrip()
            if line.startswith("#") or not line:
                continue

            line = line.split()
            if line[0] == "DUPTYPE_FIRST_OCCURRENCE" and len(block) != 0:
                process_block(block)
                block = []

            block.append(line)
        else:  # EOF
            process_block(block)


def set_env():
    """
    Sets the environment well be working on.

    To be precise, it sets:
    - the base working directory
    - the location of the rdfind result file

    :return: a tuple with the base directory and the path to the rdfind result
    file. As in (base_dir, result_path)
    """
    # if base dir is not provided assume basedir is cwd
    if len(sys.argv) > 1:
        basedir = sys.argv[1]
    else:
        basedir = os.getcwd()

    print(f"basedir: {basedir}")

    # open rdfind result file passed as arg
    # if no file passed as arg ask for file
    if len(sys.argv) > 2:
        rdfind_results = basedir + "/" + sys.argv[2]
    else:
        while True:
            try:
                print("Enter rdfind result file.")
                rdfind_results = input("Leave empty for rdfind_result.txt: ").strip()
                if rdfind_results:
                    rdfind_results = basedir + "/" + rdfind_results
                else:
                    rdfind_results = basedir + "/rdfind_result.txt"
                break
            except EOFError:  # control-d
                sys.exit()

    print(f"rdfind_results: {rdfind_results}")

    return basedir, rdfind_results


def process_block(block):
    """
    Processes a block of duplicates.

    :param block: a list of duplicates.
    block[0] is the one considered original by rdfind.
    :return:
    """
    multiplier = 0
    last = len(block) - 1
    while multiplier >= 0:
        print(f"Main:\n    [0] {block[0][7]}")

        start = 10 * multiplier + 1
        multiplier += 1
        # I'm going to calculate it anyway for the if block,
        # so I may as well save it.
        end = start + 10
        if end > last:
            end = last  # does it really matter?
            multiplier = -1  # to end while block
            print(f"Dups ({start}:{last}) of {last}:")
            subblock = block[start:]
        else:
            print(f"Dups ({start}:{end - 1}) of {last}:")
            subblock = block[start:end]

        for index, line in enumerate(subblock):
            print(f"    [{start+index}] {line[7]}")

        input("Whaddaya wanna do?: ")


if __name__ == "__main__":
    main()
