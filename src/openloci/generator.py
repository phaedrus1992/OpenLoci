"""
Palace generation engine — wraps Cookiecutter with OpenLoci conventions.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from cookiecutter.main import cookiecutter  # type: ignore[import-untyped]

from openloci.skins import get_skin_path


def generate_palace(
    name: str,
    skin: str,
    output_dir: Path,
    no_input: bool = False,
    overwrite: bool = False,
    extra_context: Optional[dict[str, Any]] = None,
) -> Path:
    """
    Generate a new OpenLoci palace using Cookiecutter.

    Args:
        name:         Human-readable palace name (used in README, frontmatter).
        skin:         Skin name (maps to templates/skins/<skin>).
        output_dir:   Directory to generate into.
        no_input:     Skip interactive prompts.
        overwrite:    Overwrite existing output directory.
        extra_context: Additional variables to pass to the template.

    Returns:
        Path to the generated palace directory.
    """
    skin_path = get_skin_path(skin)

    context: dict[str, Any] = {
        "palace_name": name,
        "skin": skin,
    }
    if extra_context:
        context.update(extra_context)

    result = cookiecutter(
        str(skin_path),
        output_dir=str(output_dir),
        no_input=no_input,
        overwrite_if_exists=overwrite,
        extra_context=context,
    )

    return Path(result)
