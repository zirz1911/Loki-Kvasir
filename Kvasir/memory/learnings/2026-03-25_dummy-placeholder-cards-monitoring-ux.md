---
name: Dummy placeholder cards improve monitoring UI before first data arrives
description: Greyed-out example cards show users what the view will look like and set expectations about data shape
type: feedback
---

Use dummy/placeholder cards in monitoring board views — show greyed-out example entries before real data arrives.

**Why:** Email board added two dummy email cards (noreply@google.com, security@facebook.com) with masked OTP codes. This tells users what information will appear and in what format, without requiring them to wait for the first real event. Empty state is less informative than a structured placeholder.

**How to apply:** For any new board/log view that waits for async data, add 1-2 dummy cards with realistic structure but masked/greyed values. Remove them on first real entry (emailCount === 0 check pattern). Apply to future monitoring views in message-board or similar tools.
