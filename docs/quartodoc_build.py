"""docs/quartodoc_build.py — Applies a compatibility patch then runs quartodoc.

Problem
-------
quartodoc 0.11.x uses griffe internally.  When griffe parses certain source
files it can generate ``DocstringSectionWarns`` objects.  The ``MdRenderer``
in quartodoc 0.11.x has no ``@dispatch`` handler for this type and raises::

    NotImplementedError: Unsupported type:
        <class 'griffe._internal.docstrings.models.DocstringSectionWarns'>

Root cause: griffe renamed ``DocstringSectionWarnings`` →
``DocstringSectionWarns`` in a recent release, and quartodoc has not yet
shipped a fix.

Fix strategy
------------
We patch the installed ``md_renderer.py`` file **in-place** to add the missing
handler, then execute ``quartodoc build`` normally.  The patch is idempotent
(safe to run multiple times) and writes a one-line sentinel comment so it can
be detected and skipped on re-runs.

This script is called from:
  - Local dev: ``uv run python docs/quartodoc_build.py``
  - CI (.github/workflows/docs.yml): same command

Safety note
-----------
The patch only adds a new ``@dispatch`` method.  No existing behaviour is
changed.  The sentinel comment makes the patch auditable.
"""
from __future__ import annotations

import importlib.util
import pathlib
import subprocess
import sys

# ── Constants ────────────────────────────────────────────────────────────────

_SENTINEL = "# PATCHED: DocstringSection handlers added by docs/quartodoc_build.py"

_NEW_HANDLER = '''
    # ── Compatibility patch: griffe DocstringSections ──────────────────────
    # PATCHED: DocstringSection handlers added by docs/quartodoc_build.py
    # griffe renamed/added sections that quartodoc 0.11.x doesn't handle yet.
    @dispatch
    def render(self, el: ds.DocstringSectionWarns) -> str:
        """Render a Warns: section as plain text."""
        if hasattr(el, "value") and el.value:
            return "\\n\\n".join(
                getattr(w, "description", str(w)) for w in el.value
            )
        return ""

    @dispatch
    def render(self, el: ds.DocstringSectionFunctions) -> str:
        """Render a Functions: section as plain text."""
        if hasattr(el, "value") and el.value:
            return "\\n\\n".join(
                getattr(f, "description", str(f)) for f in el.value
            )
        return ""
    # ── End compatibility patch ────────────────────────────────────────────
'''

_INSERTION_ANCHOR = "    # unsupported parts ----"


def _find_renderer() -> pathlib.Path:
    """Return the absolute path to the installed md_renderer.py."""
    spec = importlib.util.find_spec("quartodoc.renderers.md_renderer")
    if spec is None or spec.origin is None:
        raise RuntimeError(
            "quartodoc is not installed in the current environment. "
            "Run `uv sync --group dev` first."
        )
    return pathlib.Path(spec.origin)


def _apply_patch(renderer_path: pathlib.Path) -> None:
    """Idempotently add DocstringSection handlers to MdRenderer."""
    source = renderer_path.read_text(encoding="utf-8")

    if _SENTINEL in source:
        print("[quartodoc_build] Patch already applied — skipping.")
        return

    if _INSERTION_ANCHOR not in source:
        raise RuntimeError(
            f"Could not find insertion anchor {_INSERTION_ANCHOR!r} in "
            f"{renderer_path}.  The quartodoc version may have changed; "
            "please update this patch script."
        )

    # Insert the new handler just before the "unsupported parts" block.
    patched = source.replace(_INSERTION_ANCHOR, _NEW_HANDLER + _INSERTION_ANCHOR, 1)
    renderer_path.write_text(patched, encoding="utf-8")
    print(f"[quartodoc_build] Patch applied to {renderer_path}")


def main() -> None:
    renderer = _find_renderer()
    _apply_patch(renderer)

    # Run quartodoc build via subprocess so it picks up the patched file.
    result = subprocess.run(
        [sys.executable, "-m", "quartodoc", "build", "--config", "_quarto.yml"],
        check=False,
    )
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
