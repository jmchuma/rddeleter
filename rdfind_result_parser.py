"""
"""



def main():
    """
    """
    # if base dir is not provided assume basedir is cwd

    # if ouput file not provided assume rdfind_result_parser.txt

    # open rdfind result file passed as arg
    # if no file passed as arg ask for file

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
    pass


if __name__ == "__main__":
    main()
