---
name: Mobile Responsive — iOS Viewport & Layout Patterns
description: Patterns for preventing iOS auto-zoom and building responsive overlays in React/HTML
type: project
---

# Mobile Responsive — iOS Viewport & Layout Patterns

Discovered during Loki-Pixfice mobile responsive work (2026-03-12).

## iOS Zoom Prevention

**Full incantation** (both required):
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
```

- `maximum-scale=1.0` alone is NOT enough — iOS still zooms on input focus
- `user-scalable=no` is required to fully prevent auto-zoom
- Input elements with `font-size < 16px` trigger iOS auto-zoom even with viewport restrictions → set to 16px on mobile

## Mobile Overlay Positioning

**Wrong**: `position: fixed; inset: 0` — covers entire viewport including navbar
**Right**: Render as sibling to navbar inside a `position: relative` container, let it `flex: 1`

```jsx
// Bad: covers navbar
<div style={{ position: "fixed", inset: 0, zIndex: 99 }}>

// Good: flows below navbar naturally
<div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
  <Navbar />
  {chatOpen ? <ChatPanel /> : <MainContent />}
</div>
```

## Hamburger Dropdown Pattern

```jsx
const [menuOpen, setMenuOpen] = useState(false);
const menuRef = useRef();

// Close on outside click
useEffect(() => {
  if (!menuOpen) return;
  const handler = (e) => {
    if (!menuRef.current?.contains(e.target)) setMenuOpen(false);
  };
  document.addEventListener("mousedown", handler);
  return () => document.removeEventListener("mousedown", handler);
}, [menuOpen]);
```

## Sidebar Slide-in (vanilla JS)

```css
.sidebar { position: fixed; left: -220px; transition: left 0.2s ease; }
.sidebar.open { left: 0; }
```

Auto-close after selection to avoid user having to manually close.
