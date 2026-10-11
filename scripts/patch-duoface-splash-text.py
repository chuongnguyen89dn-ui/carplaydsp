#!/usr/bin/env python3
"""Visual-only DuoFace splash text patch for an extracted rootless package.

Keep binary size, Mach-O structure, callbacks, and animation byte-identical
except for the exact, known C string bytes. Never patch DuoNavi.
"""
import hashlib
import pathlib
import sys

STRINGS = (b"TWO SCREENS. ZERO LIMITS.", b"WORKS WITH APPLE CARPLAY")
FILES = (
    "var/jb/Applications/DuoFaceUI.app/DuoFaceUI",
    "var/jb/Library/MobileSubstrate/DynamicLibraries/DuoFaceDashboard.dylib",
)

def patch(root: pathlib.Path):
    report = []
    for relative in FILES:
        path = root / relative
        if not path.is_file():
            raise RuntimeError(f"Missing expected DuoFace binary: {relative}")
        original = path.read_bytes()
        if original[:4] not in (b"\xcf\xfa\xed\xfe", b"\xca\xfe\xba\xbe"):
            raise RuntimeError(f"Not a recognized Mach-O binary: {relative}")
        modified = original
        counts = {}
        for needle in STRINGS:
            count = modified.count(needle + b"\0")
            if count != 2:
                raise RuntimeError(f"Unexpected splash text occurrences ({count}) in {relative}: {needle!r}")
            modified = modified.replace(needle + b"\0", b" " * len(needle) + b"\0")
            counts[needle.decode()] = count
        if len(modified) != len(original):
            raise AssertionError("Binary length changed")
        path.write_bytes(modified)
        report.append((relative, hashlib.sha256(original).hexdigest(), hashlib.sha256(modified).hexdigest(), counts))
    for item in report:
        print("PATCHED", *item)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: patch-duoface-splash-text.py EXTRACTED_ROOTLESS_DEB_DIRECTORY")
    patch(pathlib.Path(sys.argv[1]))
