## Profile resolution (run before anything else)

This skill is profile-driven. Resolve the active blog profile before doing the skill's work:

1. **Local override:** if the current working directory (the blog project) contains a `blog-profile/` folder, use it as the active profile.
2. **Named profile:** else, if a profile name or path was provided (by the orchestrator or the user), resolve it under `~/.claude/blog-profiles/<name>/`.
3. **Ask:** else, list the profiles in `~/.claude/blog-profiles/` (excluding `_template` and `_presets`) and ask the user to pick one.

Once resolved, read `profile.yaml` for structured knobs, then load only the prose files this step needs:
- `identity.md` — brand, subject domain, platform, audience one-liner
- `voice.md` — author voice + banned vocab + AI-tell calibration
- `reader.md` — reader persona
- `templates.md` — content-structure / framework / angle library

Apply the active preset (`profile.yaml.preset`, resolved under `~/.claude/blog-profiles/_presets/<preset>.md`) for step defaults and framing vocabulary, with any `profile.yaml.steps` overrides.

If a required file for this step is missing, halt and report which file failed to resolve — do not fall back to a hard-coded identity.
