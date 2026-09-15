import os
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

from common import utils
from common.settings import Settings
from updater import Updater, UpdateStatus, MACOS_RELEASES_URL


class MacOSPortTests(unittest.TestCase):
    def test_sub_run_args_are_portable_on_macos(self):
        with mock.patch.object(sys, "platform", "darwin"):
            args = utils.sub_run_args()
        self.assertEqual({"capture_output": True, "text": True, "check": False}, args)

    def test_frozen_macos_data_is_in_application_support(self):
        with mock.patch.object(sys, "platform", "darwin"), \
             mock.patch.object(sys, "frozen", True, create=True), \
             mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(
                pathlib.Path.home() / "Library" / "Application Support" / "MahjongCopilot",
                utils.data_root(),
            )

    def test_resource_path_is_separate_from_writable_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict(os.environ, {"MAHJONGCOPILOT_HOME": tmp}):
                writable = pathlib.Path(utils.sub_file("models", "mortal.pth"))
                resource = pathlib.Path(utils.resource_file("resources", "icon.png"))
            self.assertEqual(pathlib.Path(tmp).resolve() / "models" / "mortal.pth", writable)
            self.assertTrue(resource.is_file())
            self.assertNotEqual(resource.parent, writable.parent)

    def test_settings_save_to_application_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict(os.environ, {"MAHJONGCOPILOT_HOME": tmp}):
                settings = Settings("test-settings.json")
            self.assertTrue((pathlib.Path(tmp) / "test-settings.json").is_file())

    def test_required_macos_build_files_exist(self):
        root = pathlib.Path(__file__).resolve().parents[1]
        for relative in (
            "MahjongCopilot-macOS.spec",
            "requirements-macos.txt",
            "scripts/build_macos.sh",
            ".github/workflows/build-macos.yml",
        ):
            self.assertTrue((root / relative).is_file(), relative)

    def test_native_engines_load_on_macos(self):
        import libriichi
        import libriichi3p
        self.assertTrue(hasattr(libriichi, "mjai"))
        self.assertTrue(hasattr(libriichi3p, "mjai"))

    def test_macos_update_opens_github_release(self):
        updater = Updater("https://update.invalid")
        updater.update_status = UpdateStatus.NEW_VERSION
        with mock.patch.object(sys, "platform", "darwin"), \
             mock.patch("updater.webbrowser.open", return_value=True) as opened:
            updater.prepare_update()
        opened.assert_called_once_with(MACOS_RELEASES_URL)
        self.assertEqual(UpdateStatus.NO_UPDATE, updater.update_status)


if __name__ == "__main__":
    unittest.main()
