from pathlib import Path
from typing import List, Tuple

from src.utils.fs import read_text_safely, list_repo_files
from src.utils.log import log


KEY_FILES = [
    "README.md",
    "README.rst",
    "README.txt",
    "package.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "pyproject.toml",
    "requirements.txt",
    "setup.py",
    "Pipfile",
    "poetry.lock",
    "go.mod",
    "Cargo.toml",
    "Makefile",
    "docker-compose.yml",
    "Dockerfile",
    ".env.example",
    "tsconfig.json",
]


def _pick_core_source_files(repo_path: Path, max_count: int = 5) -> List[Path]:
    """
    Very simple heuristic: pick a few non-test source files.
    """
    candidates = []
    for p in list_repo_files(repo_path):
        s = str(p).lower()
        if any(part in s for part in ["/.git/", "/node_modules/", "/dist/", "/build/", "/.venv/"]):
            continue
        if "/tests/" in s or "/test/" in s:
            continue
        if p.suffix.lower() in [".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs"]:
            candidates.append(p)

    # prefer likely entrypoints
    preferred = []
    for p in candidates:
        name = p.name.lower()
        if name in ["main.py", "__main__.py", "app.py", "server.py", "index.js", "index.ts"]:
            preferred.append(p)

    chosen = preferred[:max_count]
    if len(chosen) < max_count:
        for p in candidates:
            if p not in chosen:
                chosen.append(p)
            if len(chosen) >= max_count:
                break
    return chosen


def build_context(repo_path: Path, stack: dict, max_files: int, max_bytes: int) -> dict:
    """
    Builds a compact context object to send to the LLM.
    """
    all_files = list_repo_files(repo_path)
    file_tree = [str(p.relative_to(repo_path)) for p in all_files][: max_files * 5]

    picked: List[Tuple[str, str]] = []
    total = 0

    # Add key files first
    for name in KEY_FILES:
        p = repo_path / name
        if p.exists() and p.is_file():
            txt = read_text_safely(p, max_chars=35_000)
            chunk = f"--- {name} ---\n{txt}\n"
            if total + len(chunk.encode("utf-8", errors="ignore")) > max_bytes:
                continue
            picked.append((name, txt))
            total += len(chunk.encode("utf-8", errors="ignore"))

    # Add a few core source files
    for p in _pick_core_source_files(repo_path, max_count=6):
        rel = str(p.relative_to(repo_path))
        txt = read_text_safely(p, max_chars=18_000)
        chunk = f"--- {rel} ---\n{txt}\n"
        if total + len(chunk.encode("utf-8", errors="ignore")) > max_bytes:
            continue
        picked.append((rel, txt))
        total += len(chunk.encode("utf-8", errors="ignore"))

    log.info(f"Context includes {len(picked)} files, approx bytes: {total}")

    return {
        "repo_name": repo_path.name,
        "stack": stack,
        "file_tree": file_tree,
        "files": [{"path": p, "content": c} for (p, c) in picked],
    }
