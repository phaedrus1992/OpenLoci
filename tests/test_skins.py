"""
Tests for skin discovery and metadata loading.

Run with: pytest tests/ -v
"""

import json
from pathlib import Path

import pytest

from openloci.skins import list_skins, get_skin_path, get_skin_info


# ── list_skins ─────────────────────────────────────────────────────────────────


class TestListSkins:
    def test_returns_list(self):
        result = list_skins()
        assert isinstance(result, list)

    def test_xfiles_clue_present(self):
        assert "clue" in list_skins()

    def test_xfiles_skin_present(self):
        assert "xfiles" in list_skins()

    def test_siliconvalley_skin_present(self):
        assert "siliconvalley" in list_skins()

    def test_muppets_skin_present(self):
        assert "muppets" in list_skins()

    def test_digitalcircus_skin_present(self):
        assert "digitalcircus" in list_skins()

    def test_result_is_sorted(self):
        result = list_skins()
        assert result == sorted(result)

    def test_no_hidden_dirs(self):
        for name in list_skins():
            assert not name.startswith(".")


# ── get_skin_path ──────────────────────────────────────────────────────────────


class TestGetSkinPath:
    def test_xfiles_path_exists(self):
        assert get_skin_path("xfiles").is_dir()

    def test_siliconvalley_path_exists(self):
        assert get_skin_path("siliconvalley").is_dir()

    def test_invalid_skin_raises(self):
        with pytest.raises(FileNotFoundError):
            get_skin_path("nonexistent_skin_xyz")

    def test_all_skins_have_cookiecutter_json(self):
        for skin in list_skins():
            cc = get_skin_path(skin) / "cookiecutter.json"
            assert cc.exists(), f"Missing cookiecutter.json for: {skin}"
            data = json.loads(cc.read_text())
            assert "palace_name" in data


# ── get_skin_info ──────────────────────────────────────────────────────────────


class TestGetSkinInfo:
    def test_returns_dict(self):
        assert isinstance(get_skin_info("xfiles"), dict)

    def test_required_keys_present(self):
        for skin in list_skins():
            info = get_skin_info(skin)
            for key in ("name", "description", "room_map", "characters"):
                assert key in info, f"Skin '{skin}' missing key: {key}"

    def test_ten_rooms(self):
        for skin in list_skins():
            info = get_skin_info(skin)
            assert len(info["room_map"]) == 10, (
                f"Skin '{skin}' has {len(info['room_map'])} rooms, expected 10 (9 + Vestibule)"
            )

    def test_six_characters(self):
        for skin in list_skins():
            info = get_skin_info(skin)
            assert len(info["characters"]) == 6, (
                f"Skin '{skin}' has {len(info['characters'])} characters, expected 6"
            )

    def test_room_map_fields(self):
        for skin in list_skins():
            for room in get_skin_info(skin)["room_map"]:
                for key in ("clue", "name", "prefix", "function"):
                    assert key in room, f"[{skin}] room missing '{key}': {room}"

    def test_invalid_skin_raises(self):
        with pytest.raises(FileNotFoundError):
            get_skin_info("nonexistent_xyz")


# ── template structure ─────────────────────────────────────────────────────────


class TestTemplateStructure:
    def _template_root(self, skin_name: str) -> Path:
        skin_path = get_skin_path(skin_name)
        candidates = [d for d in skin_path.iterdir() if d.is_dir() and "cookiecutter" in d.name]
        assert len(candidates) == 1
        return candidates[0]

    def test_has_vestibule(self):
        for skin in list_skins():
            assert (self._template_root(skin) / "The Vestibule").exists()

    def test_has_palace(self):
        for skin in list_skins():
            assert (self._template_root(skin) / "The Palace").exists()

    def test_vestibule_has_readme(self):
        for skin in list_skins():
            assert (self._template_root(skin) / "The Vestibule" / "README.md").exists()

    def test_vestibule_has_master_prompt(self):
        for skin in list_skins():
            assert (
                self._template_root(skin) / "The Vestibule" / "Principles" / "master_prompt.md"
            ).exists()

    def test_vestibule_has_characters(self):
        for skin in list_skins():
            chars = list((self._template_root(skin) / "The Vestibule" / "Characters").glob("*.md"))
            assert len(chars) >= 4, f"[{skin}] expected ≥4 character files, found {len(chars)}"
