from pathlib import Path
from pyexpat import model

from src.llm.client import llm_chat
from src.llm.prompts import TESTS_SYSTEM
from src.utils.json_safe import parse_json_filemap
from src.utils.fs import write_text, ensure_parent
from src.utils.log import log


def generate_test_files(repo_path: Path, context: dict, model: str) -> None:
    user_msg = {
        "role": "user",
        "content": (
            "Generate test files for this repository.\n"
            "Return JSON mapping file paths to contents.\n\n"
            f"REPO CONTEXT JSON:\n{context}\n"
        ),
    }

    raw = llm_chat(model=model, messages=[{"role": "system", "content": TESTS_SYSTEM}, user_msg], force_json=True)

    filemap = parse_json_filemap(raw)
    if not filemap:
        log.warn("No test files returned by LLM.")
        return

    for rel_path, content in filemap.items():
        target = repo_path / rel_path
        ensure_parent(target)
        write_text(target, content)

    log.success(f"Wrote {len(filemap)} test/config files.")
