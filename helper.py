class ApplicationConstants:
    verbosity = False

def set_verbosity(state: bool):
    if state:
        print("[INFO] verbosity is turned on")
        ApplicationConstants.verbosity = True

def verboseprint(*args, **kwargs):
    if ApplicationConstants.verbosity:
        print(*args, **kwargs)

def get_file_content(filepath: str) -> str:
    try:
        with open(filepath) as fd:
            return fd.read()
    except FileNotFoundError:
        print(f"[ERROR] file {filepath} not found")
        exit(1)

def write_content_to_file(filepath: str, content: str):
    try:
        with open(filepath, "w+") as fd:
            fd.write(content)
    except FileExistsError:
        print(f"[ERROR] file '{filepath}' exists")
        exit(1)