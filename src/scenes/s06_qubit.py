from manim import *
from src.base import NarratedScene
from src.style import *


class S06Qubit(NarratedScene):
    SID = "s06"

    def construct(self):
        L = 9
        chain = Chain(L=L, spacing=1.3, width=0.9, height=0.48, dot_r=0.085).shift(DOWN * 0.4)
        nb = pair_bonds(chain, [(2 * j + 2, 2 * j + 3) for j in range(L - 1)], TEAL_M, 5)
        e1, e2 = chain.majorana(1), chain.majorana(2 * L)
        e1.set_color(PINK_M).scale(1.7)
        e2.set_color(PINK_M).scale(1.7)

        # 0 the qubit
        self.beat(0)
        card = chapter_card(5, "A qubit with no address")
        self.play(FadeIn(card, shift=UP * 0.3), run_time=1.0)
        self.wait(0.8)
        self.play(FadeOut(card), run_time=0.6)
        self.play(FadeIn(chain), FadeIn(nb), run_time=1.0)
        arc = DashedVMobject(ArcBetweenPoints(e1.get_center() + UP * 0.35, e2.get_center() + UP * 0.35,
                                              angle=-PI / 3.5).set_stroke(PINK_M, 3), num_dashes=70)
        f = M(r"f = \tfrac12\left(b' + i\,b''\right)", size=44, color=PINK_M).next_to(arc, UP, 0.15)
        self.play(Create(arc), Write(f), run_time=1.6)
        st = VGroup(M(r"f^\dagger f = 0:\ |\psi_0\rangle", size=36), M(r"f^\dagger f = 1:\ |\psi_1\rangle", size=36)
                    ).arrange(RIGHT, buff=1.2).to_edge(DOWN, buff=0.8)
        self.fill(FadeIn(st), lead=0.2)

        # 1 local noise near one end
        self.beat(1)
        self.play(FadeOut(st), run_time=0.4)
        rng = np.random.default_rng(5)
        zone = Circle(radius=1.1, stroke_color=RED_M, stroke_width=2).move_to(e1).set_fill(RED_M, 0.08)
        self.play(FadeIn(zone), run_time=0.6)
        for _ in range(2):
            sparks = VGroup(*[Dot(radius=0.04, color=RED_M).move_to(e1.get_center() + rng.normal(size=3) * [0.8, 0.8, 0])
                              for _ in range(14)])
            self.play(LaggedStart(*[s.animate(rate_func=there_and_back).move_to(e1) for s in sparks],
                                  lag_ratio=0.05), run_time=1.2)
            self.remove(*sparks)
        only = M(r"b' \text{ alone: odd} \Rightarrow \text{not in } H", size=34, color=RED_M).next_to(zone, DOWN, 0.3)
        only.shift(RIGHT * 1.2)
        self.play(Write(only), run_time=1.4)
        need = M(r"\text{to measure: } -i\,b'b''", size=40).to_edge(DOWN, buff=0.6)
        br = BraceBetweenPoints(e1.get_center() + DOWN * 0.5, e2.get_center() + DOWN * 0.5, DOWN, color=INK)
        self.play(FadeOut(only), FadeOut(zone), run_time=0.5)
        self.fill(GrowFromCenter(br), Write(need.next_to(br, DOWN, 0.2)), lead=0.2)

        # 2 both error types blocked
        self.beat(2)
        self.play(FadeOut(VGroup(br, need, f, arc)), VGroup(chain, nb).animate.shift(UP * 1.4), run_time=0.8)
        rows = VGroup(
            VGroup(M(r"\sigma^x", size=44, color=RED_M), T("bit flip: create/destroy an electron", 28),
                   T("parity forbids", 28, GREEN_M)),
            VGroup(M(r"\sigma^z", size=44, color=PURPLE_M), T("phase error: needs b' and b'' to talk", 28),
                   M(r"\propto e^{-L/l_0}", size=40, color=GREEN_M)),
        )
        for r in rows:
            r.arrange(RIGHT, buff=0.5)
        rows.arrange(DOWN, buff=0.6, aligned_edge=LEFT).shift(DOWN * 1.3)
        self.play(FadeIn(rows[0][:2]), run_time=1.0)
        self.play(FadeIn(rows[0][2], shift=LEFT * 0.2), run_time=0.8)
        self.wait(0.6)
        self.play(FadeIn(rows[1][:2]), run_time=1.0)
        self.fill(FadeIn(rows[1][2], shift=LEFT * 0.2), lead=0.2)

        # 3 geometry
        self.beat(3)
        g = T("protected by geometry, not by correction", 38, PINK_M).to_edge(UP, buff=0.6)
        self.play(Write(g), run_time=1.6)
        quote = T("“intrinsically immune to decoherence”  (abstract)", 26, DIM).next_to(g, DOWN, 0.25)
        self.fill(FadeIn(quote), lead=0.3)

        # 4 but fine tuned?
        self.beat(4)
        self.play(FadeOut(VGroup(rows, g, quote)), run_time=0.6)
        q = M(r"w \neq |\Delta|\ ?\qquad \mu \neq 0\ ?", size=56).shift(DOWN * 1.6)
        self.play(Write(q), run_time=1.4)
        self.fill(Wiggle(VGroup(chain, nb), scale_value=1.03, rotation_angle=0.02 * TAU), lead=0.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
