from pathlib import Path


def list_repo_files(repo_path: Path):
    return sorted([p for p in repo_path.rglob("*") if p.is_file()])


def read_text_safely(path: Path, max_chars: int = 50_000) -> str:
    try:
        data = path.read_text(encoding="utf-8", errors="ignore")
        if len(data) > max_chars:
            return data[:max_chars] + "\n\n...[TRUNCATED]..."
        return data
    except Exception:
        return ""


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> None:
    ensure_parent(path)
    path.write_text(content, encoding="utf-8", errors="ignore")
