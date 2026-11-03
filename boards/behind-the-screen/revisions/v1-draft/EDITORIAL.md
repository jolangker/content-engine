# Behind the Screen — editorial v1 (proposed)

## Identity and audience

**Promise:** Understand what happens behind your everyday clicks.

English-language short-form explainers for adults who use phones, browsers and online services without needing to know their internal vocabulary. Start with international English and concrete everyday situations. US, UK, Canada and Australia are proposed initial markets; actual audience geography must be measured after publication. Do not equate English narration with distribution in those countries.

The intended emotional progression is recognition → curiosity → a visible causal discovery → a more accurate expectation. The narrator is a thoughtful guide who shares the viewer's question and gives a direct answer. Never frame the viewer as foolish.

## Scope and pillars

| Pillar | Everyday entry point | Explanatory territory |
| --- | --- | --- |
| Identity and access | A login prompt, lost phone, authentication request | Passkeys, sessions, local verification, recovery, permissions |
| Copies and memory | A photo disappears, storage fills, a change appears elsewhere | Device/cloud copies, synchronization, backups, caches, deletion |
| Connections and delivery | Fast Wi-Fi feels slow, a video buffers, a message arrives late | Bandwidth, latency, local networks, routing, content delivery |
| Visibility and control | A private tab, consent choice, suggested content | Who can observe what, permission boundaries, account state and data flows |

Prioritize general mechanisms with a clearly identified example. Name a product/version only when its behavior is necessary to the answer. Avoid drifting into gadget reviews, daily AI announcements, software-buying lists, generic productivity tips or unsupported speculation about platform intent. These are scope choices for a coherent audience promise, not claims that those formats lack demand.

## Topic selection

Choose a question with all of the following:

1. A recognizable action or result that can be shown immediately.
2. One answerable causal question; distinguish cause from correlation.
3. At least two useful visual discoveries, not just a definition and tips.
4. Accessible primary evidence for the explanation and relevant exceptions.
5. A clear observation, expectation or bounded action the viewer can carry away.
6. A manageable visualization whose simplification can be stated honestly.

Audience questions from Reddit can supply wording and pain points. Read the original post, record the URL and distinguish the poster's experience from verified behavior. Archived discussions may indicate a recurring question but are not current reply opportunities. Never invent a post, quote or audience demographic.

## Reusable story contract

Default proposal: **60–90 seconds**, 9:16. Duration and shot count follow explanation density; do not inherit the other boards' ninety-second or sixteen-frame locks. A starting plan may use 9–14 explanatory shots, with enough time for route direction, labels and captions to be read. This range is an implementation proposal, not a proven retention formula.

| Story role | Required contribution |
| --- | --- |
| Familiar event | Show the action or result that makes the question meaningful. Write the hook and its bridge together. |
| Locate the hidden relationship | Identify who or what is involved, where information lives and the first useful distinction. |
| Follow the process | Show input → transfer or local operation → response, naming terms at their point of use. Each beat resolves a question or exposes the next dependency. |
| Test the expectation | Compare the original assumption with the demonstrated mechanism; include the exception needed to avoid a false takeaway. |
| Return and answer | Revisit the opening event and give its plain-language answer. Add one bounded practical implication only if supported. |

These are story roles rather than mandatory title cards or a fixed shot order. Supply an early substantive answer rather than withholding the whole explanation. Put qualifications beside the claim they limit. Finish with the viewer's question answered rather than an unrelated engagement slogan.

## Voice and perspective

- Use conversational English, contractions and short concrete sentences. Explain one new term when it becomes useful.
- Address the viewer as “you” when they retain the same role. Identify a website, device, provider and attacker explicitly when roles change. “It” must have one obvious referent.
- Say what an operation does before naming its implementation. A simple analogy must preserve source, destination, copies and limits; label where it stops matching.
- Do not attribute intent to an algorithm or company without evidence. Avoid “your phone is listening”, “nothing is ever deleted”, “VPNs make you anonymous”, or “passkeys can never be stolen” as unsupported absolutes.
- Separate authentication from encryption, local verification from sending biometrics, synchronization from backup, and geographic distance from all causes of network delay.
- Write captions from the final narration. Emphasis copy supplies orientation or the current question rather than duplicating paragraphs of speech.

Run a narration-only continuity review before synthesis: identify the initiating actor, the information or state being followed, each destination and every perspective transition. Then verify the storyboard expresses the same roles and causal order.

## Evidence and research requirements

Episode research follows the production skill's research/script reference. Use primary standards, provider documentation and reproducible observations where suitable; a vendor explanation supports documented behavior, not every performance or marketing claim. Use Context7 first for current library/API/SDK/CLI/cloud-service implementation documentation. If unavailable, record the limitation and use primary official documentation as the fallback. Do not require Context7 for ordinary audience research or original visual design.

Record platform, version/date and configuration wherever behavior depends on them. Keep an explicit claim/source/scope/visual-simplification table in the production. For consequential security claims, cross-check broad assertions against another authoritative source or a standard. Mechanism evidence stays separate from creative references and audience-demand evidence.

Special domain checks:

- **Passkeys:** distinguish biometric/PIN unlocking from the credential, synced from device-bound credentials, and sign-in from recovery. Never animate a face or private key being sent to a relying website as if that were ordinary authentication.
- **Privacy:** name the observer and information available to them. Closing a private session is not erasing downloads/bookmarks or activity from a visited service. Do not imply an ISP can necessarily read HTTPS contents.
- **Storage:** distinguish deletion intent, visibility, retained copies, trash windows, backups and physical erasure. Verify the specific provider's behavior before offering a procedure.
- **Networking:** distinguish bandwidth, latency, congestion, distance and cache availability. A schematic nearby copy does not guarantee the nearest server or that all content is cached.

## Initial topic bank — questions, not verified scripts

| Candidate hook | Core distinction to investigate | Production note |
| --- | --- | --- |
| What does a passkey actually prove? | Local approval versus proof sent to a website | Strong fit with the first visual study; scope recovery separately |
| What happens to your passkeys when you lose your phone? | Synced versus device-bound credentials and recovery | Requires a selected provider and current recovery documentation |
| Private browsing: private from whom? | Local history versus remote observation | Scope a specific browser; state exceptions |
| Why can a video come from somewhere nearby? | Origin versus cached copy | Demonstrate a cache hit, then acknowledge misses |
| Why can fast Wi-Fi still feel slow? | Link rate versus the rest of the delivery path | Pick one demonstrated bottleneck per episode |
| Did deleting that photo delete every copy? | Device copy, sync, trash and backup | Requires a selected product/configuration |
| Why does logging out of one device leave another signed in? | Separate sessions versus account identity | Verify the chosen service's session behavior |
| Why does a permission prompt appear again? | Permission scope, persistence and context | Avoid implying every reset has one cause |
| Why does a website remember you after you close a tab? | Tab lifetime versus persistent state | Separate cookies, account state and other mechanisms |
| Why can two people see different versions of the same page? | Cache state, rollout or personalization | Choose one supported mechanism rather than claiming a universal cause |

The three static studies illustrate the board's range. They do not select an episode or constitute a full factual review of these candidate hooks.

## Evaluation proposal

After an explicitly requested production test, compare early retention, average watch/completion, saves/shares per view, substantive follow-up questions and audience geography at comparable post ages. Treat results as exploratory when reach, traffic source, duration or account age differs. Do not infer demand or geographic fit from views alone. Publishing targets are configured in ACCOUNTS.json only after user selection.
