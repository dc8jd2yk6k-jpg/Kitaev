from manim import *
from src.base import NarratedScene
from src.style import *


class S05Pairing(NarratedScene):
    SID = "s05"

    def construct(self):
        L = 7
        chain = Chain(L=L, spacing=1.6, width=1.05, height=0.56, dot_r=0.1).shift(DOWN * 0.2)
        on = pair_bonds(chain, [(2 * j + 1, 2 * j + 2) for j in range(L)], GREEN_M, 6)
        nb = pair_bonds(chain, [(2 * j + 2, 2 * j + 3) for j in range(L - 1)], TEAL_M, 6)

        # 0 case (a)
        self.beat(0)
        card = chapter_card(4, "Two ways to pair")
        self.play(FadeIn(card, shift=UP * 0.3), run_time=1.0)
        self.wait(0.8)
        self.play(FadeOut(card), run_time=0.6)
        ca = VGroup(T("(a)", 36, GREEN_M), M(r"|\Delta| = w = 0,\quad \mu < 0", size=40)).arrange(RIGHT, buff=0.4)
        ca.to_edge(UP, buff=0.5)
        ha = M(r"H_1 = \frac{i}{2}(-\mu)\sum_j c_{2j-1}c_{2j}", size=40).next_to(ca, DOWN, 0.35)
        self.play(FadeIn(ca), FadeIn(chain), run_time=1.0)
        self.fill(Write(ha), lead=0.2)

        # 1 on-site pairing: trivial
        self.beat(1)
        self.play(LaggedStart(*[Create(b) for b in on], lag_ratio=0.1), run_time=1.6)
        kets = VGroup(*[M(r"|0\rangle", size=32, color=DIM).next_to(s, DOWN, 0.35) for s in chain.sites])
        self.play(LaggedStart(*[FadeIn(k, shift=UP * 0.1) for k in kets], lag_ratio=0.06), run_time=1.2)
        triv = T("every site empty: trivial", 30, DIM).to_edge(DOWN, buff=0.7)
        self.fill(FadeIn(triv), lead=0.2)

        # 2 case (b)
        self.beat(2)
        cb = VGroup(T("(b)", 36, TEAL_M), M(r"|\Delta| = w > 0,\quad \mu = 0", size=40)).arrange(RIGHT, buff=0.4)
        cb.move_to(ca)
        self.play(FadeOut(VGroup(kets, triv, ha)), ReplacementTransform(ca, cb), run_time=1.0)
        self.fill(*[b.animate.set_stroke(opacity=0.12) for b in on], lead=0.2)

        # 3 eq (7): inter-site bonds
        self.beat(3)
        h7 = M(r"H_1 = i w \sum_j c_{2j}\, c_{2j+1}", size=44).next_to(cb, DOWN, 0.35)
        self.play(Write(h7), run_time=1.4)
        self.fill(LaggedStart(*[Create(b) for b in nb], lag_ratio=0.12), FadeOut(on), lead=0.2)

        # 4 slid over by one: compare with fig 2
        self.beat(4)
        ghost = chain.copy().fade(0.75).shift(DOWN * 1.9)
        gon = pair_bonds(ghost, [(2 * j + 1, 2 * j + 2) for j in range(L)], GREEN_M, 4).set_stroke(opacity=0.35)
        shift = M(r"c_m \mapsto c_{m+1}", size=36, color=DIM).next_to(ghost, DOWN, 0.3)
        self.play(FadeIn(ghost), FadeIn(gon), run_time=0.8)
        arrows = VGroup(*[CurvedArrow(gon[j].get_center() + UP * 0.25, nb[j].get_center() + DOWN * 0.25,
                                      angle=-PI / 4, color=DIM, stroke_width=2) for j in range(L - 1)])
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.08), Write(shift), run_time=1.6)
        self.fill(Wait(), lead=0.6)
        self.play(FadeOut(VGroup(ghost, gon, arrows, shift)), run_time=0.6)

        # 5 the unpaired ends
        self.beat(5)
        e1, e2 = chain.majorana(1), chain.majorana(2 * L)
        self.play(e1.animate.set_color(PINK_M).scale(1.7), e2.animate.set_color(PINK_M).scale(1.7), run_time=1.2)
        l1 = M(r"b' = c_1", size=38, color=PINK_M).next_to(e1, DOWN, 0.55)
        l2 = M(r"b'' = c_{2L}", size=38, color=PINK_M).next_to(e2, DOWN, 0.55)
        self.play(Write(l1), Write(l2), run_time=1.2)
        un = T("unpaired!", 34, PINK_M).to_edge(DOWN, buff=0.6)
        self.fill(FadeIn(un, scale=1.2), lead=0.2)

        # 6 new fermions across sites
        self.beat(6)
        self.play(FadeOut(un), run_time=0.4)
        caps = VGroup()
        for j in range(L - 1):
            a, b = chain.majorana(2 * j + 2), chain.majorana(2 * j + 3)
            c = DashedVMobject(RoundedRectangle(width=np.linalg.norm(b.get_center() - a.get_center()) + 0.5,
                                                height=0.62, corner_radius=0.31).set_stroke(TEAL_M, 2),
                               num_dashes=26).move_to((a.get_center() + b.get_center()) / 2)
            caps.add(c)
        self.play(LaggedStart(*[Create(c) for c in caps], lag_ratio=0.08), run_time=1.6)
        at = M(r"\tilde a_j = \tfrac12\left(c_{2j} + i\,c_{2j+1}\right)", size=38).next_to(chain, UP, 0.8)
        self.play(FadeOut(h7), FadeOut(cb), Write(at), run_time=1.4)
        hh = M(r"H_1 = 2w\sum_{j=1}^{L-1}\left(\tilde a_j^\dagger \tilde a_j - \tfrac12\right)", size=38).next_to(at, UP, 0.3)
        hh.shift(DOWN * 0.0)
        self.fill(Write(hh), lead=0.2)

        # 7 two degenerate ground states, eq (8)
        self.beat(7)
        world = VGroup(chain, nb, caps, l1, l2)
        self.play(FadeOut(VGroup(at, hh)), world.animate.scale(0.62).to_edge(UP, buff=0.9), run_time=1.2)
        ax = Line(DOWN * 2.6, UP * 0.6, color=DIM).shift(LEFT * 5.6)
        elab = M("E", size=34, color=DIM).next_to(ax, UP, 0.1)
        g0 = Line(LEFT * 0.9, RIGHT * 0.9, color=PINK_M, stroke_width=6).shift(LEFT * 3.9 + DOWN * 2.2)
        g1 = g0.copy().shift(RIGHT * 2.3)
        ex = Line(LEFT * 2.05, RIGHT * 2.05, color=TEAL_M, stroke_width=4).shift(LEFT * 2.75 + UP * 0.2)
        ex_l = M(r"2w", size=34, color=TEAL_M).next_to(ex, RIGHT, 0.3)
        k0 = M(r"|\psi_0\rangle", size=40).next_to(g0, DOWN, 0.2)
        k1 = M(r"|\psi_1\rangle", size=40).next_to(g1, DOWN, 0.2)
        self.play(Create(ax), FadeIn(elab), Create(ex), FadeIn(ex_l), run_time=1.0)
        self.play(Create(g0), Create(g1), Write(k0), Write(k1), run_time=1.4)
        e8 = VGroup(M(r"-i b' b''\,|\psi_0\rangle = +|\psi_0\rangle", size=36),
                    M(r"-i b' b''\,|\psi_1\rangle = -|\psi_1\rangle", size=36)).arrange(DOWN, aligned_edge=LEFT)
        e8.shift(RIGHT * 3.4 + DOWN * 1.6)
        self.fill(Write(e8), lead=0.2)

        # 8 parity, eq (9)
        self.beat(8)
        p9 = M(r"P = \prod_j \left(-i\,c_{2j-1}c_{2j}\right)", size=38).next_to(e8, UP, 0.5)
        ev = T("even", 26, GREEN_M).next_to(k0, DOWN, 0.15)
        od = T("odd", 26, ORANGE_M).next_to(k1, DOWN, 0.15)
        self.play(Write(p9), run_time=1.4)
        self.fill(FadeIn(ev), FadeIn(od), lead=0.2)

        # 9 bulk identical: relabel
        self.beat(9)
        self.play(FadeOut(VGroup(ax, elab, g0, g1, ex, ex_l, k0, k1, e8, p9, ev, od, world)), run_time=0.8)
        def strip(n=14, pairs_shift=0, color=GREEN_M):
            dots = VGroup()
            for k in range(2 * n):
                dots.add(glow_dot(BLUE_M if k % 2 == 0 else GOLD_M, 0.08))
            dots.arrange(RIGHT, buff=0.38)
            bonds = VGroup(*[bond(dots[k], dots[k + 1], color, 4)
                             for k in range(pairs_shift, 2 * n - 1, 2)])
            return VGroup(bonds, dots)
        sa = strip().shift(UP * 1.0)
        sbb = strip(pairs_shift=1, color=TEAL_M).shift(DOWN * 1.0)
        fade_l = Rectangle(width=2.5, height=5, stroke_width=0, fill_color=BG, fill_opacity=1).to_edge(LEFT, buff=0)
        fade_r = fade_l.copy().to_edge(RIGHT, buff=0)
        fade_l.set_fill(opacity=0.9)
        fade_r.set_fill(opacity=0.9)
        la = T("(a)", 30, GREEN_M).next_to(sa, LEFT, 0.3).shift(RIGHT * 2.4)
        lb = T("(b)", 30, TEAL_M).next_to(sbb, LEFT, 0.3).shift(RIGHT * 2.4)
        self.play(FadeIn(sa), FadeIn(sbb), FadeIn(fade_l), FadeIn(fade_r), run_time=1.0)
        self.add(la, lb)
        self.play(sa[0].animate.shift(RIGHT * (sa[1][1].get_x() - sa[1][0].get_x())), run_time=1.8)
        same = T("same bulk", 32).shift(DOWN * 2.6)
        self.fill(FadeIn(same), lead=0.2)

        # 10 cannot cut a site in half
        self.beat(10)
        self.play(FadeOut(VGroup(sa, sbb, fade_l, fade_r, la, lb, same)), run_time=0.7)
        s = Site(width=2.6, height=1.3, dot_r=0.2)
        cut = DashedLine(UP * 1.2, DOWN * 1.2, color=RED_M, dash_length=0.12)
        self.play(FadeIn(s), run_time=0.8)
        self.play(Create(cut), run_time=0.8)
        x = Cross(s, stroke_color=RED_M, stroke_width=8).scale(0.8)
        self.play(Create(x), run_time=0.6)
        q = T("“one can not cut a physical site into two halves”", 32).shift(DOWN * 2.2)
        self.fill(FadeIn(q, shift=UP * 0.2), lead=0.3)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
