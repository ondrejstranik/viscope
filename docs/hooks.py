"""mkdocs hook: (re)generate the API reference pages under docs/reference/.

Runs automatically on `mkdocs build`/`mkdocs serve` (module-level code below
executes as soon as mkdocs loads this config) -- no third-party plugin needed.
"""

import shutil
from pathlib import Path

DOCS_DIR = Path(__file__).parent
ROOT = DOCS_DIR.parent
SRC = ROOT / "viscope"
REF_DIR = DOCS_DIR / "reference"


def _generate():
    if REF_DIR.exists():
        shutil.rmtree(REF_DIR)

    for path in sorted(SRC.rglob("*.py")):
        parts = path.relative_to(ROOT).with_suffix("").parts

        if parts[-1] == "__init__":
            parts = parts[:-1]
            if not parts:
                continue
            doc_path = REF_DIR.joinpath(*parts[1:], "index.md")
        elif parts[-1] == "__main__":
            continue
        else:
            doc_path = REF_DIR.joinpath(*parts[1:-1], parts[-1] + ".md")

        identifier = ".".join(parts)
        doc_path.parent.mkdir(parents=True, exist_ok=True)
        doc_path.write_text(f"# {identifier}\n\n::: {identifier}\n")


def _build_nav(dir_path, rel):
    """Walk a generated reference directory into a nested mkdocs nav list."""
    items = []
    if (dir_path / "index.md").is_file():
        items.append((rel / "index.md").as_posix())
    for entry in sorted(dir_path.iterdir(), key=lambda p: p.name):
        if entry.is_dir():
            sub = _build_nav(entry, rel / entry.name)
            if sub:
                items.append({entry.name: sub})
        elif entry.suffix == ".md" and entry.name != "index.md":
            items.append((rel / entry.name).as_posix())
    return items


def on_config(config):
    """Append the auto-generated API reference tree to the end of nav.

    Leaves nav alone if it isn't set in mkdocs.yml (fully automatic mode).
    """
    if config.get("nav"):
        config["nav"] = list(config["nav"]) + [
            {"Code Reference": _build_nav(REF_DIR, Path("reference"))}
        ]
    return config


_generate()
