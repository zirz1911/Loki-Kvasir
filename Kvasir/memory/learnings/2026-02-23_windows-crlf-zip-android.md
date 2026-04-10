# Learning: Windows CRLF in Zip Files for Android

**Date**: 2026-02-23
**Source**: rrr: nethunter-zip-fix-success
**Tags**: python, windows, android, crlf, zip, shell

---

## Pattern

Python `open()` in text mode on Windows silently converts `\n` → `\r\n` on write. When shell scripts are patched this way and re-packed into a zip for Android/Linux, every line ending becomes `\r\n`. POSIX shell treats `\r` as a command, causing:

```
}: not found
return: not found
{: not found
```

on nearly every line — the entire script fails before reaching any logic.

## Detection

```bash
cat -A script.sh | head -5
# Lines ending with ^M$ = CRLF

python3 -c "
import zipfile
data = zipfile.ZipFile('file.zip','r').read('path/in/zip')
print('CR count:', data.count(b'\r'))
"
```

## Fix

Always use binary mode when handling shell scripts for Linux/Android:

```python
# WRONG — introduces CRLF on Windows
with open('script.sh', 'r') as f:
    content = f.read()
with open('script.sh', 'w') as f:
    f.write(content)

# CORRECT — preserve LF
with open('script.sh', 'rb') as f:
    content = f.read()
content = content.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
with open('script.sh', 'wb') as f:
    f.write(content)
```

When rebuilding a zip, strip CRLF before `writestr()`:

```python
with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename.endswith(('.sh', 'update-binary', 'update-magisk')):
            data = data.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
        zout.writestr(item, data)
```

## Related

- NetHunter `push_modules()` also needed patching for r0ttenbeef kernel layout (`kernel/` vs `lib/` directory structure)
- Always verify after patching: `data.count(b'\r')` should be 0
