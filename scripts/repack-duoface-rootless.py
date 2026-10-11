#!/usr/bin/env python3
"""Repack DuoFace 1.0.3-6 as 1.0.3-7 with rootless payload paths.
Preserve all original binaries, hooks and maintainer scripts. Never overwrite DuoNavi.
"""
import hashlib
import pathlib
import shutil
import subprocess
import sys
import tempfile

EXPECTED = "2120480166170c5f71b12a595bed7a5ab892fbd84038ef878eca8e8243062e9a"
src, dst = map(pathlib.Path, sys.argv[1:3])
assert hashlib.sha256(src.read_bytes()).hexdigest() == EXPECTED, "Original DEB SHA-256 mismatch"
with tempfile.TemporaryDirectory() as tmp:
    root = pathlib.Path(tmp)
    subprocess.run(["dpkg-deb", "-R", str(src), str(root)], check=True)
    for name in ("Applications", "Library", "etc", "usr"):
        old = root / name
        if old.exists():
            new = root / "var" / "jb" / name
            new.parent.mkdir(parents=True, exist_ok=True)
            if new.exists():
                raise RuntimeError("Conflicting rootless destination: " + str(new))
            shutil.move(str(old), str(new))
    ctl = root / "DEBIAN" / "control"
    lines = ctl.read_text().splitlines()
    lines = ["Version: 1.0.3-7" if x.startswith("Version: ") else x for x in lines]
    ctl.write_text("\n".join(lines) + "\n")
    assert (root / "var/jb/Applications/DuoFaceUI.app").is_dir()
    assert (root / "var/jb/Library/MobileSubstrate/DynamicLibraries/DuoFaceDashboard.dylib").is_file()
    for name in ("Applications", "Library", "etc", "usr"):
        assert not (root / name).exists(), "Unexpected rootful path: " + name
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["dpkg-deb", "--build", "--root-owner-group", str(root), str(dst)], check=True)
    assert subprocess.check_output(["dpkg-deb", "-f", str(dst), "Package"], text=True).strip() == "com.duoface.app"
    assert subprocess.check_output(["dpkg-deb", "-f", str(dst), "Version"], text=True).strip() == "1.0.3-7"
    listing = subprocess.check_output(["dpkg-deb", "-c", str(dst)], text=True)
    assert "./var/jb/Applications/DuoFaceUI.app/" in listing
    assert "./Applications/" not in listing
    print("SHA256", hashlib.sha256(dst.read_bytes()).hexdigest(), dst)
