# nmaci
[![CI](https://github.com/OleBialas/nmaci/actions/workflows/ci.yaml/badge.svg)](https://github.com/OleBialas/nmaci/actions/workflows/ci.yaml)
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
Automated tools for building and verifying NMA tutorial materials.

## Installation

```bash
pip install git+https://github.com/OleBialas/nmaci@main
```

## Usage

```
nmaci <command> [args]
```

| Command | Description |
|---|---|
| `process-notebooks` | Execute notebooks, extract solutions, create student/instructor versions |
| `verify-exercises` | Check exercise cells match solution cells |
| `lint-tutorial` | Run flake8/pyflakes over notebook code cells |
| `generate-readmes` | Auto-generate tutorial `README.md` files |
| `generate-book` | Build Jupyter Book from `materials.yml` |
| `generate-book-dl` | Build Jupyter Book (Deep Learning variant) |
| `generate-book-precourse` | Build Jupyter Book (Precourse variant) |
| `select-notebooks` | Filter which notebooks to process |
| `make-pr-comment` | Generate PR comment with Colab badges and lint report |
| `find-unreferenced` | Identify unused solution images/scripts |
| `extract-links` | Extract video/slide links from notebooks |
| `parse-html` | Check HTML build output for errors |

## Development

```bash
git clone https://github.com/OleBialas/nmaci
cd nmaci
uv sync --extra dev
uv run pytest tests/
```

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/iamzoltan"><img src="https://avatars.githubusercontent.com/u/21369773?v=4?s=100" width="100px;" alt="Zoltan"/><br /><sub><b>Zoltan</b></sub></a><br /><a href="https://github.com/neuromatch/nmaci/commits?author=iamzoltan" title="Code">💻</a> <a href="https://github.com/neuromatch/nmaci/commits?author=iamzoltan" title="Tests">⚠️</a> <a href="#maintenance-iamzoltan" title="Maintenance">🚧</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/OleBialas"><img src="https://avatars.githubusercontent.com/u/38684453?v=4?s=100" width="100px;" alt="Ole Bialas"/><br /><sub><b>Ole Bialas</b></sub></a><br /><a href="https://github.com/neuromatch/nmaci/commits?author=OleBialas" title="Code">💻</a> <a href="#maintenance-OleBialas" title="Maintenance">🚧</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!