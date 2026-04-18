---
name: Cloudflare-blocked sites → WebSearch fallback
description: When a documentation site returns 403 on all paths, pivot to WebSearch site: operator instead of retrying WebFetch
type: feedback
---

If a site returns 403 on homepage AND subpaths (especially GitBook, Cloudflare-protected), do NOT keep retrying WebFetch paths. Detect early:
1. robots.txt loads but homepage 403 → whole site is blocked
2. After 2-3 WebFetch 403s → stop, pivot to `WebSearch site:domain.com`

WebSearch often returns indexed snippets with enough content to build documentation, even when the live site blocks scrapers.

**Why:** Spent ~8 WebFetch attempts on manual.gemlogin.io before accepting the block. Each failed call wastes tokens and time. The pattern is detectable after 2 attempts.

**How to apply:** In /learn for web URLs — if first WebFetch fails with 403, immediately try WebSearch before retrying more paths.
