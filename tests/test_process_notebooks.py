import sys
import os
from subprocess import run
from pytest import fixture

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scripts.process_notebooks import (
    clean_whitespace,
    has_solution,
    has_colab_badge,
    redirect_colab_badge_to_main_branch,
    redirect_colab_badge_to_student_version,
    ORG,
    REPO,
    MAIN_BRANCH,
)


@fixture
def cmd():
    return ["python", "scripts/process_notebooks.py"]


def test_raises_not_implemented_error(cmd):

    nb = "tutorials/raises_notimplemented_error.ipynb"
    cmdline = cmd + ["--check-only", "--execute", nb]
    res = run(cmdline, capture_output=True)
    assert not res.returncode
    assert nb in res.stdout.decode("utf-8")


def test_raises_name_error(cmd):

    nb = "tutorials/raises_name_error.ipynb"
    cmdline = cmd + ["--check-only", "--execute", nb]
    res = run(cmdline, capture_output=True)
    assert res.returncode
    assert nb in res.stdout.decode("utf-8")
    assert nb in res.stderr.decode("utf-8")
    assert "NameError" in res.stderr.decode("utf-8")


def test_executed_out_of_order(cmd):

    nb = "tutorials/executed_out_of_order.ipynb"
    cmdline = cmd + ["--check-only", nb]
    res = run(cmdline, capture_output=True)
    assert res.returncode
    assert nb in res.stderr.decode("utf-8")
    assert "not sequentially executed" in res.stderr.decode("utf-8")


def test_executed_partially(cmd):

    nb = "tutorials/executed_partially.ipynb"
    cmdline = cmd + ["--check-only", "--check-execution", nb]
    res = run(cmdline, capture_output=True)
    assert res.returncode
    assert nb in res.stderr.decode("utf-8")
    assert "has unexecuted code cell(s)" in res.stderr.decode("utf-8")


def test_executed_with_error(cmd):

    nb = "tutorials/executed_with_error.ipynb"
    cmdline = cmd + ["--check-only", "--check-execution", nb]
    res = run(cmdline, capture_output=True)
    assert res.returncode
    assert nb in res.stderr.decode("utf-8")
    assert "NameError" in res.stderr.decode("utf-8")


def test_executed_successfully(cmd):

    nb = "tutorials/executed_successfully.ipynb"
    cmdline = cmd + ["--check-only", "--check-execution", nb]
    res = run(cmdline, capture_output=True)
    assert not res.returncode
    assert nb in res.stdout.decode("utf-8")


# --- Unit tests extracted from scripts/process_notebooks.py ---


def test_clean_whitespace():

    nb = {
        "cells": [
            {"cell_type": "code", "source": "import numpy  \nimport matplotlib   "},
            {"cell_type": "markdown", "source": "# Test notebook  "},
        ]
    }
    clean_whitespace(nb)
    assert nb["cells"][0]["source"] == "import numpy\nimport matplotlib"
    assert nb["cells"][1]["source"] == "# Test notebook  "


def test_has_solution():

    cell = {"source": "# solution"}
    assert not has_solution(cell)

    cell = {"source": "def exercise():\n    pass\n# to_remove"}
    assert not has_solution(cell)

    cell = {"source": "# to_remove_solution\ndef exercise():\n    pass"}
    assert has_solution(cell)


def test_has_colab_badge():

    cell = {"source": "import numpy as np"}
    assert not has_colab_badge(cell)

    cell = {
        "source": '<img src="https://colab.research.google.com/assets/colab-badge.svg" '
    }
    assert has_colab_badge(cell)


def test_redirect_colab_badge_to_main_branch():

    original = (
        f'"https://colab.research.google.com/github/{ORG}/'
        f"{REPO}/blob/W1D1-updates/tutorials/W1D1_ModelTypes/"
        'W1D1_Tutorial1.ipynb"'
    )
    cell = {"source": original}
    redirect_colab_badge_to_main_branch(cell)

    expected = (
        f'"https://colab.research.google.com/github/{ORG}/'
        f"{REPO}/blob/{MAIN_BRANCH}/tutorials/W1D1_ModelTypes/"
        'W1D1_Tutorial1.ipynb"'
    )

    assert cell["source"] == expected


def test_redirect_colab_badge_to_student_version():

    original = (
        f'"https://colab.research.google.com/github/{ORG}/'
        f"{REPO}/blob/{MAIN_BRANCH}/tutorials/W1D1_ModelTypes/"
        'W1D1_Tutorial1.ipynb"'
    )

    cell = {"source": original}
    redirect_colab_badge_to_student_version(cell)

    expected = (
        f'"https://colab.research.google.com/github/{ORG}/'
        f"{REPO}/blob/{MAIN_BRANCH}/tutorials/W1D1_ModelTypes/student/"
        'W1D1_Tutorial1.ipynb"'
    )

    assert cell["source"] == expected
