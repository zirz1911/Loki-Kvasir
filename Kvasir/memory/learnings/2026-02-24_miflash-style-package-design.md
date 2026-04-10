# Learning: Miflash-Style Flash Package Design for Custom ROM

**Date**: 2026-02-24
**Source**: rrr: nethunter-miflash-package
**Tags**: android, fastboot, twrp, miflash, package-design, surya, poco-x3-nfc

---

## Pattern

Miflash-style packages (MIUI stock ROM) have a consistent structure:
- `images\` — all partition images
- `flash_all.bat` — flashes everything via fastboot
- `flash_all_except_data_storage.bat` — same but skips userdata

This pattern is reusable for custom ROM packages. Key design principle: **separate build from deploy**.

## Package Structure for Custom ROM (LOS + TWRP + Magisk + NetHunter)

```
surya_nethunter_los20\
├── prepare.bat          # Step 1: build images\
├── prepare.py           # extracts boot/dtbo/vbmeta from LOS zip, copies TWRP
├── flash_all.bat        # Step 2: fastboot flash + TWRP install pipeline
├── flash_all_except_data.bat
├── source\              # user drops source files here
└── images\              # auto-built by prepare.bat
    ├── boot.img         # from LOS zip
    ├── recovery.img     # = TWRP
    ├── dtbo.img         # from LOS zip
    ├── vbmeta.img       # from LOS zip
    └── vbmeta_system.img
```

## Critical Distinction: MIUI vs LOS flash scope

**MIUI `flash_all.bat`** flashes ALL partitions including firmware:
- xbl, aop, tz, hyp, modem, bluetooth, storsec, devcfg, abl...
- Safe because MIUI firmware matches MIUI system

**LOS `flash_all.bat`** should only flash high-level partitions:
- boot, recovery, dtbo, vbmeta, vbmeta_system
- system/vendor handled by TWRP install of the LOS zip
- **DO NOT** reflash firmware unless deliberately updating firmware version

## LOS 20 Zip Structure (OTA format, not fastboot)

```
lineage-20.0-surya-signed.zip
├── boot.img              ← direct fastboot image
├── dtbo.img              ← direct fastboot image
├── recovery.img          ← direct fastboot image (replace with TWRP)
├── vbmeta.img            ← direct fastboot image
├── vbmeta_system.img     ← direct fastboot image
├── system.new.dat.br     ← brotli-compressed sparse system
├── system.transfer.list  ← sdat2img input
├── vendor.new.dat.br     ← same for vendor
├── vendor.transfer.list
├── product.new.dat.br    ← same for product
└── ...
```

To flash system/vendor via fastboot: convert `.dat.br` → `.img` using:
```
brotli -d system.new.dat.br → system.new.dat
sdat2img.py system.transfer.list system.new.dat system.img
fastboot reboot fastboot  # enter fastbootd for logical partitions
fastboot flash system system.img
```

Simpler: let TWRP handle it via `adb shell twrp install /sdcard/rom.zip`

## Device Identity: surya

- `surya` = **POCO X3 NFC** (Snapdragon 732G)
- NOT Redmi Note 9 Pro (which uses `joyeuse`/`miatoll`)
- Verify: `fastboot getvar product` → should return `surya` or `karna`
