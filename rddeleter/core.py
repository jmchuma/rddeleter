"""rddeleter core functions.

"""


import environment


current_line = 0


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
                current_line -=1
                break

            block.append(line)

    return block
