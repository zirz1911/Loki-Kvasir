# Learning: Build Custom ROM — Full Playlist (surya / POCO X3 NFC)

**Date**: 2026-02-24
**Source**: YouTube Playlist — "Build Custom Rom" (12 episodes)
**Playlist**: https://www.youtube.com/watch?v=d8JhwX-cdDQ&list=PLQcIdsw6jRy2Et-TES3BVitOQKx733WkG
**Tags**: android, custom-rom, surya, poco-x3-nfc, lineageos, build-environment, device-tree

---

## Ep 01: Introduction

**Key concepts:**
- ROM building = sourcing the right puzzle pieces, not writing Android from scratch
- Three core components: device tree, vendor tree, kernel tree
- Understanding directory structure before touching a terminal

**Resources**: source.android.com, XDA Developers, GitHub

**Summary**: High-level intro to Android ROM development. Know where your surya-specific source files live before opening a terminal.

---

## Ep 02: How To Get Help?

**Key concepts:**
- Never send screenshots of errors — share full text logs
- Search XDA / Google before pinging maintainers
- Paste full output so experienced devs can actually read it

**Tools**: Telegram groups, Del.dog (pastebin), XDA Forums

**Summary**: Inevitable compilation errors need full log context. Learn log-sharing etiquette to get help from Telegram communities effectively.

---

## Ep 03: Device Trees

**Key concepts:**
- Three mandatory trees: **Device Tree**, **Vendor Tree**, **Kernel Tree**
- Key Makefiles: `BoardConfig.mk`, `device.mk` — map hardware configs
- Common Trees: Snapdragon 732G (surya) may share code with other devices
- Vendor blobs needed for MIUI firmware compatibility

**For surya specifically:**
- Device tree: `device/xiaomi/surya`
- Vendor tree: `vendor/xiaomi` (MIUI blobs)
- Kernel tree: `kernel/xiaomi/surya`

**Summary**: The build system reads hardware configs via Makefiles. Locate the three trees on GitHub before syncing.

---

## Ep 04: Build Environment

**Key concepts:**
- Minimum hardware: **16GB+ RAM**, **300–500GB storage**
- OS: Ubuntu 18.04 LTS or newer
- Options: local VM (VirtualBox) or cloud (GCP) for CPU headroom

**Tools**: Ubuntu 18.04, Oracle VM VirtualBox, Google Cloud Platform

**Summary**: ROM compilation is CPU/RAM intensive. Provision the environment before starting to avoid mid-build crashes.

---

## Ep 05: Install GUI

**Key concepts:**
- Install Ubuntu Desktop for GUI on remote server
- Configure SSH for remote desktop access
- Add sudo user

**Commands:**
```bash
sudo apt update && sudo apt upgrade
sudo apt install ubuntu-desktop
sudo adduser [user]
usermod -aG sudo [user]
# edit /etc/ssh/sshd_config
```

**Tools**: NoMachine (remote desktop)

**Summary**: For cloud build servers, install a desktop + NoMachine for graphical remote access instead of pure SSH.

---

## Ep 06: Setup Build Environment

**Key concepts:**
- Install Android build dependencies (Java, Python, specific libraries)
- Use automated script to avoid missing packages

**Commands:**
```bash
# Akhil Narang's script — installs everything in one hit
git clone https://github.com/akhilnarang/scripts
bash scripts/setup/android_build_env.sh
```

**Summary**: Never install dependencies manually. One script handles all required packages for Android compilation.

---

## Ep 07: GitHub

**Key concepts:**
- Set Git credentials before cloning any repos
- Required for cloning, syncing, and committing device trees

**Commands:**
```bash
sudo apt install git
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

**Summary**: Link your Git identity before starting. You'll clone surya repos heavily.

---

## Ep 08: Choosing the OS

**Key concepts:**
- Pick base ROM: LineageOS, Evolution X, etc. — match exact Android version branch
- `repo init` + `repo sync` pulls ~100GB of source

**Commands:**
```bash
mkdir ~/android/lineage && cd ~/android/lineage
repo init -u https://github.com/LineageOS/android.git -b lineage-20
repo sync -c --no-clone-bundle --no-tags
```

**Summary**: Pick your ROM flavor, run repo sync, let it download for hours. For surya: `lineage-20` branch (Android 13).

---

## Ep 09: Syncing Trees

**Key concepts:**
- Clone device/vendor/kernel trees into **exact correct paths** within ROM source
- Use `grep` to find expected paths if Makefile throws missing folder error

**Commands:**
```bash
# Clone into exact required paths
git clone -b [branch] [DEVICE_TREE_URL] device/xiaomi/surya
git clone -b [branch] [VENDOR_TREE_URL] vendor/xiaomi/surya
git clone -b [branch] [KERNEL_TREE_URL] kernel/xiaomi/surya

# Find expected path if unsure
grep -nr "surya" .
```

**Summary**: Inject surya-specific files into the generic Android source at precisely the right paths.

---

## Ep 10: Compiling ROM

**Key concepts:**
- Init build environment variables
- Select device target via `lunch`
- Cherry-pick patches if needed
- Run compile command — takes several hours

**Commands:**
```bash
. build/envsetup.sh
lunch lineage_surya-userdebug

# Optional: cherry-pick specific fixes
git cherry-pick [commit-hash]

# Compile
mka bacon          # LineageOS style
# or
make -j$(nproc)
```

**Summary**: Set environment → pick `surya` target → compile. CPU will crunch for hours.

---

## Ep 11: Fixing Errors

**Key concepts:**
- Common failure causes: missing vendor blobs, duplicate Makefile rules, SEpolicy conflicts
- Resume build without wiping entire output directory
- Read ninja error logs to pinpoint exact file/rule conflict

**Strategy:**
1. Read the last error line carefully — usually names the file
2. Fix the conflict in the device/vendor tree
3. Re-run `mka bacon` — build resumes from where it failed

**Summary**: First builds almost always fail. Don't wipe `out/` — fix the specific conflict and resume.

---

## Ep 12: Finalize and Distribute

**Key concepts:**
- Compiled ROM ZIP lives in `out/target/product/surya/`
- Upload to SourceForge via SFTP

**Commands:**
```bash
# Find your ROM
ls out/target/product/surya/*.zip

# Upload to SourceForge
sftp [user]@frs.sourceforge.net
put lineage-20.0-*-surya.zip
```

**Summary**: Build success → ZIP in `out/target/product/surya/`. Push to SourceForge to share.

---

## Critical Path for surya Build

```
1. Prep environment (ep 04-06)
   └── Ubuntu + 16GB RAM + 300GB storage + akhilnarang script

2. Setup git + init repo (ep 07-08)
   └── git config + repo init lineage-20 + repo sync (~100GB)

3. Clone surya trees (ep 09)
   ├── device/xiaomi/surya
   ├── vendor/xiaomi/surya   ← vendor blobs (MIUI firmware)
   └── kernel/xiaomi/surya

4. Compile (ep 10)
   └── . build/envsetup.sh → lunch lineage_surya-userdebug → mka bacon

5. Fix errors (ep 11)
   └── read ninja log → fix conflict → resume

6. Output (ep 12)
   └── out/target/product/surya/*.zip
```

---

## Key Repos to Find

| Component | Expected Path | Where to Find |
|-----------|--------------|---------------|
| Device tree | `device/xiaomi/surya` | GitHub: LineageOS/android_device_xiaomi_surya |
| Vendor tree | `vendor/xiaomi/surya` | TheMuppets or extract from device |
| Kernel tree | `kernel/xiaomi/surya` | GitHub: LineageOS or r0ttenbeef kernel |
