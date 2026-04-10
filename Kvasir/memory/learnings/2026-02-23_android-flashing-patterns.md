# Android Flashing Patterns — surya / LineageOS / NetHunter

**Date**: 2026-02-23
**Source**: nethunter-flash-pipeline session

---

## Partition Consistency Rule

boot, kernel, system, vendor **ต้องมาจาก ROM version เดียวกัน** เสมอ

- LOS 22.2 boot + LOS 20 system = WiFi/hardware ไม่ทำงาน
- kernel driver ต้องตรงกับ HAL version ใน vendor

**Rule**: เลือก ROM version ก่อน แล้ว extract ทุก partition จาก zip เดียว

---

## Magisk + TWRP Flash Order

```
1. Flash ROM zip via TWRP   ← overwrites boot.img
2. Flash Magisk.zip via TWRP ← patches new boot.img
3. Reboot system
```

ห้าม flash ROM แล้วข้าม Magisk — ต้อง flash ทุกครั้งหลัง ROM

---

## NetHunter Version Matrix (surya)

| LineageOS | Android | NetHunter tag |
|-----------|---------|---------------|
| LOS 20 | Android 13 | `los-thirteen` |
| LOS 21 | Android 14 | `los-fourteen` |
| LOS 22 | Android 15 | `los-fifteen` |

**NetHunter 2025.x ต้อง install ผ่าน Magisk** — ไม่ใช่ TWRP recovery

---

## adb sideload Diagnosis

`Total xfer: 0.10x` = updater-script reject เร็ว = version/device assertion ล้มเหลว

ดู log: `adb shell cat /tmp/recovery.log | grep -E "error|assert|failed|NetHunter"`

---

## Android Transfer List Format

```
cmd count,start,end,start,end,...
```

- ตัวเลขแรกหลัง cmd = count (จำนวน endpoints) — ต้อง skip
- endpoints ที่เหลือ = pairs (start, end)

```python
def parse_ranges(s):
    nums = list(map(int, s.split(",")))
    return [(nums[i], nums[i+1]) for i in range(1, len(nums)-1, 2)]
```

---

## VirtualBox USB — ADB vs Fastboot

Device เปลี่ยน VID:PID เมื่อเปลี่ยน mode:
- ADB mode: `2717:ff48` (Xiaomi)
- Fastboot mode: `05c6:9025` (Qualcomm)

ต้องเพิ่ม USB filter ทั้ง 2 ใน VirtualBox Settings → USB
หรือใช้ Bridged/Host-only network + ทำ fastboot บน Windows Host แทน
