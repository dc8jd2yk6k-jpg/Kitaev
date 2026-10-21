"""Build the full video.

    python build.py voice                 # synthesize narration (cached)
    python build.py render [-q l|m|h] [s03 s07 ...]   # render scenes
    python build.py assemble [-q l|m|h]   # concat + music + subtitles
    python build.py all -q h

Run with the venv python (manim, kokoro-onnx, soundfile, scipy).
"""
import argparse
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "out"
FINAL = ROOT / "final"

SCENES = [
    ("s01", "s01_cold_open", "S01ColdOpen"),
    ("s02", "s02_fragile", "S02Fragile"),
    ("s03", "s03_split", "S03Split"),
    ("s04", "s04_chain", "S04Chain"),
    ("s05", "s05_pairing", "S05Pairing"),
    ("s06", "s06_qubit", "S06Qubit"),
    ("s07", "s07_phases", "S07Phases"),
    ("s08", "s08_zero_modes", "S08ZeroModes"),
    ("s09", "s09_majorana_number", "S09MajoranaNumber"),
    ("s10", "s10_fermi_points", "S10FermiPoints"),
    ("s11", "s11_josephson", "S11Josephson"),
    ("s12", "s12_legacy", "S12Legacy"),
]
QUALITY = {"l": ("480p15", "-ql"), "m": ("720p30", "-qm"), "h": ("1080p60", "-qh"),
           "p": ("1440p60", "-qp")}


def scene_video(sid, q):
    _, mod, cls = next(s for s in SCENES if s[0] == sid)
    return OUT / "media/videos" / mod / QUALITY[q][0] / f"{cls}.mp4"


def render_one(sid, q):
    _, mod, cls = next(s for s in SCENES if s[0] == sid)
    log = OUT / "logs" / f"{sid}_{q}.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, "-m", "manim", "render", QUALITY[q][1], "--disable_caching",
           "--media_dir", str(OUT / "media"), "--progress_bar", "none",
           str(ROOT / "src/scenes" / f"{mod}.py"), cls]
    env = dict(os.environ, PYTHONPATH=str(ROOT))
    with open(log, "w") as f:
        r = subprocess.run(cmd, cwd=ROOT, env=env, stdout=f, stderr=subprocess.STDOUT)
    print(f"{sid}: {'ok' if r.returncode == 0 else 'FAILED, see ' + str(log)}", flush=True)
    return r.returncode


def render(q, only, jobs):
    ids = only or [s[0] for s in SCENES]
    with ThreadPoolExecutor(jobs) as ex:
        codes = list(ex.map(lambda s: render_one(s, q), ids))
    if any(codes):
        sys.exit("some scenes failed")


