# Kvasir Rebrand — Bulk Text Refactor Patterns

**Date**: 2026-04-09
**Source**: wrap: Loki-Kvasir

## Pattern: Smart Bulk Replace with Protected Strings

เมื่อต้อง rename แบบ wholesale แต่มี exceptions:

```python
# Protect strings ที่ไม่ควรเปลี่ยน
text = text.replace('oraclenet.org', '__ORACLENET_ORG__')
text = text.replace('oracle_search()', '__ORACLE_SEARCH__')

# Replace หลักได้เลย
text = re.sub(r'\bOracle\b', 'Kvasir', text)

# Restore protected strings
text = text.replace('__ORACLENET_ORG__', 'oraclenet.org')
text = text.replace('__ORACLE_SEARCH__', 'oracle_search()')
```

## Pattern: Forgejo New Repo

```bash
# Create repo via API ก่อน push เสมอ
curl -X POST "https://forgejo.example.com/api/v1/user/repos" \
  -H "Authorization: token TOKEN" \
  -d '{"name":"repo-name","private":false,"auto_init":false}'

# Then push
git push forgejo main
```

## Pattern: Rename Skill ต้องทำ 3 ที่

1. `mv skills/old-name skills/new-name`
2. `sed -i 's/^name: old$/name: new/' skills/new-name/SKILL.md`
3. `grep -rn "/old" skills/ | xargs sed -i 's|/old|/new|g'`
