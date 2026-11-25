# Dua Dunia — editorial framework v2

## Scope

**Dua Dunia** produces short-form Indonesian thought-experiment simulations that test big "what if" questions about public policy, everyday economics, urban systems, and social incentives by placing two identical miniature worlds side by side and changing **exactly one rule**.

- **In scope:** Counterfactual policy/system tests with clear first-order friction and second-order compounding (e.g., free public transit, 4-day workweek, congestion pricing, universal basic services, waste-sorting penalties, plastic bans).
- **Out of scope:** Partisan campaigning, real-world personal attacks, ungrounded conspiracy theories, or retelling the reference video's exact corruption episode.

## Audience experience

The viewer should feel like they are watching a fair, playful miniature laboratory rather than a lecture:
1. Hooked by a tempting intuition ("kalau X berubah besok pagi, langsung enak nggak?").
2. Surprised when the "good" policy actually hurts or stalls in the short term.
3. Convinced by a concrete physical mechanism they can *see* in 3D, followed by a crossover graph and a 100-world sensitivity check.
4. Left with a memorable long-term trade-off and a low-friction choice question.

## Epistemic transparency

- Every episode keeps a subtle, fixed top-center disclaimer: **`Eksperimen pikiran. Angka dari model.`**
- Model numbers (wages, commute times, percentages, 100-world win rates) must be internally consistent, grounded in plausible published mechanisms/ranges researched per episode, and clearly framed as illustrative simulation outcomes—never misrepresented as official forecasts.

## Story shape

Follow the 12-beat twin-world simulation arc (flexible in shot count, locked in causal logic):

1. **Simulation hook (0–4.5 s):** Locked spoken formula over a street-level 3D vignette + bold title—declare the identical twin worlds and the one difference, then ask which world is better (see [Hook pattern](#hook-pattern)).
2. **Controlled twin-world setup (4.5–10 s):** 50/50 split-screen locking 3 shared baselines (population, income/traffic, rules).
3. **Single-variable manipulation (10–16 s):** Dim inactive panel; highlight the one rule that differs between World A and World B.
4. **Audience prediction (16–20 s):** Ask how long until residents feel the benefit ("Sebulan? Setahun?").
5. **Short-term honeymoon (20–26 s):** Immediate visible relief in Month 1.
6. **Unexpected short-term friction (26–38 s):** 2–3 concrete street/institution vignettes showing realistic transition pain or bottlenecks.
7. **Counterintuitive dip + voiced skepticism (38–45 s):** Split-screen scoreboard where World A temporarily trails World B, plus citizens voicing the viewer's doubt.
8. **Concrete physical mechanism (45–60 s):** A visual cutaway or spatial comparison showing *why* the system behaves differently underneath.
9. **Inflection point / crossover proof (60–68 s):** Recovery vignette + dark-navy line chart showing World A overtaking World B (`Nyalip!`).
10. **Long-term compounding payoff (68–86 s):** Second-order benefits + end-horizon split-screen scoreboard (e.g., Year 10 or Year 20) + brief note on who loses out.
11. **100-world robustness check (86–94 s):** 10×10 Monte Carlo grid showing overall win rate alongside how many worlds still suffer a short-term dip.
12. **Human takeaway + choice CTA (94–105 s):** Quiet everyday payoff scene + split-screen closing choice question. Weave the account name into the closing line by keeping the exact phrase **dua dunia** consecutive—such as `Jadi di dua dunia ini, kamu pilih tinggal di mana?` or `Dari dua dunia ini, menurut kamu mana yang lebih baik?`—then let the viewer answer. The CTA stays a choice question, never a sales ask: no spoken `follow`, `subscribe`, or `like` prompts. The configured handle lives in [ACCOUNTS.json](ACCOUNTS.json).

## Hook pattern

Every hook is one spoken run built from two slots:

> **Kita simulasikan dua dunia yang sama, tapi beda {topik dan overview}. {pertanyaan mana yang lebih baik}?**

| Slot | What goes in it |
| --- | --- |
| `Kita simulasikan dua dunia yang sama, tapi beda {topik dan overview}.` | Name the episode's topic plus the single rule, price, or habit that differs between the worlds, such as `aturan parkir`, `subsidi bensin`, or `jam kerja`. The difference is declared up front, not revealed later. |
| `{pertanyaan mana yang lebih baik}?` | A short comparison question that invites a prediction, such as `Mana yang lebih baik?` or `Menurut kamu, dunia mana yang menang?`. |

The dots in the shorthand stand for words to fill in; complete each slot and use ordinary punctuation in the finished hook. Vary the exact wording across episodes so the series does not open identically every time—`Kita coba dua dunia yang sama persis, cuma beda …`, `Aku bikin dua dunia kembar; satu-satunya bedanya …`, `Dua dunia ini sama, kecuali satu aturan …`—but every variation keeps the same skeleton: identical twin worlds, one named difference, then the comparison question. Keep the whole run inside one breath of roughly 3–4.5 seconds so the setup beat still lands on schedule.

## Duration and pace

- **Target runtime:** `75–115 s` (sweet spot `90–105 s`; reference `101.98 s`).
- **Shot cadence:** `12–34` shots (avg `2.8–4.5 s` per shot), changing on narration clauses.
- **Narration density:** `180–290` words (`2.1–2.7` words/sec; reference `244` words at `2.39` wps).

## Voice

- **Narrator:** Conversational, curious, lightly theatrical Indonesian ("Aku coba di dua kota kembar…", "Coba tebak…", "Tapi coba lihat…"). Uses *aku/kamu* to feel like a smart friend running a tabletop experiment, never stiff academic Indonesian.
- **Dialogue:** Citizens' reactions appear visually via expressions and short diegetic protest/status signs; one narrator voice carries the entire spoken track.
- **Promotion:** The closing invites a choice; it never pushes a follow. The account name surfaces only inside the natural `dua dunia` phrasing of the final question.
- **Publishing targets & voice override:** See [ACCOUNTS.json](ACCOUNTS.json) and [AUDIO.json](AUDIO.json).
