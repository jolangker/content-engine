# Sources and claim boundaries

Research date: 2026-10-24. Discovery and extraction used Tavily CLI; query-focused extraction flags failed validation, then plain extraction succeeded. Source excerpts support the claims below; the script is original Indonesian paraphrase. No source image is reproduced.

## Evidence

1. Schlage, Rekeying Quick Start Guide, manufacturer reference: https://www.schlage.com/content/dam/sch-us/documents/pdf/installation-manuals/P513-325.pdf . Glossary defines cylinder, plug, bottom pin, pin-tumbler mechanism and simultaneous alignment by correctly cut key; rotating plug drives tailpiece/drive mechanism.
2. Schlage, Key Systems, Cylinders and Keys catalog, manufacturer glossary: https://commercial.schlage.com/content/dam/allegion-us-2/web-files/schlage/information-documents/Schlage_Key_Systems_Cylinders_and_Keys_Catalog_109487.pdf . Defines bottom pin in direct contact with the key, top pin contacting its spring, body surrounding plug, and cam transferring rotation to bolt mechanism. Technical alternative models and master pins are outside this episode.
3. Lockwiki, Pin tumbler, specialist cross-check and four operating-state diagrams: https://www.lockwiki.com/index.php/Pin_tumbler . Sections Principles of operation and Components establish rest, correct key, rotated plug and incorrect-key states; fixed driver pins/springs in housing, different lower-pin lengths, cam and reset. Raw extraction retained in research-extract.json. No bypass instructions used or included.

## Claim map

| ID | Script / visual assertion | Support and limit |
| --- | --- | --- |
| C1 | Compatible keyway entry alone does not satisfy all pin heights | 1 pin-tumbler definition; 3 incorrect-key state. Says can enter, not that any key fits. |
| C2 | Stationary housing encloses rotating plug and chambers | 1 cylinder/plug; 2 body/plug; 3 operating diagrams. |
| C3 | Conventional chamber has bottom pin, upper pin and spring | 1 mechanism definition; 2 top/bottom pin definitions. Single split per chamber; no master pins. |
| C4 | Key profile lifts paired pins and compresses springs | 1 pin tumbler/key-cut alignment; 2 direct key/spring contacts; 3 component and correct-key sections. Continuous contact path is an original schematic interpretation. |
| C5 | Correct key aligns all pair splits with the shear line; too low and too high both obstruct rotation | 1 simultaneous alignment; 3 principles, historical positive-locking explanation and bad-key diagram. Relative geometry is schematic; no tolerances claimed. |
| C6 | Key, plug and lower pins rotate; upper pins and springs stay housed | 3 components, correct-key rotated state; 1 rotating plug. No longitudinal side view is falsely rotated. |
| C7 | Rear cam transfers rotation; return and withdrawal allow spring reset | 2 cam definition; 3 plug/cam/springs and no-key state. Exact downstream bolt linkage omitted; position of removal identified as this example. |

## Visual provenance and qualifications

All illustrations are original SVG. Five chambers are an illustrative conventional configuration, not a claim about every manufacturer. Geometry is not to scale. Shell removed, vertical section and end-on view are labeled. Time is slowed. Oversized clearances aid visibility; rigid parts remain rigid. Upper and lower pins remain in contact during insertion. Low and high key examples change the matching key profile with the pin height together. No branded product, strength, security guarantee, tolerance or universality claim.

Creative source: board v3 and its canonical frame.md. Manrope / IBM Plex Mono copied with their OFL licenses. Catalog search found generic exploded layers and mechanical shutter transitions, no faithful pin-tumbler mechanism; original mechanical geometry is necessary. BGM and SFX to be resolved for this operating explanation.
