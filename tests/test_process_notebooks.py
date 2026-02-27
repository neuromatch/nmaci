import sys
import os
from subprocess import run
from pytest import fixture

from scripts.process_notebooks import (
    add_badge_cell,
    generate_badge_cell,
    remove_existing_badges,
    clean_whitespace,
    has_solution,
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


# --- Badge function tests ---
def test_remove_existing_badges_colab_only():
    """Test removing a cell with only a Colab badge."""
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "source": '<a href="https://colab.research.google.com/github/neuromatch/course/blob/main/test.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>',
            },
            {"cell_type": "code", "source": "import numpy as np"},
        ]
    }
    remove_existing_badges(nb)
    assert len(nb["cells"]) == 1
    assert nb["cells"][0]["source"] == "import numpy as np"


def test_remove_existing_badges_both():
    """Test removing a cell with both Colab and Kaggle badges."""
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "source": '<a href="https://colab.research.google.com/github/neuromatch/course/blob/main/test.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> &nbsp; <a href="https://kaggle.com/kernels/welcome?src=https://raw.githubusercontent.com/neuromatch/course/main/test.ipynb" target="_parent"><img src="https://kaggle.com/static/images/open-in-kaggle.svg" alt="Open in Kaggle"/></a>',
            },
            {"cell_type": "code", "source": "import numpy as np"},
        ]
    }
    remove_existing_badges(nb)
    assert len(nb["cells"]) == 1
    assert nb["cells"][0]["source"] == "import numpy as np"


def test_remove_existing_badges_preserves_content():
    """Test that non-badge content is preserved after badge removal."""
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "source": '# Title\n<a href="https://colab.research.google.com/github/neuromatch/course/blob/main/test.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>',
            },
        ]
    }
    remove_existing_badges(nb)
    assert len(nb["cells"]) == 1
    assert nb["cells"][0]["source"] == "# Title"


def test_remove_existing_badges_no_badges():
    """Test that cells without badges are unchanged."""
    nb = {
        "cells": [
            {"cell_type": "markdown", "source": "# Introduction"},
            {"cell_type": "code", "source": "import numpy as np"},
        ]
    }
    remove_existing_badges(nb)
    assert len(nb["cells"]) == 2
    assert nb["cells"][0]["source"] == "# Introduction"
    assert nb["cells"][1]["source"] == "import numpy as np"


def test_generate_badge_cell_structure():
    """Test that generate_badge_cell creates correct cell structure."""
    cell = generate_badge_cell("tutorials/W1D1_Intro/W1D1_Tutorial1.ipynb")

    assert cell["cell_type"] == "markdown"
    assert cell["metadata"]["id"] == "view-in-github"
    assert cell["metadata"]["colab_type"] == "text"


def test_generate_badge_cell_colab_badge():
    """Test that generate_badge_cell includes correct Colab badge."""
    cell = generate_badge_cell("tutorials/W1D1_Intro/W1D1_Tutorial1.ipynb")

    assert "colab-badge.svg" in cell["source"]
    assert "colab.research.google.com/github" in cell["source"]
    assert "tutorials/W1D1_Intro/W1D1_Tutorial1.ipynb" in cell["source"]


def test_generate_badge_cell_kaggle_badge():
    """Test that generate_badge_cell includes correct Kaggle badge."""
    cell = generate_badge_cell("tutorials/W1D1_Intro/W1D1_Tutorial1.ipynb")

    assert "open-in-kaggle.svg" in cell["source"]
    assert "kaggle.com/kernels/welcome" in cell["source"]
    assert "tutorials/W1D1_Intro/W1D1_Tutorial1.ipynb" in cell["source"]


def test_generate_badge_cell_student_path():
    """Test that generate_badge_cell works with student paths."""
    cell = generate_badge_cell("tutorials/W1D1_Intro/student/W1D1_Tutorial1.ipynb")

    assert "tutorials/W1D1_Intro/student/W1D1_Tutorial1.ipynb" in cell["source"]


def test_add_badge_cell_replaces_old_badges():
    """Test that add_badge_cell removes old badges and adds new one at top."""
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "source": '<a href="https://colab.research.google.com/github/old/path" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>',
            },
            {"cell_type": "code", "source": "import numpy as np"},
        ]
    }

    add_badge_cell(nb, "tutorials/W1D1_Intro/W1D1_Tutorial1.ipynb")

    # Should have 2 cells: new badge cell + code cell
    assert len(nb["cells"]) == 2
    # First cell should be the new badge
    assert nb["cells"][0]["metadata"]["id"] == "view-in-github"
    assert "W1D1_Intro/W1D1_Tutorial1.ipynb" in nb["cells"][0]["source"]
    # Second cell should be the code
    assert nb["cells"][1]["source"] == "import numpy as np"


def test_add_badge_cell_to_empty_notebook():
    """Test adding badge to notebook without existing badges."""
    nb = {
        "cells": [
            {"cell_type": "code", "source": "import numpy as np"},
        ]
    }

    add_badge_cell(nb, "tutorials/W1D1_Intro/W1D1_Tutorial1.ipynb")

    assert len(nb["cells"]) == 2
    assert nb["cells"][0]["metadata"]["id"] == "view-in-github"
    assert nb["cells"][1]["source"] == "import numpy as np"
