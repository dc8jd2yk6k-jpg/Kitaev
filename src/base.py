"""NarratedScene: beats of voice-over drive the animation timeline.

Each call to ``self.beat()`` starts the next narration line (its audio is
placed at the current scene time) after waiting for the previous line to end.
Animations inside a beat may use ``self.remaining()`` to fill the line.
Actual start times are written to out/timing/<SID>.json for subtitles.
"""
import json
from pathlib import Path

from manim import Scene, config
from .style import BG

ROOT = Path(__file__).resolve().parent.parent
GAP = 0.45
TAIL = 0.8


class NarratedScene(Scene):
    SID = None

    def setup(self):
        # separate TeX cache per scene: parallel renders otherwise race on shared files
        tex = ROOT / "out/tex" / self.SID
        tex.mkdir(parents=True, exist_ok=True)
        config.tex_dir = str(tex)
        self.camera.background_color = BG
        dur = json.loads((ROOT / "out/audio/durations.json").read_text())
        self._beats = dur[self.SID]
        self._i = -1
        self._t0 = 0.0
        self._marks = []

    @property
    def now(self):
        return self.renderer.time

    def remaining(self, gap=GAP):
        if self._i < 0:
            return 0.0
        return max(0.0, self._t0 + self._beats[self._i]["dur"] + gap - self.now)

    def _finish(self):
        r = self.remaining()
        if r > 1.0 / config.frame_rate:
            self.wait(r)

    def beat(self, n=None):
        self._finish()
        self._i += 1
        if n is not None:
            assert n == self._i, f"{self.SID}: expected beat {self._i}, got {n}"
        assert self._i < len(self._beats), f"{self.SID}: ran out of beats"
        self._t0 = self.now
        self._marks.append(self._t0)
        self.add_sound(str(ROOT / self._beats[self._i]["wav"]))

    def fill(self, *anims, lead=0.0, min_t=0.6, **kw):
        """Play animations stretched over the rest of the current beat."""
        rt = max(min_t, self.remaining() - lead)
        self.play(*anims, run_time=rt, **kw)

    def tear_down(self):
        self._finish()
        assert self._i == len(self._beats) - 1, \
            f"{self.SID}: used {self._i + 1} of {len(self._beats)} beats"
        self.wait(TAIL)
        out = ROOT / "out/timing"
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{self.SID}.json").write_text(json.dumps(
            {"marks": self._marks, "end": self.now}))
        super().tear_down()
