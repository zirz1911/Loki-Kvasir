# Electron Plugin Development Patterns (Tabby)

**Discovered**: 2026-03-01
**Context**: Tabby-sessions plugin — runtime debugging session

---

## 1. `process.execPath` ≠ Node.js in Electron

In Electron apps, `process.execPath` is the **Electron binary** (e.g., `Tabby.exe`), NOT Node.js.
Spawning subprocesses with `process.execPath` opens a new app window, not a Node script.

**Fix**: Use `'node'` as the command and rely on PATH. Or find Node.js via known installation paths.

---

## 2. Dev typings must match the installed runtime

For Electron plugins, always point tabby deps to the **installed version**:

```json
"tabby-core": "file:C:/Users/.../Programs/Tabby/resources/builtin-plugins/tabby-core"
```

npm registry versions drift silently. Wrong typings → runtime crashes with cryptic errors.

---

## 3. Silent APP_INITIALIZER = constructor DI failure

When an Angular plugin produces **zero logs and zero errors**, the most likely cause:
- A constructor dependency can't be resolved
- This prevents APP_INITIALIZER from ever running

Diagnose: Settings tab appears (module loaded OK) vs lifecycle logs appear (initializer ran).
Remove injections one by one to find the failing token.

---

## 4. `BaseTabComponent` requires `Injector` in Tabby 1.0.197+

```typescript
constructor(public injector: Injector, ...deps) {
  super(injector)  // required — constructor calls injector.get(ConfigService)
}
```

Older typings show `protected constructor()` — ignore them. Always pass injector.

---

## 5. `openNewTab()` wraps in `SplitTabComponent`

Any code receiving a `tab: BaseTabComponent` that was opened via `app.openNewTab()` is
actually a `SplitTabComponent`. To get the inner terminal tab:

```typescript
const innerTab = tab instanceof SplitTabComponent ? tab.getAllTabs()[0] ?? tab : tab
const frontend = (innerTab as any).frontend  // now accessible
```

---

## 6. Tab creation vs tab-list insertion

| Method | Creates | Adds to tab bar |
|--------|---------|-----------------|
| `tabsService.create(params)` | ✅ | ❌ |
| `app.openNewTabRaw(params)` | ✅ | ✅ |
| `app.openNewTab(params)` | ✅ | ✅ + wraps in SplitTab |

Use `tabsService.create()` when you need to instantiate a tab to **manually insert into a split**:
```typescript
const newTab = this.tabs.create({ type: MyTabComponent, inputs: {...} })
splitTab.addTab(newTab, relativeTab, 'r')  // 'r'=right, 'b'=bottom
```
