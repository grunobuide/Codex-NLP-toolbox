# ADR 0005 — Demo on Streamlit Community Cloud

**Status:** accepted (2026-07-14)

**Context:** The plan targeted Hugging Face Spaces, but HF deprecated the
native Streamlit SDK for new Spaces and the Docker path required a paid
tier for this account.

**Decision:** Deploy on Streamlit Community Cloud (free, native Streamlit,
auto-redeploys on push to main): https://codex-nlp-toolbox.streamlit.app.
Keep `.github/workflows/hf-space.yml` gated behind the `HF_SPACE` repo
variable in case a Docker Space becomes viable.

**Consequences:** A one-line `requirements.txt` deploy manifest lives in
the repo root (see ADR 0002). The app must keep importing `nlp_toolbox`
from the repo root (no install step on the platform).
