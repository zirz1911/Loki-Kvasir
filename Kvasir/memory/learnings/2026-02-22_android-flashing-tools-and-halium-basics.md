# Android Flashing Tools + Halium Basics

**Date**: 2026-02-22
**Source**: rrr — surya-linux-port-planning

## Pattern

When helping with Android device Linux porting on Xiaomi/Poco hardware:

### Flashing Tool Disambiguation (ALWAYS state upfront)
- **MiFlash** = official Xiaomi tool, MIUI/HyperOS only, `.tgz` packages
- **fastboot** = universal, works for everything (custom ROMs, Linux, recovery)
- **Heimdall** = Samsung ONLY (Odin/Thor protocol) — never for Xiaomi
- **EDL (9008 mode)** = emergency Qualcomm flashing, needs auth for most devices

### Halium/Hybris Path for Snapdragon Devices
1. Hybris (Android kernel + Linux userspace) >> Mainline for hardware support
2. Mainline kernel on Qualcomm Snapdragon (pre-8gen): camera/modem dead
3. Start with LineageOS device trees — cleanest base for Halium
4. Always pull vendor blobs BEFORE any flashing (stock ROM → blobs)
5. sm7150 (Snapdragon 732G) has LineageOS trees for surya — confirmed

### WSL2 + Android Development
- `usbipd` is REQUIRED for adb/fastboot to see USB devices from WSL2
- Install: `winget install usbipd` on Windows
- Per-session: `usbipd attach --wsl --busid <ID>` each time device is plugged
- Without this, WSL2 cannot see any USB device at all

### Build Space Requirements
- Halium 12 full sync: ~40-60 GB source
- Build output: ~20-30 GB
- Vendor blobs: ~5-10 GB
- Total: plan for 100 GB minimum

## Concepts
`halium`, `hybris`, `droidian`, `sm7150`, `surya`, `fastboot`, `wsl2`, `usbipd`, `android-porting`
