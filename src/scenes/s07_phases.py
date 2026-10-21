from manim import *
from src.base import NarratedScene
from src.style import *
from src.physics import bulk_spectrum


class S07Phases(NarratedScene):
    SID = "s07"

    def construct(self):
        w = 1.0
        mu = ValueTracker(0.0)
        dl = ValueTracker(1.0)

        # 0 spectrum formula + plot
        self.beat(0)
        card = chapter_card(6, "Gaps and phases")
        self.play(FadeIn(card, shift=UP * 0.3), run_time=1.0)
        self.wait(0.6)
        self.play(FadeOut(card), run_time=0.6)
        eq = M(r"\epsilon(q) = \pm\sqrt{(2", r"w", r"\cos q + ", r"\mu", r")^2 + 4|", r"\Delta", r"|^2\sin^2 q}", size=42)
        eq[1].set_color(TEAL_M)
        eq[3].set_color(GREEN_M)
        eq[5].set_color(ORANGE_M)
        eq.to_edge(UP, buff=0.45)
        ax = axes([-PI, PI, PI / 2], [-5.2, 5.2, 1], w=6.4, h=4.6).shift(LEFT * 2.8 + DOWN * 0.6)
        xl = M("q", size=32, color=DIM).next_to(ax.x_axis, RIGHT, 0.1)
        yl = M(r"\epsilon", size=32, color=DIM).next_to(ax.y_axis, UP, 0.1)
        ticks = VGroup(M(r"-\pi", size=26, color=DIM).next_to(ax.c2p(-PI, 0), DOWN, 0.15),
                       M(r"\pi", size=26, color=DIM).next_to(ax.c2p(PI, 0), DOWN, 0.15))

        def band(sign):
            return always_redraw(lambda: ax.plot(
                lambda q: sign * bulk_spectrum(q, mu.get_value(), w, dl.get_value()),
                x_range=[-PI, PI, 0.02], color=BLUE_M if sign > 0 else GOLD_M, stroke_width=5))

        up, dn = band(1), band(-1)
        self.play(Write(eq), run_time=2.4)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(ticks), run_time=1.0)
        self.add(up, dn)
        self.play(FadeIn(up), FadeIn(dn), run_time=1.0)

        # readouts
        def readout():
            return VGroup(
                M(r"\mu = %.2f" % mu.get_value(), size=36, color=GREEN_M),
                M(r"|\Delta| = %.2f" % dl.get_value(), size=36, color=ORANGE_M),
                M(r"w = 1", size=36, color=TEAL_M),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 4.6 + UP * 1.4)
        ro = always_redraw(readout)
        self.add(ro)
        self.fill(Wait(), lead=0.1)

        # 1 healthy gap
        self.beat(1)

        def gap_brace():
            qs = np.linspace(-PI, PI, 801)
            e = bulk_spectrum(qs, mu.get_value(), w, dl.get_value())
            q0 = qs[np.argmin(e)]
            g = max(e.min(), 0.02)
            return VGroup(DoubleArrow(ax.c2p(q0, -g), ax.c2p(q0, g), buff=0, color=PINK_M,
                                      stroke_width=4, tip_length=0.15, max_tip_length_to_length_ratio=0.3))
        gb = always_redraw(gap_brace)
        gl = T("gap", 28, PINK_M).move_to(ax.c2p(0.6, 0.0) + RIGHT * 0.2)
        self.play(FadeIn(gb), FadeIn(gl), run_time=1.0)
        self.play(dl.animate.set_value(0.6), run_time=2.0)
        self.fill(Wait(), lead=0.1)

        # 2 raise mu
        self.beat(2)
        self.play(FadeOut(gl), run_time=0.3)
        self.fill(mu.animate.set_value(1.5), lead=0.1, rate_func=linear)

        # 3 gap closes at mu = 2w
        self.beat(3)
        self.play(mu.animate.set_value(2.0), run_time=2.0, rate_func=smooth)
        flash = Flash(ax.c2p(PI, 0), color=PINK_M, line_length=0.4, flash_radius=0.3)
        crit = M(r"|\mu| = 2w", size=44, color=PINK_M).move_to(RIGHT * 4.6 + DOWN * 0.8)
        self.play(flash, Write(crit), Flash(ax.c2p(-PI, 0), color=PINK_M, line_length=0.4, flash_radius=0.3),
                  run_time=1.0)
        self.fill(Wait(), lead=0.1)

        # 4 reopens: trivial
        self.beat(4)
        self.play(mu.animate.set_value(3.0), run_time=2.4)
        tl = T("trivial", 34, DIM).move_to(RIGHT * 4.6 + DOWN * 1.8)
        self.fill(FadeIn(tl), lead=0.1)

        # 5 hallmark
        self.beat(5)
        self.play(mu.animate.set_value(0.6), run_time=2.6)
        self.play(mu.animate.set_value(3.0), run_time=2.6)
        hall = T("topological transition = the gap must close", 30, PINK_M).to_edge(DOWN, buff=0.35)
        self.fill(FadeIn(hall), lead=0.1)

        # 6 phase diagram
        self.beat(6)
        self.play(FadeOut(VGroup(crit, tl, hall)), run_time=0.5)
        pd = Axes(x_range=[-4, 4, 1], y_range=[-1.5, 1.5, 0.5], x_length=4.4, y_length=3.0,
                  axis_config=dict(color=DIM, stroke_width=2, include_tip=False, include_ticks=False))
        pd.move_to(RIGHT * 4.2 + DOWN * 1.3)
        topo = Polygon(pd.c2p(-2, -1.5), pd.c2p(2, -1.5), pd.c2p(2, 1.5), pd.c2p(-2, 1.5),
                       stroke_width=0, fill_color=PINK_M, fill_opacity=0.28)
        lab_t = T("Majoranas", 22, PINK_M).move_to(pd.c2p(0, 0.85))
        lab_a = T("trivial", 20, DIM).move_to(pd.c2p(3.05, 0.85))
        lab_b = T("trivial", 20, DIM).move_to(pd.c2p(-3.05, 0.85))
        pdx = M(r"\mu/w", size=26, color=DIM).next_to(pd.x_axis, DOWN, 0.1).shift(RIGHT * 1.9)
        pdy = M(r"\Delta/w", size=26, color=DIM).next_to(pd.y_axis.get_top(), RIGHT, 0.1)
        t2 = VGroup(M(r"-2", size=22, color=DIM).next_to(pd.c2p(-2, -1.5), DOWN, 0.08),
                    M(r"2", size=22, color=DIM).next_to(pd.c2p(2, -1.5), DOWN, 0.08))
        cond = M(r"2|w| > |\mu|,\ \Delta \neq 0", size=34, color=PINK_M).next_to(pd, UP, 0.35)
        dot = always_redraw(lambda: Dot(pd.c2p(mu.get_value(), dl.get_value()), color=WHITE, radius=0.07))
        self.play(FadeOut(ro), run_time=0.3)
        self.play(Create(pd), FadeIn(topo), FadeIn(pdx), FadeIn(pdy), FadeIn(t2), run_time=1.2)
        self.play(FadeIn(lab_t), FadeIn(lab_a), FadeIn(lab_b), Write(cond), run_time=1.2)
        self.add(dot)
        self.play(mu.animate.set_value(-1.0), dl.animate.set_value(-0.8), run_time=2.0)
        self.fill(mu.animate.set_value(1.0), dl.animate.set_value(0.5), lead=0.1)

        # 7 delta = 0: metal
        self.beat(7)
        metal = Line(pd.c2p(-2, 0), pd.c2p(2, 0), color=WHITE, stroke_width=6)
        ml = T("normal metal", 20, WHITE).next_to(metal, DOWN, 0.08).shift(RIGHT * 0.6)
        self.play(Create(metal), FadeIn(ml), run_time=1.0)
        self.play(dl.animate.set_value(0.0), run_time=2.2)
        gapless = T("gapless", 30, WHITE).move_to(ax.c2p(1.6, 4.0))
        self.play(FadeIn(gapless), run_time=0.6)
        self.wait(0.6)
        self.play(dl.animate.set_value(0.15), FadeOut(gapless), run_time=1.6)
        self.fill(Wait(), lead=0.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
