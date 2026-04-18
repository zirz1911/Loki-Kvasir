---
name: owntracks-http-device-topic
description: OwnTracks HTTP mode ส่ง device ID ใน topic JSON field ไม่ใช่ query param
type: feedback
---

OwnTracks HTTP mode ไม่ส่ง `?d=deviceid` เป็น query parameter — แต่ส่งใน `topic` field ของ JSON body แทน: `owntracks/{username}/{deviceid}`

**Why:** Debug ผ่าน log พบว่า `d=''` ตลอด แต่ `data["topic"]` = `"owntracks/winter/android"` — consistent กับ MQTT topic format แต่ซ่อนใน payload

**How to apply:** เมื่อ implement OwnTracks HTTP receiver ให้ extract device จาก `topic.split("/")[2]` เสมอ อย่า rely on query params หรือ `tid` (tid = 2-char Tracker ID, ไม่ใช่ Device ID)
