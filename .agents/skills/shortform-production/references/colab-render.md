# Video Rendering Offload Rule (Google Colab CLI)

NEVER run Hyperframes video rendering locally on this VM, as it lacks a GPU and sufficient CPU resources. Whenever a task requires rendering a Hyperframes video, you MUST offload the rendering process to a Google Colab GPU instance using `google-colab-cli`.

## Scope and Workspace Integration

This rule governs every HyperFrames video render on the `antigravity-cloud` branch, including:

- Verification draft proofs (`productions/<slug>/video/verification/proof.mp4`)
- Final delivery exports (`productions/<slug>/exports/<file>.mp4`)
- Board motion previews (`boards/<slug>/motion-preview.mp4`)

Keep the installed upstream HyperFrames skills (`hyperframes`, `hyperframes-cli`, `hyperframes-registry`, and `media-use`) unchanged; pass this rule as run context whenever invoking them so no local `hyperframes render` command runs on the Antigravity VM. Lightweight local checks and inspections (`lint`, `check`, `snapshot`, `dom_lint.py`, `episode_qa.py`, `ffprobe`) continue locally on this VM after downloading the rendered output.

## Execution Workflow

Follow these steps strictly for every render job:

1. **Check Prerequisites:** Ensure `google-colab-cli` is installed (`colab --help`). If missing, install it via `pip install google-colab-cli` or `uv tool install google-colab-cli`.
2. **Provision GPU Runtime:** Start a new Colab session with an L4 GPU (fallback to T4 if L4 is unavailable) using headless auth:
   ```bash
   colab --auth=adc new -s hyperframes-render --gpu L4
   ```
   If an L4 runtime is unavailable, retry with `--gpu T4`.
3. **Upload Project Files:** Upload only the necessary Hyperframes project directory and assets (exclude `node_modules`, `.git`, or large temporary caches) to `/content/project`:
   ```bash
   colab upload -s hyperframes-render ./<PROJECT_DIR> /content/project
   ```
4. **Install Dependencies & Render:** Execute the setup and Hyperframes render command remotely on the Colab VM. Ensure hardware acceleration (GPU/NVENC) is enabled if supported by the render script:
   ```bash
   colab exec -s hyperframes-render -c "cd /content/project && <RENDER_COMMAND>"
   ```
5. **Download Output:** Pull the rendered video file back to the local Antigravity VM:
   ```bash
   colab download -s hyperframes-render /content/project/<OUTPUT_PATH> ./<LOCAL_OUTPUT_PATH>
   ```
6. **Mandatory Teardown:** ALWAYS terminate the Colab session immediately after the download finishes—or if any error occurs—to prevent wasting Compute Units:
   ```bash
   colab stop -s hyperframes-render
   ```

## Safety & Error Handling Rules

- Wrap the workflow in a cleanup guard (e.g., `trap 'colab stop -s hyperframes-render' EXIT` in bash) so the remote VM is guaranteed to shut down even if the render fails.
- Verify that `./<LOCAL_OUTPUT_PATH>` exists and has a non-zero file size before reporting success, then run the required `ffprobe` duration and [quality gate](quality-gate.md) checks locally against the downloaded file.
- If the Colab render fails, fetch the last 50 lines of the error log before stopping the session, then report the root cause.
