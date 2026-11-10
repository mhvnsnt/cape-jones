# cape-jones devcontainer image: Python 3.11 + pinned Blender 4.5.12 LTS.
# Blender pin: docs/research/RENDER-2026-OPTIMAL.md — "Why Blender 4.5 (not 4.0.2,
# not 5.x)": LTS until July 2027, denoising_use_gpu requires 4.2+, SHA-256
# verified official build. URL verified live 2026-10-16 (HTTP 200).
FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm

ARG BLENDER_VERSION=4.5.12
ARG BLENDER_URL=https://download.blender.org/release/Blender4.5/blender-4.5.12-linux-x64.tar.xz

# Headless Blender system deps (official linux-x64 tarball, no X server needed for -b).
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 \
        libxi6 \
        libxrender1 \
        libxfixes3 \
        libxkbcommon0 \
        libsm6 \
        libxxf86vm1 \
        xz-utils \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install Blender to /opt and expose on PATH.
RUN curl -fsSL "${BLENDER_URL}" -o /tmp/blender.tar.xz \
    && tar -xJf /tmp/blender.tar.xz -C /opt \
    && rm /tmp/blender.tar.xz \
    && ln -s /opt/blender-${BLENDER_VERSION}-linux-x64/blender /usr/local/bin/blender \
    && blender --version

# Blender's bundled python sits at:
#   /opt/blender-4.5.12-linux-x64/4.5/python/bin/python3.11
# Point .vscode/settings.json python.defaultInterpreterPath here if you want
# the interpreter that ships with Blender; keep the system python for repo tooling.
