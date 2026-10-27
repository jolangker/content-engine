# Ruang di Antara audio-boundary investigation

Date: 2026-10-27. Scope: the six completed productions registered to the `ruang-di-antara` board. This is a diagnostic report; production sources, cached narration, exports, tracker states and remote deliveries were not changed.

## Finding

The primary defect is in editorial audio placement. The preparation scripts insert silence at the midpoint between two provider word timestamps without checking whether that midpoint is actually silent. At several inspected boundaries, the following word has already started in the waveform. Its beginning remains in the outgoing scene, inserted silence interrupts it, and its remainder resumes around the next scene. A second, smaller defect is the use of arbitrary fractional-second scene boundaries without reserving enough quiet time for 30fps visual sampling.

The inspected delivery exports accurately preserve the placed audio. This investigation found no additional export offset in 30 correlation windows across the six episodes. Incorrect placement is already present in the local narration WAVs.

## Primary evidence: speech split by inserted silence

These three examples combine source waveform inspection, the placement manifest, the actual placed WAV, exported audio excerpts, and independent local ASR of the preserved source. ASR supports the word identity; its estimated word-start times are not treated as precise acoustic boundaries because they can include preceding silence.

| Production | Scene boundary | Following word | Measurable signal before insertion cut | Inserted silence |
| --- | --- | --- | --- | --- |
| `gua-kira-udah-kelihatan` | 08 → 09 | “Ini” | approximately 20–25ms | 2.100s |
| `coba-hal-baru-berdua` | 06 → 07 | “Lo” | approximately 20ms | 0.27375s |
| `terima-kasih-yang-melihat` | 14 → 15 | “Jadi” | approximately 70–75ms | 0.35875s |

The durations above measure signal preceding the inserted pause, not the distance to the eventual visual cut. That small piece of speech plays while the outgoing scene remains visible; the pause then separates it from the rest of the word.

For `terima-kasih-yang-melihat`, the source cut is 76.122s. A clearly separated signal begins around 76.047–76.052s, after a quiet interval. The placement script leaves that first 70–75ms before the pause. In the placed timeline the fragment begins around 81.838–81.843s; inserted silence runs approximately 81.91325–82.272s. The first video frame showing Scene 15 is at 82.300s. This explains both the small incoming-word fragment in the old scene and the interrupted onset.

See [waveform evidence](waveform-evidence.png), [onset estimates](selected-onsets.json), and [independent ASR](independent-asr.json). Four-second export excerpts for direct listening:

- [“Ini”, Scene 08 → 09](gua-kira-udah-kelihatan-export-seam08.wav)
- [“Lo”, Scene 06 → 07](coba-hal-baru-berdua-export-seam06.wav)
- [“Jadi”, Scene 14 → 15](terima-kasih-yang-melihat-export-seam14.wav)

Corresponding `*-source-seam*.wav` files retain uninterrupted source context.

The onset estimates use 5ms RMS windows, the end of the last quiet interval lasting at least 50ms, and three thresholds: −55, −50 and −45dBFS. They are approximate signal onsets, not phoneme annotations or perceptual listening. The source/placed-waveform relationship is direct; exact identification of the first phoneme remains a listening task.

## Code path

The same implementation appears in [gua-kira-udah-kelihatan/prepare_audio.py](../../productions/gua-kira-udah-kelihatan/prepare_audio.py), [coba-hal-baru-berdua/prepare_audio.py](../../productions/coba-hal-baru-berdua/prepare_audio.py), and [terima-kasih-yang-melihat/prepare_audio.py](../../productions/terima-kasih-yang-melihat/prepare_audio.py):

1. Compute `at = (previous_word.end + next_word.start) / 2`.
2. Split decoded samples at `round(at * 48000)` and insert zero-valued samples.
3. Shift metadata based on each word's estimated start.
4. Set the scene boundary to the end of the inserted pause.

Relevant latest-production lines: midpoint at 28, sample concatenation at 32, word remapping at 45, and scene boundary at 51. The earlier [jeda-punya-waktu-kembali/prepare_audio.py](../../productions/jeda-punya-waktu-kembali/prepare_audio.py) uses the same midpoint strategy.

These steps assume provider timing separates the physical speech samples correctly. Text equality, valid timestamps, matching word counts and matching hashes do not establish that. Once the midpoint is inside the following word, shifting that word's metadata cannot move its already-separated initial samples. Loudness normalization preserves this incorrect arrangement.

As a broad diagnostic screen, 44 of 57 inserted-pause positions have at least one adjacent 25ms source window above −50dBFS. This count is not a claim that all 44 contain incoming speech: outgoing speech tails, breaths or other signal can also trigger it. It identifies positions requiring inspection. Three incoming-word cases were examined in detail above.

## Secondary evidence: fractional cuts and video sampling

