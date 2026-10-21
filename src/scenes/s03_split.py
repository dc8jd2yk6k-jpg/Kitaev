from manim import *
from src.base import NarratedScene
from src.style import *


class S03Split(NarratedScene):
    SID = "s03"

    def construct(self):
        # 0 a and a-dagger
        self.beat(0)
        card = chapter_card(2, "Splitting a fermion in two")
        self.play(FadeIn(card, shift=UP * 0.3), run_time=1.0)
        self.wait(1.2)
        self.play(FadeOut(card), run_time=0.6)
        box = RoundedRectangle(width=1.6, height=1.6, corner_radius=0.3, stroke_color=DIM,
                               stroke_width=2.5, fill_color="#141b27", fill_opacity=0.9).shift(LEFT * 4.5)
        ops = VGroup(M("a", size=60), M(r"a^\dagger", size=60)).arrange(RIGHT, buff=1.2).shift(RIGHT * 1)
        la = T("annihilate", 24, DIM).next_to(ops[0], DOWN, 0.3)
        lb = T("create", 24, DIM).next_to(ops[1], DOWN, 0.3)
        self.play(FadeIn(box), run_time=0.6)
        self.fill(Write(ops), FadeIn(la), FadeIn(lb), lead=0.2)

        # 1 complex-number analogy, eq (1)
        self.beat(1)
        plane = ComplexPlane(x_range=[-0.5, 2.5], y_range=[-0.5, 2.0], x_length=3.6, y_length=2.6,
                             background_line_style={"stroke_color": FAINT, "stroke_width": 1},
                             axis_config={"stroke_color": DIM}).shift(LEFT * 3.6 + UP * 0.8)
        z = plane.n2p(2 + 1.5j)
        o = plane.n2p(0)
        zv = Arrow(o, z, buff=0, color=INK, stroke_width=5)
        xv = Arrow(o, plane.n2p(2), buff=0, color=BLUE_M, stroke_width=6)
        yv = Arrow(plane.n2p(2), z, buff=0, color=GOLD_M, stroke_width=6)
        zl = M("z = x + iy", size=36).next_to(plane, DOWN, 0.2)
        zl[0][2].set_color(BLUE_M)
        zl[0][5].set_color(GOLD_M)
        self.play(FadeOut(VGroup(box, la, lb)), ops.animate.scale(0.8).to_edge(UP, buff=0.5).shift(RIGHT * 2.5),
                  Create(plane), run_time=1.2)
        self.play(GrowArrow(zv), Write(zl), run_time=1.0)
        self.play(TransformFromCopy(zv, xv), TransformFromCopy(zv, yv), run_time=1.2)
        eq1 = M(r"c_1", r"=", r"a + a^\dagger", size=54).shift(RIGHT * 2.8 + UP * 0.9)
        eq2 = M(r"c_2", r"=", r"{a - a^\dagger \over i}", size=54).next_to(eq1, DOWN, 0.6, aligned_edge=LEFT)
        eq1[0].set_color(BLUE_M)
        eq2[0].set_color(GOLD_M)
        self.play(Write(eq1), run_time=1.2)
        self.fill(Write(eq2), lead=0.2)

        # 2 properties, eq (2)
        self.beat(2)
        props = VGroup(
            M(r"c_m^\dagger = c_m", size=46),
            M(r"c_m^2 = 1", size=46),
            M(r"c_l c_m + c_m c_l = 2\delta_{lm}", size=46),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).shift(LEFT * 3.4 + DOWN * 1.9)
        tag = T("own antiparticle", 22, PINK_M).next_to(props[0], RIGHT, 0.4)
        self.play(FadeOut(VGroup(plane, zv, xv, yv, zl)), run_time=0.6)
        self.play(VGroup(eq1, eq2).animate.shift(UP * 0.4), Write(props[0]), FadeIn(tag), run_time=1.4)
        self.play(Write(props[1]), run_time=1.0)
        self.fill(Write(props[2]), lead=0.2)

        # 3 inverse: two Majoranas make a fermion
        self.beat(3)
        inv = M(r"a = {", r"c_1", r"+ i", r"c_2", r"\over 2}", size=60).shift(LEFT * 3.3 + UP * 1.0)
        inv[1].set_color(BLUE_M)
        inv[3].set_color(GOLD_M)
        self.play(FadeOut(VGroup(props, tag)), Write(inv), run_time=1.4)
        site = Site(width=2.2, height=1.1, dot_r=0.16).shift(LEFT * 3.3 + DOWN * 1.6)
        self.play(FadeIn(site.capsule), run_time=0.6)
        bdot = site.blue.copy().move_to(inv[1])
        gdot = site.gold.copy().move_to(inv[3])
        self.play(FadeIn(bdot), FadeIn(gdot), run_time=0.4)
        self.play(bdot.animate.move_to(site.blue), gdot.animate.move_to(site.gold), run_time=1.2)
        self.add(site)
        self.remove(bdot, gdot)
        cap = T("2 Majoranas = 1 ordinary fermion", 30).next_to(site, DOWN, 0.4)
        self.fill(FadeIn(cap), lead=0.2)

        # 4 phase error in Majoranas
        self.beat(4)
        pe = M(r"a^\dagger a", r"=", r"\tfrac{1}{2}\big(1 + i\,", r"c_1", r"c_2", r"\big)", size=64).shift(RIGHT * 2.5 + DOWN * 1.4)
        pe[0].set_color(PURPLE_M)
        pe[3].set_color(BLUE_M)
        pe[4].set_color(GOLD_M)
        self.play(VGroup(eq1, eq2).animate.set_opacity(0.35), Write(pe), run_time=2.0)
        self.fill(Circumscribe(VGroup(pe[3], pe[4]), color=PINK_M), lead=0.2)

        # 5 separate the halves onto distant sites
        self.beat(5)
        self.play(FadeOut(VGroup(inv, eq1, eq2, ops, cap)),
                  pe.animate.scale(0.75).to_edge(UP, buff=0.6), run_time=1.0)
        sA = RoundedRectangle(width=1.3, height=0.9, corner_radius=0.45, stroke_color=DIM,
                              fill_opacity=0).shift(LEFT * 4.5 + DOWN * 0.6)
        sB = sA.copy().shift(RIGHT * 9)
        self.play(site.capsule.animate.fade(1),
                  site.blue.animate.move_to(sA), site.gold.animate.move_to(sB),
                  FadeIn(sA), FadeIn(sB), run_time=2.0)
        link = DashedLine(sA.get_right(), sB.get_left(), color=PURPLE_M, dash_length=0.15)
        q = T("interaction needed", 26, PURPLE_M).next_to(link, UP, 0.2)
        self.play(Create(link), FadeIn(q), run_time=1.0)
        x = Cross(Square(0.9), stroke_color=RED_M, stroke_width=8).move_to(link)
        self.fill(Create(x), lead=0.3)

        # 6 lone Majorana cannot appear in H
        self.beat(6)
        self.play(FadeOut(VGroup(link, q, x)), run_time=0.5)
        rule = M(r"H \not\ni ", r"c_m", r"\quad\text{(odd under parity)}", size=44).shift(DOWN * 2.3)
        rule[1].set_color(BLUE_M)
        self.play(Write(rule), run_time=1.6)
        shields = VGroup(*[Circle(radius=0.75, stroke_color=PINK_M, stroke_width=3).move_to(m)
                           for m in (site.blue, site.gold)])
        self.play(*[GrowFromCenter(s) for s in shields], run_time=1.0)
        imm = T("immune to every local error", 34, PINK_M).shift(UP * 1.2)
        self.fill(FadeIn(imm, shift=UP * 0.2), *[s.animate.set_stroke(opacity=0.4) for s in shields], lead=0.3)

        # 7 goal of the paper
        self.beat(7)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        g1 = T("Goal:", 40, BLUE_M)
        g2 = T("a Hamiltonian in which unpaired Majoranas", 40)
        g3 = T("emerge as low-energy degrees of freedom", 40)
        g = VGroup(g1, g2, g3).arrange(DOWN, buff=0.25).shift(UP * 0.5)
        n = T("... even from non-interacting electrons", 30, DIM).next_to(g, DOWN, 0.6)
        self.play(Write(g), run_time=2.4)
        self.fill(FadeIn(n, shift=UP * 0.2), lead=0.3)

        # 8 quadratic H as pairing
        self.beat(8)
        self.play(FadeOut(VGroup(g, n)), run_time=0.6)
        h = M(r"H = \frac{i}{4}\sum_{l,m} A_{lm}\, c_l c_m", size=58).to_edge(UP, buff=0.8)
        self.play(Write(h), run_time=1.6)
        cols = [BLUE_M, GOLD_M] * 5
        dots = VGroup(*[glow_dot(cols[i], 0.11) for i in range(10)]).arrange(RIGHT, buff=0.22).shift(DOWN * 0.4)
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.06), run_time=1.2)
        pa = VGroup(*[bond(dots[2 * k], dots[2 * k + 1], INK, 5) for k in range(5)])
        self.play(LaggedStart(*[Create(b) for b in pa], lag_ratio=0.15), run_time=1.6)
        lab1 = T("all paired", 26, DIM).next_to(dots, DOWN, 0.6)
        self.play(FadeIn(lab1), run_time=0.5)
        pb = VGroup(*[bond(dots[2 * k + 1], dots[2 * k + 2], TEAL_M, 5) for k in range(4)])
        self.play(*[ReplacementTransform(pa[k], pb[k]) for k in range(4)], FadeOut(pa[4]), run_time=1.6)
        self.play(dots[0].animate.set_color(PINK_M).scale(1.5), dots[-1].animate.set_color(PINK_M).scale(1.5),
                  Transform(lab1, T("two left over", 26, PINK_M).next_to(dots, DOWN, 0.6)), run_time=1.0)
        self.fill(Indicate(dots[0], color=PINK_M), Indicate(dots[-1], color=PINK_M), lead=0.3)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
