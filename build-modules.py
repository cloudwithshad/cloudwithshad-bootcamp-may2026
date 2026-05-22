#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
  cloudwithshad — Self-Paced Module Builder
═══════════════════════════════════════════════════════════════

WHAT THIS DOES
  Reads self-paced/modules.json and regenerates:
    1. Every module page (self-paced/module-XX/index.html)
    2. The module grid on the self-paced index page

HOW TO USE
  1. Edit self-paced/modules.json — set a module's "status" to "live"
     and fill in title, youtube, pdf, audio, etc.
  2. Drop the PDF in the module folder, the MP3 in module-XX/audio/
  3. Run:   python3 build-modules.py
  4. Commit + push. Done. You never edit the HTML by hand.

SAFE TO RE-RUN
  Running this repeatedly just regenerates from the JSON. It never
  loses data because the JSON is the single source of truth.
═══════════════════════════════════════════════════════════════
"""

import json
import os
import sys
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
SELF_PACED = ROOT / "self-paced"
CONFIG = SELF_PACED / "modules.json"
LIVE_TEMPLATE = SELF_PACED / "_module_template.html"
COMING_SOON_TEMPLATE = SELF_PACED / "_coming_soon_template.html"
INDEX = SELF_PACED / "index.html"

GRID_START_MARKER = "<!-- MODULES_GRID_START -->"
GRID_END_MARKER = "<!-- MODULES_GRID_END -->"


def load_config():
    if not CONFIG.exists():
        sys.exit(f"❌ Config not found: {CONFIG}")
    with open(CONFIG, encoding="utf-8") as f:
        return json.load(f)


def build_module_page(mod):
    """Generate a single module's index.html from the right template."""
    n = mod["n"]
    nn = f"{n:02d}"
    folder = SELF_PACED / f"module-{nn}"
    folder.mkdir(exist_ok=True)
    (folder / "audio").mkdir(exist_ok=True)

    is_live = mod.get("status") == "live"
    template_path = LIVE_TEMPLATE if is_live else COMING_SOON_TEMPLATE

    if not template_path.exists():
        print(f"  ⚠️  Template missing: {template_path.name} (skipping module {nn})")
        return None

    html = template_path.read_text(encoding="utf-8")

    # Replacements applied to BOTH templates
    replacements = {
        "MODULE 01": f"MODULE {nn}",
        "Module 01": f"Module {nn}",
        "module-01": f"module-{nn}",
        "MODULE_TITLE_HERE": mod.get("title", f"Module {nn}"),
        "MODULE_SUBTITLE_HERE": mod.get("subtitle", ""),
        "MODULE_DURATION_HERE": mod.get("duration", "") or "—",
        "MODULE_DATE_HERE": mod.get("date", "") or "TBA",
        "MODULE_DESCRIPTION_HERE": mod.get("description", "") or mod.get("subtitle", ""),
        "YOUTUBE_VIDEO_ID_HERE": mod.get("youtube", ""),
        "PDF_FILENAME_HERE": mod.get("pdf", ""),
        "AUDIO_FILENAME_HERE": mod.get("audio", ""),
    }
    for old, new in replacements.items():
        html = html.replace(old, new)

    out = folder / "index.html"
    out.write_text(html, encoding="utf-8")
    return ("live" if is_live else "coming_soon")


def build_index_grid(modules):
    """Render the module cards and inject them into the self-paced index."""
    cards = []
    for mod in modules:
        n = mod["n"]
        nn = f"{n:02d}"
        is_live = mod.get("status") == "live"
        title = mod.get("title", f"Module {nn}")
        subtitle = mod.get("subtitle", "")

        if is_live:
            theme = subtitle or "Now available"
            cards.append(f'''    <a href="module-{nn}/index.html" class="module-card">
      <div class="module-num">{nn}</div>
      <h3>{esc(title)}</h3>
      <div class="theme">{esc(theme)}</div>
      <div class="formats">
        <span class="format-pill">📺 Video</span>
        <span class="format-pill">🎧 Audio</span>
        <span class="format-pill">📄 PDF</span>
      </div>
    </a>''')
        else:
            cards.append(f'''    <a href="module-{nn}/index.html" class="module-card locked">
      <span class="lock-overlay">🔒</span>
      <div class="module-num">{nn}</div>
      <h3>{esc(title)}</h3>
      <div class="theme">Coming soon</div>
      <div class="formats">
        <span class="format-pill">📺 Video</span>
        <span class="format-pill">🎧 Audio</span>
        <span class="format-pill">📄 PDF</span>
      </div>
    </a>''')

    grid_html = "\n" + GRID_START_MARKER + "\n" + "\n\n".join(cards) + "\n    " + GRID_END_MARKER + "\n  "

    index_html = INDEX.read_text(encoding="utf-8")

    # If markers already exist, replace between them. Otherwise, replace the whole grid contents.
    if GRID_START_MARKER in index_html and GRID_END_MARKER in index_html:
        before = index_html.split(GRID_START_MARKER)[0]
        after = index_html.split(GRID_END_MARKER)[1]
        index_html = before + grid_html.strip() + "\n  " + after
    else:
        # First run: find <div class="modules-grid"> ... </div> and replace its inner content
        import re
        # Match the modules-grid div and its contents up to its matching close.
        # We use a simple balanced-div finder.
        start_idx = index_html.find('<div class="modules-grid">')
        if start_idx == -1:
            print("  ⚠️  Could not find modules-grid in index.html — grid not updated.")
            return False
        # find content start (after the opening tag)
        open_tag_end = index_html.find(">", start_idx) + 1
        # balance divs
        depth = 1
        i = open_tag_end
        while i < len(index_html) and depth > 0:
            next_open = index_html.find("<div", i)
            next_close = index_html.find("</div>", i)
            if next_close == -1:
                break
            if next_open != -1 and next_open < next_close:
                depth += 1
                i = next_open + 4
            else:
                depth -= 1
                i = next_close + 6
        close_idx = i  # position just after the matching </div>
        grid_close_pos = index_html.rfind("</div>", open_tag_end, close_idx)
        new_index = (
            index_html[:open_tag_end]
            + grid_html
            + index_html[grid_close_pos:]
        )
        index_html = new_index

    INDEX.write_text(index_html, encoding="utf-8")
    return True


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def main():
    cfg = load_config()
    modules = cfg["modules"]
    print(f"📦 Building {len(modules)} self-paced modules from modules.json\n")

    live_count = 0
    coming_count = 0
    for mod in modules:
        result = build_module_page(mod)
        if result == "live":
            live_count += 1
            print(f"  ✅ Module {mod['n']:02d} — LIVE — {mod.get('title','')}")
        elif result == "coming_soon":
            coming_count += 1
            print(f"  🔒 Module {mod['n']:02d} — coming soon — {mod.get('title','')}")

    print()
    if build_index_grid(modules):
        print("  ✅ Index grid updated")

    print(f"\n🎉 Done. {live_count} live, {coming_count} coming soon.")
    if live_count > 0:
        print("\n   Reminder: make sure the PDF and MP3 files are in place:")
        for mod in modules:
            if mod.get("status") == "live":
                nn = f"{mod['n']:02d}"
                if mod.get("pdf"):
                    print(f"     • self-paced/module-{nn}/{mod['pdf']}")
                if mod.get("audio"):
                    print(f"     • self-paced/module-{nn}/audio/{mod['audio']}")


if __name__ == "__main__":
    main()
