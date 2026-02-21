#!/usr/bin/env bash
# Openclaw Dashboard — Check status of all Openclaw instances
# Usage: bash .claude/openclaw-dashboard.sh

SESSIONS=("claude28" "claude29" "claude30")
BOTS=("@conclaw28bot" "@conclaw29bot" "@conclaw30bot")
IPS=("192.168.1.229" "192.168.1.34" "local")
VERSIONS=("2026.2.19-2" "2026.2.19-2" "2026.2.9")

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║         🦞 Openclaw Dashboard                        ║"
printf "║         %-44s║\n" "$(date '+%Y-%m-%d %H:%M:%S')"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "  Polling all instances..."

# Send health checks to all sessions simultaneously
for i in "${!SESSIONS[@]}"; do
    SESSION="${SESSIONS[$i]}"
    if ! tmux has-session -t "$SESSION" 2>/dev/null; then
        continue
    fi
    VERSION="${VERSIONS[$i]}"
    if [[ "$VERSION" == "2026.2.9" ]]; then
        CMD="openclaw health 2>&1"
    else
        CMD="openclaw health 2>&1"
    fi
    tmux send-keys -t "$SESSION" C-u 2>/dev/null
    sleep 0.3
    tmux send-keys -t "$SESSION" "$CMD" 2>/dev/null
    sleep 0.5
    tmux send-keys -t "$SESSION" C-m 2>/dev/null
done

sleep 35

echo ""
for i in "${!SESSIONS[@]}"; do
    SESSION="${SESSIONS[$i]}"
    BOT="${BOTS[$i]}"
    IP="${IPS[$i]}"
    VER="${VERSIONS[$i]}"

    printf "┌─────────────────────────────────────────────────────\n"
    printf "│ %-12s  %-18s  %s\n" "$SESSION" "$BOT" "$IP"
    printf "│ version: %-43s\n" "$VER"
    printf "├─────────────────────────────────────────────────────\n"

    if ! tmux has-session -t "$SESSION" 2>/dev/null; then
        printf "│ ❌ tmux session not found\n"
        printf "└─────────────────────────────────────────────────────\n\n"
        continue
    fi

    OUTPUT=$(tmux capture-pane -t "$SESSION" -p 2>/dev/null | tail -30)

    if echo "$OUTPUT" | grep -q "Telegram: ok"; then
        TG_STATUS="✅ ok"
    elif echo "$OUTPUT" | grep -q "Telegram:"; then
        TG_STATUS="⚠️  issue"
    else
        TG_STATUS="❓ unknown"
    fi

    if echo "$OUTPUT" | grep -q "Gateway.*ok\|gateway.*online"; then
        GW_STATUS="✅ ok"
    elif echo "$OUTPUT" | grep -q "error\|Error\|fail\|1008\|reject"; then
        GW_STATUS="❌ error"
    else
        GW_STATUS="❓ unknown"
    fi

    if echo "$OUTPUT" | grep -q "Heartbeat interval\|agent:main"; then
        AGENT_STATUS="✅ active"
    elif echo "$OUTPUT" | grep -q "Running\|Musing"; then
        AGENT_STATUS="🔄 running"
    else
        AGENT_STATUS="💤 idle"
    fi

    printf "│ Telegram : %s\n" "$TG_STATUS"
    printf "│ Gateway  : %s\n" "$GW_STATUS"
    printf "│ Agent    : %s\n" "$AGENT_STATUS"
    printf "└─────────────────────────────────────────────────────\n\n"
done

echo "  Gateway: ws://127.0.0.1:18789 (shared)"
echo "  Lokkji chatId: 8190607091"
echo ""
