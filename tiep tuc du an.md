# Tiếp tục dự án CarPlay Split

## 2026-10-21 — Gate1 0.0.5~roster1 Sileo live VERIFIED (device icon still UNVERIFIED)

- New isolated Gate1-only pin in `.github/workflows/build.yml` at commit `d9aef6857c525bd0a8c600759ac952632248e400`. Source repo `chuongnguyen89dn-ui/Duoface`, implementation commit `3c6613bc268d5ce82d3a126da7e44d023784c945`, CI [39541588347](https://github.com/chuongnguyen89dn-ui/Duoface/actions/runs/39541588347) completed SUCCESS; source binary saver HEAD `e00891cf9f65fa32fb3bf52482054e3fdf628d4c`.
- Version `0.0.5~roster1`, package `com.duoface.carplay.gate1smoke`, exact source DEB `sideplay/carplay-gate1-smoke/packages/com.duoface.carplay.gate1smoke_0.0.5~roster1_iphoneos-arm64.deb`, SHA256 `781ccc1baefcde3d4374bcbd7ec609e7ade7b90c0248d20e90f3bf756e23c752`.
- Publisher [Actions 39541812741](https://github.com/chuongnguyen89dn-ui/carplaydsp/actions/runs/39541812741) build/deploy/live `verify-qa11-pages` **completed SUCCESS**; live verifier job **119031942866**, stdout includes `GATE1_PUBLIC_SILEO_SINGLE_ISOLATED_APT_ENTRY_PASS`, `/home/runner/work/_temp/gate1-public.deb: OK`, `GATE1_PUBLIC_SILEO_BINARY_SHA256_PASS_NO_DEVICE_CARPLAY_PROOF`, and stable QA regression. Workflow YAML validator [39541812669](https://github.com/chuongnguyen89dn-ui/carplaydsp/actions/runs/39541812669) completed success.
- Public APT source `https://chuongnguyen89dn-ui.github.io/carplaydsp/`. Public binary `https://chuongnguyen89dn-ui.github.io/carplaydsp/debs/com.duoface.carplay.gate1smoke_0.0.5~roster1_iphoneos-arm64.deb`. Verifier fetched actual live Packages and DEB with exact version/hash; this is **NOT proof the Home icon or UIKit scene works on physical DiPlay**.
- Scope: Sileo Gate1 stanza only; packages Native12/HUD8/stable QA untouched. Test only when parked: update Gate1 via Sileo, explicitly enable as needed, ensure actual CarPlay Home visible, then use new phone button **THỬ HIỆN TRÊN CARPLAY** and read `Result`. Old **KIỂM TRA ĐĂNG KÝ** still only read-only. Error `DASHBOARD_CONTROLLER_NOT_LOADED` means live Dashboard class unavailable on that process at that time, not rejection of entitlement. Do not claim success until icon+scene+Dock tested.


## 2026-10-21 — Gate1 0.0.4~runtimeaudit1 live Sileo verified (read-only CarPlay roster diagnostics; NOT app acceptance)

- User requires a thoroughly verified end-to-end iOS16 jailbreak CarPlay Home registration before feature merge; physical Gate1 `0.0.3~enablefix1` reported `GATE1_ENABLED=YES` but **NO CarPlay Home icon**. Do not claim a working DuoFace.
- Distinct app/package `com.duoface.carplay.gate1smoke` now **`0.0.4~runtimeaudit1`**. Source repo `chuongnguyen89dn-ui/Duoface` feature code commit `ca24c76f46174ede367e4a643941e7144c2f6c22`, tested in [Actions 39535736561](https://github.com/chuongnguyen89dn-ui/Duoface/actions/runs/39535736561) **PASS**; artifact saver GitHub commit `d4e43ac9035a4bf57272885e73434ab9874e9d74`, blob `1b258d38bab43ab4d3483b12ad3359c60bb1ca6b`, size 34012 bytes, SHA256 `41344200e62e4a152c2ddd1eaa8bfa02840a322cbfb44c14f90b9846b77d9106`, file `sideplay/carplay-gate1-smoke/packages/com.duoface.carplay.gate1smoke_0.0.4~runtimeaudit1_iphoneos-arm64.deb`.
- Only existing publisher `.github/workflows/build.yml` Gate1 pin/version/source updated, commit `25b239cf8979ced7369f476a191edf53486467b7`. [Publisher Actions 39535973691](https://github.com/chuongnguyen89dn-ui/carplaydsp/actions/runs/39535973691) **SUCCESS** including build, Pages deployment and `verify-qa11-pages` job `119013314492`. Decoded logs `GATE1_PUBLIC_SILEO_SINGLE_ISOLATED_APT_ENTRY_PASS` and `GATE1_PUBLIC_SILEO_BINARY_SHA256_PASS_NO_DEVICE_CARPLAY_PROOF`. Verified actual public Pages APT single Gate1 stanza for version 0.0.4 and remote DEB SHA exact. Sileo `https://chuongnguyen89dn-ui.github.io/carplaydsp/`, binary `https://chuongnguyen89dn-ui.github.io/carplaydsp/debs/com.duoface.carplay.gate1smoke_0.0.4~runtimeaudit1_iphoneos-arm64.deb`. Original QA/Native12/HUD8 pins left unchanged and public QA checks PASS.
- This isolated update adds **only a bounded read-only diagnostics button** `KIỂM TRA ĐĂNG KÝ` on the iPhone Gate1 app. Produces per-process matching UUID nonce/age<=45s feedback, true hook-armed bit, own LaunchServices existence and iOS16 ABI-gated single-bundle `DBApplicationController` roster check. UI auto-refresh 2s; `CHƯA TRẢ LỜI` is explicitly unknown, not app failure or pass. No roster/icon mutation, third-party code, respring or Dock overlay. Need one actual parked iPhoneX + DiPlay screenshot from user showing fresh **CarPlay HookReady, LSOwn, Roster, DashBoardLoaded**. Then implement correct admission adapter based on exact real observed failure; **no further blind entitlement/timer fixes**. Do not represent this diagnostic as working CarPlay Home app.
- Full implementation/evidence/handoff: `Duoface/sideplay/tiep tuc du an.md` main commit `8a7d31c200672c9f0c8a89dd991994428ad8edbf`, and `Duoface/sideplay/audit/gate1-end-to-end-20261021/INTEGRATION_AUDIT.md` feature commit `f0023985d7bdd59324051a836e54204726cdf51f`.



## 2026-10-21 — Gate1 0.0.3~enablefix1 public Sileo SHA VERIFIED; device pending

- User's 2026-10-21 actual iPhone photos show original Gate1 smoke2 modules LOADED in SpringBoard + CarPlay, but enable button repeatedly `enable-refused (old gate enabled or preferences denied)` and `GATE1_ENABLED=NO`. DuoFace repo feature source fixed effective legacy gate checks, explicit user-confirmed temporary kill-switch pause/rollback, precise error reason and removed arbitrary 10 minute expiry; updated app version `0.0.3~enablefix1`, no code or packages touching Native12/HUD8, no monolithic 0.0.7 release.
- Verified DuoFace [GitHub Actions run 39528331434](https://github.com/chuongnguyen89dn-ui/Duoface/actions/runs/39528331434) success, artifact source/binary commit `2f9b881a240aaac6ba8df8665e6143833a2058a0`, SHA256 **`e4ac22e948f1936cd5f54ad7bc14fa31696a1e80bc2f7358b0ba8b2cce9af732`**, path `sideplay/carplay-gate1-smoke/packages/com.duoface.carplay.gate1smoke_0.0.3~enablefix1_iphoneos-arm64.deb` (29968 bytes).
- This **publisher** `.github/workflows/build.yml` immutable Gate1 pin updated by commit `0581361baedb8c02c38d082dd57fc22642f41596`; no other independent QA pins altered. [Sileo run 39528590666](https://github.com/chuongnguyen89dn-ui/carplaydsp/actions/runs/39528590666) completed SUCCESS including Pages deploy and live verifier job `118989577852`: exact public APT one Gate1 package version 0.0.3, downloaded remote .deb checksum PASS `GATE1_PUBLIC_SILEO_SINGLE_ISOLATED_APT_ENTRY_PASS`, `GATE1_PUBLIC_SILEO_BINARY_SHA256_PASS_NO_DEVICE_CARPLAY_PROOF`; stable QA package integrity tests PASS. Official APT source `https://chuongnguyen89dn-ui.github.io/carplaydsp/`; remote file `https://chuongnguyen89dn-ui.github.io/carplaydsp/debs/com.duoface.carplay.gate1smoke_0.0.3~enablefix1_iphoneos-arm64.deb`. Previous smoke2 superseded.
- **Real device status**: not yet tested after this fix. Next only Gate1 beta update via Sileo on parked iPhone X JB; confirm `GATE1_ENABLED=YES` and no exact enable-refused reason first, then Home icon and native CarPlay UIWindowScene, Dock. Legacy QA module untouched; when Gate1 explicitly paused it via its kill switch, app `TẮT` / `prerm` restores. Do not infer runtime success from CI/Pages. Full technical handoff: `chuongnguyen89dn-ui/Duoface:sideplay/tiep tuc du an.md` main commit `f6992a2068a1f809bb07ff4921569583e0636a33`.



## 2026-10-21 — LIVE SILEO DuoFace Gate1 smoke2, proof in public Packages (NO hardware proof)

- Updated ONLY existing `.github/workflows/build.yml` pin and live verifier, commits `0b9ded45f3974d63aa34318aa0ec9fd2a396c23d` (initial smoke1) and final `4164bc5ba395eb18368cf9ee76bcf74e49911eac` (superseding smoke2). New **separate** package `com.duoface.carplay.gate1smoke 0.0.2~smoke2`, architecture `iphoneos-arm64`; no Conflicts/Replaces/Breaks/Provides, no dependency on Native12/HUD8/QA, no installed stable package changed. This is NOT the monolithic `com.duoface.jb.embedded`. Earlier smoke1 is superseded; install only smoke2.
- Source exact DuoFace project feature artifact commit `140433a37a33f0bd53618d8504f2c830e8316698`, `sideplay/carplay-gate1-smoke/packages/com.duoface.carplay.gate1smoke_0.0.2~smoke2_iphoneos-arm64.deb`. SHA256 `f1effac6051103ff9c0cff60e0fe9cb8faa0647e7606d94e15829f84c89832a3`, signed Mach-O headerpad and signature nonoverlap static check PASS in DuoFace CI [39522725164](https://github.com/chuongnguyen89dn-ui/Duoface/actions/runs/39522725164). Own iPhone app + icon, opt-in 600sec unique SpringBoard/CarPlay tweak + kill switch and native UIWindowScene handler. No auto-respring.
- **Verified public release:** GitHub Actions [39522945378](https://github.com/chuongnguyen89dn-ui/carplaydsp/actions/runs/39522945378) build, Pages deploy and verify-qa11-pages all SUCCESS. Actual live Pages verifier job `118971806875`: `GATE1_PUBLIC_SILEO_SINGLE_ISOLATED_APT_ENTRY_PASS`, `GATE1_PUBLIC_SILEO_BINARY_SHA256_PASS_NO_DEVICE_CARPLAY_PROOF`; HTTP download `https://chuongnguyen89dn-ui.github.io/carplaydsp/debs/com.duoface.carplay.gate1smoke_0.0.2~smoke2_iphoneos-arm64.deb` matched SHA. Single exact `Packages` APT stanza. Existing QA/Native12/HUD8 package checks in same CI PASS.
- User acceptance is still **NOT DONE**: actual iPhone X rootless iOS16 + DiPlay, CarPlay Home icon, native blue Gate1 proof scene, Dock, reconnect/disable/uninstall. Must not declare DuoFace functional before user test. Sileo source `https://chuongnguyen89dn-ui.github.io/carplaydsp/`; search `DuoFace CarPlay Gate 1 (Safe Beta)`. Original DuoFace project primary handoff `Duoface/sideplay/tiep tuc du an.md` on main commit `baafb1ee672bbabcfe45f1d99182ca1ad1b015f7` contains complete build instructions and device QA constraints. Do not modify old Native12/HUD8 or rerun feature-merge before Gate1 acceptance.



## 2026-10-02 — phát hành DuoDash gốc + adapter qua Sileo

Yêu cầu hiện tại: DEB phải xuất hiện trong nguồn Sileo
`https://chuongnguyen89dn-ui.github.io/carplaydsp/`, không yêu cầu người dùng
tải artifact để cài thủ công.

Gói mới: **DuoDash Fullscreen (Original UI)**,
`com.chuong.duodash-fullscreen-complete`, phiên bản `1.1.3+adapter1~test1`.
Workflow main build adapter từ commit `ccadfe2`, rồi đóng gói cùng DuoDash
1.1.3 trong DEB đã có tại DauDat-CarPlay. Giữ nguyên từng byte của 42 file
DuoDash (binary, UI/app picker/split, tài nguyên, Settings); chỉ bỏ hai file
`DuoDashUnifiedFullscreen` cũ và thêm hai file adapter. Không ghép Airaw.
Script kiểm tra SHA256 DEB nguồn, toàn bộ payload và các script cài/gỡ.

Gói đầy đủ chứa sẵn DuoDash nên không phụ thuộc sai phiên bản `= 1.1.3` trên
máy đang có `1.1.3+fullscreen1`. Khai báo xung đột với các bản DuoDash/Airaw,
Split độc lập và adapter rời để Sileo không cài chồng các engine/fullscreen.
Không thay chỉ mục hay xóa các gói cũ khỏi nguồn.

Đây là **bản thử nghiệm**: adapter đã build/test vòng đời đối tượng PASS;
chưa có ảnh Simulator của UI gốc hoặc kết quả runtime CarPlay thật.
Lỗi đỏ từng báo thuộc bản Split tự viết, chưa được xác nhận ở DuoDash gốc.
Không coi lỗi đó là điều kiện chặn việc dùng lại engine DuoDash nguyên bản.
Sau deploy phải đọc lại Packages/Packages.gz và tải DEB từ Pages để đối chiếu
SHA256, tên, phiên bản, phụ thuộc và payload trước khi báo đã lên Sileo.

## 2026-09-29 — phát hành alpha theo yêu cầu chủ repo

Đưa gói độc lập `com.chuong.carplaysplit` phiên bản `0.2.0~alpha1` vào nguồn Sileo hiện có. DEB gồm app điều khiển và tweak; không chứa binary DuoDash/Airaw. Đã biên dịch arm64/iOS 16 rootless, kiểm tra chữ ký Mach-O, phụ thuộc hệ thống và cấu trúc DEB. Chưa xác minh hoạt động trên thiết bị CarPlay thật.

Trong Sileo tìm **CarPlay Split**. Sau cài đặt và respring, mở app CarPlay Split trên iPhone khi đang kết nối CarPlay để bật. Menu ba chấm chọn app/thoát; kéo tay nắm đổi tỷ lệ; nút mũi tên đổi bên. Bản alpha không được quảng cáo là đã hoàn thiện hoặc hoạt động đúng video.

Mã nguồn bản dựng: commit a31be26 trong nhánh triển khai cục bộ. Lần xuất bản này chỉ thêm DEB và ghi chú phát hành vào main; không công khai thêm các tài liệu phân tích riêng của nhánh nghiên cứu.


## 2026-09-29 — sửa lỗi khởi động alpha1

Crash report của người dùng: EXC_BAD_INSTRUCTION/SIGILL tại `-[CPSPhoneController viewDidLoad] + 0`, offset 0xD58, iPhone 8 Plus/iOS 16.7.16. Binary alpha1 có vùng load commands kết thúc ở 0xD68 nhưng `__text` bắt đầu 0xD58: LC_CODE_SIGNATURE 16 byte đã ghi đè đầu mã. Cả executable và dylib đều có cùng lỗi.

Alpha2 bổ sung `-Wl,-headerpad,0x1000`, dựng bằng Xcode trên macOS, nâng CFBundleVersion lên 2. Trình kiểm tra gói từ chối mọi section dữ liệu/mã chồng lên load commands và đã tái hiện lỗi với alpha1. Không thay đổi tính năng chia đôi trong bản sửa này. Không đưa crash report chứa định danh thiết bị lên repo.

Sau cập nhật Sileo lên 0.2.0~alpha2 và respring, app điều khiển phải hiện giao diện ngay cả khi chưa nối CarPlay. Chia đôi trên CarPlay vẫn cần xác minh trên thiết bị thật.

Xác minh: GitHub Actions run 36506567707 build/deploy thành công; đã tải lại alpha2 từ nguồn Sileo và kiểm tra cấu trúc binary cùng SHA256 khớp chỉ mục APT. Chưa xác nhận mở app trên thiết bị người dùng sau cập nhật.


## 2026-10-02 — test2: không thấy DuoDash trong Settings

Người dùng xác nhận không có mục DuoDash sau khi đóng/mở Settings. Chưa có log
Preferences trên thiết bị nên chưa kết luận nguyên nhân runtime. Kiểm tra test1
cho thấy bundle có đủ nhưng loader entry chỉ dùng dạng inline, không trỏ tới
DuoDashPrefs.bundle. Test2 khai báo bundle, bundlePath rootless và isController
rõ ràng; dùng đúng DuoDashRootListController có sẵn. Giữ danh sách items gốc
và đưa toàn bộ danh sách đó vào Root.plist của bundle để giữ cả Choose Apps
to Bridge, ngôn ngữ và các mục gốc khác. Icon trỏ tới file thực sự có trong gói.

Không đổi binary DuoDash, picker hoặc split engine. 40 file nguyên bản còn lại
giữ từng byte; chỉ sửa hai plist Settings bên cạnh thay helper fullscreen từ
test1. Phiên bản Sileo: 1.1.3+adapter1~test2. Sau deploy kiểm tra chỉ mục, hash
và loader/bundle/Root trong DEB tải từ nguồn; hiển thị Settings vẫn cần người
dùng xác nhận trên iPhone. Nếu vẫn không có, cần kiểm tra PreferenceLoader có
được inject vào Preferences và phiên bản thực sự đã cài; không quy lỗi do người
dùng hoặc tiếp tục khẳng định chỉ cần mở lại Settings.


## 2026-10-03 — quay về DEB nguồn nguyên trạng để đối chứng

Người dùng báo Settings trống sau test2. Chưa xác định nguyên nhân runtime;
không coi build PASS hoặc việc giữ binary là bằng chứng giữ nguyên hành vi.

Đưa nguyên DEB tại DauDat-CarPlay commit 5f683ad lên cùng nguồn Sileo.
Tên hiển thị trong chỉ mục: **DuoDash (Source DEB)**; mã gói thật:
`com.sensetechlab.duodash`; phiên bản thật: `1.1.3+fullscreen1`.
DEB SHA256: `ea0d3bb8c8b9da2b45c3f158f390a7966419e84899f820d06f45cd51401fa465`.
Không đóng gói lại, không sửa control, script, plist, binary hoặc helper đi kèm.
Nhãn Name chỉ thêm trong chỉ mục APT để tránh người dùng chọn nhầm.
Đây là nguyên bản file nguồn đã có trong repo, KHÔNG tuyên bố bản vendor 1.1.3
chưa chỉnh sửa: file này vốn đã có helper fullscreen và suffix +fullscreen1.

Trên máy: gỡ DuoDash Fullscreen (Original UI), rồi cài DuoDash (Source DEB),
respring và kiểm tra Settings trước khi thử split. Không cài chồng các bản
DuoDash/Airaw/adapter khác. Không tự cài/gỡ trên máy người dùng từ CI.
Chỉ tiếp tục ghép adapter khi có kết quả đối chứng. Các gói thử cũ giữ trên
nguồn phục vụ truy vết, nhưng không hướng dẫn cài test2 để làm đối chứng.


## 2026-10-20 — PUBLISH EXISTING OMNICAR UNIFIED 1.0.3-omnicar1 TO SILEO; KEEP OTHERS

- User explicitly requires new OmniCar QA releases via Sileo rather than manually downloading a DEB. This publishing repository is chuongnguyen89dn-ui/carplaydsp main, with source https://chuongnguyen89dn-ui.github.io/carplaydsp/.
- Changed ONLY existing .github/workflows/build.yml, commit b38dd812ee100f1e568bc2a92c0e9fa2d639b19c: added SHA256-pinned existing OmniCar 1.0.3-omnicar1 QA .deb from chuongnguyen89dn-ui/Omnicar commit 251ccec43f602a48b448427eb80d49d7c223ea9e. Exact SHA256 8a84b3d6a4d44ecdf2f7185ef6d79139eba85d4dd0b5769044daf8f61b7a8757, package com.anlai.omnicar architecture iphoneos-arm64. Verifies all 4 added dylib+plist pairs plus original OmniCarSplitScreen, and exactly one APT stanza; it never removes DuoFace/DuoDash/Hub from this repo. Do not silently update their pinned bytes or dependencies for OmniCar releases.
- YAML/actionlint run 39370226744 SUCCESS. Existing Sileo build/deploy GitHub Actions run https://github.com/chuongnguyen89dn-ui/carplaydsp/actions/runs/39370226883: build job 118456193155 SUCCESS, GitHub Pages deploy job 118456966918 SUCCESS, existing QA11 live validator job 118457022575 SUCCESS.
- Independent OmniCar live public verifier https://github.com/chuongnguyen89dn-ui/Omnicar/actions/runs/39370310105, job 118456451243 SUCCESS: actual public APT Packages + compressed index + Release SHA checksum entries, exactly one com.anlai.omnicar 1.0.3-omnicar1 entry, preserved DuoFace entries, downloaded full public OmniCar .deb sha256 EXACT, original SplitScreen and 4 module dylibs+plists present. Display name in original control is OmniCar. No real iPhone/CarPlay device QA yet.
- New delivery policy: for each future approved OmniCar build, publish by updating immutable OmniCar source commit/version/SHA in the SAME block of .github/workflows/build.yml, verifying APT/deploy/public downloaded hash, then instruct user only Sileo Sources → CarPlayDSP → Refresh → OmniCar upgrade; never require Filza/manual DEB downloads. Preserve all other packages and existing Sileo indexes. Latest OmniCar handoff: Omnicar/tiep tuc du an.md commit 2ad6605d4ee29ac23cfd7abe7eec4fae30bc2097.


## 2026-10-20 — OMNICAR QA3 PUBLIC SILEO HASH VERIFIED (OTHERS PRESERVED)

- User requires ALL further OmniCar test updates only through existing Sileo source https://chuongnguyen89dn-ui.github.io/carplaydsp/; no DEB manual/Filza. This repo is distributor, not OmniCar source.
- Changed ONLY .github/workflows/build.yml OmniCar SHA-pinned block commit 0716261e9077836c9a17bba9d8201643c4fe7813. Fetches exact immutable original-derived QA3 artifact from chuongnguyen89dn-ui/Omnicar commit 08671fb35e5b487a062895f4bb699d3d394f232a, ID com.anlai.omnicar, version 1.0.3-omnicar3, SHA256 482253a8bedc51a73f69745c797cdbc2ef84a8b2947a95aeccc77f39641ac310. Package contains 176 original files unchanged plus 4 tweak dylibs + 4 plist filters, no changed DuoFace/DuoDash/Hub pin.
- Actual YAML/actionlint validation run 39375171089 SUCCESS; CarPlayDSP publisher run https://github.com/chuongnguyen89dn-ui/carplaydsp/actions/runs/39375171119 all jobs SUCCESS: build 118471591680, deploy 118472099719, existing QA11 public validation 118472149751. Independent OmniCar live consumer verifier run https://github.com/chuongnguyen89dn-ui/Omnicar/actions/runs/39375190490, job 118471653160 SUCCESS, verified public Packages (one OmniCar newest entry), Packages.gz, Release, exact downloaded .deb SHA and four module payload; preserved relevant DuoFace Sileo APT stanzas. Runtime device testing of the behavioral bug fixes is still PENDING.
- This QA3 supersedes QA2 1.0.3-omnicar2 (which corrected Zoom/Swap state and SOLO but had an uncovered hosted pane handle); fixes source hostHandle and hostedPanes 4s auto-hide per original ABI. QA1 and QA2 archived in OmniCar project for rollback; do not alter independent package rows. Further OmniCar updates: update single pin and SHA only, deploy, verify downloaded public bytes before saying ready. Latest OmniCar handoff commit 791948446737bc097303c034b4a28d0b8a40a077.


## 2026-10-20 — SILEO published OmniCar QA4 native hosted-SOLO persistent menu

- User mandates tests through Sileo only, no manual DEB download. Sileo publisher for OmniCar uses the EXISTING source https://chuongnguyen89dn-ui.github.io/carplaydsp/ and existing .github/workflows/build.yml. DO NOT touch other DuoFace/DuoDash packages for future OmniCar releases.
- OmniCar project `chuongnguyen89dn-ui/Omnicar` has original verified unified QA4 `com.anlai.omnicar_1.0.3-omnicar4_iphoneos-arm64.deb` from immutable Omnicar commit 80dea078d87170b63116e0913ec1639c41bccfce, path dist/candidates/omnicar-unified-1.0.3-omnicar4/, package com.anlai.omnicar, SHA256 `209edb29c2da3f3a0ca366c015fc5f55fd7cbb2438eba526f5b85930c98b1ce4`, 1,369,844 bytes, preserves 176 original files and adds four dylibs/filters. Build/manifest GH Actions 39379051075 SUCCESS.
- THIS PUBLISHER UPDATE: .github/workflows/build.yml commit `d28fb16f1003323a7bd0c30058414f3f06f90dfb` updates ONLY the OmniCar source/version/file/SHA exact pin from QA3→QA4 and one APT entry assertion; other package logic untouched. YAML validator 39379352564 SUCCESS. Publish+Pages GitHub Actions run https://github.com/chuongnguyen89dn-ui/carplaydsp/actions/runs/39379352562 build and deploy SUCCESS. Independent Omnicar public byte verification https://github.com/chuongnguyen89dn-ui/Omnicar/actions/runs/39379372189 job 118484691667 SUCCESS: one exact public package, existing DuoFace packages retained; publicly downloaded whole QA4 DEB SHA exact, Release+Packages.gz good and original/four module bytes present.
- User-facing: only Sileo → Sources → CarPlayDSP → Refresh → OmniCar → upgrade 1.0.3-omnicar4. Device-functional QA of SOLO menu host-window overlay NOT YET PERFORMED. Zoom+Swap previously user-confirmed working and unchanged. If updated runtime still fails, inspect `[OmniCarSoloDots]` log and correct actual host window owner; do not infer functional success from Sileo deployment.
- Current QA4 OmniCar project handoff `Omnicar/tiep tuc du an.md` commit 02293c8f58f6c434a9fe1f7cc5c2b66673bf2660.


## 2026-10-20 — OmniCar emergency rollback QA5 after QA4 native CarPlay device regression

- User reports OmniCar QA4 Sileo caused a disconnect/crash with YouTube in split; two-map split loses divider/menu. Distinguish user-device FAIL from earlier CI-success.
- Sileo publisher build.yml commit e955b12c438d946a9236cd4f1467445507c2ba19 replaced pinned OmniCar QA4 ONLY with emergency **QA5**: com.anlai.omnicar 1.0.3-omnicar5 rootless iPhone ARM64, source archive Omnicar immutable commit a66b48a7a145f4adc47b12939a442ea3d4430664, file dist/candidates/omnicar-unified-1.0.3-omnicar5/com.anlai.omnicar_1.0.3-omnicar5_iphoneos-arm64.deb, SHA256 7198bce289bd0f7913c4a10c018ab4412207a478ce8a525d8b4674c903665249. QA5 compiles exact five runtime source blob hashes from previously user-tested QA2, no risky QA4 host UIWindow overlay; preserves 176 original original files +4 dylibs+4 plists. Other package build/pins and Sileo metadata not modified.
- Publisher YAML syntax validation run 39381943807 SUCCESS. GitHub Actions publishing https://github.com/chuongnguyen89dn-ui/carplaydsp/actions/runs/39381943870: build job 118492810406 SUCCESS, GitHub Pages deploy 118493823745 SUCCESS, existing other QA job 118493887600 SUCCESS. Public independent Omnicar Actions https://github.com/chuongnguyen89dn-ui/Omnicar/actions/runs/39381964894 job 118492876271 SUCCESS, actual public /Packages exact single QA5 stanza, downloaded QA5 .deb SHA256 `: OK`, original plus 8 added native files. Source https://chuongnguyen89dn-ui.github.io/carplaydsp/ .
- Device retest PENDING. User should refresh Sileo CarPlayDSP -> OmniCar 1.0.3-omnicar5; test YouTube+map and two map apps divided (control bar, per-pane menu), preserve Zoom/Swap. User-requested SOLO three-dot restore and 4s hide are NOT resolved by this emergency rollback. Coordinate next release only from actual device evidence and Omnicar/tiep tuc du an.md.
