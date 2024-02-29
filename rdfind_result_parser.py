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
    # if base dir is not provided assume basedir is cwd
    if len(sys.argv) > 1:
        BASEDIR = sys.argv[1]
    else:
        BASEDIR = os.getcwd()

    print(f"BASEDIR: {BASEDIR}")

    # open rdfind result file passed as arg
    # if no file passed as arg ask for file
    if len(sys.argv) > 2:
        RDFIND_RESULTS = BASEDIR+"/"+sys.argv[2]
    else:
        while True:
            try:
                print("Enter rdfind result file.")
                RDFIND_RESULTS = input("Leave empty for rdfind_result.txt: ").strip()
                if len(RDFIND_RESULTS.strip()) != 0:
                    RDFIND_RESULTS = BASEDIR+"/"+RDFIND_RESULTS
                else:
                    RDFIND_RESULTS = BASEDIR+"/rdfind_result.txt"
                break
            except EOFError:  # control-d
                sys.exit()

    print(f"RDFIND_RESULTS: {RDFIND_RESULTS}")

    with open(RDFIND_RESULTS, "r") as file_in:
        num_main = 0
        num_dups = 0
        for line in file_in:
            line = line.lstrip()
            if line.startswith("#"):
                continue

            line = line.split()
            if line[0] == "DUPTYPE_FIRST_OCCURRENCE":
                num_main += 1
                if num_dups == 0:  # first line
                    print(f"{num_main:04d}{line[7]}", end="")
                else:
                    print(f" :: {num_dups}\n{num_main:04d} {line[7]}", end="")
                    num_dups = 0
            else:
                num_dups += 1
        else: # EOF
            print(f" :: {num_dups}")

    # if output file not provided assume rdfind_result_parser.txt
    # open file
    # clone file to working file
    #
    # if line starts with #
    #     ignore
    # if line starts with DUPTYPE_FIRST_OCCURRENCE
    #     split line keeping only line[0] and line[7]
    #     ask: compare with dups or delete all or quit

    #     if quit
    #         quit
    #     else if trash all
    #         trash all
    #     else if compare with dups
    #         while line starts with DUPTYPE_WITHIN_SAME_TREE
    #             show paths and ask
    #             keep both
    #             trash dup
    #             trash orig and use dup as new original
    #             trash both (or ask this where there are no dups)
    #         endwhile
    #         ask if trash orig (if it's just one remaining)
    #     else ask again if compare or delete or quit
    # write report of actions to file


if __name__ == "__main__":
    main()
