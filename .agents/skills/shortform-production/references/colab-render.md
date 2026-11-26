# Video Rendering Offload Rule (Google Colab CLI)

NEVER run HyperFrames video rendering locally on this VM, as it lacks a GPU and sufficient CPU resources. Whenever a task requires rendering a HyperFrames video, you MUST offload the rendering process to a Google Colab GPU instance using `google-colab-cli`.

## Scope and Workspace Integration

This rule governs every HyperFrames video render on the `antigravity-cloud` branch, including:

- Verification draft proofs (`productions/<slug>/video/verification/proof.mp4`)
- Final delivery exports (`productions/<slug>/exports/<file>.mp4`)
- Board motion previews (`boards/<slug>/motion-preview.mp4`)

Keep the installed upstream HyperFrames skills (`hyperframes`, `hyperframes-cli`, `hyperframes-registry`, and `media-use`) unchanged; pass this rule as run context whenever invoking them so no local `hyperframes render` command runs on the Antigravity VM. Lightweight local checks and inspections (`lint`, `check`, `snapshot`, `dom_lint.py`, `episode_qa.py`, `ffprobe`) continue locally on this VM before and after downloading the rendered output. Keep all composition assets self-contained inside the project folder (`video/` or `motion-preview/`) so the uploaded archive renders cleanly on Colab.

## Authentication Setup (Headless ADC)

`google-colab-cli` requires Application Default Credentials (`--auth=adc`) with four specific scopes for headless agent runs. Mint ADC once on a machine with a browser:

```bash
gcloud auth application-default login \
  --scopes=openid,https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/colaboratory
```

To restore ADC automatically inside Antigravity Cloud VMs, store the base64-encoded file as `GOOGLE_COLAB_ADC_JSON_B64` in Doppler (Linux: `base64 -w 0 ~/.config/gcloud/application_default_credentials.json`; macOS: `base64 -i ~/.config/gcloud/application_default_credentials.json | tr -d '\n'`). Running `fetch_env.py --check` restores `~/.config/gcloud/application_default_credentials.json` (`0600`) and verifies the required `colaboratory` scope via `colab --auth=adc whoami`.

Verify readiness at any time without allocating a billable VM:

```bash
python .agents/skills/shortform-production/scripts/colab_render.py --check
```

## Recommended Wrapper (`colab_render.py`)

Use [colab_render.py](../scripts/colab_render.py) for every HyperFrames render job. It enforces every rule below automatically: prerequisite and ADC preflight, filtered `.tar.gz` packaging (excluding `node_modules`, `.git`, `.hyperframes`, `.env`, caches, and prior outputs), L4 provisioning with T4 fallback, remote Node 22 / HyperFrames / browser setup with automatic `--gpu` (NVENC) and `--browser-gpu` flags when supported, last-50-lines error log retrieval before stop on failure, non-zero output verification, and guaranteed session teardown on exit or signal (`SIGINT`/`SIGTERM`).

```bash
# Verification draft proof
python .agents/skills/shortform-production/scripts/colab_render.py \
  --project productions/<slug>/video \
  --output productions/<slug>/video/verification/proof.mp4 \
  --quality draft

# Final delivery export (pass --fps 24 when building a 1x master for 1.25x retiming)
python .agents/skills/shortform-production/scripts/colab_render.py \
  --project productions/<slug>/video \
  --output productions/<slug>/exports/<file>.mp4 \
  --quality delivery

# Board motion preview
python .agents/skills/shortform-production/scripts/colab_render.py \
  --project boards/<slug>/motion-preview \
  --output boards/<slug>/motion-preview.mp4 \
  --quality delivery
```

Use `--dry-run` to verify archive contents without provisioning a VM, `--extra-arg <flag>` to pass extra `hyperframes render` flags, or `--render-cmd "<cmd>" --remote-output <rel-path>` for custom render scripts.

## Manual Execution Workflow (`google-colab-cli`)

If running `colab` directly without `colab_render.py`, follow these steps strictly. Note three `google-colab-cli` CLI rules:
- Always place `--auth=adc` **before** every subcommand (otherwise `colab` defaults to browser `oauth2`).
- `colab upload LOCAL REMOTE` uploads a **single file** — pack `<PROJECT_DIR>` into a filtered `.tar.gz` archive first.
- `colab exec` runs Python/IPython code (not `-c "<bash>"`) and has a 30-second idle output timeout by default — pass `--timeout 0` and execute shell commands via Python `subprocess.run(..., check=True)` (or `colab --auth=adc ssh -s hyperframes-render -- '<cmd>'` if SSH keys are configured).

1. **Check Prerequisites:** Ensure `google-colab-cli` is installed (`colab --help`) and ADC is valid (`colab --auth=adc whoami`). If missing, install via `uv tool install google-colab-cli` or `pip install google-colab-cli`.
2. **Provision GPU Runtime (with Cleanup Guard):** Wrap the job in a bash cleanup trap and start a Colab session with an L4 GPU (fallback to T4 if L4 is unavailable) using headless auth:
   ```bash
   trap 'colab --auth=adc stop -s hyperframes-render' EXIT
   colab --auth=adc new -s hyperframes-render --gpu L4 || \
     colab --auth=adc new -s hyperframes-render --gpu T4
   ```
3. **Upload Project Files:** Package only the necessary HyperFrames project directory and assets (excluding `node_modules`, `.git`, `.hyperframes`, `.env`, caches, and prior exports) into a `.tar.gz` archive and upload it:
   ```bash
   tar --exclude=node_modules --exclude=.git --exclude=.hyperframes \
       --exclude=.env --exclude=verification --exclude=exports \
       -czf /tmp/project.tar.gz -C ./<PROJECT_DIR> .
   colab --auth=adc upload -s hyperframes-render /tmp/project.tar.gz /content/project.tar.gz
   ```
4. **Install Dependencies & Render:** Extract to `/content/project`, ensure Node 22+, `ffmpeg`, HyperFrames, and Chrome are installed, enable GPU/NVENC flags (`--gpu --browser-gpu`) when available, tee output to `/content/render.log`, and execute the render remotely via `colab --auth=adc exec -s hyperframes-render --timeout 0 -f <runner.py>`.
5. **Download Output:** Pull the rendered video file back to the local Antigravity VM:
   ```bash
   colab --auth=adc download -s hyperframes-render /content/project/<OUTPUT_PATH> ./<LOCAL_OUTPUT_PATH>
   ```
6. **Mandatory Teardown:** ALWAYS terminate the Colab session immediately after the download finishes—or if any error occurs—to prevent wasting Compute Units:
   ```bash
   colab --auth=adc stop -s hyperframes-render
   ```

## Safety & Error Handling Rules

- Wrap every workflow in a cleanup guard (`colab_render.py`'s `finally` + signal handler, or `trap 'colab --auth=adc stop -s hyperframes-render' EXIT` in bash) so the remote VM is guaranteed to shut down even if the render fails or is interrupted.
- Verify that `./<LOCAL_OUTPUT_PATH>` exists and has a non-zero file size before reporting success, then run local `ffprobe` duration and [quality gate](quality-gate.md) checks against the downloaded file.
- If the Colab render fails, fetch the last 50 lines of `/content/render.log` (or `colab --auth=adc log -s hyperframes-render -n 50`) **before** stopping the session, then report the root cause.
