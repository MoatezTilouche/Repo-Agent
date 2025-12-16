from pathlib import Path

from src.llm.client import llm_chat
from src.llm.prompts import README_SYSTEM
from src.utils.fs import write_text
from src.utils.log import log


def generate_readme_file(repo_path: Path, context: dict, model: str) -> None:
    user_msg = {
        "role": "user",
        "content": (
            "Write a README.md for this repository using ONLY this context.\n\n"
            f"REPO CONTEXT JSON:\n{context}\n"
        ),
    }

    content = llm_chat(model=model, messages=[{"role": "system", "content": README_SYSTEM}, user_msg])
    if not content.strip():
        log.warn("README generation produced empty output; skipping write.")
        return

    write_text(repo_path / "README.md", content)
