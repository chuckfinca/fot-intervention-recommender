# Demo Application

A Python project for coding exercises and development.

## Setup for Development

This is the standard setup for working on this project. It will install the application and all the necessary development tools (pytest, black, etc.).

1. **Create the virtual environment:**
   ```bash
   uv venv
   ```

2. **Install the project in editable mode with development dependencies:**
   ```bash
   uv pip install -e ".[dev]"
   ```
   This command installs the project, all development tools (like pytest and black), and creates the demo-app command-line script.


## Running the Application

After setup, run the application using its console script entry point. This is the standard way to run the app and avoids any warnings.

```bash
uv run demo-app
```

## Development Tools

After setting up for development, you can use the following tools.

**Run Tests:**
```bash
uv run pytest
```

**Format Code:**
```bash
uv run black .
```

**Lint Code:**
```bash
uv run ruff check .
```

**Type Checking:**
```bash
uv run mypy src/
```

## Project Structure

```
src/demo_application/    # Main package
tests/                   # Test files
pyproject.toml          # Project configuration
```