# Next.js Interactive Patterns — HTML-to-Next.js Conversion

**Date**: 2026-02-24
**Source**: Nong Nooch Garden project — 8 HTML → Next.js 16 App Router

---

## Fragment Key Prop

`<>` shorthand fragment cannot receive props. When using `.map()` that returns multiple sibling elements:

```tsx
// ❌ key is invisible to React
{items.map(item => (
  <>
    <div key={item.id}>...</div>  // React never sees this key
    <div>...</div>
  </>
))}

// ✅ key on the outer element
import { Fragment } from 'react'
{items.map(item => (
  <Fragment key={item.id}>
    <div>...</div>
    <div>...</div>
  </Fragment>
))}
```

## Lightbox Modal Pattern

```tsx
const [lightbox, setLightbox] = useState<Item | null>(null)

// ESC to close
useEffect(() => {
  const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setLightbox(null) }
  window.addEventListener('keydown', onKey)
  return () => window.removeEventListener('keydown', onKey)  // cleanup!
}, [])

// Click outside to close
<div onClick={() => setLightbox(null)}>
  <div onClick={e => e.stopPropagation()}>
    {/* modal content */}
  </div>
</div>
```

## Set for Toggle State (reminders, favorites)

```tsx
const [reminders, setReminders] = useState<Set<string>>(new Set())

const toggle = (id: string) => setReminders(prev => {
  const next = new Set(prev)
  if (next.has(id)) next.delete(id)
  else next.add(id)
  return next
})
```

## Zone-Switch with Fade Transition

```tsx
const [activeZone, setActiveZone] = useState(0)
const [transitioning, setTransitioning] = useState(false)

const goToZone = (idx: number) => {
  setTransitioning(true)
  setTimeout(() => { setActiveZone(idx); setTransitioning(false) }, 300)
}

// Apply to image: opacity-0 during transition
<img className={`transition-opacity duration-300 ${transitioning ? 'opacity-0' : 'opacity-100'}`} />
```

## Typed Form Validation Pattern

```tsx
type FormField = 'firstname' | 'email' | 'cardnumber'  // etc

const [form, setForm] = useState<Record<FormField, string>>({ ... })
const [errors, setErrors] = useState<Partial<Record<FormField, string>>>({})

const set = (field: FormField) => (e: ChangeEvent<HTMLInputElement>) => {
  setForm(f => ({ ...f, [field]: e.target.value }))
  setErrors(err => { const next = { ...err }; delete next[field]; return next })
}

const validate = (): Partial<Record<FormField, string>> => {
  const e: Partial<Record<FormField, string>> = {}
  if (!form.firstname.trim()) e.firstname = 'Required'
  // ...
  return e
}
```

## Background Image with Special Characters in URL

```tsx
// ❌ Tailwind JIT can choke on & in arbitrary class
<div className="bg-[url('...?q=80&w=2670...')]" />

// ✅ Inline style is safe
<div style={{ backgroundImage: "url('https://...?q=80&w=2670...')" }} />
```

## Static Build + Client Interactivity

Next.js 16 prerenderers `'use client'` pages as static HTML shells. All `useState` / `useEffect` runs client-side after hydration. Pages with only client-side state (no server data fetching) will show `○ (Static)` in build output — this is correct and desirable.

## Zoom Array Pattern

```tsx
const ZOOM_STEPS = [50, 75, 100, 125, 150, 200]
const [zoomIdx, setZoomIdx] = useState(2) // starts at 100%

const zoomIn = () => setZoomIdx(i => Math.min(i + 1, ZOOM_STEPS.length - 1))
const zoomOut = () => setZoomIdx(i => Math.max(i - 1, 0))
const zoom = ZOOM_STEPS[zoomIdx] // current % value
```
