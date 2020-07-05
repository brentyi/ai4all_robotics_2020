START_DELETE_TOKEN = "# ~~START DELETE~~"
END_DELETE_TOKEN = "# ~~END DELETE~~"
DELETE_LINE_TOKENS = ("# ~~DELETE LINE~~", "# fmt: off", "# fmt: on")
WARNING_TOKEN = "~~"
CODE_TAG_START = "# ***** Start of your code *****"
CODE_TAG_END = "# ***** End of your code *****"

__doc__ = f"""
Helper script for processing assignment scripts/notebooks for release as "starter code".
Based on infrastructure from cs231n.

Takes code that looks like this:
```
def fizzbuzz(max):
    print("Line to delete") {DELETE_LINE_TOKENS[0]}
    for i in range(max):
        {START_DELETE_TOKEN}
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        {END_DELETE_TOKEN}
```

And outputs:
```
def fizzbuzz(max):
    for i in range(max):
        {CODE_TAG_START}
        raise NotImplementedError()
        {CODE_TAG_END}
```

For notebooks, we also (a) reset execution counts and (b) clear all outputs.

"""

import argparse
import json


def handle_code(in_code, is_code=True):
    """
    Remove tagged lines from source code.
    Inputs:
    - in_code: List of lines of source code
    Returns: Tuple of:
    - List of lines of source code
    - Number of source code lines removed
    """
    out_code = []
    lines_removed = 0
    skip_block = False
    for line_num, line in enumerate(in_code):
        # Keep track if the line matches any tokens
        matched = False

        # Check if we are at the start of a delete block
        if line.strip().startswith(START_DELETE_TOKEN):
            skip_block = True
            matched = True
            lines_removed -= 1
            if is_code:
                num_spaces = len(line) - len(line.lstrip(" "))
                out_code.append(num_spaces * " " + CODE_TAG_START + "\n")

        # Check if we should skip this line
        skip_line = False
        for token in DELETE_LINE_TOKENS:
            if line.strip().endswith(token):
                skip_line = True
                matched = True

        # Maybe output the line
        if not skip_block and not skip_line:
            out_code.append(line)
        else:
            lines_removed += 1

        # Check to see if we are at the end of a delete block
        if line.strip().startswith(END_DELETE_TOKEN):
            matched = True
            skip_block = False
            # When we hit the end of a skip block, insert a pass
            # at the correct indentation level.
            num_spaces = len(line) - len(line.lstrip(" "))
            if is_code:
                out_code.append(num_spaces * " " + "raise NotImplementedError()\n")
                out_code.append(num_spaces * " " + CODE_TAG_END + "\n")

        # If the line did not match any tokens but contains the warning token
        # then there was probably a typo in the input file; issue a warning.
        if not matched and WARNING_TOKEN in line:
            print("WARNING: line %d:" % (line_num + 1))
            print(line)
            print()
            # assert False

    # Remove trailing line breaks
    if out_code[-1][-1] == "\n":
        out_code[-1] = out_code[-1][:-1]

    return (out_code, lines_removed)


def handle_notebook_file(in_path, out_path):
    total_lines_removed = 0
    with open(in_path, "r") as in_file:
        notebook = json.load(in_file)
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            in_code = cell["source"]
            out_code, lines_removed = handle_code(in_code)
            total_lines_removed += lines_removed
            cell["source"] = out_code
            cell["outputs"] = []
            cell["execution_count"] = None
        elif cell["cell_type"] == "markdown":
            in_source = cell["source"]
            out_source, _ = handle_code(in_source, is_code=False)
            cell["source"] = out_source
    with open(out_path, "w") as out_file:
        json.dump(notebook, out_file, indent=1)
    return total_lines_removed


def handle_python_file(in_path, out_path):
    with open(in_path, "r") as in_file:
        in_code = in_file.readlines()
    out_code, lines_removed = handle_code(in_code)
    with open(out_path, "w") as out_file:
        for line in out_code:
            out_file.write(line)
    return lines_removed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "in_path", type=str, help="Input path. Should end in *.py or *.ipynb."
    )
    parser.add_argument(
        "out_path",
        type=str,
        help="Output path. File extension should match input path.",
    )
    args = parser.parse_args()

    # Validate inputs
    extension = args.in_path.rpartition(".")[-1]
    assert extension == args.out_path.rpartition(".")[-1], "File extensions must match!"
    assert args.in_path != args.out_path, "Input/output paths should be unique!"

    # Parse
    if extension == "py":
        handle_python_file(args.in_path, args.out_path)
    elif extension == "ipynb":
        handle_notebook_file(args.in_path, args.out_path)
    else:
        assert False, "Invalid file extension"