The HTML scene starts match `timing.json`, and all six actual exports report 30fps with video start PTS 0. A planned cut between frame times can only become visible at the next sample: `ceil(cut * 30) / 30`. Several scenes leave less quiet time before the next word than that sampling delay.

| Production | Scene boundary | Planned visual cut | First new video sample | Next word metadata | Metadata lead before new visual |
| --- | --- | --- | --- | --- | --- |
| `kabar-baik` | 05 → 06 | 31.704s | 31.733333s | 31.717s | 16.33ms |
| `kabar-baik` | 06 → 07 | 37.004s | 37.033333s | 37.024s | 9.33ms |
| `gua-kira-udah-kelihatan` | 05 → 06 | 27.303s | 27.333333s | 27.323s | 10.33ms |
| `coba-hal-baru-berdua` | 14 → 15 | 78.838s | 78.866667s | 78.865s | 1.67ms |
| `terima-kasih-yang-melihat` | 06 → 07 | 37.56725s | 37.600s | 37.58725s | 12.75ms |
| `terima-kasih-yang-melihat` | 14 → 15 | 82.272s | 82.300s | 82.285s | 15.00ms |

These are metadata-derived timing conflicts, not independent measurements of exact phoneme onset. They demonstrate inadequate timing margins even under the metadata's own assumptions.

Decoded latest-production frames independently confirm Scene 06 at frame 1127 / 37.566667s ([image](seam06-01.png)) and Scene 07 at frame 1128 / 37.600s ([image](seam06-02.png)). No metadata-derived conflicts occurred in `cerita-belum-selesai` or `jeda-punya-waktu-kembali`; this does not certify their acoustic alignment.

## What export verification establishes

Cross-correlated five two-second windows per episode at source times 2, 18, 35, 52 and 65s. Accounted for `kabar-baik`'s authored 0.3s audio start. All 30 windows match at zero additional offset at 8kHz measurement resolution (0.125ms); correlations exceed 0.998. This rules against a consistent renderer/mux delay or accumulating drift in those sampled windows. It does not establish every individual seam or the timing of a social platform's transcoded copy.

The existing [sound_design.py](../../.agents/skills/shortform-production/scripts/sound_design.py) verifies narration/source hashes and SFX placement/presence. The latest [delivery verification](../../productions/terima-kasih-yang-melihat/VERIFICATION.md) and [review](../../productions/terima-kasih-yang-melihat/video/REVIEW.md) also disclose that perceptual listening was unavailable. Passing those checks never established that each narration boundary was an acoustic gap. Visual seam strips cannot detect a split word. This is the verification gap through which the defect passed.

## Recommended correction

1. Replace duplicated midpoint-only placement with one maintained helper. Use word alignment to locate a semantic boundary, then verify the actual decoded audio contains a suitable quiet interval there. If it does not, flag the boundary for local realignment or listening rather than inserting silence through speech.
2. Preserve complete spoken units. Insert any editorial pause inside the verified quiet region. A tiny fade can smooth a quiet splice, but cannot repair a phoneme already split between scenes.
3. Use integer audio samples and integer video frames as the timing authorities. Put the scene cut within the verified pause, leaving a deliberate quiet lead into the incoming scene; approximately 50–100ms after its first visible frame is a practical starting margin, subject to the intended rhythm. Rounding alone cannot repair the primary split-word issue.
4. Derive scene starts, captions and cue times from the same finalized placement map. Measure source-to-export offsets, and inspect/listen across every narration seam in the actual export. Fail validation for cuts through active speech or negative incoming-speech margins.
5. Re-edit the preserved recordings and rebuild only affected timing, captions, cue plans and exports. New voice synthesis is not needed to correct the diagnosed placement defect. Existing published/queued media require separately scoped replacement work.

## Reproduction and limits

- `python reports/ruang-di-antara-audio-cuts-2026-10-27/audit.py`: inspect 88 scene boundaries, 57 inserted cuts, HTML timing consistency, actual video stream metadata and 30 audio correlation windows; writes [measurements.json](measurements.json).
- `python reports/ruang-di-antara-audio-cuts-2026-10-27/transcribe_evidence.py`: offline cached multilingual faster-whisper-large-v3, CPU/int8, Indonesian, word timestamps; writes [independent-asr.json](independent-asr.json). One complete source recording and two short source contexts were transcribed. Minor ASR lexical errors are retained as evidence; no ASR output changes the script or captions.
- `python reports/ruang-di-antara-audio-cuts-2026-10-27/plot_evidence.py`: rebuild waveform proof, selected onset estimates and six listening excerpts.

No perceptual listening or remote-platform playback was performed. Findings concern preserved local source files, placed WAVs and delivered local MP4s. No preview server was started, and no remote draft, schedule or published post was modified.
