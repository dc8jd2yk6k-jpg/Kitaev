from manim import *
from src.base import NarratedScene
from src.style import *


class Bloch(VGroup):
    """A 2D drawing of a Bloch sphere with a state arrow given by (theta, phi)."""

    def __init__(self, r=1.6, **kw):
        super().__init__(**kw)
        self.r = r
        self.sphere = Circle(radius=r, stroke_color=DIM, stroke_width=2)
        self.equator = Ellipse(width=2 * r, height=0.55 * r, stroke_color=FAINT, stroke_width=2)
        self.back = DashedVMobject(Ellipse(width=2 * r, height=0.55 * r).set_stroke(FAINT, 2),
                                   num_dashes=40)
        self.axis = DashedLine(UP * r * 1.15, DOWN * r * 1.15, color=FAINT, dash_length=0.08)
        self.k0 = M(r"|0\rangle", size=40).next_to(UP * r, UP, 0.15)
        self.k1 = M(r"|1\rangle", size=40).next_to(DOWN * r, DOWN, 0.15)
        self.th = ValueTracker(0.0)
        self.ph = ValueTracker(0.0)
        self.arrow = always_redraw(lambda: Arrow(
            self.get_center(), self.point(self.th.get_value(), self.ph.get_value()),
            buff=0, color=GOLD_M, stroke_width=6, max_tip_length_to_length_ratio=0.15))
        self.add(self.sphere, self.equator, self.axis, self.k0, self.k1)

    def point(self, th, ph):
        r = self.r
        x = r * np.sin(th) * np.cos(ph)
        y = r * np.cos(th) - 0.275 * r * np.sin(th) * np.sin(ph)
        return self.get_center() + np.array([x, y, 0])


def site_box(full=False, w=1.3, h=1.3):
    box = RoundedRectangle(width=w, height=h, corner_radius=0.25, stroke_color=DIM,
                           stroke_width=2.5, fill_color="#141b27", fill_opacity=0.9)
    g = VGroup(box)
    if full:
        g.add(glow_dot("#8ab6ff", 0.18).move_to(box))
    return g


