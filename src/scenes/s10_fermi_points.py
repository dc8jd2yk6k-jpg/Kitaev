from manim import *
from src.base import NarratedScene
from src.style import *
from src.physics import normal_band


class S10FermiPoints(NarratedScene):
    SID = "s10"

    def construct(self):
        w = 1.0
        mu = ValueTracker(0.6)
        h = ValueTracker(0.0)      # Zeeman splitting
        dup = ValueTracker(0.0)    # show second spin band

        # 0 the normal band
        self.beat(0)
        card = chapter_card(9, "Count the Fermi points")
        self.play(FadeIn(card, shift=UP * 0.3), run_time=1.0)
        self.wait(0.6)
        self.play(FadeOut(card), run_time=0.6)
        ax = axes([-PI, PI, PI / 2], [-4.4, 4.4, 1], w=7.0, h=4.8).shift(LEFT * 2.2 + DOWN * 0.7)
        half = Rectangle(width=ax.c2p(PI, 0)[0] - ax.c2p(0, 0)[0], height=4.8, stroke_width=0,
                         fill_color=BLUE_M, fill_opacity=0.08).move_to(ax.c2p(PI / 2, 0))
        ticks = VGroup(M(r"-\pi", size=26, color=DIM).next_to(ax.c2p(-PI, 0), DOWN, 0.15),
                       M("0", size=26, color=DIM).next_to(ax.c2p(0, 0), DL, 0.08),
                       M(r"\pi", size=26, color=DIM).next_to(ax.c2p(PI, 0), DOWN, 0.15))
        yl = M(r"\epsilon_0(q)", size=30, color=DIM).next_to(ax.y_axis, UP, 0.1)
        eq = M(r"\epsilon_0(q) = -2w\cos q - \mu", size=38).to_edge(UP, buff=0.5)

        def band(shift, color):
            return ax.plot(lambda q: normal_band(q, mu.get_value(), w) + shift, x_range=[-PI, PI, 0.02],
                           color=color, stroke_width=5)
        b_up = always_redraw(lambda: band(-h.get_value(), BLUE_M))
        b_dn = always_redraw(lambda: band(h.get_value(), GOLD_M).set_stroke(opacity=dup.get_value()))

        def fpoints():
            g = VGroup()
            for sh, col, op in ((-h.get_value(), BLUE_M, 1.0), (h.get_value(), GOLD_M, dup.get_value())):
                if op < 0.05:
                    continue
                c = -(mu.get_value() - sh) / (2 * w)
                if abs(c) < 1:
                    q = np.arccos(c)
                    g.add(Dot(ax.c2p(q, 0), color=col, radius=0.1).set_opacity(op))
            return g
        fp = always_redraw(fpoints)

        def counter():
            n = len(fpoints())
            par = "odd" if n % 2 else "even"
            col = PINK_M if n % 2 else DIM
            return VGroup(T(f"Fermi points in [0, π]: {n}", 28), T(par, 34, col)).arrange(DOWN, buff=0.2).move_to(RIGHT * 4.6 + UP * 0.3)
        cnt = always_redraw(counter)
        self.play(Write(eq), run_time=1.2)
        self.play(Create(ax), FadeIn(ticks), FadeIn(yl), run_time=1.0)
        self.add(b_up)
        self.fill(Create(b_up), lead=0.2)

        # 1 eq (28)
        self.beat(1)
        e28 = M(r"\mathcal{M}(H_0) = (-1)^{\nu(\pi) - \nu(0)}", size=42, color=PINK_M).next_to(eq, DOWN, 0.25)
        self.play(Write(e28), run_time=1.8)
        self.fill(FadeIn(half), lead=0.2)

        # 2 count: one
        self.beat(2)
        self.add(fp)
        self.play(FadeIn(fp), run_time=0.6)
        self.add(cnt)
        self.play(FadeIn(cnt), run_time=0.8)
        self.fill(Flash(fp[0], color=PINK_M) if len(fp) else Wait(), lead=0.2)

        # 3 lower until no crossing
        self.beat(3)
        self.fill(mu.animate.set_value(2.6), lead=0.3)

        # 4 spin: doubled bands
        self.beat(4)
        self.play(mu.animate.set_value(0.6), run_time=1.6)
        self.add(b_dn)
        self.play(dup.animate.set_value(1.0), h.animate.set_value(0.04), run_time=1.4)
        legend = VGroup(T("spin ↑", 24, BLUE_M), T("spin ↓", 24, GOLD_M)).arrange(DOWN, aligned_edge=LEFT)
        legend.move_to(RIGHT * 4.6 + DOWN * 1.6)
        self.fill(FadeIn(legend), lead=0.2)

        # 5 lift the degeneracy
        self.beat(5)
        self.play(h.animate.set_value(0.9), mu.animate.set_value(1.2), run_time=3.0)
        tr = T("needs broken time reversal", 26, ORANGE_M).next_to(legend, DOWN, 0.4)
        so = T("(spin-orbit alone won't do)", 22, DIM).next_to(tr, DOWN, 0.12)
        self.fill(FadeIn(tr), FadeIn(so), lead=0.2)

        # 6 Kitaev's speculation: field + CDW
        self.beat(6)
        cdw = VGroup(T("Kitaev's idea:", 24, DIM), T("magnetic field +", 26), T("charge-density wave", 26)).arrange(DOWN, buff=0.08).next_to(so, DOWN, 0.35)
        self.play(FadeIn(cdw), run_time=1.0)
        self.fill(Wait(), lead=0.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
