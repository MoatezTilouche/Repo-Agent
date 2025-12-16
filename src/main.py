import argparse
from pathlib import Path

from src.utils.log import log
from src.ingest.clone_repo import clone_repo
from src.analysis.detect_stack import detect_stack
from src.analysis.build_context import build_context

from src.generate.readme import generate_readme_file
from src.generate.tests import generate_test_files
from src.generate.scripts import generate_script_files

from src.utils.validate import validate_repo


def parse_args():
    p = argparse.ArgumentParser(description="Repo-to-README+tests agent (Ollama local).")
    p.add_argument("--repo", required=True, help="GitHub repo URL (https://github.com/owner/repo)")
    p.add_argument("--model", default="llama3.1:8b", help="Ollama model name (e.g. llama3.1:8b)")
    p.add_argument("--workspace", default="workspace", help="Workspace folder")
    p.add_argument("--max-files", type=int, default=40, help="Max files to include in context")
    p.add_argument("--max-bytes", type=int, default=120_000, help="Max total bytes read into context")
    p.add_argument("--no-scripts", action="store_true", help="Do not generate scripts/")
    p.add_argument("--no-validate", action="store_true", help="Do not run tests after generation")
    return p.parse_args()


def main():
    args = parse_args()

    workspace = Path(args.workspace).resolve()
    workspace.mkdir(parents=True, exist_ok=True)

    log.info(f"Cloning: {args.repo}")
    repo_path = clone_repo(args.repo, workspace)

    log.info("Detecting stack...")
    stack = detect_stack(repo_path)
    log.info(f"Detected stack: {stack}")

    log.info("Building LLM context...")
    context = build_context(
        repo_path=repo_path,
        stack=stack,
        max_files=args.max_files,
        max_bytes=args.max_bytes,
    )

    log.info("Generating README.md...")
    generate_readme_file(repo_path, context, model=args.model)

    log.info("Generating tests/...")
    generate_test_files(repo_path, context, model=args.model)

    if not args.no_scripts:
        log.info("Generating scripts/...")
        generate_script_files(repo_path, context, model=args.model)

    if not args.no_validate:
        log.info("Validating (running tests best-effort)...")
        validate_repo(repo_path, stack)

    log.success(f"Done. Repo located at: {repo_path}")


if __name__ == "__main__":
    main()
