"""PyInstaller runtime setup for the macOS app bundle."""
import os
import pathlib
import sys

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    contents_resources = pathlib.Path(sys.executable).resolve().parent.parent / "Resources" / "playwright-browsers"
    browser_root = contents_resources if contents_resources.exists() else pathlib.Path(sys._MEIPASS) / "playwright-browsers"
    os.environ.setdefault(
        "PLAYWRIGHT_BROWSERS_PATH",
        str(browser_root),
    )
