# Sources and provenance

Read date: 2026-11-03. Creative output is original; no third-party artwork or logos are embedded.

## Fonts actually used

Copied from the project-local `.agents/skills/canvas-design/canvas-fonts/` bundle, whose upstream provenance is documented in `.agents/skills/shortform-board/references/visual-craft.md`:

- BricolageGrotesque-Bold.ttf; BricolageGrotesque-OFL.txt. Used as Bricolage Grotesque, weight 700.
- InstrumentSans-Regular.ttf, InstrumentSans-Bold.ttf; InstrumentSans-OFL.txt. Used as Instrument Sans, weights 400 and 700.

Files and original licenses are preserved beside this document. Hashes are recorded in asset-manifest.json after copying. No remote font loading is required.

## Evidence behind the illustrative studies

| Study | Source body read | Supported scope | Simplification / limit |
| --- | --- | --- | --- |
| Passkey sign-in | [FIDO Alliance passkeys FAQ](https://fidoalliance.org/passkeys/) | Local biometric processing is not sent to a remote server; authentication uses cryptographic credentials and a challenge-response protocol | The original diagram is a conceptual local-check/proof exchange, not full protocol choreography. The credential may be synced or device-bound. No claim that all private keys can never leave their first device. |
| Private-browsing boundary | [Google Chrome Help: Browse in Incognito mode](https://support.google.com/chrome/answer/95464?hl=en) | Chrome removes the Incognito session's browsing-history record/site data after all Incognito windows close; visited sites may still observe activity | Downloads/bookmarks remain; the illustration concerns the history record and one website receiving a visit. It is not total anonymity, erasure of all local data, or a claim about what every network observer can read. |
| Nearby video copy | [Cloudflare Learning Center: What is a CDN?](https://www.cloudflare.com/learning/cdn/what-is-a-cdn/) | CDN servers can serve cached content closer to users, including video | This is a schematic cache hit with an available copy. Locations are conceptual, not a geographic map or a claim about a named streaming service. “Nearby” does not promise the absolute nearest server. |

SearXNG's reader returned an extensive navigation section for FIDO; the relevant FAQ was also read through the web reader. The Chrome URL initially consulted redirected to the canonical page above. Cloudflare's conceptual learning article was read as a mechanism reference, not implementation documentation for a cloud-service API. No library, SDK, API or CLI setup is part of the user's board request.

These anchors constrain static illustrative copy. A later episode must complete its own claim-level research and review. Titles and UI are original sample writing. `example.com` is reserved example-domain UI text, not a capture or an instruction to visit a service.

## Audience research inherited from the discussion

- [Passkey confusion in r/PasswordManagers](https://www.reddit.com/r/PasswordManagers/comments/1rg3nl4/eli5_what_is_a_passkey_and_why_are_so_many/): audience question, not technical authority.
- [FIDO 2026 consumer/workforce report](https://fidoalliance.org/the-state-of-passkeys-2026-global-consumer-and-workforce-report/): survey context; does not prove demand for this channel or distribution in proposed countries.

No membership counts, views, competition estimates or revenue forecasts are inferred from these sources. No Reddit replies or external messages were posted.
