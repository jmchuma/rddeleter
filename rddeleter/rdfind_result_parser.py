"""Parses rdfind result file.

Arguments [result_file]
If result_file is not provided it asks for it and if it's not provided assumes
rdfind_result.txt in the current working directory.
"""


import core
import environment
import os
import sys


def main():
    """ Reads and processes lines from a rdfind result file.

    Call set_env() to set the environment.
    Reads the content of the rdfind result file, grouping sets of duplicates,
    and feeds them to process_block.
    """
    while True:
        results_path, exit_requested = menu_result_file()
        if exit_requested:
            sys.exit()

        environment.set_env(results_path)
        while True:
            try:
                block = core.load_next_block()
                if not block:
                    break

                exit_requested = process_block(block)
                if exit_requested:
                    sys.exit()
            except FileNotFoundError:
                print(f"FILE NOT FOUND: {results_path}")
                break


def menu_delete() -> str:
    """Ask how to delete files.

    :return: a str with the selected option.
    """
    while True:
        print("Do you want to…")
        print("[1] delete permanently")
        print("[2] move to trash")
        print("[3] cancel")
        ans = input("> ").strip()
        if ans in ("1", "2", "3"):
            return ans
        else:
            print(f"{ans} is not a valid option.")
            print("Valid options are 1, 2, or 3.")


def menu_listdups() -> str:
    """
    Displays main menu.
    :return: the user selection
    """
    while True:
        print("Choose an option:")
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


def menu_result_file() -> (str, bool):
    results_path = ""
    exit_requested = False

    if len(sys.argv) > 1:
        results_path = sys.argv[1]
    else:
        while True:
            print("Choose an option:")
            print("[1] Load result file")
            print("[2] Exit")
            ans = input("> ").strip()
            if ans in ("1", "2"):
                break

        if ans == "1":
            print("Enter path to rdfind result file.")
            print("Leave empty for rdfind_result.txt")
            results_path = input(f"in {os.getcwd()} > ").strip()

            if not results_path:
                results_path = f"{os.getcwd()}/rdfind_result.txt"
        elif ans == "2":  # Exit
            exit_requested = True

    return results_path, exit_requested


def menu_select_dups(dups: list[list[str]], multi: bool = False) -> str | tuple[str, ...]:
    """Displays a menu with action to select duplicates.

    :param dups: a list of duplicates. Each element if a list with information
    of a file.
    :param multi: if true, can select many, if false (default) only one.
    :return: a list with the selected options, "ALL", "CANCEL", or, if multi is
    False, a str representing a single selection.
    """
    valid = [str(x) for x in range(len(dups))]
    valid.append("CANCEL")
    if multi:
        valid.append("ALL")

    while True:
        print(f"Paths relative to: {environment.RD_BASEDIR}")
        for index, dup in enumerate(dups):
            print(f"[{index}] {dup[7]}")

        if multi:
            opts = input("Enter a space separated list of indexes, ALL, or CANCEL > ").strip().split()
            if not opts:  # no option selected
                continue
            # just in case there are repeated options
            opts = set(opts)

            bad_opts = set()
            for o in opts:
                if o not in valid:
                    bad_opts.add(o)

            if bad_opts:
                if len(bad_opts) == 1:
                    print(f"{bad_opts.pop()} is not valid option.")
                else:
                    print(f"{bad_opts} are not valid options.")

                print(f"Valid options are {valid}.")
            else:
                if len(opts) == 1:
                    if "CANCEL" in opts or "ALL" in opts:
                        return opts.pop()
                else:
                    if "CANCEL" in opts:
                        while True:
                            print("CANCEL takes priority over other options!!!")
                            ans = input("Cancel? ").strip().lower()
                            if ans == "yes":
                                return "CANCEL"
                            elif ans == "no":
                                opts.remove("CANCEL")
                            else:
                                print("Enter Yes or No.")
                    if "ALL" in opts:
                        while True:
                            print("ALL takes priority over other options!!!")
                            ans = input("Select all? ").strip().lower()
                            if ans == "yes":
                                return "ALL"
                            elif ans == "no":
                                opts.remove("ALL")
                            else:
                                print("Enter Yes or No.")

                return tuple(opts)
        else:  # multi == False
            opt = input("Select a file or type CANCEL > ").strip()
            if opt in valid:
                return opt
            else:
                print(f"{opt} is not a valid option.")
                print(f"Valid options are {valid}.")


def process_block(block: list[list[str]]) -> bool:
    """
    Processes a block of duplicates.

    :param block: a list of duplicates.
    block[0] is the one considered original by rdfind.
    :return: boolean value. If true, the uses requested to exit.
    False otherwise.
    """
    multiplier = 0  # to control the sub block we are in
    last = len(block) - 1
    while multiplier >= 0:
        print(f"Paths relative to: {environment.RD_BASEDIR}")
        print(f"Main:\n    [0] {block[0][7]}")

        start = 10 * multiplier + 1
        multiplier += 1
        # I'm going to calculate it anyway for the if block,
        # so I may as well save it.
        end = start + 10
        if end > last:
            multiplier = -1  # end while block
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
            index_dup = menu_select_dups(subblock)
            if index_dup != "CANCEL":
                index_dup = int(index_dup)
                tmp = block[0]
                block[0] = block[start + index_dup]
                block[start + index_dup] = tmp
                # swap the duptype too
                tmp = block[0][0]
                block[0][0] = block[start + index_dup][0]
                block[start + index_dup][0] = tmp
        elif ans == "4":  # Remove SOME duplicates in sub block
            indexes = menu_select_dups(subblock, True)
            if indexes == "CANCEL":
                continue
            elif indexes == "ALL":
                indexes = ()
            else:
                # add start to the indexes in the sub-block
                # to delete the right elements
                indexes = tuple(start + int(x) for x in indexes)

            ans = menu_delete()
            if ans == "1":  # delete permanently
                block = core.delete_dups(block, indexes, "rm")
                last = len(block) - 1
            elif ans == "2":  # move to trash
                block = core.delete_dups(block, indexes)
                last = len(block) - 1
            # elif ans == "3":  # cancel
            #    pass  # do nothing to show this sub block again
        elif ans == "5":  # Remove ALL duplicates
            ans = menu_delete()
            if ans == "1":  # delete permanently
                core.delete_dups(block[1:], cmd="rm")
                break  # exit loop, load next block
            elif ans == "2":  # move to trash
                core.delete_dups(block[1:])
                break  # exit loop, load next block
            # elif ans == "3":  # cancel
            #    pass  # do nothing to show this sub block again
        elif ans == "6":  # Remove original and ALL duplicates
            ans = menu_delete()
            if ans == "1":  # delete permanently
                core.delete_dups(block, cmd="rm")
                break  # exit loop, load next block
            elif ans == "2":  # move to trash
                core.delete_dups(block)
                break  # exit loop, load next block
            # elif ans == "3":  # cancel
            #    pass  # do nothing to show this sub block again
        elif ans == "7":  # Exit
            return True  # exit script

        # show this sub block again
        if multiplier > 0:
            multiplier -= 1
        else:  # it's the last sub-block
            multiplier = 0

    return False  # keep the script running


if __name__ == "__main__":
    main()
