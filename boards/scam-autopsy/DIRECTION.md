# Scam Autopsy

**Draft v1 · Editorial and visual review.** Each episode follows one reported scam from the first thing a recipient sees to the detail that gives it away. A viewer should be able to point to that detail the next time it appears, or forward the clip to a parent who can.

## Reading the board

- The brief sets the US and UK audience aged 35–65, the three subject pillars, the four beats, English narration and captions, and a dated official advisory in frame. Shorts and Reels run 35–45 seconds. TikTok runs 61–75 seconds and adds a recovery beat tailored to the case. The commissioning questions and checkable limits are in the [editorial framework](EDITORIAL.md) and [production contract](CONTRACT.json).
- The proposed art direction places a reconstructed object on a dark examination desk. A marker catches the precise word, charge or physical seam to inspect. A separate paper record identifies the source. The [visual guide](frame.md), [static style board](style-board.png) and [editable studies](style-board.html) cover the wrong-number text, a parcel charge, a task deposit and a parking sticker.
- Play the [16.5-second wrong-number study](motion-preview.mp4) with sound. Watch what happens *after* the recipient corrects the mistake. The follow-up appears, the marker catches the invitation to stay in touch, and the picture cuts from the chat to the destination of a later investment payment. The last shot returns to the same words. The editable project includes its [composition](motion-preview/index.html), [timing](motion-preview/assets/pilot.js) and local assets.

## Sources and reconstructions

| Study | Evidence used |
| --- | --- |
| Wrong-number text, US | On-screen credit dated 14 April 2025. Item 5 describes an unexpected text becoming a friendship and an invitation to a bogus investment platform. The advisory recommends leaving unexpected texts unanswered. Items 1 and 2 support the separate redelivery-fee and task-deposit studies. [FTC, *Top text scams of 2024*](https://search.ftc.gov/system/files/ftc_gov/pdf/spotlight-top-text-scams.pdf) |
| Current circulation | A regional BBB warning reported on 2 November 2026 describes wrong-number messages leading into investment conversations in West Tennessee. The pilot makes no claim about local UK prevalence. [WBBJ report](https://www.wbbjtv.com/2026/11/02/wrong-number-texts-used-lure-west-tennessee-victims-into-scams-bbb-says/) |
| Parking sticker, US | On 24 November 2025 the bank advised checking parking codes for a sticker covering the printed sign. The three poses isolate the lifted corner. The drawn fragment contains no QR payload. [Commerce Bank, *QR code scams*](https://www.commercebank.com/personal/ideas-and-tips/2025/qr-code-scams) |

The conversation with “Nina,” the reserved 555 number, the parcel brand and the fee are illustrative. All exhibit artwork was drawn for this board. Archivo and IBM Plex Mono are bundled with their OFL notices.

## Sound and playback

The proposed English narrator is ElevenLabs Alice, recorded in one take with `eleven_v4`. All 39 spoken words passed the alignment check. A buzz cues the first text, a muted ping accompanies the follow-up, and a low tone introduces the payment record. The final line plays without a music bed. The visible AI voice credit sits beside the dated source. See the [voice selection](AUDIO.json), [timings and provenance](motion-preview/audio_meta.json), [mix recipe](motion-preview/audio/mix.py) and [Pixabay license for the bundled ping](https://pixabay.com/service/license-summary/).

To rebuild from the board folder, run `npm --prefix motion-preview run check`, then `npm --prefix motion-preview run render`. The saved mix plays without contacting ElevenLabs.

## Draft review

The 1560 × 1569 static export loads both local typefaces. Its message, checkout and transfer panels show different evidence at the same phone scale. The parking study shows the movement from the whole label to its seam.

The H.264/AAC pilot was checked at phone size and at decoded frames across all four beats. The first question is visible on frame zero. At 1080 × 1920 and 30 fps, first measured motion is **0.2 s**, the longest still interval is **2.8 s**, and the held share is **50.4%** with the caption region masked. The mix measures **−14.29 LUFS** integrated and **−3.36 dBTP**. HyperFrames reported zero errors and five safe-zone warnings for the upper masthead and lower duplicate advisory slip. The dated credit, spoken captions and AI disclosure also appear inside the safe area. The session-owned HyperFrames preview was stopped after inspection.

**Next review.** Watch once with sound and once muted. Does the continued conversation stand out before the payment diagram arrives? The light-table treatment and Alice voice are proposed choices pending user review.
