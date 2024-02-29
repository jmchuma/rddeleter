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
