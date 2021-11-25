import os
import sys
import argparse
from variable import Variable
from helper import set_verbosity, verboseprint, get_file_content, write_content_to_file

ACCEPTED_EXTENSIONS = ["c"]

def get_arguments():
    parser = argparse.ArgumentParser(
        prog="CVarMan",
        description='C Variable Manipulator', 
    )

    parser.add_argument("source", type=str, help="c source file")
    parser.add_argument("-o", "--output", help="output filepath")
    parser.add_argument("-v", "--verbose", help="enable verbosity", action="store_true")
    parser.add_argument("-t", "--test", help="enable test mode", action="store_true")

    subparsers = parser.add_subparsers(title="subcommand", dest="subcommand", required=('-t' not in sys.argv and '--test' not in sys.argv))
    append_command = subparsers.add_parser("append", aliases=["ap"])
    append_command.add_argument("append_text")

    return parser.parse_args()

def check_extension(sourcefile: str):
    extension = sourcefile.split(".")[::-1][0] 
    if extension not in ACCEPTED_EXTENSIONS:
        print(f"[ERROR] extension .{extension} not accepted")
        print(f"        accepted extensions: {', '.join([f'.{ext}' for ext in ACCEPTED_EXTENSIONS])}")
        exit(1)

def write_source_code(sourcefile, sourcecode: str, command: str, output: str = None):
    basename = os.path.basename(sourcefile)
    name, ext = os.path.splitext(basename)
    tempfilename = f"{name}.{command}{ext}"
    
    if not output:
        output = tempfilename
    elif os.path.isdir(output):
        output = os.path.join([output, tempfilename])
    elif os.path.exists(output):
        response = input(f"[INFO] file {output} exists. Do you want to override it? (Y/N) ")
        if response.lower() == "n":
            return

    print(f"[INFO] writing output to {output}")
    
    write_content_to_file(output, sourcecode)

def test(sourcecode: str):
    set_verbosity(True)
    print("[INFO] running test mode")
    print("[INFO] source code")
    print(sourcecode)
    print("[INFO] testing get_all_string_literals()")
    string_literals = Variable.get_all_string_literals(sourcecode)

    for s, start, end in string_literals:
        print(f"'{s}': {start}, {end}")

    print("[INFO] testing append_to_all_variable_name()")
    print(Variable.append_to_all_variable_name(sourcecode, "_770"))

def main():
    arguments = get_arguments()
    
    set_verbosity(arguments.verbose)

    sourcefile = arguments.source
    check_extension(sourcefile)
    sourcecode = get_file_content(sourcefile)

    if arguments.test:
        test(sourcecode)
        return

    subcommand = arguments.subcommand

    if subcommand == "append":
        append = arguments.append_text
        verboseprint(f"[INFO] appending '{append}' to all variables in the source code")
        new_sourcecode = Variable.append_to_all_variable_name(sourcecode, append)

        write_source_code(sourcefile, new_sourcecode, "append", arguments.output)

if __name__ == "__main__":
    main()
