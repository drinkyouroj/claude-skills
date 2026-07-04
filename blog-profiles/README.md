# blog-profiles has moved

This profile store now lives in the `hearn-systems-customer-tools` repo:

    /Volumes/fast/Github/hearn-systems-customer-tools/skills/blog-profiles/

(decided 2026-07-04, Voice Newsroom Story 1.1). The runtime symlink
`~/.claude/blog-profiles` points at the new location, so leaf `blog-*` skills
resolve profiles there with no change. Do not add profile content here; it
would silently diverge from the live store.
