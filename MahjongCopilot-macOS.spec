# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, collect_submodules

playwright_datas, playwright_binaries, playwright_hidden = collect_all("playwright")
mitm_datas, mitm_binaries, mitm_hidden = collect_all("mitmproxy")

analysis = Analysis(
    ["main.py"],
    pathex=["."],
    binaries=playwright_binaries + mitm_binaries + [
        ("libriichi/libriichi.so", "libriichi"),
        ("libriichi3p/libriichi3p-3.12-aarch64-apple-darwin.so", "libriichi3p"),
    ],
    datas=playwright_datas + mitm_datas + [
        ("resources", "resources"),
        ("liqi_proto/liqi.json", "liqi_proto"),
        ("version", "."),
        ("LICENSE", "."),
        ("THIRD_PARTY_NOTICES.md", "."),
    ],
    hiddenimports=playwright_hidden + mitm_hidden + collect_submodules("tkhtmlview") + [
        "libriichi.libriichi",
        "libriichi3p",
        "PIL._tkinter_finder",
    ],
    runtime_hooks=["macos_runtime.py"],
    excludes=["win32api", "win32con", "win32gui", "pywintypes"],
    noarchive=False,
)
pyz = PYZ(analysis.pure)
exe = EXE(
    pyz,
    analysis.scripts,
    [],
    exclude_binaries=True,
    name="MahjongCopilot",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    argv_emulation=False,
    target_arch="arm64",
)
collect = COLLECT(
    exe,
    analysis.binaries,
    analysis.datas,
    strip=False,
    upx=False,
    name="MahjongCopilot",
)
app = BUNDLE(
    collect,
    name="MahjongCopilot.app",
    icon="resources/icon.icns",
    bundle_identifier="com.siriuspeng.mahjongcopilot",
    info_plist={
        "CFBundleDisplayName": "Mahjong Copilot",
        "CFBundleShortVersionString": "0.6.0-macos.1",
        "CFBundleVersion": "1",
        "LSMinimumSystemVersion": "12.0",
        "NSHighResolutionCapable": True,
        "NSHumanReadableCopyright": "GPL-3.0; based on MahjongCopilot by Latorc",
    },
)
