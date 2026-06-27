## `general` preset

The neutral default suitable for most non-fiction blogs. All nine pipeline steps are enabled. Framing vocabulary is de-branded and platform-agnostic.

---

### Step defaults

| Step | Default |
|---|---|
| `outline` | on |
| `outline-more` | on |
| `headline` | on |
| `opener` | on |
| `draft` | on |
| `readability` | on |
| `humanizer` | on |
| `fact-check` | on |
| `fact-reconcile` | on |

Individual profiles may override any step via `profile.yaml`.

---

### Framing vocabulary

| Concept | Term used in this preset |
|---|---|
| How to position + structure an article | **angle/hook + structure selection** |
| Understanding the target reader before drafting | **reader-persona pre-assessment** |
| Checking prose clarity, load, and sentence flow | **density/comprehension audit** |

These terms appear in orchestrator prompts and leaf-skill headers. Substitute them wherever a pipeline step refers to its own framing phase.
