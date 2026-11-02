# Bangku di jalan pulang

New production selected under --board=ruang-di-antara --topic=auto --delivery=queue --automation. Topic selection: auto. Endpoint: publishing / queue=next, one Instagram Reel for every inherited account. Commit after the completed pipeline is explicitly requested.

execution_policy: automation
automation_after: none
automation_state: active
human_review: none
pre_render_authorization: delegated by the user's --automation instruction
human_approval: false

Board: [editorial v1.4](../../boards/ruang-di-antara/EDITORIAL.md), [visual v1.2, implementation 2026-10-21](../../boards/ruang-di-antara/frame.md), audio v1.2. Board approved; this episode is agent-verified under delegation. Format 1080x1920, 30fps, sixteen meaningful frames, exactly two charcoal turns 08/10, approximately 90s (85–95 target). Indonesian lo–gua. Purpose: distinguish repeated practical behavior from mutually meaningful relationship ritual using a fictional Friday park-bench stop. No B-roll. Full spoken captions, sparse material sounds, intentional no music so the question and answer remain emotionally open.

## Delegated editorial shortlist (before file creation)

1. **Recommended/selected — Bangku di jalan pulang.** Investigate how a repeated park stop acquires shared symbolic meaning; ask whether both partners understand it as their ritual. A positive ordinary scene, distinct from past-memory savoring and novel-activity self-expansion.
2. Remembering a small preference. Investigate accurate partner knowledge through a familiar snack choice; distinguish curiosity from assuming knowledge stays current.
3. Laughing at the same mishap. Investigate shared laughter through a harmless dropped grocery bag; avoid treating all teasing as connection.
4. The invitation hidden in a small remark. Investigate bids for connection through a remark about a street cat; distinguish an invitation from an obligation to respond always.
5. Celebrating an effort before its result. Investigate process-focused encouragement after a rejected application; keep encouragement distinct from praise for good news.
6. A disagreement without a verdict on character. Investigate behavioral specificity through an ordinary untidy shelf conflict; distinguish action description from a global person label.
7. Revising an old assumption. Investigate updating partner knowledge when an old favorite changes; ask rather than fixing the partner in a remembered version.
8. The joke that did not land. Investigate repair after unintended hurt without inferring malicious intent or prescribing forced forgiveness.
9. Good enough shared plans. Investigate coordination when two preferred weekend options differ; negotiate one concrete choice without diagnosing the relationship.
10. An affectionate gesture with permission. Investigate preferences for touch after a tiring day; keep consent and individual variability explicit.

These are provisional editorial leads, not researched claims. Selected 1 for a clean one-concept 90s explanation, accessible original study and positive relational scene. Tracker and existing folders checked. Nearest episodes: momen-kecil-dinikmati-lagi (attention to a positive memory, tea scene); coba-hal-baru-berdua (novelty and expansion); ruang-untuk-memilih (autonomous choices). This episode instead examines mutual symbolic meaning in repeated activity, with a park bench and no instruction to invent novelty. No duplicate slug.

## Research and preflight

Original Garcia-Rada, Sezer & Norton (2019) paper read through MarkItDown from HBS; publisher abstract also read. Definition: repeated joint activity with symbolic meaning. Mutual agreement may be tacit or explicit. Studies of reported own relationships do not establish causal direction; the manipulated vignette study measures observer judgments. No promised happiness effect or diagnostic claim. SOURCES.md maps claims and fiction. SearXNG and Context7 tools unavailable; Jina search failed with quota error. Fallback: web search/open for source discovery and publisher body, MarkItDown for the original PDF; installed skill/CLI docs for HyperFrames.

Live preflight: Admin's Workspace 01a171dd-5281-730d-af07-f2168d17add7, connected Instagram @eliansatya 01a172ed-9899-7177-ab1e-627c835e4a57. Caller publishes directly, requires_approval=false. Queue configured daily 05:00 Asia/Jakarta. Final write uses next free queue slot and actual returned schedule. instagram_reel: up to 900s, 314572800 bytes; text 2200 characters, five hashtags. Usage known at intake. HyperFrames 0.9.1 pinned. Existing unrelated tracker/board/production changes are preserved and excluded from the requested commit.

## Hook selection before drafting

1. “Setiap Jumat, lo dan pasangan mampir ke bangku taman yang sama. Kenapa kebiasaan sederhana itu terasa spesial?” Selected/recommended: concrete recurring place, a question answered by shared meaning.
2. “Lo menyebutnya waktu spesial berdua. Dia menyebutnya istirahat sebelum pulang. Lagi menjalani kebiasaan yang sama?” Competing meanings; strong but opens with more interpretive tension.
3. “Kalau tempat duduknya biasa aja, apa yang bikin lo ingin kembali ke sana bareng dia?” Object-first curiosity; less explicit repetition.

All three evaluated before SCRIPT.md drafting; agent chose 1 under --automation, no human approval claimed.

## POV contract and narration-only check — script v1

Viewer lo = partner who already values the Friday stop. Dia = the other partner whose meaning remains unknown. Narrator = observing companion, with no personal autobiography. Scene 4's kita = the established couple inside an explicitly introduced viewer interpretation (buat lo). Scene 11 audibly says Lo bisa bilang before gua/kita; gua is viewer, kita is the same couple. Scene 12 audibly says lo tanya ke dia before Buat lo; quoted lo addresses the partner. Return to narration at scene 13 directs the viewer to listen. Kalian always means both partners. No dialogue spoken by the partner is invented as fact. Every instruction remains actionable by the original viewer. Hook, application and closing preserve the role. Complete spoken text read without visuals: pass; no unresolved speaker changes. Recheck identical synthesis text/captions before audio.

## Publishing targets

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

## Stage record

Brief, research and script agent-verified. Next: complete and inspect all styled storyboard artifacts before synthesis.
