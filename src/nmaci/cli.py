"""Single entry point for the nmaci CLI."""
import sys


COMMANDS = {
    "process-notebooks":        "nmaci.process_notebooks",
    "verify-exercises":         "nmaci.verify_exercises",
    "lint-tutorial":            "nmaci.lint_tutorial",
    "make-pr-comment":          "nmaci.make_pr_comment",
    "extract-links":            "nmaci.extract_links",
    "generate-readmes":         "nmaci.generate_tutorial_readmes",
    "generate-book":            "nmaci.generate_book",
    "generate-book-dl":         "nmaci.generate_book_dl",
    "generate-book-precourse":  "nmaci.generate_book_precourse",
    "select-notebooks":         "nmaci.select_notebooks",
    "find-unreferenced":        "nmaci.find_unreferenced_content",
    "parse-html":               "nmaci.parse_html_for_errors",
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("Usage: nmaci <command> [args]")
        print("Commands:", ", ".join(COMMANDS))
        sys.exit(1)
    import importlib
    module = importlib.import_module(COMMANDS[sys.argv[1]])
    module.main(sys.argv[2:])
