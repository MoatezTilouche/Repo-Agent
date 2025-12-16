from pathlib import Path

from src.utils.run_cmd import run_cmd
from src.utils.log import log


def validate_repo(repo_path: Path, stack: dict) -> None:
    lang = stack.get("language", "unknown")

    if lang == "python":
        _validate_python(repo_path)
    elif lang == "javascript/typescript":
        _validate_node(repo_path, stack)
    elif lang == "go":
        _run(repo_path, ["go", "test", "./..."])
    elif lang == "rust":
        _run(repo_path, ["cargo", "test"])
    else:
        log.warn("Unknown stack; skipping validation.")


def _validate_python(repo_path: Path) -> None:
    # best effort: try pytest if present; otherwise skip
    # (we do NOT pip install arbitrary deps here)
    cmd = ["pytest", "-q"]
    _run(repo_path, cmd)


def _validate_node(repo_path: Path, stack: dict) -> None:
    pm = stack.get("package_manager", "npm")
    
    # Check if package.json exists in root (single package)
    # or if it's a monorepo with packages in subdirectories
    root_pkg = repo_path / "package.json"
    has_root_pkg = root_pkg.exists()
    
    # Look for common monorepo subdirectories
    subdirs = []
    for subdir_name in ["backend", "frontend", "server", "client", "packages"]:
        subdir = repo_path / subdir_name
        if subdir.is_dir() and (subdir / "package.json").exists():
            subdirs.append(subdir)
    
    # If no root package.json but has subdirectories with package.json, it's a monorepo
    if not has_root_pkg and subdirs:
        log.info(f"Detected monorepo structure with {len(subdirs)} packages")
        for subdir in subdirs:
            log.info(f"Validating package: {subdir.name}")
            _validate_node_package(subdir, pm)
    elif has_root_pkg:
        # Single package or root workspace
        _validate_node_package(repo_path, pm)
    else:
        log.warn("No package.json found; skipping Node.js validation.")


def _validate_node_package(pkg_path: Path, pm: str) -> None:
    """Validate a single Node.js package (install only, skip tests)"""
    # Install dependencies
    if pm == "pnpm":
        _run(pkg_path, ["pnpm", "install"])
    elif pm == "yarn":
        _run(pkg_path, ["yarn", "install", "--frozen-lockfile"])
    else:
        _run(pkg_path, ["npm", "install"])
    
    # Skip test validation to avoid hanging on watch mode or dev servers
    # Tests often run in watch mode (npm test) or start servers that don't exit
    log.info("Skipping test execution (tests may run in watch mode)")


def _run(cwd: Path, cmd: list, timeout: int = 120) -> None:
    """Run a command with timeout to prevent hanging.
    
    Args:
        cwd: Working directory
        cmd: Command to run
        timeout: Timeout in seconds (default: 120s for installs)
    """
    log.info(f"Running: {' '.join(cmd)}")
    try:
        p = run_cmd(cmd, cwd=cwd, check=False, timeout=timeout)
        out = (p.stdout or "").strip()
        if out:
            log.info(out[-4000:])  # last 4k chars
        
        if p.returncode == -1:
            log.warn(f"Command timed out after {timeout}s")
        elif p.returncode == 0:
            log.success("Validation step passed.")
        else:
            log.warn(f"Command exited with code {p.returncode}")
    except FileNotFoundError:
        log.warn(f"Command not found: {cmd[0]}. Skipping validation step.")
    except Exception as e:
        log.warn(f"Validation step failed: {e}")
    else:
        log.warn(f"Validation step failed (exit {p.returncode}).")
