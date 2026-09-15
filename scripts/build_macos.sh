#!/bin/zsh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
[[ "$(uname -s)" == "Darwin" ]] || { echo "macOS is required" >&2; exit 2; }
[[ "$(uname -m)" == "arm64" ]] || { echo "This build currently targets Apple Silicon (arm64)" >&2; exit 2; }
PYTHON="${PYTHON:-python3.12}"
command -v "$PYTHON" >/dev/null || { echo "Python 3.12 is required" >&2; exit 2; }

AKAGI_COMMIT="11c0ffc0d70bf8142585b92405b4412976c9e205"
fetch_native() {
  local url="$1" output="$2" expected="$3"
  mkdir -p "$(dirname "$output")"
  curl -fL --retry 3 "$url" -o "$output"
  local actual
  actual="$(shasum -a 256 "$output" | awk '{print $1}')"
  [[ "$actual" == "$expected" ]] || { echo "Checksum mismatch for $output" >&2; exit 3; }
}
fetch_native \
  "https://raw.githubusercontent.com/Xe-Persistent/Akagi-NG/${AKAGI_COMMIT}/lib/libriichi-3.12-aarch64-apple-darwin.so" \
  "libriichi/libriichi.so" \
  "83f5e0bad7dabed22fc69a9e81b2022b888bdada85dc861bf56d50dc596432c6"
fetch_native \
  "https://raw.githubusercontent.com/Xe-Persistent/Akagi-NG/${AKAGI_COMMIT}/lib/libriichi3p-3.12-aarch64-apple-darwin.so" \
  "libriichi3p/libriichi3p-3.12-aarch64-apple-darwin.so" \
  "d8e12cb0460d24dc88f7de527893326ac31ab46686b54f54201e5ece2f326c65"

VENV="${VENV:-.venv-macos}"
"$PYTHON" -m venv "$VENV"
"$VENV/bin/python" -m pip install --upgrade pip wheel
"$VENV/bin/pip" install -r requirements-macos.txt
"$VENV/bin/python" -m unittest discover -s tests -v
if [[ ! -d build/playwright-browsers/chromium-1105 ]]; then
  PLAYWRIGHT_BROWSERS_PATH="$ROOT/build/playwright-browsers" "$VENV/bin/playwright" install chromium
fi

rm -rf build/pyinstaller dist/MahjongCopilot dist/MahjongCopilot.app dist/MahjongCopilot-macOS-arm64.zip
"$VENV/bin/pyinstaller" --noconfirm --clean --workpath build/pyinstaller MahjongCopilot-macOS.spec
mkdir -p dist/MahjongCopilot.app/Contents/Resources
/usr/bin/ditto build/playwright-browsers dist/MahjongCopilot.app/Contents/Resources/playwright-browsers
codesign --force --deep --sign - dist/MahjongCopilot.app
codesign --verify --deep --strict --verbose=2 dist/MahjongCopilot.app
/usr/bin/ditto -c -k --sequesterRsrc --keepParent dist/MahjongCopilot.app dist/MahjongCopilot-macOS-arm64.zip
shasum -a 256 dist/MahjongCopilot-macOS-arm64.zip > dist/MahjongCopilot-macOS-arm64.zip.sha256
echo "Built: $ROOT/dist/MahjongCopilot-macOS-arm64.zip"
