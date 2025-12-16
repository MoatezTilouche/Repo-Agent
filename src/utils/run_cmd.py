import subprocess
import sys
from pathlib import Path
from typing import List, Optional


def run_cmd(
    cmd: List[str], 
    cwd: Optional[Path] = None, 
    check: bool = False,
    timeout: Optional[int] = None
) -> subprocess.CompletedProcess:
    """Run a command with optional timeout.
    
    Args:
        cmd: Command and arguments to run
        cwd: Working directory
        check: Whether to raise on non-zero exit
        timeout: Timeout in seconds (None = no timeout)
    
    Returns:
        CompletedProcess instance
    """
    # On Windows, use shell=True to find commands in PATH (npm, pnpm, etc.)
    use_shell = sys.platform == "win32"
    try:
        return subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=check,
            shell=use_shell,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as e:
        # Return a CompletedProcess-like object for timeout
        return subprocess.CompletedProcess(
            args=cmd,
            returncode=-1,
            stdout=f"Command timed out after {timeout} seconds",
            stderr=""
        )
