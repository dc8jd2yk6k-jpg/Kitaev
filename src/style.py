"""Shared look: palette, typography and the recurring Majorana visuals."""
from manim import *
import numpy as np

BG = "#0b0f17"
INK = "#e8ecf2"
DIM = "#7d8796"
FAINT = "#3a4352"
BLUE_M = "#58C4DD"      # c_{2j-1}
GOLD_M = "#F4C152"      # c_{2j}
PINK_M = "#FF5C8A"      # unpaired Majoranas
GREEN_M = "#7FD17F"
TEAL_M = "#4fd1c5"
PURPLE_M = "#a78bfa"
RED_M = "#FC6255"
ORANGE_M = "#FF9A3C"
SC_COLOR = "#23314a"    # superconductor slab

SERIF = "CMU Serif"
SANS = "CMU Sans Serif"

# colour-coding for MathTex substrings
TEX_COLORS = {
    r"\mu": GREEN_M, r"w": TEAL_M, r"\Delta": ORANGE_M,
    r"b'": PINK_M, r"b''": PINK_M,
}


def T(s, size=36, color=INK, font=SERIF, **kw):
    return Text(s, font=font, font_size=size, color=color, **kw)


def M(*s, size=44, color=INK, **kw):
    return MathTex(*s, font_size=size, color=color, **kw)


def glow_dot(color, radius=0.11, point=ORIGIN, layers=6, strength=0.35):
    """A dot with a soft halo."""
    g = VGroup()
    for i in range(layers, 0, -1):
        r = radius * (1 + 0.55 * i)
        g.add(Circle(radius=r, stroke_width=0, fill_color=color,
                     fill_opacity=strength * (1 - i / (layers + 1)) ** 2 * 0.6))
    core = Circle(radius=radius, stroke_width=0, fill_color=color, fill_opacity=1)
    g.add(core)
    g.move_to(point)
    return g


class Site(VGroup):
    """One physical fermionic site: a capsule holding a blue and a gold Majorana."""

    def __init__(self, width=0.95, height=0.5, dot_r=0.085, glow=True, **kw):
        super().__init__(**kw)
        self.capsule = RoundedRectangle(width=width, height=height,
                                        corner_radius=height / 2,
                                        stroke_color=DIM, stroke_width=2.2,
                                        fill_color="#141b27", fill_opacity=0.85)
        mk = (lambda c: glow_dot(c, dot_r)) if glow else (lambda c: Dot(radius=dot_r, color=c))
        self.blue = mk(BLUE_M).move_to(LEFT * width * 0.24)
        self.gold = mk(GOLD_M).move_to(RIGHT * width * 0.24)
        self.add(self.capsule, self.blue, self.gold)


class Chain(VGroup):
    def __init__(self, L=6, spacing=1.35, **site_kw):
        super().__init__()
        self.sites = VGroup(*[Site(**site_kw) for _ in range(L)])
        self.sites.arrange(RIGHT, buff=spacing - self.sites[0].width)
        self.add(self.sites)
        self.L = L

    def majorana(self, m):
        """Majorana c_m with the paper's 1-based index."""
        j, r = divmod(m - 1, 2)
        s = self.sites[j]
        return s.blue if r == 0 else s.gold

    @property
    def blues(self):
        return VGroup(*[s.blue for s in self.sites])

    @property
    def golds(self):
        return VGroup(*[s.gold for s in self.sites])


def bond(a, b, color=INK, width=6, arc=0.0, opacity=1.0):
    p, q = a.get_center(), b.get_center()
    if arc:
        ln = ArcBetweenPoints(p, q, angle=arc)
    else:
        ln = Line(p, q)
    ln.set_stroke(color, width=width, opacity=opacity)
    return ln


def pair_bonds(chain, pairs, color=INK, width=6, arc=0.0):
    return VGroup(*[bond(chain.majorana(l), chain.majorana(m), color, width, arc)
                    for l, m in pairs])


def chapter_card(num, title):
    n = T(f"Chapter {num}", 30, DIM, font=SANS)
    t = T(title, 60)
    if t.width > 12:
        t.scale_to_fit_width(12)
    g = VGroup(n, t).arrange(DOWN, buff=0.3)
    line = Line(LEFT * 3, RIGHT * 3, stroke_color=BLUE_M, stroke_width=2).next_to(g, DOWN, 0.4)
    return VGroup(g, line)


def paper_ref(eq):
    """Small corner tag pointing back to the paper."""
    return T(f"Kitaev (2000), {eq}", 20, DIM, font=SANS).to_corner(DR, buff=0.3)


def axes(xr, yr, w=6, h=3.5, **kw):
    a = Axes(x_range=xr, y_range=yr, x_length=w, y_length=h,
             axis_config=dict(color=DIM, stroke_width=2, include_tip=False,
                              include_ticks=False), **kw)
    return a
