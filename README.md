<h1 align="center"> Ereiarrus/beat-saber-to-auto-trip-map-converter </h1>

<p align="center">
Converts a Beat Saber map (specified through a bsr code from https://beatsaver.com/ or https://bsaber.com/) to an Audio Trip map that gets created straight in your Audio Trip maps folder
</p>

<div align="center">

![Python Boilerplate](https://img.shields.io/badge/python-3.10+-blue.svg)
![uv](https://img.shields.io/badge/uv-0.7.13-purple.svg)
![Docker](https://img.shields.io/badge/docker-enabled-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
<!-- [![GitHub Actions Status](https://github.com/monok8i/python-boilerplate/actions/workflows/code-quality.yml/badge.svg)](https://github.com/monok8i/python-boilerplate/actions/workflows/code-quality.yml) -->
[![GitHub Actions Status](https://github.com/Ereiarrus/beat-saber-to-auto-trip-map-converter/actions/workflows/code-quality.yml/badge.svg)](https://github.com/monok8i/python-boilerplate/actions/workflows/code-quality.yml)
<!-- [![GitHub Actions Status](https://github.com/monok8i/python-boilerplate/actions/workflows/codeql.yml/badge.svg)](https://github.com/monok8i/python-boilerplate/actions/workflows/codeql.yml) -->
[![GitHub Actions Status](https://github.com/Ereiarrus/beat-saber-to-auto-trip-map-converter/actions/workflows/codeql.yml/badge.svg)](https://github.com/monok8i/python-boilerplate/actions/workflows/codeql.yml)
</div>


## 🚀 Features

- **Python 3.10+**
- **[uv](https://docs.astral.sh/uv/)** — Ultra-fast Python package installer and dependency resolver
- **[Docker Support](https://docs.docker.com/)** — Multi-stage Dockerfiles for both local development and clean production containers
- **[GitHub Actions CI/CD](https://docs.github.com/en/actions)** — Automated pipelines for code quality checks, testing, security scanning, and Python compatibility validation
- **[Dev Containers](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers)** — Pre-configured development environment for codespaces or remote development
- **[Code Quality Tools](https://docs.astral.sh/ruff/)** — Integrated linting and formatting with [Ruff](https://docs.astral.sh/ruff/), static type checking with [MyPy](https://mypy.readthedocs.io/en/stable/), comprehensive testing with [Pytest](https://docs.pytest.org/en/stable/) and checking minimal Python version to run your code (without dependencies) with [Vermin](https://github.com/netromdk/vermin)
- **[Pre-commit Hooks](https://pre-commit.com/)** — Automated code quality enforcement (linting, formatting, and tests before every commit)
- **[Commitizen](https://commitizen-tools.github.io/commitizen/)** — Standardized commit messages and automated changelog/versioning
- **Environment Management** — Stage-based configuration system supporting development and production environments
- **[MkDocs Documentation](https://www.mkdocs.org/)** — Documentation with Material theme and automated generation
- **[Makefile Automation](https://www.gnu.org/software/make/)** — Simplified command interface for common development tasks
- **[Python Template](https://github.com/python-boilerplate/uv-template)** — Boilerpalte taken from monok8i's python boilerplate repo.


## ⚡ Quick Start

- **Initialize the project:**
   ```bash
   make init
   ```

- **Run the application:**
   ```bash
   make run
   ```

- **Linting:**
   ```bash
   make lint
   ```

- **Type checking:**
   ```bash
   make typecheck
   ```

- **Formatting:**
   ```bash
   make format
   ```

- **Run the tests:**
   ```bash
   make test
   ```

- **To check the docs:**
   ```bash
   uv run mkdocs serve
   ```
---

### Development Options:

1. **Local Development:**
   Use `uv` and Makefile for local development without containers.

3. **GitHub Codespaces:**
   Launch in [GitHub Codespaces](https://github.com/features/codespaces) for instant cloud-based development with pre-configured devcontainer support.

## 📚 Documentation

<!--
Note: This link will work once you enable GitHub Pages for your repository. To set it up:
1. Go to your repository settings on GitHub
2. Navigate to Pages in the left sidebar
3. Under "Source", select the branch where your MkDocs build output is (usually gh-pages or main if you build docs there)
4. Save the settings
-->
<!-- **For detailed guides and advanced scenarios, see the [full documentation](https://python-boilerplate.github.io/uv-template/).** -->
**More details: [full documentation](https://ereiarrus.github.io/beat-saber-to-auto-trip-map-converter/).**

## TODO

Ordered highest priority to lowest; numbers are just for referencing the TODOs in the codebase. Conversions are marked with a 'c': ([more info](docs/conversion-format.md))
- (c2) add conversions for walls
- (c4) add support for directional notes to directional gems (optionally toggleable by the player)
- (c11) add conversions for bombs to walls (optionally toggleable by the player)
- (5) what is the 'beats_per_measure' variable? can we un-hardcode it?
- (c3) add conversion for stacks/sliders/windows to drums
- (c10) convert chains to ... something...? maybe just more gems? or rails? player can toggle between rails/gems?
- (c8) convert poodles to rails
- (6) what is "spawnAheadTime"? Is this AT's equivalent for JD (jump distance)? Can we un-hardcode it? Should we allow the player to modify it, as in BS, JDFixer lets you change it?
- (c1) add support for >4 lane maps
- (c9) convert arcs to AT's arcs thingy (which are barely visible in AT)
- (7) "gemSpeed" vs. njs: is the mapping just a constant multiplier away, as it is coded up, or is it different? Should the player have control over this, or no, since in BS, you cannot control it?
