"""
Skin discovery and metadata loading for OpenLoci.

A skin is a named template overlay in the /templates/skins/ directory.
Each skin contains a skin.json (metadata) and a cookiecutter template.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

# Bundled templates ship alongside the package
TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"
SKINS_DIR = TEMPLATES_DIR / "skins"


def list_skins() -> list[str]:
    """Return sorted list of available skin names."""
    if not SKINS_DIR.exists():
        return []
    return sorted(d.name for d in SKINS_DIR.iterdir() if d.is_dir() and not d.name.startswith("."))


def get_skin_path(skin_name: str) -> Path:
    """Return the path to a skin's template directory, or raise FileNotFoundError."""
    # Check bundled skins first
    bundled = SKINS_DIR / skin_name
    if bundled.exists():
        return bundled

    # Check base template
    if skin_name == "base":
        base = TEMPLATES_DIR / "base"
        if base.exists():
            return base

    raise FileNotFoundError(f"Skin '{skin_name}' not found in {SKINS_DIR}")


def get_skin_info(skin_name: str) -> dict[str, Any]:
    """
    Return metadata for a skin. Reads skin.json if present,
    otherwise returns minimal defaults.
    """
    skin_path = get_skin_path(skin_name)

    meta_file = skin_path / "skin.json"
    if meta_file.exists():
        return cast(dict[str, Any], json.loads(meta_file.read_text()))

    # Minimal fallback
    return {
        "name": skin_name,
        "description": "No description available.",
        "room_map": [],
        "characters": [],
    }
