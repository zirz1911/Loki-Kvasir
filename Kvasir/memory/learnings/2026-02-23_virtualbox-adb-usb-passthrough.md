# VirtualBox ADB USB Passthrough

**Discovered**: 2026-02-23
**Context**: Kali Linux as VirtualBox VM on Windows, Poco X3 NFC (surya)

## The Pattern

VirtualBox USB passthrough creates a **new host identity** for ADB. The phone authorizes ADB per RSA key (`~/.android/adbkey`). Windows ADB key ≠ Linux VM ADB key — so a device previously authorized on Windows will show `offline` under Linux.

## Fix

1. Phone: Settings → Developer Options → **Revoke USB debugging authorizations**
2. Phone screen must be ON and UNLOCKED
3. USB must be attached to VirtualBox (not Windows)
4. Run `adb devices` → popup appears on phone → accept
5. Device shows `authorized`

## Ongoing Risk

VirtualBox may **drop USB** when phone reboots or changes mode (same issue as WSL2 usbipd). Add a persistent USB filter in VirtualBox settings to auto-reattach:
> VirtualBox → Machine Settings → USB → Add filter → select Xiaomi device

## USB Product IDs (Xiaomi/surya)

| ID | Mode |
|----|------|
| `2717:ff20` | MTP/Charging (no ADB) |
| `2717:ff48` | MTP + ADB |
| `18d1:d00d` | Fastboot |

## Diagnosis Flow

```
lsusb → device visible?
  NO  → hardware/cable issue
  YES → adb devices
          empty   → ADB not running / no USB rule
          offline → authorization blocked (revoke + re-auth)
          authorized → working ✓
```

## Note on "Native Linux"

VirtualBox Kali ≠ bare metal Linux. For serious Android development, bare metal dual boot eliminates this entire problem class. Always clarify target environment before predicting USB behavior.
