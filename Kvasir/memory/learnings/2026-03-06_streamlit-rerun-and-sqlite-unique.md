# Streamlit + SQLite Patterns

**Date**: 2026-03-06
**Source**: auto-web-gen

---

## Pattern 1: Streamlit Single-Pass Render

Streamlit renders TOP → BOTTOM in a single pass per interaction.

**Rule**: If you save data to `st.session_state` inside a button handler and want it reflected in a widget BELOW the button in the SAME script, you MUST call `st.rerun()`.

```python
if st.button("Regenerate"):
    new_html = generate(...)
    st.session_state.result[id] = new_html  # save
    st.rerun()  # REQUIRED — starts fresh pass where session_state is used

# Below the button — only renders correctly AFTER rerun
st.components.v1.html(st.session_state.result.get(id, ""))
```

Without `st.rerun()`: the widget below was already rendered before the button was clicked. Session_state update has no effect on the current pass.

---

## Pattern 2: SQLite ON CONFLICT Requires UNIQUE Index

`ON CONFLICT(col)` in an INSERT statement does nothing without a UNIQUE constraint on `col`.

**Wrong**: just defining `col TEXT NOT NULL` — no uniqueness enforced
**Right**: add `CREATE UNIQUE INDEX IF NOT EXISTS idx_name ON table(col)`

Best practice in `init_db()`:
```python
conn.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS idx_gen_business_id
    ON generated_sites(business_id)
""")
```

This auto-migrates existing DBs safely. Silent insert failures are the symptom — no error raised, try/except catches nothing visible.

---

## Pattern 3: Streamlit Error Visibility

In Streamlit pipeline code, `print()` is invisible to users. Use `st.error()` for any exception that should be visible.

```python
# Wrong
except Exception as e:
    print(f"Error: {e}")  # nobody sees this

# Right
except Exception as e:
    st.error(f"Error: {e}")  # visible in UI
```
