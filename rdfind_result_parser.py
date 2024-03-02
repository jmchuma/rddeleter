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
    """ Reads and processes lines from a rdfind result file.

    Call set_env() to set the environment.
    Reads the content of the rdfind result file, grouping sets of duplicates,
    and feeds them to process_block.
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


def exec_delete(dups, indexes=(), method="trash"):
    """Delete files using the given method.

    :param dups: list of duplicates to delete
    :param indexes: the indexes from dups that should be deleted. If empty,
    deletes all files in dups.
    :param method: the method to delete files. Possible values are rm and trash.
    :return: a list of the remaining files.
    """
    if indexes:  # delete many
        if method == "rm":
            for i in indexes:
                print(f"rm {dups[int(i)][7]}")
        else:  # trash
            for i in indexes:
                print(f"trash {dups[int(i)][7]}")
    else:
        if method == "rm":
            for line in dups:
                print(f"rm {line[7]}")
        else:  # trash
            for line in dups:
                print(f"trash {line[7]}")

    return dups


def menu_delete():
    """Ask how to delete files.

    :return: a str with the selected option.
    """
    while True:
        print("Do you want to…")
        print("[1] delete permanently")
        print("[2] move to trash")
        print("[3] abort")
        print("[4] quit")
        ans = input("> ").strip()
        if ans in ("1", "2", "3", "4"):
            return ans
        else:
            print(f"{ans} is not a valid option.")
            print("Valid options are 1, 2, 3, or 4.")


def menu_listdups():
    """
    Displays main menu.
    :return: the user selection
    """
    while True:
        print("Whaddaya wanna do?")
        print("[1] Display next sub block")
        print("[2] Display next block")
        print("[3] Swap main file with a duplicate in sub block")
        print("[4] Remove SOME duplicates in sub block")
        print("[5] Remove ALL duplicates")
        print("[6] Remove original and ALL duplicates")
        print("[7] Exit")
        ans = input("> ").strip()
        if ans in ("1", "2", "3", "4", "5", "6", "7"):
            return ans
        else:
            print(f"{ans} is not a valid option.")
            print("Valid options are 1, 2, 3, 4, 5, 6, or 7.")


def menu_select_dups(dups, multi=False):
    """Displays a menu with action to select duplicates.

    :param dups: a list of duplicates. Each element if a list with information
    of a file.
    :param multi: if true, can select many, if false (default) only one.
    :return: a list with the selected options or ["ALL"].
    """
    valid = [str(x) for x in range(len(dups))]
    valid.append("ABORT")
    if multi:
        valid.append("ALL")

    while True:
        for index, dup in enumerate(dups):
            print(f"[{index}] {dup[7]}")

        if multi:
            opts = input("Enter a space separated list of indexes, ALL, or ABORT > ").strip().split()
            if not opts:  # no option selected
                continue
            # just in case there are repeated options
            # TODO do I need a list for choices or is a set OK?
            opts = list(set(opts))

            bad_opts = []
            for o in opts:
                if o not in valid:
                    bad_opts.append(o)

            if bad_opts:
                if len(bad_opts) == 1:
                    print(f"{bad_opts[0]} is not valid option.")
                else:
                    print(f"{bad_opts} are not valid options.")

                print(f"Valid options are {valid}.")
            else:
                if len(opts) > 1:
                    if "ABORT" in opts:
                        while True:
                            print("ABORT takes priority over other options!!!")
                            ans = input("Abort? ").strip().lower()
                            if ans == "yes":
                                #return {"ABORT"}
                                return ["ABORT"]
                            elif ans == "no":
                                opts.remove("ABORT")
                            else:
                                print("Enter Yes or No.")
                    if "ALL" in opts:
                        while True:
                            print("ALL takes priority over other options!!!")
                            ans = input("Select all? ").strip().lower()
                            if ans == "yes":
                                #return {"ALL"}
                                return ["ALL"]
                            elif ans == "no":
                                opts.remove("ALL")
                            else:
                                print("Enter Yes or No.")

                return opts
        else:  # multi == False
            opt = input("Select a file or type ABORT > ").strip()
            if opt in valid:
                return [opt]
            else:
                print(f"{opt} is not a valid option.")
                print(f"Valid options are {valid}.")


def process_block(block):
    """
    Processes a block of duplicates.

    :param block: a list of duplicates.
    block[0] is the one considered original by rdfind.
    :return:
    """
    multiplier = 0  # to control the sub block we are in
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

        ans = menu_listdups()
        if ans == "1":    # Display next sub block
            continue
        elif ans == "2":  # Display next block
            break
        elif ans == "3":  # Swap main file with a duplicate in sub block
            index_dup = menu_select_dups(subblock)[0]
            if index_dup != "ABORT":
                index_dup = int(index_dup)
                tmp_line = block[0]
                block[0] = block[start + index_dup]
                block[start + index_dup] = tmp_line
            # show this sub block again, with the updated info
            if multiplier > 0:
                multiplier -= 1
            else:  # it's the last sub-block
                multiplier = 0
        elif ans == "4":  # Remove SOME duplicates in sub block
            indexes = menu_select_dups(subblock, True)
            print(indexes)
        elif ans == "5":  # Remove ALL duplicates
            ans = menu_delete()
            if ans == "1":  # delete permanently
                exec_delete(block[1:], method="rm")
                break  # exit loop, load next block
            elif ans == "2":  # move to trash
                exec_delete(block[1:])
                break  # exit loop, load next block
            elif ans == "3":  # abort
                # show this sub block again
                if multiplier > 0:
                    multiplier -= 1
                else:  # it's the last sub-block
                    multiplier = 0
                continue
            elif ans == "4":  # exit
                sys.exit()
        elif ans == "6":  # Remove original and ALL duplicates
            ans = menu_delete()
            if ans == "1":  # delete permanently
                exec_delete(block, method="rm")
                break  # exit loop, load next block
            elif ans == "2":  # move to trash
                exec_delete(block)
                break  # exit loop, load next block
            elif ans == "3":  # abort
                # show this sub block again
                if multiplier > 0:
                    multiplier -= 1
                else:  # it's the last sub-block
                    multiplier = 0
                continue
            elif ans == "4":  # exit
                sys.exit()
        elif ans == "7":  # Exit
            sys.exit()


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

    # open rdfind result file passed as arg
    # if no file passed as arg ask for file
    if len(sys.argv) > 2:
        rdfind_results = basedir + "/" + sys.argv[2]
    else:
        print("Enter rdfind result file.")
        rdfind_results = input("Leave empty for rdfind_result.txt: ").strip()
        if rdfind_results:
            rdfind_results = basedir + "/" + rdfind_results
        else:
            rdfind_results = basedir + "/rdfind_result.txt"

    return basedir, rdfind_results


if __name__ == "__main__":
    main()
