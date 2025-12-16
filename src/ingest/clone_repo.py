import re
from pathlib import Path

from src.utils.run_cmd import run_cmd
from src.utils.log import log


def _repo_dir_name(url: str) -> str:
    # supports: https://github.com/owner/repo or .../repo.git
    m = re.search(r"github\.com/([^/]+)/([^/]+?)(?:\.git)?$", url.strip())
    if not m:
        return "repo"
    owner, repo = m.group(1), m.group(2)
    return f"{owner}__{repo}"


def clone_repo(url: str, workspace: Path) -> Path:
    repo_dir = workspace / _repo_dir_name(url)

    if repo_dir.exists():
        log.warn(f"Repo folder already exists. Pulling latest: {repo_dir}")
        run_cmd(["git", "-C", str(repo_dir), "pull"], check=False)
        return repo_dir

    run_cmd(["git", "clone", "--depth", "1", url, str(repo_dir)], check=True)
    return repo_dir
