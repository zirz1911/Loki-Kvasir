# Lesson: UI Label Changes vs Behavior Changes

**Date**: 2026-02-22
**Source**: World-Conflict session

## Pattern

When a user asks to rename a UI element (e.g. "Dark Matter" → "Map Default"), clarify whether the intent is:
1. **Label only** — just the display text
2. **Label + behavior** — text AND the underlying functionality (tile URL, color, data)

In this session, a rename request became a full tile swap → then reverted. Three rounds of edits for net-zero change.

**Fix**: Ask one question before touching code — "just the name, or also the tile/color?"

---

## Pattern: Mock Data Has a Shelf Life

World-Conflict data was frozen at late 2024. Major events happened Dec 2024–Jan 2025:
- Assad fell (Syria)
- Goma fell (DRC)
- Gaza ceasefire Phase 1
- Sudan famine declared

**Rule**: For news/events dashboards, mock data should be versioned with a `dataAsOf` timestamp and refreshed at meaningful intervals. Build the refresh into the project workflow, not as a one-off task.

---

## World-Conflict Project Notes

- Path: `D:\Paji AI\World-Conflict`
- Stack: Next.js 16 + React 19 + Leaflet + Tailwind v4
- All data in `src/data/mockData.ts` — ready to wire to ACLED / UNHCR / OCHA APIs
- Default map style: `"dark"` (CartoDB Dark Matter tiles)
- Sibling to WorldMap (`D:\Paji AI\WorldMap`) — same stack patterns apply