def probe_video_duration(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=duration", "-of", "csv=p=0", str(path)])
    return float(out)


def srt_time(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"


def wrap(text, width=64):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    # subtitles: at most two lines per card
    return ["\n".join(lines[i:i + 2]) for i in range(0, len(lines), 2)]


def make_srt(offsets):
    dur = json.loads((OUT / "audio/durations.json").read_text())
    cues = []
    for sid, off in offsets.items():
        marks = json.loads((OUT / "timing" / f"{sid}.json").read_text())["marks"]
        for t0, b in zip(marks, dur[sid]):
            chunks = wrap(b["sub"])
            weights = np.array([len(c) for c in chunks], float)
            bounds = np.concatenate([[0], np.cumsum(weights / weights.sum())]) * b["dur"]
            for c, a, z in zip(chunks, bounds[:-1], bounds[1:]):
                cues.append((off + t0 + a, off + t0 + z, c))
    lines = []
    for i, (a, z, c) in enumerate(cues, 1):
        lines += [str(i), f"{srt_time(a)} --> {srt_time(z)}", c, ""]
    return "\n".join(lines)


def music_bed(total, sr=48000, seed=7):
    """A slow, quiet ambient pad: drifting chords of soft partials, lightly reverberated."""
    rng = np.random.default_rng(seed)
    n_total = int(total * sr)
    out = np.zeros(n_total)
    # i - VI - III - VII in D minor, very slow
    chords = [[50, 57, 62, 65, 69], [46, 53, 58, 62, 65], [53, 60, 65, 69, 72], [48, 55, 60, 64, 67]]
    seg = 16.0
    for k in range(int(np.ceil(total / seg)) + 1):
        notes = chords[k % len(chords)]
        start = k * seg - 4.0
        i0, i1 = max(0, int(start * sr)), min(n_total, int((start + seg + 8.0) * sr))
        if i1 <= i0:
            continue
        t = np.arange(i0, i1) / sr
        et = t - start
        env = np.sin(np.clip(et / 6.0, 0, 1) * np.clip((seg + 8.0 - et) / 6.0, 0, 1) * np.pi / 2) ** 2
        chunk = np.zeros_like(t)
        for n in notes:
            f = 440 * 2 ** ((n - 69) / 12)
            ph = rng.uniform(0, 2 * np.pi)
            arg = 2 * np.pi * f * t + ph + 0.02 * np.sin(2 * np.pi * 0.13 * t + ph)
            chunk += (np.sin(arg) + 0.3 * np.sin(2 * arg) + 0.12 * np.sin(3 * arg)) / len(notes)
        out[i0:i1] += env * chunk
    for d, g in [(0.113, 0.35), (0.271, 0.28), (0.419, 0.22), (0.733, 0.15)]:
        n = int(d * sr)
        out[n:] += g * out[:-n]
    out /= np.max(np.abs(out)) + 1e-9
    t = np.arange(n_total) / sr
    fade = np.clip(t / 4, 0, 1) * np.clip((total - t) / 6, 0, 1)
    return (out * fade * 0.5).astype(np.float32), sr


def voice_track(offsets, total, sr=48000):
    """Place every narration clip at its recorded beat start (sample accurate)."""
    import soundfile as sf
    from scipy.signal import resample_poly
    dur = json.loads((OUT / "audio/durations.json").read_text())
    out = np.zeros(int(total * sr) + sr, np.float32)
    for sid, off in offsets.items():
        marks = json.loads((OUT / "timing" / f"{sid}.json").read_text())["marks"]
        for t0, b in zip(marks, dur[sid]):
            a, r = sf.read(ROOT / b["wav"], dtype="float32")
            if r != sr:
                a = resample_poly(a, sr, r).astype(np.float32)
            i = int(round((off + t0) * sr))
            out[i:i + len(a)] += a[:len(out) - i]
    out *= 0.9 / max(1e-9, np.abs(out).max())
    return out, sr


def assemble(q):
    import soundfile as sf
    FINAL.mkdir(exist_ok=True)
    work = OUT / "assemble"
    work.mkdir(parents=True, exist_ok=True)
    offsets, t = {}, 0.0
    lst = []
    for sid, _, _ in SCENES:
        v = scene_video(sid, q)
        offsets[sid] = t
        t += probe_video_duration(v)
        lst.append(f"file '{v}'")
    (work / "list.txt").write_text("\n".join(lst))
    total = t
    print(f"total length {total / 60:.2f} min")
    joined = work / f"joined_{q}.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(work / "list.txt"),
                    "-map", "0:v", "-c:v", "copy", str(joined)], check=True)
    voice, sr = voice_track(offsets, total)
    sf.write(work / "voice.wav", voice, sr)
    music, sr = music_bed(total + 1)
    sf.write(work / "music.wav", music, sr)
    srt_path = FINAL / "kitaev_majorana.srt"
    srt_path.write_text(make_srt(offsets))
    name = {"h": "1080p", "m": "720p", "l": "480p", "p": "1440p"}[q]
    final = FINAL / f"kitaev_majorana_{name}.mp4"
    filt = ("[1:a]asplit=2[v1][v2];"
            "[2:a]volume=0.15[m];"
            "[m][v2]sidechaincompress=threshold=0.03:ratio=6:attack=80:release=900[md];"
            "[v1][md]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(joined), "-i", str(work / "voice.wav"),
                    "-i", str(work / "music.wav"), "-i", str(srt_path), "-filter_complex", filt,
                    "-map", "0:v", "-map", "[a]", "-map", "3:s", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-c:s", "mov_text", "-metadata:s:s:0", "language=eng",
                    "-t", f"{total:.3f}", "-movflags", "+faststart", str(final)], check=True)
    print("wrote", final)
    return final


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["voice", "render", "assemble", "all"])
    ap.add_argument("scenes", nargs="*")
    ap.add_argument("-q", default="l", choices=list(QUALITY))
    ap.add_argument("-j", type=int, default=4)
    a = ap.parse_args()
    if a.step in ("voice", "all"):
        subprocess.run([sys.executable, "-m", "src.voice"], cwd=ROOT, check=True)
    if a.step in ("render", "all"):
        render(a.q, a.scenes, a.j)
    if a.step in ("assemble", "all"):
        assemble(a.q)


if __name__ == "__main__":
    main()
