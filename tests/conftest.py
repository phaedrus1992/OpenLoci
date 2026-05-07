"""
Shared fixtures for OpenLoci tests.
"""

from pathlib import Path

import pytest


# Resolve the templates dir relative to this file
REPO_ROOT = Path(__file__).parent.parent
TEMPLATES_DIR = REPO_ROOT / "templates"
SKINS_DIR = TEMPLATES_DIR / "skins"


@pytest.fixture
def templates_dir() -> Path:
    return TEMPLATES_DIR


@pytest.fixture
def skins_dir() -> Path:
    return SKINS_DIR


@pytest.fixture
def xfiles_skin_dir(skins_dir: Path) -> Path:
    return skins_dir / "xfiles"


@pytest.fixture
def sv_skin_dir(skins_dir: Path) -> Path:
    return skins_dir / "sv"
