# Motion direction — proposed v2

The user wants to work primarily through motion design, with more illustration and little text. This board plans behavior before adding typography. The current package contains static hero compositions and four separately authored diagnostic poses; it contains no timeline, rendered video or playback verification.

## Core rules

1. **Begin with an action.** A hand prepares to touch, a page turns, a copy separates, or a request crosses a local boundary. Set the viewer's question through a concrete event.
2. **Give information an identity.** A proof, a visit record and a media copy need different recognizable silhouettes or patterns. Carry that identity through movement. An avatar/face never morphs into transmitted proof.
3. **Let a cause lead the camera.** Follow the transfer after initiation, then allow time to inspect the changed state. Do not give every object an idle loop.
4. **Keep what persists.** Leave the local face, retained source picture or remote visit visible at the moment its persistence matters. A purposeful hold can be the explanatory payoff.
5. **Change the world through its subject.** A screen can fill the frame before its illustrated interior is revealed; a traveling media tile can carry attention into another location. Preserve identity and direction at a handoff. Discover a fitting registry primitive before implementing a named effect in production.

## Planned local-verification study

The four poses in `studies/pose-1.svg` through `pose-4.svg` describe one interaction, not an entire episode.

| Pose | Visible cause / response | Identity to preserve | Timing starting point at a future 30fps |
| --- | --- | --- | --- |
| Anticipate | The hand approaches the device control; receiver is unresolved | Face remains inside the device | 6–10 frames of preparation |
| Act | Finger makes contact; a separate patterned proof object begins to leave | Proof has no face/biometric imagery | 3–5 contact frames, then 10–16 for emergence |
| Travel | Proof follows a continuous arc toward the receiver | Same pattern, orientation evolves continuously | 24–36 frames; allow observation of its separation |
| Land | Proof seats at the receiver and its state changes after arrival | Local face remains; receiver adds a resolved state | 8–12 settling frames, then 18–30 hold frames |

These are proposed planning numbers, not measured animation or a fixed scene duration. A production must build and inspect the intermediate poses, including the source exit, route apex, receiver entry and post-arrival response. The static strip does not prove a continuous physical trajectory.

## Other illustration studies

**Local privacy record:** show a request reaching the external service first. Then clear the local history representation through a wipe confined to the local surface. Keep the remote visit visible. The metaphor does not imply invisibility, deletion from every observer, or removal of saved downloads/bookmarks. Narration establishes the Chrome Incognito session scope.

**Nearby delivery:** establish the original media and an available cached copy. Keep the source still while a separate matching tile moves toward the viewer. A stronger active route can contrast with a quiet longer route. If the subject instead involves a cache miss or synchronization, research and restage it; do not reuse this action as a universal internet diagram.

## Motion character

- A gesture or illustrated object may have 4–8% squash/overlap when it makes contact, provided its identity and contact remain understandable. Do not distort security or data relationships to make a flourish.
- Arrivals may use a small positional overshoot, with a proposed spring damping ratio around 0.78. Avoid springing text, opacity or every UI element.
- Use distinct easing roles: controlled ease-out for a hand settling, accelerating/decelerating motion around a transfer arc, quick geometry change after contact, and a stable inspection hold. Do not apply one fade-and-slide treatment everywhere.
- Overlap secondary reactions after the initiating event is legible, approximately 3–5 frames later as a starting guide. A destination response may not start before arrival.
- Preserve line weight and object volume through turns. A path is not a decorative looping background; it is there only while the transfer matters.
- Keep emphasis words still while they are read. Start with zero words and add an anchor only when it resolves real ambiguity.

## Editable rig handoff

The original SVG sources mark semantic groups with `data-piece`: `holding-hand`, `touching-thumb`, `phone`, `local-face`, `proof-token`, `service-receiver` and `local-browser`. Future scene authoring should give unique IDs within its actual composition and use neutral animation wrappers around the authored transforms. Keep the camera wrapper, moving token, device, face, hand and receiver separately controllable.

For a requested animation demonstration or episode, use the project-local HyperFrames contract and relevant production workflow: choose the actual scene window, author a deterministic paused timeline, verify forward/reverse seeking and diagnostic frames, and inspect playback with narration/captions/audio as applicable. No production folder is created by this board revision.

## Review before an animated handoff

Check the gesture before/at/after contact, proof emergence, continuous route, arrival before response, face/source persistence, local wipe bounds, camera handoff, caption clearance and timing at phone size. Show actual playback before claiming that the motion language has been verified. SFX should reinforce selected contacts/transfers without obscuring English narration.
