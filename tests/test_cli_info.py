"""
Tests for the `info` command's README rendering.

Regression: char-count truncation could slice mid-Rich-tag and corrupt
output. The fix truncates by line and renders the body as a plain
`rich.text.Text` so brackets in the README are not parsed as markup.
"""

from pathlib import Path

from typer.testing import CliRunner

from openloci.cli import app

runner = CliRunner()


def _make_palace(tmp_path: Path, readme_body: str) -> Path:
    vestibule = tmp_path / "The Vestibule"
    vestibule.mkdir(parents=True)
    (vestibule / "README.md").write_text(readme_body)
    return tmp_path


def test_info_handles_rich_like_brackets(tmp_path: Path) -> None:
    body = "# Title\n\nSome [bold]brackets[/bold] that look like Rich markup.\n"
    palace = _make_palace(tmp_path, body)
    result = runner.invoke(app, ["info", str(palace)])
    assert result.exit_code == 0
    # Rich must NOT have parsed [bold]…[/bold] as markup —
    # the literal brackets should appear in the output.
    assert "[bold]brackets[/bold]" in result.stdout


def test_info_handles_long_readme(tmp_path: Path) -> None:
    # 200 lines, well past the 40-line preview window.
    body = "\n".join(f"line {i}" for i in range(200)) + "\n"
    palace = _make_palace(tmp_path, body)
    result = runner.invoke(app, ["info", str(palace)])
    assert result.exit_code == 0
    assert "line 0" in result.stdout
    assert "…" in result.stdout
    # Lines beyond the preview window must not appear.
    assert "line 100" not in result.stdout


def test_info_missing_palace_exits_nonzero(tmp_path: Path) -> None:
    # tmp_path has no "The Vestibule/README.md".
    result = runner.invoke(app, ["info", str(tmp_path)])
    assert result.exit_code == 1
