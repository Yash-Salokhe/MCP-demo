# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A minimal Python MCP (Model Context Protocol) server, built for learning MCP
architecture. It exposes one tool, `list_threads`, which returns a hardcoded
list of three thread objects (`id`, `title`). Pure code, no LLM involved —
keep it that way unless a feature genuinely requires model judgment.

## Setup

```
pip install -e ".[dev]"
```

This installs the `mcp` SDK, the package itself (editable), and `pytest`.

## Commands

- Run the server (stdio transport): `python -m mcp_demo.server`
- Run all tests: `python -m pytest`
- Run a single test: `python -m pytest tests/test_server.py::test_list_threads_function_returns_three_threads`

## Architecture

- `src/mcp_demo/server.py` — the whole server. A module-level `FastMCP("mcp-demo")`
  instance, a hardcoded `THREADS` list, and `list_threads()` registered as a
  tool via `@mcp.tool()`. `FastMCP.tool()` returns the function unchanged, so
  `list_threads()` can still be called directly as a plain function in tests —
  no protocol round-trip needed for that path.
- `tests/test_server.py` — two complementary tests:
  - one calls `list_threads()` directly (fast, pure-function check);
  - one drives the tool through a real MCP session via
    `mcp.shared.memory.create_connected_server_and_client_session`, which wires
    an in-memory client and server together without spawning a subprocess or
    touching stdio. This exercises the actual `call_tool` protocol path
    (request → `structuredContent` in the response) rather than just the
    underlying Python function.
- `pyproject.toml` uses a `src/` layout (`tool.setuptools.packages.find` with
  `where = ["src"]`) and sets `pythonpath = ["src"]` under `[tool.pytest.ini_options]`,
  so tests import `mcp_demo` without requiring the editable install — though
  `pip install -e ".[dev]"` is still what makes `python -m mcp_demo.server` work
  from anywhere.

## CI

`.github/workflows/claude-review.yaml` runs Claude as an automated PR reviewer
on every opened pull request. It explicitly reads this file and defers to its
conventions, and flags any use of an LLM/agent where plain deterministic code
would be more reliable (and vice versa) — this repo's `list_threads` tool is
a deliberate example of the deterministic-first approach.
