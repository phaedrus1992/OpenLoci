"""
OpenLoci CLI — A filesystem-native collaborative Memory Palace for distributed cognition.
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, Optional

import typer
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from openloci import __version__
from openloci.generator import generate_palace
from openloci.skins import list_skins, get_skin_info

console = Console()
err_console = Console(stderr=True, style="bold red")

# ── Banner ─────────────────────────────────────────────────────────────────────

BANNER = """
[bold cyan]  ╔═══════════════════════════════════╗[/bold cyan]
[bold cyan]  ║         O P E N L O C I           ║[/bold cyan]
[bold cyan]  ║   filesystem-native memory palace  ║[/bold cyan]
[bold cyan]  ╚═══════════════════════════════════╝[/bold cyan]
[dim]  A finite game is played to win.[/dim]
[dim]  An infinite game is played to continue.[/dim]
"""

# ── App ────────────────────────────────────────────────────────────────────────

app = typer.Typer(
    name="openloci",
    help="Generate and manage filesystem-native memory palaces.",
    rich_markup_mode="rich",
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
)


def version_callback(value: bool) -> None:
    if value:
        rprint(f"[bold cyan]openloci[/bold cyan] v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            "-v",
            help="Show version and exit.",
            callback=version_callback,
            is_eager=True,
        ),
    ] = None,
) -> None:
    """
    [bold cyan]OpenLoci[/bold cyan] — A filesystem-native memory palace generator.

    Build finite games (projects, investigations, migrations) and infinite games
    (RPG worlds, knowledge systems) from plain text and directory structures.

    [dim]The palace is being built.[/dim]
    """


# ── new ────────────────────────────────────────────────────────────────────────


@app.command()
def new(
    name: Annotated[
        str, typer.Argument(help="Name of the new palace (becomes the directory name).")
    ],
    skin: Annotated[
        str,
        typer.Option(
            "--skin",
            "-s",
            help="Skin to apply (e.g. xfiles, jobhunt, office). Run [bold]openloci skins[/bold] to list available skins.",
        ),
    ] = "base",
    output_dir: Annotated[
        Optional[Path],
        typer.Option(
            "--output",
            "-o",
            help="Directory to create the palace in. Defaults to current directory.",
        ),
    ] = None,
    no_input: Annotated[
        bool,
        typer.Option(
            "--no-input",
            "-n",
            help="Skip interactive prompts and use defaults.",
        ),
    ] = False,
    overwrite: Annotated[
        bool,
        typer.Option(
            "--overwrite",
            "-f",
            help="Overwrite if output directory already exists.",
        ),
    ] = False,
) -> None:
    """
    [bold]Generate a new memory palace.[/bold]

    Creates a fresh OpenLoci palace from the specified skin template.

    [dim]Examples:[/dim]
      [cyan]openloci new my-project[/cyan]                    [dim]# base template[/dim]
      [cyan]openloci new my-xfiles -s xfiles[/cyan]           [dim]# X-Files skin[/dim]
      [cyan]openloci new job-hunt -s jobhunt -o ~/projects[/cyan]
    """
    rprint(BANNER)

    target = (output_dir or Path.cwd()) / name

    if target.exists() and not overwrite:
        err_console.print(
            f"[bold]✗[/bold] Directory already exists: [yellow]{target}[/yellow]\n"
            f"  Use [bold]--overwrite[/bold] / [bold]-f[/bold] to replace it."
        )
        raise typer.Exit(code=1)

    console.print(f"[bold]→[/bold] Skin:    [cyan]{skin}[/cyan]")
    console.print(f"[bold]→[/bold] Output:  [cyan]{target}[/cyan]")
    console.print()

    try:
        generate_palace(
            name=name,
            skin=skin,
            output_dir=output_dir or Path.cwd(),
            no_input=no_input,
            overwrite=overwrite,
        )
    except FileNotFoundError as e:
        err_console.print(f"[bold]✗[/bold] Skin not found: [yellow]{skin}[/yellow]")
        err_console.print(f"  {e}")
        err_console.print("  Run [bold]openloci skins[/bold] to see available skins.")
        raise typer.Exit(code=1) from e
    except Exception as e:
        err_console.print(f"[bold]✗[/bold] Generation failed: {e}")
        raise typer.Exit(code=1) from e

    console.print()
    console.print(
        Panel(
            f"[bold green]✓ Palace generated:[/bold green] [cyan]{target}[/cyan]\n\n"
            f"  [dim]Enter the vestibule:[/dim]\n"
            f"  [bold]cd {target}/The\\ Vestibule && cat README.md[/bold]",
            title="[bold]OpenLoci[/bold]",
            border_style="cyan",
        )
    )


# ── skins ──────────────────────────────────────────────────────────────────────


@app.command()
def skins(
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Show full skin descriptions."),
    ] = False,
) -> None:
    """
    [bold]List available palace skins.[/bold]

    Skins are template overlays that give your palace a cultural frame
    while preserving the underlying OpenLoci structure.
    """
    available = list_skins()

    if not available:
        console.print("[yellow]No skins found.[/yellow] Check your templates directory.")
        raise typer.Exit()

    table = Table(
        title="Available Skins",
        show_header=True,
        header_style="bold cyan",
        border_style="dim",
    )
    table.add_column("Skin", style="bold", min_width=12)
    table.add_column("Description", style="dim")
    if verbose:
        table.add_column("Rooms", style="cyan")

    for skin_name in available:
        info = get_skin_info(skin_name)
        if verbose:
            table.add_row(skin_name, info.get("description", "—"), info.get("rooms", "—"))
        else:
            table.add_row(skin_name, info.get("description", "—"))

    console.print()
    console.print(table)
    console.print()
    console.print("[dim]Use a skin:[/dim] [cyan]openloci new my-palace --skin <name>[/cyan]")


# ── rooms ──────────────────────────────────────────────────────────────────────


@app.command()
def rooms(
    skin: Annotated[
        str,
        typer.Argument(help="Skin name to inspect."),
    ] = "base",
) -> None:
    """
    [bold]Show the room map for a skin.[/bold]

    Displays the nine rooms of a palace skin with their semantic prefixes,
    Clue chassis mapping, and primary functions.

    [dim]Example:[/dim]
      [cyan]openloci rooms xfiles[/cyan]
    """
    try:
        info = get_skin_info(skin)
    except FileNotFoundError as e:
        err_console.print(f"[bold]✗[/bold] Skin not found: [yellow]{skin}[/yellow]")
        err_console.print("  Run [bold]openloci skins[/bold] to see available skins.")
        raise typer.Exit(code=1) from e

    room_data = info.get("room_map", [])
    if not room_data:
        console.print(f"[yellow]No room map defined for skin:[/yellow] {skin}")
        raise typer.Exit()

    table = Table(
        title=f"Room Map — [bold cyan]{skin}[/bold cyan] skin",
        show_header=True,
        header_style="bold cyan",
        border_style="dim",
    )
    table.add_column("#", style="dim", width=3)
    table.add_column("Clue Room", style="dim")
    table.add_column("Skin Room", style="bold")
    table.add_column("Prefix", style="cyan")
    table.add_column("Function", style="dim")

    for i, room in enumerate(room_data, 1):
        table.add_row(
            str(i),
            room.get("clue", "—"),
            room.get("name", "—"),
            room.get("prefix", "—"),
            room.get("function", "—"),
        )

    console.print()
    console.print(table)


# ── info ───────────────────────────────────────────────────────────────────────


@app.command()
def info(
    palace_dir: Annotated[
        Optional[Path],
        typer.Argument(help="Path to an existing palace. Defaults to current directory."),
    ] = None,
) -> None:
    """
    [bold]Show info about an existing palace.[/bold]

    Reads the Vestibule README and reports the palace's skin, rooms, and status.
    """
    target = palace_dir or Path.cwd()
    vestibule = target / "The Vestibule" / "README.md"

    if not vestibule.exists():
        err_console.print(
            f"[bold]✗[/bold] No palace found at [yellow]{target}[/yellow]\n"
            "  (Looking for [dim]The Vestibule/README.md[/dim])"
        )
        raise typer.Exit(code=1)

    lines = vestibule.read_text().splitlines()
    preview_limit = 40
    truncated = lines[:preview_limit]
    if len(lines) > preview_limit:
        truncated.append("…")
    body = Text("\n".join(truncated))
    console.print(
        Panel(
            body,
            title=f"[bold cyan]{target.name}[/bold cyan] — Vestibule",
            border_style="cyan",
        )
    )


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app()
