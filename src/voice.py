"""Synthesize every narration beat with Kokoro (ONNX) and record durations.

    python -m src.voice            # all scenes, cached by text hash
Writes out/audio/<sid>_<i>.wav and out/audio/durations.json.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

from .narration import SCENES, beats

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out/audio"
MODEL = "/opt/tts/kokoro-v1.0.onnx"
VOICES = "/opt/tts/voices-v1.0.bin"
VOICE = "am_michael"
SPEED = 1.06

# espeak mispronounces a few names; give Kokoro the phonemes directly.
LEXICON = {
    "Kitaev's": "kɪtˈɑːjɛfs",
    "Kitaev": "kɪtˈɑːjɛf",
    "Majoranas": "mˌaɪəɹˈɑːnəz",
    "Majorana": "mˌaɪəɹˈɑːnə",
    "Josephson": "dʒˈoʊzəfsən",
}
_pat = re.compile(r"\b(" + "|".join(re.escape(k) for k in LEXICON) + r")(?![\w'])")


def to_phonemes(tok, text):
    parts, pos = [], 0
    for m in _pat.finditer(text):
        if m.start() > pos:
            parts.append(tok.phonemize(text[pos:m.start()]))
        parts.append(LEXICON[m.group(1)])
        pos = m.end()
    if pos < len(text):
        parts.append(tok.phonemize(text[pos:]))
    return " ".join(p for p in parts if p)


def main(only=None):
    from kokoro_onnx import Kokoro
    OUT.mkdir(parents=True, exist_ok=True)
    k = Kokoro(MODEL, VOICES)
    db_path = OUT / "durations.json"
    db = json.loads(db_path.read_text()) if db_path.exists() else {}
    for sid in SCENES:
        if only and sid not in only:
            continue
        entries = []
        for i, b in enumerate(beats(sid)):
            key = hashlib.sha1(f"{VOICE}|{SPEED}|{b['say']}".encode()).hexdigest()[:12]
            wav = OUT / f"{sid}_{i:02d}_{key}.wav"
            if not wav.exists():
                ph = to_phonemes(k.tokenizer, b["say"])
                audio, sr = k.create(ph, voice=VOICE, speed=SPEED, is_phonemes=True)
                # short fades avoid clicks
                n = int(0.01 * sr)
                audio[:n] *= np.linspace(0, 1, n)
                audio[-n:] *= np.linspace(1, 0, n)
                sf.write(wav, audio, sr)
            info = sf.info(wav)
            entries.append({"wav": str(wav.relative_to(ROOT)), "dur": info.duration,
                            "sub": b["sub"]})
        db[sid] = entries
        print(sid, f"{sum(e['dur'] for e in entries):6.1f}s", len(entries), "beats", flush=True)
    db_path.write_text(json.dumps(db, indent=1, ensure_ascii=False))
    total = sum(sum(e["dur"] for e in v) for v in db.values())
    print(f"total narration {total / 60:.1f} min")


if __name__ == "__main__":
    main(sys.argv[1:] or None)
