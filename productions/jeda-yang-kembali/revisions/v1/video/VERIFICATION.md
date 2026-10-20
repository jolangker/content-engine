# Verification — final look v1

HyperFrames 0.8.176; 1080×1920/30 fps; automation authorization. Rendering completed in 111.7 seconds, drawElement capture, hardware Intel Iris Xe GPU. Four screenshot ground-truth comparisons passed.

Final check: zero lint, runtime, layout, motion or contrast findings. Root-level motion assertions target each headline and both actors; 42 assertions across 300 motion samples pass. Dense transition/layout pass also found no runtime/layout issues. All 14 scene proofs inspected; full-size opening 30s frames and refined labels inspected before rendering. No unchanged check was repeated after export.

The entire encoded audiovisual file decodes with FFmpeg -xerror. All 14 representative encoded frames match their preview frames (SSIM >= 0.998615). Original narration 84.64s, 187 words in exact alignment order, 0.4s preroll, total 86.266667s. Forty-five caption phrases contain spoken words only. Native gain +3dB and true-peak ceiling -3dBTP, measured encoded stereo -16.56 LUFS / -2.63dBTP, mono -19.56 LUFS. No speed change, no provider substitution.

Persistent preview was exposed and HTTP 200 verified. The computer-use connector had no browser/app surface, so no interactive realtime preview listen is claimed. Technical runtime, motion, complete decode, measured audio and encoded pixel evidence are the agent verification basis.

Export details and hash: ../exports/verification.json. Draft identity, exact caption, media and settings: ../PUBLISHING.json. All required delivery links exist. Local fonts and licenses included; original audio preserved.
