#!/usr/bin/env python3
"""Repack DuoFace 1.0.3-6 as 1.0.3-8 with rootless payload paths.
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
    # Shared DuoNavi/ElleKit paths must never be owned by DuoFace.
    # Keep private copies of DuoFace helpers instead of overwriting DuoNavi.
    private_helpers = {
        "var/jb/usr/bin/cboptimize": "var/jb/usr/bin/duoface-cboptimize",
        "var/jb/usr/libexec/cboptimize_helper": "var/jb/usr/libexec/duoface_cboptimize_helper",
    }
    for original, private in private_helpers.items():
        old = root / original
        if old.exists():
            target = root / private
            target.parent.mkdir(parents=True, exist_ok=True)
            old.rename(target)
    # OldABI is supplied by the existing jailbreak/ElleKit; do not overwrite it.
    oldabi = root / "var/jb/usr/lib/ellekit/OldABI.dylib"
    if oldabi.exists():
        oldabi.unlink()
    postinst = root / "DEBIAN/postinst"
    if postinst.exists():
        script = postinst.read_text()
        script = script.replace("/var/jb/usr/libexec/cboptimize_helper", "/var/jb/usr/libexec/duoface_cboptimize_helper")
        script = script.replace("/usr/libexec/cboptimize_helper", "/var/jb/usr/libexec/duoface_cboptimize_helper")
        # Remove the complete OldABI permissions block, preserving shell syntax.
        begin = script.find("# Auto-configure OldABI permissions")
        end = script.find("# Set setuid root permissions", begin)
        if begin != -1 and end != -1:
            script = script[:begin] + script[end:]
        postinst.write_text(script)
    for original in (*private_helpers, "var/jb/usr/lib/ellekit/OldABI.dylib"):
        assert not (root / original).exists(), "Shared file remains: " + original
    ctl = root / "DEBIAN" / "control"
    lines = ctl.read_text().splitlines()
    lines = ["Version: 1.0.3-8" if x.startswith("Version: ") else x for x in lines]
    ctl.write_text("\n".join(lines) + "\n")
    assert (root / "var/jb/Applications/DuoFaceUI.app").is_dir()
    assert (root / "var/jb/Library/MobileSubstrate/DynamicLibraries/DuoFaceDashboard.dylib").is_file()
    for name in ("Applications", "Library", "etc", "usr"):
        assert not (root / name).exists(), "Unexpected rootful path: " + name
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["dpkg-deb", "--build", "--root-owner-group", str(root), str(dst)], check=True)
    assert subprocess.check_output(["dpkg-deb", "-f", str(dst), "Package"], text=True).strip() == "com.duoface.app"
    assert subprocess.check_output(["dpkg-deb", "-f", str(dst), "Version"], text=True).strip() == "1.0.3-8"
    listing = subprocess.check_output(["dpkg-deb", "-c", str(dst)], text=True)
    assert "./var/jb/Applications/DuoFaceUI.app/" in listing
    assert "./Applications/" not in listing
    print("SHA256", hashlib.sha256(dst.read_bytes()).hexdigest(), dst)
