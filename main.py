""" Mahjong Copilot

Copyright (C) 2024 Latorc (Github page: https://github.com/latorc)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import pathlib
import sys

from gui.main_gui import MainGUI
from common import utils
from common.log_helper import LogHelper
from common.settings import Settings
from bot_manager import BotManager


def main():
    """ Main entry point """
    LogHelper.config_logging()
    setting = Settings()
    # utils.set_dpi_awareness()
    utils.prevent_sleep()
    bot_manager = BotManager(setting)
    gui = MainGUI(setting, bot_manager)
    gui.mainloop()


def macos_self_test() -> int:
    """Validate the native engines and bundled Chromium without starting the GUI."""
    import libriichi
    import libriichi3p

    browser_root = pathlib.Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", ""))
    chromium = browser_root / "chromium-1105" / "chrome-mac" / "Chromium.app" / "Contents" / "MacOS" / "Chromium"
    checks = {
        "platform": sys.platform == "darwin",
        "arm64": os.uname().machine == "arm64",
        "libriichi": hasattr(libriichi, "mjai"),
        "libriichi3p": hasattr(libriichi3p, "mjai"),
        "chromium": chromium.is_file() and os.access(chromium, os.X_OK),
        "resources": pathlib.Path(utils.resource_file(utils.Folder.RES, "icon.png")).is_file(),
    }
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        print("SELF_TEST_FAILED " + ",".join(failed))
        return 1
    print("SELF_TEST_OK platform=darwin arch=arm64 engines=4p,3p chromium=present resources=present")
    return 0

if __name__ == "__main__":
    if "--self-test" in sys.argv:
        raise SystemExit(macos_self_test())
    main()
