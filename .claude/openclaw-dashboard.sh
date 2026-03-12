#!/usr/bin/env bash
# Openclaw Dashboard — ใช้ CLI โดยตรง + HTTP ping สำหรับ remote
# Usage: bash .claude/openclaw-dashboard.sh

# ── Fleet Config ─────────────────────────────────────────────
# format: "label|type|endpoint|bot"
# type: local = ใช้ openclaw CLI โดยตรง
#       http  = ping ผ่าน HTTP (Tailscale IP:port)
INSTANCES=(
  "local (paji)|local|ws://127.0.0.1:18789|@openpaji_bot"
)

# เพิ่ม remote instances ที่นี่ เช่น:
# "Note8|http|http://100.x.x.x:18789|@conclaw30bot"

# ─────────────────────────────────────────────────────────────

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║         🦞 Openclaw Dashboard                        ║"
printf "║         %-44s║\n" "$(date '+%Y-%m-%d %H:%M:%S')"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

for entry in "${INSTANCES[@]}"; do
  IFS="|" read -r label type endpoint bot <<< "$entry"

  printf "┌─────────────────────────────────────────────────────\n"
  printf "│ %-20s  %-18s\n" "$label" "$bot"
  printf "│ endpoint: %-41s\n" "$endpoint"
  printf "├─────────────────────────────────────────────────────\n"

  if [[ "$type" == "local" ]]; then
    # ── Local: ใช้ openclaw CLI โดยตรง ──────────────────────
    if ! command -v openclaw &>/dev/null; then
      printf "│ ❌ openclaw CLI ไม่พบในเครื่อง\n"
    else
      OUTPUT=$(timeout 15 openclaw health 2>&1)
      if echo "$OUTPUT" | grep -q "Telegram: ok"; then
        TG=$(echo "$OUTPUT" | grep "^Telegram:" | head -1)
        printf "│ ✅ %s\n" "$TG"
      elif echo "$OUTPUT" | grep -q "Telegram:"; then
        TG=$(echo "$OUTPUT" | grep "^Telegram:" | head -1)
        printf "│ ⚠️  %s\n" "$TG"
      else
        printf "│ ❌ ไม่ได้รับข้อมูล Telegram\n"
      fi

      if echo "$OUTPUT" | grep -q "WhatsApp:"; then
        WA=$(echo "$OUTPUT" | grep "^WhatsApp:" | head -1)
        printf "│ ✅ %s\n" "$WA"
      fi

      if echo "$OUTPUT" | grep -q "Agents:"; then
        AG=$(echo "$OUTPUT" | grep "^Agents:" | head -1)
        printf "│ 🤖 %s\n" "$AG"
      fi

      if echo "$OUTPUT" | grep -q "Heartbeat interval:"; then
        HB=$(echo "$OUTPUT" | grep "^Heartbeat" | head -1)
        printf "│ 💓 %s\n" "$HB"
      fi
    fi

  elif [[ "$type" == "http" ]]; then
    # ── Remote: HTTP ping ────────────────────────────────────
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$endpoint" 2>/dev/null)
    if [[ "$HTTP_CODE" == "200" ]]; then
      printf "│ ✅ Gateway UP — %s\n" "$endpoint"
    elif [[ -z "$HTTP_CODE" || "$HTTP_CODE" == "000" ]]; then
      printf "│ ❌ Gateway ไม่ตอบสนอง (timeout)\n"
    else
      printf "│ ⚠️  Gateway ตอบ HTTP %s\n" "$HTTP_CODE"
    fi
  fi

  printf "└─────────────────────────────────────────────────────\n\n"
done
