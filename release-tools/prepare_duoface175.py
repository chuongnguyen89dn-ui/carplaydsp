"""Print a narrowly scoped release diff. No network, Git writes, or deployment.

Input is the exact existing publisher workflow. The prior QA174 release block
and its signed archive stay unchanged. Only DuoFace's active version metadata
and its checksum verification are advanced to the already signed QA175 DEB.
"""
from pathlib import Path
import difflib
import hashlib
import sys

PATH = Path('.github/workflows/build.yml')
BASE_BLOB = 'abd43043cbd889c7bac7843423aa7a9e9b734998'
OLD = '0.0.174~mapwake1'
NEW = '0.0.175~wakepick1'
OLD_SHA = 'f45e30bc92c984b7beaf13d1d03d88ffd5015780bd0080c15d859bddbc3f02cd'
NEW_SHA = 'e53451895bd991be072dfa1cfaf515ee5a1fee28ca992b6952c09c259bf6dbb1'
OLD_URL = 'https://raw.githubusercontent.com/chuongnguyen89dn-ui/Duoface/f63d2e1f15a842088f17b4af2c4c498aabbe674d/sideplay/jb-embedded-appbridge/evidence/runs/42155565599/'
NEW_URL = 'https://raw.githubusercontent.com/chuongnguyen89dn-ui/Duoface/1688f4e92135b6b46d7fa3e8fa5cb94d850ea447/sideplay/jb-embedded-appbridge/evidence/runs/42168269030/'

def once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise ValueError('Publisher context changed: ' + repr(old[:100]))
    return text.replace(old, new, 1)

def proposed(original: bytes) -> str:
    blob = hashlib.sha1(b'blob ' + str(len(original)).encode() + b'\0' + original).hexdigest()
    if blob != BASE_BLOB:
        raise ValueError('Unexpected publisher blob; review current source instead of overwriting')
    source = original.decode('utf-8')
    start = source.index('          # QA174: official latest DuoFace build, exact signed immutable source archive.')
    stop = source.index('          cd repo\n          dpkg-scanpackages -m debs /dev/null > Packages', start)
    retained = source[start:stop]
    addition = retained.replace('QA174', 'QA175').replace('qa174', 'qa175')
    addition = addition.replace(OLD_URL, NEW_URL).replace(OLD, NEW).replace(OLD_SHA, NEW_SHA)
    addition = once(addition, "str(info['CFBundleVersion'])=='174'", "str(info['CFBundleVersion'])=='175'")
    addition = once(addition, 'test -s "$QA_DIR/debs/$QA173_FILE"', 'test -s "$QA_DIR/debs/$QA174_FILE"')
    addition = once(addition,
        "          assert b'qa178-native-map-picker-ack-applied' in spring\n",
        "          assert b'qa178-native-map-picker-ack-applied' in spring\n"
        "          assert b'DFOwnedWakeSurface180' in spring\n"
        "          assert b'qa180-wake-contact' in spring\n"
        "          assert b'qa180-map-replace-prepared' in spring\n")
    addition = addition.replace('# Preserve QA173 and all previous binaries', '# Preserve QA174 and all previous binaries')
    tail = source[stop:]
    tail = once(tail, 'assert len(hits)==121,hits', 'assert len(hits)==122,hits')
    set_end = tail.index("'},hits", tail.index("assert {x.get('Version') for x in hits}==")) + len("'},hits")
    history, active = tail[:set_end], tail[set_end:]
    history = once(history, "'" + OLD + "'},hits", "'" + OLD + "','" + NEW + "'},hits")
    if active.count(OLD) < 5 or active.count(OLD_SHA) != 2:
        raise ValueError('Unexpected active DuoFace verification references')
    active = active.replace(OLD, NEW).replace(OLD_SHA, NEW_SHA)
    anchor = "          echo 'DUOFACE_PUBLIC_SILEO_DEB_DOWNLOAD_AND_CHECKSUM_VERIFIED'\n"
    rollback = (
        "          # Verify the immediately previous signed release remains downloadable.\n"
        "          OLD174='com.duoface.jb.embedded_" + OLD + "_iphoneos-arm64.deb'\n"
        "          curl -fLsS --retry 4 \"$SITE/debs/$OLD174\" -o \"$RUNNER_TEMP/duoface-mapwake1-rollback.deb\"\n"
        "          printf '%s  %s\\n' '" + OLD_SHA + "' \"$RUNNER_TEMP/duoface-mapwake1-rollback.deb\" | sha256sum -c -\n"
        "          test \"$(dpkg-deb -f \"$RUNNER_TEMP/duoface-mapwake1-rollback.deb\" Version)\" = '" + OLD + "'\n"
        "          echo 'DUOFACE_QA174_ROLLBACK_BYTES_PRESERVED'\n")
    active = once(active, anchor, anchor + rollback)
    result = source[:stop] + '\n' + addition + history + active
    if result[:stop] != source[:stop] or retained not in result:
        raise ValueError('Historical release bytes must be retained')
    for protected in ('permissions:', 'contents: read', 'pages: write', 'id-token: write', 'cancel-in-progress: true'):
        if result.count(protected) != source.count(protected):
            raise ValueError('Permissions or concurrency changed')
    return result

def main() -> None:
    original = PATH.read_bytes()
    candidate = proposed(original)
    diff = difflib.unified_diff(original.decode('utf-8').splitlines(keepends=True),
        candidate.splitlines(keepends=True), fromfile='a/' + str(PATH), tofile='b/' + str(PATH))
    sys.stdout.write(''.join(diff))

if __name__ == '__main__':
    main()
