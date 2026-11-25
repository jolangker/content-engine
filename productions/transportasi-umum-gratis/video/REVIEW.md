# Verification Review — Semua Transportasi Umum Gratis

- **Production:** `productions/transportasi-umum-gratis`
- **Board:** `dua-dunia` (`editorial v2 / visual v1`)
- **Format:** `1080x1920 @ 30fps`, `96.63s` (`19` scenes, `239` spoken words, `~2.49 wps`)
- **Narration:** Single-take ElevenLabs `eleven_v4` (`TX3LPaxmHKxFdv7VOQHJ`, Liam — user-authorized episode override) + dynamic F-major 112 BPM acoustic-guitar/wooden-mallet BGM (`-14.15 LUFS`, `-1.48 dBTP`)
- **Determinism check:** Seek `45.0s -> 90.0s -> 10.0s -> 45.0s` bit-for-bit identical (`a2b75d0c2fdc`), zero console/page errors.
- **DOM lint (`dom_lint.py`):** Passed (`g5_fails: 0`, `readcheck_fails: 0`, bound to composition digest below).

## Gate record

composition_sha256: a1a49d583945f49450cf8f1c5fd55a0a5449276efffcb6dade1956075f474ddb
independent_review: subagent
listening: agent
weakest_shot: s11, the lower-third caption brushes the top border of the 3D DUNIA B plaque while DUNIA A sits flush against the left margin
wow_upgrade: s11-s12, pull cutCam back ~12% in s11 so both cutaway plaques clear the caption band and left margin cleanly, and orbit cutCam ~18 deg higher/right in s12 so Dunia B's single-file front-door queue is completely unobstructed by the ticket booth roof

- rubric.style_fidelity: 8.5/10 — faithful dua-dunia tabletop-miniature look across all 19 scenes with matte Polyfork models, expressive capsule characters, exact palette, persistent disclaimer, 50/50 split spotlighting, and both board HUD proof cards
- rubric.concept_wow: 8.0/10 — counterintuitive urban-policy arc (short-trip pedestrian shift, 1/3 front-door dwell-time bottleneck, fleet-expansion precondition, and PAJAK -> ARMADA fiscal trade-off) anchored by an unoccluded TARIF Rp 0 hook at t=0.00s
- rubric.motion_craft: 7.5/10 — deterministic renderAt(t) keeps vehicles, pedestrians, and camera moves alive from t=0.00s through 96.63s with crisp HUD entrances, progressive crossover draw, and 100-tile cascade; slightly held back by booth-roof queue occlusion in s12 and passing tram in s19
- rubric.design_typography: 7.5/10 — clean Fredoka hierarchy with high-contrast navy strokes and strong 360px phone legibility across headlines, pills, captions, and HUD cards; slight caption brush on s11 DUNIA B plaque top edge
- rubric.finish_texture: 7.5/10 — cohesive matte sRGB low-poly lighting with 21 local Polyfork GLBs (15 topic-specific assets beyond the 6 starters) and zero shadow acne; minor foreground head clipping at the bottom edge of s15
- rubric.sound_sync: 8.0/10 — native audition of master-mix.wav confirms warm, clear Indonesian eleven_v4 narration cleanly ducking the dynamic acoustic-guitar/wooden-mallet bed (-14.15 LUFS, -1.48 dBTP) with tension dip on s07-s10 and harmonic accents on s12/s14/s18
- rubric.technical: 8.5/10 — satisfies all CONTRACT.json hard limits (96.63s, 19 scenes, 239 words, 3.703s first sentence, 4.449s full hook, -14.15 LUFS / -1.48 dBTP), bit-for-bit seek determinism, zero dom-lint G5/readcheck hits, and passing storyboard gate

