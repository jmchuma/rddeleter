"""rddeleter core functions.

"""


import environment


current_line = 0


def delete_dups(dups: list[list[str]], indexes: tuple[int, ...] = (), cmd: str = "trash") -> list[list[str]]:
    """Delete files using the given method.

    :param dups: list of duplicates to delete.
    :param indexes: the indexes from dups that should be deleted. If empty,
    deletes all files in dups.
    :param cmd: the method to delete files. Possible values are rm and trash.
    :return: a list of the remaining files.
    """
    if indexes:  # delete some
        # Reversing indexes to delete the higher indexes first.
        # Avoids deleting the wrong element or getting an IndexError
        # because a lower index was previously deleted in the loop.
        for i in sorted(indexes, reverse=True):
            print(f"{cmd} {dups[i][7]}")
            del dups[i]
    else:  # delete all
        for line in dups:
            print(f"{cmd} {line[7]}")
        dups.clear()

    return dups


def load_next_block() -> list[list[str]]:
    """ Load next block from current result file.

    :return: a list representing the information of each file. It's represented
    as a list of lists of strs.
    """

    with open(environment.RD_RESULTS, "r") as file_in:
        block = []
        global current_line

        for pos, line in enumerate(file_in):
            if pos < current_line:
                continue

            current_line += 1
            line = line.strip()
            if line.startswith("#") or not line:
                continue

            line = line.split(maxsplit=7)
            if line[0] == "DUPTYPE_FIRST_OCCURRENCE" and len(block) != 0:
                current_line -= 1
                break

            block.append(line)

    return block
