from rich.console import Console

_console = Console()


class _Log:
    def info(self, msg: str):
        _console.print(f"[cyan]INFO[/cyan]  {msg}")

    def warn(self, msg: str):
        _console.print(f"[yellow]WARN[/yellow]  {msg}")

    def success(self, msg: str):
        _console.print(f"[green]OK[/green]    {msg}")

    def error(self, msg: str):
        _console.print(f"[red]ERR[/red]   {msg}")


log = _Log()
