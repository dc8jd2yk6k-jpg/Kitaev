# Unpaired Majoranas — an animated explainer of Kitaev (2000)

A ~16-minute, 3Blue1Brown-style video explaining A. Yu. Kitaev's
*Unpaired Majorana fermions in quantum wires* (arXiv:cond-mat/0010440),
built with [Manim Community](https://www.manim.community/), a neural voice-over
(Kokoro-82M via `kokoro-onnx`) and a procedurally generated ambient score.

Every curve on screen (band structures, zero-mode wavefunctions, the exponential
splitting, Pfaffian signs) is computed live from the model in `src/physics.py`.

## Chapters

| # | Scene | Paper |
|---|-------|-------|
| – | Cold open: an electron cut in half | abstract |
| 1 | Why quantum memory is fragile (σˣ vs σᶻ, parity) | Intro |
| 2 | Splitting a fermion: Majorana operators | eqs. 1–3 |
| 3 | The toy chain on a superconductor | eqs. 4–6, fig. 1 |
| 4 | Two ways to pair; the unpaired ends | eqs. 7–10, fig. 2 |
| 5 | A qubit with no address | eqs. 8–9 |
| 6 | Bulk gap, phase transition, phase diagram | eq. 13 |
| 7 | Zero modes and exponential splitting | eqs. 14–15 |
| 8 | The Majorana number and Pfaffians | eqs. 17–26, fig. 3 |
| 9 | Counting Fermi points; why spin makes it hard | eq. 28, fig. 4 |
| 10 | The 4π Josephson effect | eqs. 16, 29–30, fig. 5 |
| – | Legacy and recap | |

The full voice-over is in [`script/narration.md`](script/narration.md).

## Layout

```
build.py                 voice → render → assemble (concat, voice track, music, subtitles)
src/narration.py         voice-over, one list of beats per scene
src/voice.py             Kokoro TTS per beat (cached), writes out/audio/durations.json
src/base.py              NarratedScene: beats of narration drive the animation timeline
src/style.py             palette, typography, Majorana/site/chain visuals
src/physics.py           Kitaev chain numerics + self-test (python -m src.physics)
src/scenes/s01…s12_*.py  one Manim scene per chapter
assets/                  four pages of the paper shown in the outro
```

Each scene calls `self.beat()` to start the next line of narration; the scene
waits for the line to finish before moving on, and records when each line
started (`out/timing/`). The assembler places the narration clips at exactly
those times, so picture and voice stay locked regardless of animation lengths.

## Building

Requirements: Python 3.11+, ffmpeg, a TeX Live install with `dvisvgm`,
Cairo/Pango dev headers, `espeak-ng`, and the CMU fonts (`fonts-cmu`).

```bash
python -m venv venv && . venv/bin/activate
pip install manim "pillow<12" kokoro-onnx soundfile scipy
mkdir -p /opt/tts && cd /opt/tts && \
  curl -LO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx && \
  curl -LO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
cd -
python -m src.physics          # sanity-check the numerics
python build.py all -q h       # ≈ 1 h on 4 cores; -q l for a fast 480p preview
```

Output: `final/kitaev_majorana_1080p.mp4` (with an embedded English subtitle
track) and `final/kitaev_majorana.srt`.

## Credits

Physics and figures after A. Yu. Kitaev, *Physics-Uspekhi* **44**, 131 (2001),
arXiv:cond-mat/0010440. Animation, script and code in this repository; voice by
Kokoro-82M (Apache-2.0).
