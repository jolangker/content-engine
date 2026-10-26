# Retained replay resources

Read this only when replaying an existing production that directly reads these files. New authoring follows the current [HyperFrames contract](../SKILL.md) and [motion guidance](motion.md).

`productions/coba-hal-baru-berdua/animate.py` reads the core worker, explainer delta, SVG path rule, and spring entrance rule at their original paths. Their linked rule dependencies are retained too. These seven files are historical text inputs, preserved byte for byte; process names in their prose do not activate removed workflows or override current project policy.

| Retained input | Reason |
| --- | --- |
| [Core frame worker](frame-worker-core.md) | Direct script input |
| [Explainer worker delta](../../faceless-explainer/sub-agents/frame-worker.md) | Direct script input |
| [SVG path draw](../../hyperframes-animation/rules/svg-path-draw.md) | Direct script input |
| [Spring entrance](../../hyperframes-animation/rules/spring-pop-entrance.md) | Direct script input |
| [Press-release spring](../../hyperframes-animation/rules/press-release-spring.md) | Linked rule dependency |
| [Press reaction](../../hyperframes-animation/rules/physics-press-reaction.md) | Linked rule dependency |
| [Sine-wave loop](../../hyperframes-animation/rules/sine-wave-loop.md) | Linked rule dependency |

No standalone legacy workflow is installed. The retained folders have no skill entry points. Caption marker recipes and the audio-data extraction helper now live with their consumers in `media-use/audio/`.