class S02Fragile(NarratedScene):
    SID = "s02"

    def construct(self):
        # 0 chapter
        self.beat(0)
        card = chapter_card(1, "Why quantum memory is fragile")
        self.play(FadeIn(card, shift=UP * 0.3), run_time=1.2)
        self.fill(Wait(), lead=0.6)
        self.play(FadeOut(card), run_time=0.6)

        # 1 qubit on the Bloch sphere
        self.beat(1)
        b = Bloch().shift(LEFT * 3.2)
        self.play(Create(b), run_time=1.2)
        self.add(b.arrow)
        state = M(r"|\psi\rangle = \alpha|0\rangle + \beta|1\rangle", size=46).shift(RIGHT * 2.6 + UP * 1.5)
        self.play(Write(state), run_time=1.2)
        self.play(b.th.animate.set_value(1.0), b.ph.animate.set_value(0.6), run_time=1.5)
        self.fill(b.th.animate.set_value(0.7), lead=0.2)

        # 2 bit flip
        self.beat(2)
        sx = M(r"\sigma^x", r":\ |0\rangle \leftrightarrow |1\rangle", size=46).shift(RIGHT * 2.6 + UP * 0.2)
        sx[0].set_color(RED_M)
        lab = T("classical error", 28, RED_M).next_to(sx, DOWN, 0.2)
        self.play(Write(sx), FadeIn(lab), run_time=1.2)
        self.play(b.th.animate.set_value(PI - 0.7), run_time=1.6)
        self.fill(Indicate(b.k1, color=RED_M), lead=0.2)

        # 3 phase flip
        self.beat(3)
        sz = M(r"\sigma^z", r":\ \alpha|0\rangle + \beta|1\rangle \mapsto \alpha|0\rangle", r"-", r"\beta|1\rangle",
               size=40).shift(RIGHT * 2.6 + DOWN * 1.4)
        sz[0].set_color(PURPLE_M)
        sz[2].set_color(PURPLE_M)
        lab2 = T("phase error", 28, PURPLE_M).next_to(sz, DOWN, 0.2)
        self.play(b.th.animate.set_value(PI / 2), run_time=1.0)
        self.play(Write(sz), FadeIn(lab2), run_time=1.6)
        self.play(b.ph.animate.set_value(0.6 + PI), run_time=2.2)
        self.fill(Indicate(sz[2], color=PURPLE_M, scale_factor=1.6), lead=0.2)

        # 4 threshold
        self.beat(4)
        self.play(FadeOut(VGroup(b, state, sx, lab, sz, lab2)), FadeOut(b.arrow), run_time=0.8)
        n = 100
        side = 4.6
        cell = side / n
        bgsq = Square(side, stroke_width=0, fill_color="#283c56", fill_opacity=1)
        grid = VGroup(*[Line(bgsq.get_corner(DL) + RIGHT * k * cell, bgsq.get_corner(UL) + RIGHT * k * cell)
                        for k in range(1, n)],
                      *[Line(bgsq.get_corner(DL) + UP * k * cell, bgsq.get_corner(DR) + UP * k * cell)
                        for k in range(1, n)]).set_stroke("#0b0f17", 0.6)
        bad = Square(cell, stroke_width=0, fill_color=RED_M, fill_opacity=1).move_to(
            bgsq.get_corner(UL) + np.array([61.5, -37.5, 0]) * cell)
        img = VGroup(bgsq, grid, bad).shift(LEFT * 2.5)
        cap = M(r"p_{\text{gate}} \lesssim 10^{-4}", size=60).shift(RIGHT * 3 + UP * 0.6)
        cap2 = T("one failure in ten thousand", 30, DIM).next_to(cap, DOWN, 0.35)
        cap3 = T("(fault-tolerance threshold, ~2000)", 24, DIM).next_to(cap2, DOWN, 0.2)
        self.play(FadeIn(img, scale=0.9), run_time=1.2)
        ring = Circle(radius=0.15, color=RED_M, stroke_width=4).move_to(bad)
        self.play(Write(cap), Create(ring), run_time=1.4)
        self.fill(FadeIn(cap2), FadeIn(cap3), lead=0.3)

        # 5 question
        self.beat(5)
        self.play(FadeOut(VGroup(img, ring, cap, cap2, cap3)), run_time=0.8)
        q = T("Can the physics itself do the protecting?", 48)
        self.fill(Write(q), lead=0.4)

        # 6 fermionic sites
        self.beat(6)
        self.play(q.animate.scale(0.6).to_edge(UP, buff=0.4).set_color(DIM), run_time=0.8)
        empty = site_box(False).shift(LEFT * 2)
        full = site_box(True).shift(RIGHT * 2)
        k0 = M(r"|0\rangle", size=48).next_to(empty, DOWN, 0.35)
        k1 = M(r"|1\rangle", size=48).next_to(full, DOWN, 0.35)
        t0 = T("empty", 28, DIM).next_to(empty, UP, 0.3)
        t1 = T("one electron", 28, DIM).next_to(full, UP, 0.3)
        self.play(FadeIn(empty), FadeIn(full), run_time=1.0)
        self.fill(Write(k0), Write(k1), FadeIn(t0), FadeIn(t1), lead=0.2)

        # 7 bit flip = creating an electron: forbidden
        self.beat(7)
        ghost = glow_dot("#8ab6ff", 0.18).move_to(empty)
        self.play(FadeIn(ghost, scale=0.2), run_time=0.9)
        x = Cross(empty, stroke_color=RED_M, stroke_width=8).scale(0.7)
        self.play(Create(x), run_time=0.6)
        self.play(FadeOut(ghost), run_time=0.5)
        rule = M(r"\text{charge conserved}\quad\Rightarrow\quad \sigma^x_j \text{ impossible}", size=36).shift(DOWN * 2.2)
        rule2 = M(r"\text{superconductor: parity } (-1)^{N} \text{ still conserved}", size=34).next_to(rule, DOWN, 0.25)
        rule2.set_color(DIM)
        self.play(Write(rule), run_time=1.6)
        self.fill(FadeIn(rule2), lead=0.3)

        # 8 hopping loophole, killed by distance + gap
        self.beat(8)
        self.play(FadeOut(VGroup(x, rule, rule2)), run_time=0.5)
        dot = full[1]
        path = ArcBetweenPoints(full.get_center(), empty.get_center(), angle=PI / 3)
        self.play(MoveAlongPath(dot, path), run_time=1.2)
        self.play(MoveAlongPath(dot, path.copy().reverse_direction()), run_time=1.0)
        gap = Rectangle(width=5.5, height=1.4, stroke_width=0, fill_color=SC_COLOR, fill_opacity=0.8)
        gl = T("energy gap", 26, BLUE_M).move_to(gap)
        self.play(VGroup(empty, k0, t0).animate.shift(LEFT * 2.6),
                  VGroup(full, k1, t1).animate.shift(RIGHT * 2.6), run_time=1.3)
        self.play(FadeIn(gap), FadeIn(gl), run_time=0.8)
        tunnel = DashedVMobject(ArcBetweenPoints(full.get_center(), empty.get_center(), angle=PI / 4)
                                .set_stroke(RED_M, 3), num_dashes=30)
        self.play(Create(tunnel), run_time=0.8)
        self.fill(tunnel.animate.set_stroke(opacity=0.1), lead=0.2)

        # 9 phase errors survive
        self.beat(9)
        self.play(FadeOut(VGroup(gap, gl, tunnel, q)), run_time=0.5)

        def dial(center, rate):
            c = Circle(radius=0.45, stroke_color=DIM, stroke_width=2).move_to(center)
            hand = Line(center, center + UP * 0.4, color=PURPLE_M, stroke_width=5)
            hand.add_updater(lambda m, dt: m.rotate(-rate * dt, about_point=center))
            return VGroup(c, hand)

        d0 = dial(empty.get_center() + DOWN * 2.0 + DOWN * 0.15, 1.0)
        d1 = dial(full.get_center() + DOWN * 2.0 + DOWN * 0.15, 2.6)
        self.play(VGroup(k0, k1).animate.shift(UP * 0.0), FadeIn(d0), FadeIn(d1), run_time=0.8)
        e = M(r"a_j^\dagger a_j", size=72, color=PURPLE_M).shift(UP * 0.1)
        el = T("\"is site j full?\"  =  a phase error", 30, PURPLE_M).next_to(e, DOWN, 0.3)
        self.play(Write(e), run_time=1.2)
        self.play(FadeIn(el), run_time=0.8)
        self.fill(Wait(), lead=0.8)
        d0[1].clear_updaters()
        d1[1].clear_updaters()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
