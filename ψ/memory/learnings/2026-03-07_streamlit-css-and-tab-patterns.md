# Streamlit CSS Override + Tab Patterns

**Date**: 2026-03-07
**Source**: auto-web-gen session — Business List debugging
**Project**: D:/Project/auto-web-gen

## Pattern: Global CSS kills dataframe text

Exo-Paji theme uses:
```css
html, body, [class*="css"] { color: var(--exo-text) !important; }
```

This overrides Streamlit dataframe cell text, making it invisible (same color as background).

**Fix**: Replace `st.dataframe()` with `st.markdown()` using an HTML table with explicit inline styles:
```python
st.markdown(html_table, unsafe_allow_html=True)
```

## Pattern: df.style.apply() broken on pandas 2.3 + Streamlit 1.55

The Pandas Styler API (`df.style.apply()`) silently fails on newer stack. Avoid it.
Use plain `st.dataframe(df)` or the HTML table approach above.

## Pattern: Widget key conflicts = silent tab failure

If multiple widgets (selectbox, text_input) share the same key name across tabs, Streamlit silently fails to render the entire tab — no error, just blank.

**Fix**: Always use explicit `key=` on every interactive widget, scoped by tab:
```python
st.selectbox("Query", options, key="crawl_query")   # not "query"
st.selectbox("Location", options, key="crawl_location")
```

## Pattern: Streamlit hot reload

After editing `.py` files, Streamlit auto-reloads. Never offer to restart the app — just confirm the edit is complete.

## Pattern: Claude Haiku + max_tokens → blank HTML

Haiku sometimes writes 500+ lines of CSS and hits `max_tokens=8192` before writing `<body>`.

**Prevention**:
1. System prompt: "KEEP CSS UNDER 100 LINES"
2. Check `message.stop_reason == "max_tokens"` → raise clear error
3. Validate HTML: check `<body>` and `</html>` presence

## Pattern: Social URLs in website column

Google Maps crawler may store Facebook/Instagram URLs in the `website` field. At display time, classify using `SOCIAL_DOMAINS` set — do not modify the data, just change the view label.
