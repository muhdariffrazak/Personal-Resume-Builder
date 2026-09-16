# Build-only toolchain image: pandoc + LaTeX + fonts + the Python deps needed
# by scripts/build.py. No repo content is baked in — the repo is mounted as a
# volume at build/run time (see Makefile), so this image only needs rebuilding
# when the toolchain itself changes.
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    pandoc \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    fonts-crosextra-caladea \
    fonts-crosextra-carlito \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pyyaml jinja2

WORKDIR /work
