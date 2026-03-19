"""From a list of files, select process-able notebooks and print."""
import os
import sys

def main(arglist=None):
    if arglist is None:
        arglist = sys.argv[1:]

    # Filter paths from the git manifest
    # - Only process .ipynb
    # - Don't process student notebooks
    # - Don't process deleted notebooks
    def should_process(path):
        return all([
            path.endswith(".ipynb"),
            "student/" not in path,
            "instructor/" not in path,
            os.path.isfile(path),
        ])

    nb_paths = [f for f in arglist if should_process(f)]
    print(" ".join(nb_paths))


if __name__ == "__main__":
    main()
