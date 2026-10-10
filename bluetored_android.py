"""
bluetored-android - turn blue into red on an Android screen, driven by Python.

Runs on your PC and talks to the phone over adb. It sends a color matrix to
SurfaceFlinger (the Android compositor), so it affects the whole display,
including every app, with no overlay and no screen capture.

Setup:
  1. Install adb (Android platform-tools) and put it on your PATH.
  2. On the phone: Settings > About phone > tap Build number 7 times, then
     Developer options > enable USB debugging. Plug in and accept the prompt.

Usage:
    python bluetored_android.py swap       # red and blue trade places
    python bluetored_android.py blue2red   # blue -> red, reds stay red
    python bluetored_android.py off        # restore normal colors

The effect resets on reboot. Some phones/Android versions block this call.
"""

import shutil
import subprocess
import sys

# 4x4 matrices, flattened column-major (the order SurfaceFlinger expects).
# Math is out = M * [r, g, b, a].
MATRICES = {
    # out.r = b, out.g = g, out.b = r
    "swap": [
        0, 0, 1, 0,   # column 0 (contribution of input R)
        0, 1, 0, 0,   # column 1 (input G)
        1, 0, 0, 0,   # column 2 (input B)
        0, 0, 0, 1,   # column 3 (alpha)
    ],
    # out.r = r + b, out.g = g, out.b = 0
    "blue2red": [
        1, 0, 0, 0,
        0, 1, 0, 0,
        1, 0, 0, 0,
        0, 0, 0, 1,
    ],
}


def adb(*args: str) -> str:
    result = subprocess.run(["adb", *args], capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"adb error: {result.stderr.strip() or result.stdout.strip()}")
    return result.stdout


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "swap"
    if mode not in (*MATRICES, "off"):
        sys.exit(__doc__)
    if shutil.which("adb") is None:
        sys.exit("adb not found. Install Android platform-tools and add it to PATH.")

    devices = [l for l in adb("devices").splitlines()[1:] if l.strip()]
    if not any(l.endswith("device") for l in devices):
        sys.exit("No authorized device found. Check USB debugging and the prompt on the phone.")

    if mode == "off":
        cmd = "service call SurfaceFlinger 1015 i32 0"
    else:
        floats = " ".join(f"f {v}" for v in MATRICES[mode])
        cmd = f"service call SurfaceFlinger 1015 i32 1 {floats}"

    out = adb("shell", cmd)
    print(out.strip())
    print(f"Mode '{mode}' sent. Run with 'off' to restore colors.")


if __name__ == "__main__":
    main()