- [pass] hook-frame: s00_t0.00s.png (t=0.00s) immediately frames the street-level transit hub (unoccluded TARIF Rp 0 plaque, subway entrance, bus shelter, entering city bus, two smiling commuters) under the phone-readable headline TRANSPORTASI UMUM GRATIS? and opening caption word Kita
- [pass] pictures-alone: F01-F19b read cleanly on mute from free-transit premise (F01), twin baseline (F02), spotlight split (F03-F04), Month 1 surge + coins (F06), Year 1 traffic/crowding/budget squeeze (F07-F09), Year 2 dip scoreboard (F10), cutaway door mechanism (F11-F13), Year 4 crossover (F14), Year 10 plaza/scoreboard/tax trade-off (F15-F17), 71/100 grid (F18), and moving twin-world choice CTA (F19b)
- [pass] event-density: every scene introduces a distinct visual action, state change, or relationship beyond captions (retracting turnstiles in F03, rising coins in F06, dropping red depot gauge in F09, animated 1/3 dwell pie ring in F12, progressive curve draw in F14, 100-tile reveal in F18)
- [pass] motion-variety: neighbouring scenes alternate scale and movement across street push (F01), aerial split pull (F02), spotlight pan/hold (F03-F04), curb pan (F06), elevated pull (F07), sidewalk track (F08), shelter snap-zoom (F09), cutaways (F11-F13), HUD cards (F14, F18), and street-to-split pull (F19); longest same-shot run is 2
- [pass] subject-scale: capsule commuters, vehicles, diegetic plaques, 912px-wide HUD cards, and split scoreboards fill the portrait stage cleanly at 360px phone width
- [pass] ear-test: native audition of master-mix.wav confirms the 239-word Indonesian script is completely self-contained and unambiguous without visuals
- [pass] epistemic-disclaimer: persistent top-center Eksperimen pikiran. Angka dari model. (top: 64px, 28px Fredoka SemiBold with navy stroke) remains visible across Frame 0 and all 19 scenes (F01-F19b)
- [pass] simulation-hook: opening 4.449s (timing.json w0000-w0011; first sentence ends at 3.703s <= 4.5s) declares twin identical worlds, names the single differing variable (satu transportasinya gratis), and ends with Mana yang menang? over an active 3D diorama and bold TRANSPORTASI UMUM GRATIS? title
- [pass] controlled-twin-worlds: F02 (4.56-11.45s) establishes a 50/50 horizontal split (y=960px divider) with identical twin city grids, traffic, DUNIA A/DUNIA B labels, and center pill 100.000 warga · Kondisi awal sama before introducing the variable in F03
- [pass] short-term-dip: unexpected friction and Year 2 dip span F07-F10 (27.95-47.83s, starting at 28.9% of runtime within 20-45% window): stalled cars (Mobil -5%), pedestrian shift, overcrowded shelter + dropping depot budget (DEPOT · KAS MENIPIS), and Year 2 scoreboard (58 vs 64) before F11
- [pass] physical-mechanism: F11-F13 (47.83-62.75s) demonstrate the causal bottleneck via roof-off 3D bus/station cutaways contrasting Dunia B's closed rear doors + front-door turnstile tap queue (1/3 waktu berhenti) against Dunia A's open all-door boarding and service-bay garage fleet dispatch
- [pass] data-proof-cards: both dark-navy HUD proof cards appear over blurred moving city backdrops: F14 (Skor Akses & Mobilitas (Model 10 Tahun) with Year 4 white node & Nyalip! callout) and F18 (Uji 100 Simulasi Dunia 10x10 grid showing 71 yellow-bordered green win tiles vs 29 slate tiles)
- [pass] hybrid-3d-look: matte low-poly Polyfork buildings, vehicles, and street props (clean sRGB, NoToneMapping) integrate cohesively with procedural capsule citizens featuring clear smiling/frowning faces and props
- [pass] topic-specific-polyfork-sourcing: video/assets/models/ bundles 21 local Polyfork GLBs including 15 topic-specific transit/civic models beyond the 6 starter street models actively staged across scenes
- [pass] split-spotlight: F03 (13.16s) dims inactive bottom Dunia B (opacity: 0.46) while spotlighting Dunia A, and F04 (16.37s) cleanly flips the scrim to dim top Dunia A while spotlighting Dunia B
- [pass] caption-band: word-synced captions stay anchored in the lower band (top: 1415px, within [54, 1380, 972, 200]) in rounded bold white Fredoka (#FFFDF5), thick dark-navy stroke (14px #142A36), and warm-yellow (#FAD668) active-word highlight across every scene
- [pass] soft-closing-cta: narration closes at 90.35-96.63s with "Jadi di dua dunia ini, kamu pilih tinggal di mana?" keeping dua dunia consecutive over the PILIH TINGGAL DI MANA? 50/50 split (F19b) with zero spoken follow/subscribe/like prompts
- [pass] original-topic: policy scenario (fare-free public transit, pedestrian substitution, all-door dwell-time cutaway, fiscal fleet trade-off, 71/100 & 84-early-dip figures, and dialogue) is completely original and distinct from the reference episode

## Findings

### Resolved from Pre-Polish Independent Review v1
- P0 · t=0.00s · s01 hook · city bus occluded TARIF Rp 0 plaque and BasicShadowMap caused shadow acne on facades → shifted hubBus baseX to 7.6, upgraded to PCFShadowMap with normalBias 0.08, and set immediate headline opacity at t=0.00s · fixed
- P0 · t=4.49-5.25s · s01 audio · second hook sentence "Mana yang menang?" ended at 5.25s → applied pitch-preserving 1.18x atempo to S01 so full hook finishes at 4.449s (first sentence 3.703s) · fixed
- P0 · t=35.5s · s08 sidewalk substitution · cars hidden behind bus → elevated jamCam and increased brake-lit traffic to 16 bumper-to-bumper cars across both lanes with 7 pedestrians boarding bus · fixed
- P0 · t=40.0s · s09 overcrowded shelter · riders turned away from camera and DEPOT plaque clipped left → staged 14 visibly frowning riders facing 3/4 toward camera/bus and centered DEPOT · KAS MENIPIS plaque with full margins · fixed
- P0 · t=54.6s & 60.1s · s12-s13 cutaway plaques · DUNIA B and DUNIA A plaques cropped on edges or overlapped captions → repositioned plaques and pulled cutCam wider/higher so both sit uncropped above captions · fixed

### Remaining P1 Polish Items (Non-Blocking, Independent Review v2)
- P1 · t=49.93s · s11 dual cutaway · lower-third caption brushes the top border of the 3D DUNIA B · TAP PINTU DEPAN plaque and DUNIA A · SEMUA PINTU sits flush at the left margin → pull cutCam back ~12% and tilt slightly higher · open
- P1 · t=54.62s · s12 Dunia B macro cutaway · solid dark roof of ticket booth/turnstiles partially occludes the single-file front-door commuter queue → orbit cutCam ~18 deg higher/right or shift booth slightly left · open
- P1 · t=71.41s · s15 Year 10 plaza · STASIUN & SEKOLAH plaque sits in front of two standing students and two foreground heads clip the bottom edge → shift sign posts back/left and clear near sidewalk edge · open
- P1 · t=66.15s · s14 crossover HUD chart · X-axis labels (Thn 0, Thn 2, Thn 4, Thn 7, Thn 10) sit at visually equal intervals despite +2/+2/+3/+3 year gaps → align X-axis tick spacing proportionally or use even 2-year ticks · open
- P1 · t=91.55s · s19 afternoon payoff · passing tram briefly obscures boarding commuters in the opening 2.5s beat → offset tram entry phase by ~1.2s · open
