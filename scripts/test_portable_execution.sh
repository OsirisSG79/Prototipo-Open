#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

TARGET_NAME="${TARGET_ZIP_NAME:-OpenBreak_Cinematic_V8_1_5_Proyecto_Completo.zip}"
ZIP_PATH="${REPO_DIR}/../${TARGET_NAME}"
if [ ! -f "$ZIP_PATH" ]; then
    ZIP_PATH="${REPO_DIR}/${TARGET_NAME}"
fi

if [ ! -f "$ZIP_PATH" ]; then
    # Look for any recent OpenBreak deliverable zip
    ZIP_PATH="$(ls -t "${REPO_DIR}/../OpenBreak_Cinematic_"*.zip "${REPO_DIR}/OpenBreak_Cinematic_"*.zip 2>/dev/null | head -n 1)"
fi

TMP_DIR="/tmp/test_openbreak_extracted_portable_$$"
rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"

echo "1. Unzipping $ZIP_PATH into $TMP_DIR..."
unzip -q "$ZIP_PATH" -d "$TMP_DIR"

echo "2. Checking contents..."
if [ -d "$TMP_DIR/openbreak" ]; then
    cd "$TMP_DIR/openbreak"
else
    cd "$TMP_DIR"
fi

echo "3. Running ./run_all_audits.sh in arbitrary directory..."
bash ./run_all_audits.sh

echo ""
echo "=========================================================="
echo "PORTABILITY TEST PASSED CLEANLY IN ISOLATED DIRECTORY!   "
echo "=========================================================="

rm -rf "$TMP_DIR"
