from pathlib import Path


def detect_stack(repo_path: Path) -> dict:
    """
    Deterministic detection (no LLM).
    Returns a dict with language/tooling guesses.
    """
    files = {p.name for p in repo_path.rglob("*") if p.is_file()}

    stack = {
        "language": "unknown",
        "package_manager": "unknown",
        "test_tool": "unknown",
    }

    # Node
    if "package.json" in files:
        stack["language"] = "javascript/typescript"
        # lockfile heuristic
        if "pnpm-lock.yaml" in files:
            stack["package_manager"] = "pnpm"
        elif "yarn.lock" in files:
            stack["package_manager"] = "yarn"
        else:
            stack["package_manager"] = "npm"
        stack["test_tool"] = "npm test"

    # Python
    if "pyproject.toml" in files or "requirements.txt" in files or "setup.py" in files:
        stack["language"] = "python"
        stack["package_manager"] = "pip"
        stack["test_tool"] = "pytest"  # best guess; may be updated by context

    # Go
    if "go.mod" in files:
        stack["language"] = "go"
        stack["package_manager"] = "go"
        stack["test_tool"] = "go test ./..."

    # Rust
    if "Cargo.toml" in files:
        stack["language"] = "rust"
        stack["package_manager"] = "cargo"
        stack["test_tool"] = "cargo test"

    return stack
