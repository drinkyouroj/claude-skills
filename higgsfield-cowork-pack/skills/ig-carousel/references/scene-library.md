# Cinematic Scene Library

The cover scene defines everything. Pick the one that communicates your topic before any text is read.

## Default scenes

### Gothic library (best for: learning, courses, knowledge work)
```
A gothic library at night. Floor-to-ceiling oak bookshelves, arched windows
with moonlight spilling through, leather armchairs, persian rug. A retro CRT
computer monitor on a carved wooden desk in the foreground, screen glowing
with Claude's interface. Banker's lamp beside it, stacks of old books, quill
pen.
```

Use for: anything about learning, courses, fundamentals, deep work, expertise.

### Late-night architect's loft (best for: productivity, tools, workflows)
```
A late-night architect's loft studio. Exposed warm-red brick walls, oak
drafting table, retro CRT computer showing the Claude logo. Banker's lamp,
brass compasses, leather journal, steaming coffee mug, blueprints on a
corkboard wall. Edison bulbs overhead.
```

Use for: tools, productivity, workflows, building, automation, building tools.

### Deserted island (best for: essentials, must-haves, favorites)
```
A deserted tropical island at golden hour. Palm trees, clear shallow water,
a crashed propeller plane half-buried in the sand. A retro CRT computer
sits on a driftwood crate in the foreground, glowing with Claude's
interface. Coconuts, a worn leather satchel, sun bleached map.
```

Use for: lists of "things I'd take to a deserted island," favorites, essentials, top picks.

### Futuristic command center (best for: news, announcements, releases)
```
A futuristic command center at night. Wall of glowing screens, holographic
displays, dark glossy floors. A retro CRT computer in the foreground sits
on a sleek metal desk, Claude logo glowing on screen. Soft blue and amber
lighting from the surrounding monitors.
```

Use for: news, announcements, product releases, "this just dropped" content.

### Moonlit bedroom (best for: sleep, automation, hands-off work)
```
A moonlit bedroom at midnight. Soft duvet, pillows, a sleeping cat curled
on the bed. A retro CRT computer on a nightstand glows softly with Claude's
interface, lighting the room with warm amber. Curtains slightly open
revealing city lights.
```

Use for: scheduled tasks, hands-off automation, "while you sleep" content.

### Cozy cabin (best for: rituals, slow workflows, weekend projects)
```
A cozy mountain cabin interior. Crackling fireplace, wooden beams, plaid
blanket on a leather chair, snow visible through the window. A retro CRT
computer on a rough wooden desk glows with Claude's interface, candles
flickering nearby.
```

Use for: weekend projects, slow rituals, focused craft, comfortable work.

### TV studio control room (best for: creator economy, content, broadcasting)
```
A vintage TV studio control room. Wall of analog monitors showing camera
feeds, mixing board with glowing knobs, ON AIR sign. A retro CRT computer
in the center showing Claude's interface, casting amber light on the
controls.
```

Use for: content creation, YouTube, podcasts, broadcasting, creator-economy topics.

### Pastry kitchen (best for: cooking, recipes, nourishment topics)
```
A warm pastry kitchen at sunrise. Marble counter dusted with flour, fresh
loaves cooling on a rack, copper pots hanging from a beam. A retro CRT
computer on the counter glows with Claude's interface, soft morning light
through gauzy curtains.
```

Use for: cooking, recipes, kitchen workflows, gentle nourishment topics.

## Picking the right scene

Match the *emotional register* of your topic, not just the literal subject.

| Topic feels like | Pick this scene |
|---|---|
| Studious / academic | Gothic library |
| Hands-on / building | Architect's loft |
| Curated / collected | Deserted island |
| Just-dropped / news | Command center |
| Quiet / hands-off | Moonlit bedroom |
| Slow / focused | Cozy cabin |
| Performative / public | TV studio |
| Nourishing / warm | Pastry kitchen |

## Custom scenes

The skill accepts free-form scene descriptions. If none of the presets fit, write your own. Keep these rules:

- **2 to 4 elements max.** Don't list 10 things. The image gets cluttered.
- **One CRT computer somewhere in the frame.** The Claude logo on the CRT screen is the visual anchor across all 6 slides.
- **Warm lighting.** Amber, golden, candlelight. The locked dark theme uses warm dark tones, no cool grays or neons.
- **Photorealistic, cinematic.** Nano Banana Pro is best at editorial photo realism, not flat illustration.

## Scene reuse

If you're posting a series of carousels for the same brand, lock in one scene and reuse it across the series. That gives the audience visual consistency and helps the algorithm cluster your content.

Just save the cover's job_id once, then reference it as the style anchor for future carousels (the skill supports this via the `style_reference` parameter — pass the job_id from a previous successful carousel cover).

## What NOT to use

- **No people in the cover.** The cover is a still life. People appear in the journals/cards on content slides if needed, but never in the cover frame.
- **No big logos.** The Claude logo on the CRT is the only logo allowed. No brand logos overlaid.
- **No text on the scene props.** Text overlays go on top, on the canvas, not painted onto the wood or fabric.
