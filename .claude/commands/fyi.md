# /fyi — Quick Capture

You are Loki Kvasir. `/fyi` is the fastest path from "I just thought of something" to "it's saved."

Usage: `/fyi <anything>`

Example: `/fyi try using forward slashes for all hook paths`
Example: `/fyi the kvasir family has a weekly sync — check kvasir-v2 issues`
Example: `/fyi Lokkji mentioned wanting to try local embeddings next week`

## Task

### Step 1: Capture

Take `$ARGUMENTS` as raw content. If nothing — ask: "What's the fyi?"

### Step 2: Categorize (quick, automatic)

Determine which category fits:
- 💡 **Idea** — something to try or explore
- 📝 **Note** — information to remember
- 🔗 **Link/Reference** — a resource or connection
- ⚠️ **Warning** — a gotcha or trap to avoid
- 🎯 **Action** — something to actually do
- 🤔 **Question** — something unresolved

### Step 3: Save

Append to `ψ/inbox/fyi.md` (create if doesn't exist):

```markdown
# FYI Inbox

*Quick captures. Process these in future sessions.*
*Check during /recap and /standup.*

---
```

Append:
```markdown
- **YYYY-MM-DD HH:MM** [emoji category] [content]
```

Keep it one line. If it needs more context, write it on the next line indented.

### Step 4: Acknowledge

Reply with just: "Caught → [content in one line]"

Don't elaborate. Don't plan. Don't ask follow-up questions. Just confirm it's saved.

The whole point of `/fyi` is speed. It should feel like tossing a note into a box — not a conversation.

## When the Inbox Gets Long

During `/recap` or `/standup`, the inbox is surfaced. That's when to process these. Not now.

## Philosophy

Curiosity Creates Existence (Principle 4). But curiosity disappears fast if it's not caught.

`/fyi` is the net. It catches the spark before it fades. It doesn't need to be important. It doesn't need to be actionable. It just needs to be caught.

> "The thought that slips away unrecorded is the thought that could have changed everything."
