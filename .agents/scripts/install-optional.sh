#!/usr/bin/env bash
set -euo pipefail

# On-demand installer for heavy optional tools not installed during VM boot.
# Usage: bash .agents/scripts/install-optional.sh <blender|rea-video|all>

BLENDER_VERSION="5.2.5"
BLENDER_SERIES="Blender5.2"

usage() {
  cat <<'EOF'
Usage: bash .agents/scripts/install-optional.sh <blender|rea-video|all>

Install heavy optional tools on demand (idempotent, non-interactive):
  blender    Install Blender 5.2.5 LTS (Linux x64) to ~/.local/opt/ and ~/.local/bin/blender
  rea-video  Install rea-video[ocr,asr] and keep opencv-python-headless clean on Python <= 3.12
  all        Install both blender and rea-video
EOF
}

ensure_local_bin_path() {
  mkdir -p "$HOME/.local/bin"
  touch "$HOME/.bashrc"
  sed -i '/case \$- in/,/esac/d' "$HOME/.bashrc" 2>/dev/null || true
  local path_line='export PATH="$HOME/.local/bin:$PATH"'
  grep -qxF "$path_line" "$HOME/.bashrc" || printf '%s\n' "$path_line" >> "$HOME/.bashrc"
}

install_blender() {
  if ! command -v xz >/dev/null 2>&1; then
    sudo apt-get update -qq
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends xz-utils
  fi

  local bl_dir="$HOME/.local/opt/blender-${BLENDER_VERSION}"
  mkdir -p "$HOME/.local/opt" "$HOME/.local/bin"
  if [ ! -x "$bl_dir/blender" ]; then
    local bl_tar
    bl_tar="$(mktemp /tmp/blender-XXXXXX.tar.xz)"
    trap 'rm -f "${bl_tar:-}"' RETURN
    curl -fsSL "https://download.blender.org/release/${BLENDER_SERIES}/blender-${BLENDER_VERSION}-linux-x64.tar.xz" -o "$bl_tar"
    rm -rf "$bl_dir"
    mkdir -p "$bl_dir"
    tar -xJf "$bl_tar" --strip-components=1 -C "$bl_dir"
    rm -f "$bl_tar"
    trap - RETURN
  fi

  ln -sfn "$bl_dir/blender" "$HOME/.local/bin/blender"
  ensure_local_bin_path
  echo "blender ready: $("$HOME/.local/bin/blender" --version | head -n 1)"
}

install_rea_video() {
  if ! command -v ffmpeg >/dev/null 2>&1 || ! command -v ffprobe >/dev/null 2>&1; then
    sudo apt-get update -qq
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ffmpeg
  fi

  if ! command -v rea-video >/dev/null 2>&1; then
    pip install --no-input -q "rea-video[ocr,asr] @ git+https://github.com/JuneYaooo/rea-video"
    if pip show opencv-python >/dev/null 2>&1; then
      pip uninstall -y -q opencv-python
      pip install --no-input -q --force-reinstall --no-deps "opencv-python-headless>=4.8,<5"
    fi
  fi
  echo "rea-video ready: $(command -v rea-video)"
}

if [ "$#" -lt 1 ]; then
  usage >&2
  exit 2
fi

for target in "$@"; do
  case "$target" in
    blender)
      install_blender
      ;;
    rea-video)
      install_rea_video
      ;;
    all)
      install_blender
      install_rea_video
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown target: $target" >&2
      usage >&2
      exit 2
      ;;
  esac
done
