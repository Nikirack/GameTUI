import subprocess
import shutil
import os
import sys

SPEC_FILE = 'GameTUI.spec'
DIST_DIR = os.path.join('dist', 'GameTUI')
LICENSES_SRC = os.path.join('info', 'THIRD_PARTY_LICENSES')
LICENSES_DEST = os.path.join(DIST_DIR, 'info','THIRD_PARTY_LICENSES')

def run_pyinstaller():
    print(f"Running PyInstaller with spec file: {SPEC_FILE} ...")
    result = subprocess.run(['pyinstaller', SPEC_FILE])
    if result.returncode != 0:
        print(f"PyInstaller failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    print("PyInstaller build finished successfully.")

def move_licenses():
    print(f"Copying licenses from '{LICENSES_SRC}' to '{LICENSES_DEST}' ...")
    if not os.path.exists(LICENSES_SRC):
        print(f"Source licenses folder does not exist: {LICENSES_SRC}")
        return

    os.makedirs(os.path.dirname(LICENSES_DEST), exist_ok=True)

    if os.path.exists(LICENSES_DEST):
        shutil.rmtree(LICENSES_DEST)

    shutil.copytree(LICENSES_SRC, LICENSES_DEST)
    print("Licenses copied successfully.")

def main():
    run_pyinstaller()
    move_licenses()

if __name__ == '__main__':
    main()