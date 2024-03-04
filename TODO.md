rdfind_result_parser.py
=======================

- Try to import and use [`trashcli`](https://pypi.org/project/trash-cli/):
    - `from trashcli.put.main import main as main`
    - `import trashcli.put as trash`
- Exit using `sys.exit(main())`

`process_block`
---------------
Add options to:

- If there are more than 10 duplicates display in blocks of 10
- Switch main file with a duplicate
- Remove all duplicates
- Remove some duplicates
- Remove all (original and duplicates)
- Ask if delete permanently or move to trash
- Log actions?
    - Use an array or dictionary of actions?
    - Write that to file for every batch?
- Store progress?
    - Update rdfind_results.txt removing or reordering files?
    - Clone file to log file and store what's done with what's left?
- Quit


Type hints and function annotations
===================================
See:
- https://docs.python.org/3/library/typing.html
- https://peps.python.org/pep-3107/


Empty list as default argument
==============================
https://stackoverflow.com/questions/366422/how-can-i-avoid-issues-caused-by-pythons-early-bound-default-parameters-e-g-m


Arguments
=========
- https://stackoverflow.com/questions/36901/what-does-double-star-asterisk-and-star-asterisk-do-for-parameters
- https://www.geeksforgeeks.org/args-kwargs-python/
- https://docs.python.org/3/tutorial/controlflow.html#more-on-defining-functions
- https://pythonsimplified.com/python-parameters-and-arguments-demystified/
