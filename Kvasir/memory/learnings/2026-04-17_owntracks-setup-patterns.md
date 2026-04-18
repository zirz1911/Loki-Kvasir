---
name: owntracks-setup-patterns
description: OwnTracks + Mosquitto setup — TLS trap, config write pattern, NAT check
type: feedback
---

3 patterns จาก OwnTracks full-stack setup session:

**1. OwnTracks TLS trap**
iOS OwnTracks default เปิด TLS อยู่ — ต้องปิดก่อน connect port 1883 (plain MQTT) ถ้า app ขึ้น "Publish queued" = ยังไม่ได้ connect = เช็ค TLS settings ก่อน

**Why:** เสียเวลา debug ฝั่ง server นานก่อนเจอว่าปัญหาอยู่ที่ iPhone

**How to apply:** ทุกครั้งที่ setup OwnTracks ใหม่ ตรวจ TLS = OFF ก่อนเป็นอย่างแรก

---

**2. Mosquitto config write pattern**
เขียน config ด้วย `python3 -c "with open(path,'w') as f: f.write(content)"` แล้ว `sudo cp` — ห้ามใช้ heredoc หรือ tee เพราะ leading spaces และ shell escaping ทำให้ parse error เสมอ

**Why:** Debug Mosquitto config 20+ นาทีเพราะ tee ใส่ leading spaces และ garbage characters

**How to apply:** เมื่อต้องเขียน config file ที่ต้องการ sudo — write tmp file ด้วย Python ก่อน แล้วค่อย sudo cp

---

**3. NAT check ก่อน expose port**
ก่อน configure service ให้รับ public connections ให้ตรวจก่อนว่า `ip addr` IP ตรงกับ `curl ifconfig.me` มั้ย ถ้าต่างกัน = อยู่หลัง NAT = ต้อง port forward ก่อน

**Why:** Configure Mosquitto 0.0.0.0 แล้ว iPhone connect ไม่ได้เพราะ server อยู่หลัง NAT

**How to apply:** ถามก่อนเสมอว่า "เครื่องนี้ public IP ตรงกับ IP ใน server มั้ย?"
