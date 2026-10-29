# Maaf yang menyebut tindakan

## Brief and authorization

- topic: Acknowledgment of responsibility in an apology, illustrated by an ordinary lateness-and-waiting scene.
- topic_selection: auto; user explicitly delegated discovery and selection with --topic=auto.
- board: ruang-di-antara, editorial v1.3, visual/audio v1.2, implementation 2026-10-21. [Editorial](../../boards/ruang-di-antara/EDITORIAL.md), [frame contract](../../boards/ruang-di-antara/frame.md).
- audience/language: Indonesian adults; consistent lo–gua narration, complete spoken captions.
- destination: Instagram reel; 1080x1920, 30fps, target 85–95 seconds, exactly sixteen meaningful scenes and two charcoal scenes.
- execution_policy: automation
- automation_after: none
- automation_state: active
- human_review: none
- human_approved: false
- pre_render_authorization: delegated by the user's --automation instruction
- requested_endpoint: publishing
- delivery: queue, next configured account slot; no custom time and no future monitoring.
- commit: user explicitly requests a local commit after the pipeline finishes.

## Selection and overlap

Ten candidates presented before file creation: specific apology (selected), small connection invitations, unspoken expectations, privacy, relationship comparison, cognitive household work, explicit support requests, differing conflict memories, wanted touch, and reunion rituals. Selected apology has a concrete worked example and a primary research path; other candidates remain editorial proposals requiring research. Tracker and all production directories checked, including unregistered roda-beda-putaran. Existing listening, conflict pause, gratitude, interpretation, self-expansion, transparency, capitalization, and autonomy episodes address different central questions. This episode concerns owning a particular action after an ordinary mistake, not reading motives, listening before advice, or choosing an activity. No repeat takeaway.

## Research and hook decision

Jina source-body reads completed before hook selection: original Lewicki, Polin & Lount (2016) article abstract and original university report quoting authors. The research concerns judgments of written workplace trust-violation apologies; no couple-outcome guarantee is supported. See SOURCES.md.

Three hooks presented before script drafting:

1. “Maaf, gua sibuk.” Kalau berhenti di situ, bagian mana yang belum terjawab? Recommended and selected: a recognizable explanation that leaves responsibility unspecified.
2. Lo udah bilang maaf. Tapi apa yang sebenarnya lo akui? Focus on ownership.
3. Sesudah bikin pasangan nunggu, apa yang bisa lo bilang selain alasan? Focus on the practical response.

Hook 1 selected by the agent under immediate automation, not human approval. The episode will answer it by distinguishing context from responsibility and an offer of repair.

## Publishing targets

Inherit the complete current boards/ruang-di-antara/ACCOUNTS.json list. Exact snapshot/hash is stored in target_snapshot.json and mirrored below once initialized. The actual account file supersedes stale DIRECTION.md prose saying no accounts.

Live preflight: Trypost Admin's Workspace, workspace 01a171dd-5281-730d-af07-f2168d17add7; Instagram @eliansatya, social account 01a172ed-9899-7177-ab1e-627c835e4a57, connected, Asia/Jakarta, configured queue. Caller publishes directly with no approval requirement. Current instagram_reel schema: one video, maximum 900 seconds/314572800 bytes, caption maximum 2200 characters/five hashtags. Next observed free slot 2026-10-31T07:00:00Z; actual allocation will be read back after scheduling.

## Creative and audio choices

One fictional pair, waiting table, clock, arriving participant, spoken explanation, explicit ownership, repair plan and open receiving space. Consistent faceless silhouettes; palette encodes neither blame nor gender. Alternate wide interaction, table/clock detail, speech close-up and concrete return action. Canonical chrome and local fonts remain fixed. Two dramatic frames will mark missing acknowledgment and the receiver's freedom to need time.

Narration: ElevenLabs eleven_v4, resolve root .env ELEVENLABS_VOICE_ID with maintained narration.py; one tagged full-script request after complete storyboard verification. BGM: none, to leave room for an ordinary apology and its unanswered silence. SFX: reuse suitable sparse dry contact/short air/rounded connection assets from the frozen board library after bundled media-use inspection; no generated SFX. Objective acoustic and export verification will be recorded separately from perceptual listening availability.

## State

Research and hook selection complete; script and visual storyboard next. Context7 MCP is absent; maintained local references and installed CLI help are the technical fallback. No server started. Unrelated preexisting untracked creative-direction skill will remain outside this commit.

## Frozen intake

Script v1 agent-verified: 183 spoken words; concept name and immediate Indonesian meaning in line 2, substantive explanation and scene discussion in lines 2–9, concrete application 10–13, receiver autonomy 14, opening answered 15–16. No human approval.

Publishing target snapshot:

```json
{
  "source": "board",
  "board_accounts_file": "boards/ruang-di-antara/ACCOUNTS.json",
  "board_accounts_sha256": "0902013fc5eb56a40491d6e0614f680d6c03371e850caa7a0ff31c678d383baa",
  "accounts": [
    {
      "provider": "trypost",
      "workspace_id": "01a171dd-5281-730d-af07-f2168d17add7",
      "workspace_name": "Admin's Workspace",
      "social_account_id": "01a172ed-9899-7177-ab1e-627c835e4a57",
      "service": "instagram",
      "handle": "eliansatya"
    }
  ]
}
```

Narration selected from project .env: ElevenLabs / 3mAVBNEqop5UbHtD8oxQ / eleven_v4. Assets and licenses copied from approved board.
