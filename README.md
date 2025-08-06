# Demo Application

A Python project for coding exercises and development.

## Setup for Development

This project has dependencies with specific hardware requirements (e.g., PyTorch). To ensure a smooth setup on any machine, follow this two-step process.

1.  **Create the virtual environment:**
    ```bash
    uv venv
    ```

2.  **Install PyTorch Separately:**
    This command lets PyTorch's installer find the correct version for your specific hardware (Intel Mac, Apple Silicon, Windows, Linux, etc.).
    ```bash
    uv pip install torch --index-url https://download.pytorch.org/whl/cpu
    ```
    *Note: We are explicitly using the CPU-only version of PyTorch, which is perfect for this project and avoids complex CUDA dependencies.*

3.  **Install the Project:**
    Now that the difficult dependency is handled, install our application and its other development tools.
    ```bash
    uv pip install -e ".[dev]"
    ```

This command will now see that a compatible version of `torch` is already installed and will proceed without errors.


## Running the Application

After setup, run the application using its console script entry point. This is the standard way to run the app and avoids any warnings.

```bash
uv run fot-recommender
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