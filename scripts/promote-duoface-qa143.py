#!/usr/bin/env python3
"""Promote one SHA-pinned, independently signed QA143 DuoFace DEB to Sileo.
Publisher metadata only; keep the old QA142 archive and rollback URL.
This script intentionally fails if any upstream build.yml contract has drifted.
"""
from pathlib import Path
import argparse

FILE="com.duoface.jb.embedded_0.0.143~homebridge1_iphoneos-arm64.deb"
SHA="db9019a708c4905602d00ed500878c01f208b26655e42ee079dacf30d925c39c"
URL=("https://raw.githubusercontent.com/chuongnguyen89dn-ui/Duoface/"
     "e475878b2fe93dde2e62f66f5f8c2d1217798618/"
     "sideplay/jb-embedded-appbridge/evidence/runs/41177472190/"+FILE)
OLD="0.0.142~homeabi1"
NEW="0.0.143~homebridge1"

def only_once(s,old,new):
    n=s.count(old)
    if n!=1: raise RuntimeError(f"Expected exactly one original Sileo publisher anchor, got {n}: {old[:100]}")
    return s.replace(old,new)

def patch(s):
    if "DUOFACE_143_FILE=" in s: raise RuntimeError("QA143 publisher already present: prevent duplicate")
    # Existing QA142 is retained and still verifies its own archived binary.
    anchor="          cd repo\n          dpkg-scanpackages -m debs /dev/null > Packages"
    block=f"""          # QA143 signed first-party Home-click to hosted-scene test.
          # Sileo install is for physical QA; NOT a claimed real-device tap pass.
          # Keep QA142 source/DEB above as an immutable rollback.
          DUOFACE_143_FILE='{FILE}'
          DUOFACE_143_SHA='{SHA}'
          DUOFACE_143_URL='{URL}'
          curl -fLsS --retry 4 "$DUOFACE_143_URL" -o "repo/debs/$DUOFACE_143_FILE"
          printf '%s  %s\\n' "$DUOFACE_143_SHA" "repo/debs/$DUOFACE_143_FILE" | sha256sum -c -
          test "$(dpkg-deb -f "repo/debs/$DUOFACE_143_FILE" Package)" = 'com.duoface.jb.embedded'
          test "$(dpkg-deb -f "repo/debs/$DUOFACE_143_FILE" Version)" = '{NEW}'
          test "$(dpkg-deb -f "repo/debs/$DUOFACE_143_FILE" Architecture)" = iphoneos-arm64
          mkdir -p "$RUNNER_TEMP/duoface-143-verified"
          dpkg-deb -x "repo/debs/$DUOFACE_143_FILE" "$RUNNER_TEMP/duoface-143-verified"
          QA143_EXTRACT="$RUNNER_TEMP/duoface-143-verified" python3 - <<'PY'
          import os,plistlib
          from pathlib import Path
          root=Path(os.environ['QA143_EXTRACT'])/'var/jb'
          info=plistlib.loads((root/'Applications/DuoFaceNativeHost.app/Info.plist').read_bytes())
          assert info['CFBundleVersion']=='143',info
          assert info['CFBundleShortVersionString']=='0.1.143',info
          libs=root/'Library/MobileSubstrate/DynamicLibraries'
          for name in ('DFTouchOwnerProbe','DFCarPlayDockOwner','DFNativeMapPaneCoordinator','DFYouTubeOrientationRelay','DFGofaMapResize141'):
              assert (libs/(name+'.dylib')).is_file(),name
          car=(libs/'DFCarPlayDockOwner.dylib').read_bytes()
          host=(libs/'DFTouchOwnerProbe.dylib').read_bytes()
          app=(root/'Applications/DuoFaceNativeHost.app/DuoFaceNativeHost').read_bytes()
          assert b'DuoFaceHomeLaunch143.log' in car
          assert b'DuoFaceHomeAdmission141.log' in car
          assert b'home143-request.plist' in car
          assert b'home143-request.plist' in host
          assert b'DuoFaceHomeLaunch143.log' in app
          print('QA143_SIGNED_REAL_SCENE_BRIDGE_COMPONENTS_VERIFIED_DEVICE_PENDING')
          PY
"""
    s=only_once(s,anchor,block+anchor)
    swaps=[
      ("assert len(hits)==96,hits","assert len(hits)==97,hits"),
      ("'0.0.142~homeabi1'},hits","'0.0.142~homeabi1','0.0.143~homebridge1'},hits"),
      ("and fields(b).get('Version') != '0.0.142~homeabi1'",
       "and fields(b).get('Version') != '0.0.143~homebridge1'"),
      ("assert a.get('Version')=='0.0.142~homeabi1'",
       "assert a.get('Version')=='0.0.143~homebridge1'"),
      ("assert a.get('Filename')=='debs/com.duoface.jb.embedded_0.0.142~homeabi1_iphoneos-arm64.deb'",
       "assert a.get('Filename')=='debs/"+FILE+"'"),
      ("assert a.get('SHA256')=='9f8c35435538f5b80822f2c072260ca3b4cc55b10777d130559fef6e4d1e8329'",
       "assert a.get('SHA256')=='"+SHA+"'"),
      ("len(live)==1 and live[0]['Version']=='0.0.142~homeabi1'",
       "len(live)==1 and live[0]['Version']=='0.0.143~homebridge1'"),
      ("len(others)==1 and others[0]['Version']=='0.0.142~homeabi1'",
       "len(others)==1 and others[0]['Version']=='0.0.143~homebridge1'"),
      ("""          VER='0.0.142~homeabi1'
          FILE='com.duoface.jb.embedded_0.0.142~homeabi1_iphoneos-arm64.deb'
          SHA='9f8c35435538f5b80822f2c072260ca3b4cc55b10777d130559fef6e4d1e8329'""",
       f"""          VER='{NEW}'
          FILE='{FILE}'
          SHA='{SHA}'"""),
    ]
    for before,after in swaps:
        s=only_once(s,before,after)
    # Preserve the old QA142 immutable reference. A second latest record is forbidden.
    assert s.count("DUOFACE_142_FILE=")==1
    assert s.count("DUOFACE_143_FILE=")==1
    assert s.count("assert len(hits)==97,hits")==1
    assert "VERSION_143_NOT_PUBLISHED" not in s
    return s

def main():
    p=argparse.ArgumentParser()
    p.add_argument("publisher_workflow",type=Path)
    p.add_argument("--check-only",action="store_true")
    args=p.parse_args()
    existing=args.publisher_workflow.read_text()
    edited=patch(existing)
    if not args.check_only:
        args.publisher_workflow.write_text(edited)
    print("DUOFACE_QA143_PUBLISHER_PATCH_CHECKED",len(existing),len(edited),
          "sha",SHA,"check_only",args.check_only)

if __name__=="__main__":main()
