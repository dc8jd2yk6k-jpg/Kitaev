from manim import *
from src.base import NarratedScene
from src.style import *


def slab(width=10, depth=1.6, height=0.7, skew=0.9):
    """A pseudo-3D superconducting slab (like fig. 1 of the paper)."""
    top = Polygon([-width / 2, 0, 0], [width / 2, 0, 0], [width / 2 + skew, depth * 0.5, 0],
                  [-width / 2 + skew, depth * 0.5, 0],
                  fill_color="#2e4366", fill_opacity=1, stroke_color="#6d87b3", stroke_width=2)
    front = Polygon([-width / 2, 0, 0], [width / 2, 0, 0], [width / 2, -height, 0], [-width / 2, -height, 0],
                    fill_color=SC_COLOR, fill_opacity=1, stroke_color="#6d87b3", stroke_width=2)
    side = Polygon([width / 2, 0, 0], [width / 2 + skew, depth * 0.5, 0], [width / 2 + skew, depth * 0.5 - height, 0],
                   [width / 2, -height, 0], fill_color="#1b2639", fill_opacity=1, stroke_color="#6d87b3",
                   stroke_width=2)
    return VGroup(front, side, top)


class S04Chain(NarratedScene):
    SID = "s04"

    def construct(self):
        # 0 wire on a superconductor
        self.beat(0)
        card = chapter_card(3, "A toy model")
        self.play(FadeIn(card, shift=UP * 0.3), run_time=1.0)
        self.wait(0.8)
        self.play(FadeOut(card), run_time=0.6)
        sc = slab().shift(DOWN * 1.2)
        th = M(r"\theta", size=40, color=BLUE_M).move_to(sc[0])
        sclab = T("3D superconductor", 24, "#9fb3d6").next_to(sc, DOWN, 0.25)
        y = sc[2].get_center()[1]
        chain = Chain(L=8, spacing=1.05, width=0.8, height=0.42, dot_r=0.07)
        chain.move_to([0.45, y + 0.05, 0])
        for s in chain.sites:
            s.remove(s.blue, s.gold)
        self.play(FadeIn(sc, shift=UP * 0.3), Write(th), FadeIn(sclab), run_time=1.4)
        self.play(LaggedStart(*[FadeIn(s.capsule, shift=DOWN * 0.3) for s in chain.sites], lag_ratio=0.1),
                  run_time=1.4)
        Ll = BraceLabel(chain, r"L \text{ sites}", UP, font_size=36)
        self.fill(FadeIn(Ll), lead=0.3)

        # 1 U(1) -> Z2
        self.beat(1)
        circ = Circle(radius=0.9, stroke_color=DIM, stroke_width=3).shift(UP * 2.0 + LEFT * 4.3)
        u1 = M(r"U(1):\ a_j \mapsto e^{i\phi}a_j", size=34).next_to(circ, RIGHT, 0.4)
        ph = ValueTracker(0)
        pt = always_redraw(lambda: Dot(circ.point_at_angle(ph.get_value()), color=GOLD_M, radius=0.1))
        self.play(FadeOut(Ll), Create(circ), Write(u1), run_time=1.2)
        self.add(pt)
        self.play(ph.animate.set_value(2 * PI), run_time=1.8, rate_func=linear)
        z2pts = VGroup(Dot(circ.point_at_angle(0), color=GOLD_M, radius=0.12),
                       Dot(circ.point_at_angle(PI), color=GOLD_M, radius=0.12))
        z2 = M(r"\mathbb{Z}_2:\ a_j \mapsto -a_j", size=34).move_to(u1, aligned_edge=LEFT)
        self.remove(pt)
        self.play(FadeOut(circ), FadeIn(z2pts), TransformMatchingShapes(u1, z2), run_time=1.4)
        why = T("superconductivity", 26, ORANGE_M).next_to(z2, DOWN, 0.2, aligned_edge=LEFT)
        self.fill(FadeIn(why), lead=0.3)

        # 2 one spin species
        self.beat(2)
        arrows = VGroup(*[Arrow(DOWN * 0.25, UP * 0.25, buff=0, color=INK, stroke_width=4,
                                max_tip_length_to_length_ratio=0.35).move_to(s.capsule) for s in chain.sites])
        downs = VGroup(*[Arrow(UP * 0.25, DOWN * 0.25, buff=0, color=RED_M, stroke_width=4,
                               max_tip_length_to_length_ratio=0.35).move_to(s.capsule).shift(UP * 0.75)
                         for s in chain.sites])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.08), run_time=1.2)
        self.play(FadeIn(downs), run_time=0.6)
        crosses = VGroup(*[Cross(d, stroke_color=RED_M, stroke_width=4).scale(0.6) for d in downs])
        self.play(Create(crosses), run_time=0.8)
        foot = T("footnote 1: needs triplet (p-wave) pairing in the substrate", 22, DIM).to_edge(DOWN, buff=0.25)
        self.fill(FadeIn(foot), FadeOut(downs), FadeOut(crosses), lead=0.3)

        # 3 Hamiltonian: hopping w
        self.beat(3)
        self.play(FadeOut(VGroup(z2pts, z2, why, foot, arrows)), run_time=0.6)
        H = M(r"H_1 = \sum_j \Big(", r"-w(a_j^\dagger a_{j+1} + a_{j+1}^\dagger a_j)",
              r"-\mu(a_j^\dagger a_j - \tfrac12)", r"+\Delta a_j a_{j+1} + \Delta^* a_{j+1}^\dagger a_j^\dagger",
              r"\Big)", size=34).to_edge(UP, buff=0.6)
        H[1].set_color(TEAL_M)
        H[2].set_color(GREEN_M)
        H[3].set_color(ORANGE_M)
        for k in (1, 2, 3):
            H[k].set_opacity(0.15)
        self.play(Write(H), run_time=1.6)
        self.play(H[1].animate.set_opacity(1), run_time=0.6)
        e = glow_dot("#8ab6ff", 0.13).move_to(chain.sites[2].capsule)
        self.play(FadeIn(e, scale=0.3), run_time=0.4)
        for k in (3, 4, 5):
            self.play(e.animate(path_arc=-PI / 2).move_to(chain.sites[k].capsule), run_time=0.5)
        self.fill(e.animate(path_arc=PI / 2).move_to(chain.sites[2].capsule), lead=0.2)

        # 4 chemical potential
        self.beat(4)
        self.play(H[2].animate.set_opacity(1), run_time=0.6)
        glow = VGroup(*[s.capsule.copy().set_stroke(GREEN_M, 5) for s in chain.sites])
        mu_lab = M(r"\mu", color=GREEN_M, size=40).next_to(sclab, DOWN, 0.3)
        self.play(LaggedStart(*[Create(g) for g in glow], lag_ratio=0.06), FadeIn(mu_lab), run_time=1.4)
        self.fill(FadeOut(glow), lead=0.2)

        # 5 pairing
        self.beat(5)
        self.play(H[3].animate.set_opacity(1), FadeOut(mu_lab), run_time=0.6)
        pair = VGroup(glow_dot("#8ab6ff", 0.13), glow_dot("#8ab6ff", 0.13))
        pair[0].move_to(chain.sites[5].capsule)
        pair[1].move_to(chain.sites[6].capsule)
        sp = Line(pair[0].get_center(), pair[1].get_center(), color=ORANGE_M, stroke_width=4)
        self.play(FadeIn(pair, scale=0.2), Create(sp), run_time=0.9)
        self.play(FadeOut(pair, scale=0.2), FadeOut(sp), run_time=0.7)
        self.play(FadeIn(pair, scale=0.2), Create(sp), run_time=0.7)
        brk = M(r"\Delta = |\Delta| e^{i\theta}", size=36, color=ORANGE_M).next_to(sclab, DOWN, 0.3)
        self.fill(Write(brk), FadeOut(pair), FadeOut(sp), FadeOut(e), lead=0.2)

        # 6 rewrite in Majoranas: each site splits
        self.beat(6)
        self.play(FadeOut(VGroup(sc, th, sclab, brk)), chain.animate.move_to(DOWN * 0.3).scale(1.25), run_time=1.2)
        for s in chain.sites:
            s.blue.move_to(s.capsule.get_center() + LEFT * s.capsule.width * 0.24)
            s.gold.move_to(s.capsule.get_center() + RIGHT * s.capsule.width * 0.24)
            s.blue.scale(1.25)
            s.gold.scale(1.25)
            s.add(s.blue, s.gold)
        self.play(*[GrowFromCenter(s.blue) for s in chain.sites], *[GrowFromCenter(s.gold) for s in chain.sites],
                  run_time=1.2)
        H6 = M(r"H_1 = \frac{i}{2}\sum_j \Big(", r"-\mu\, c_{2j-1}c_{2j}", r"+ (w+|\Delta|)\, c_{2j}c_{2j+1}",
               r"+ (-w+|\Delta|)\, c_{2j-1}c_{2j+2}", r"\Big)", size=34).to_edge(UP, buff=0.6)
        H6[1].set_color(GREEN_M)
        H6[2].set_color(TEAL_M)
        H6[3].set_color(ORANGE_M)
        lbl = VGroup(M("c_1", size=30, color=BLUE_M).next_to(chain.majorana(1), DOWN, 0.35),
                     M("c_2", size=30, color=GOLD_M).next_to(chain.majorana(2), DOWN, 0.35),
                     M("c_3", size=30, color=BLUE_M).next_to(chain.majorana(3), DOWN, 0.35),
                     M("c_4", size=30, color=GOLD_M).next_to(chain.majorana(4), DOWN, 0.35))
        self.play(TransformMatchingShapes(H, H6), FadeIn(lbl), run_time=1.6)
        self.fill(Wait(), lead=0.1)

        # 7 the three kinds of bonds
        self.beat(7)
        L = chain.L
        on = pair_bonds(chain, [(2 * j + 1, 2 * j + 2) for j in range(L)], GREEN_M, 5)
        gb = pair_bonds(chain, [(2 * j + 2, 2 * j + 3) for j in range(L - 1)], TEAL_M, 5)
        bg = pair_bonds(chain, [(2 * j + 1, 2 * j + 4) for j in range(L - 1)], ORANGE_M, 4, arc=-PI / 2.5)
        self.play(Indicate(H6[1], color=GREEN_M), LaggedStart(*[Create(b) for b in on], lag_ratio=0.05), run_time=1.6)
        self.play(Indicate(H6[2], color=TEAL_M), LaggedStart(*[Create(b) for b in gb], lag_ratio=0.05), run_time=1.8)
        self.play(Indicate(H6[3], color=ORANGE_M), LaggedStart(*[Create(b) for b in bg], lag_ratio=0.05), run_time=1.8)
        legend = VGroup(
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=GREEN_M, stroke_width=5), M(r"-\mu", size=30)).arrange(RIGHT),
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=TEAL_M, stroke_width=5), M(r"w+|\Delta|", size=30)).arrange(RIGHT),
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=ORANGE_M, stroke_width=5), M(r"|\Delta|-w", size=30)).arrange(RIGHT),
        ).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.7)
        self.fill(FadeIn(legend), lead=0.2)

        # 8 two special cases
        self.beat(8)
        cases = VGroup(VGroup(T("(a)  only", 30), M(r"-\mu", size=34, color=GREEN_M)).arrange(RIGHT, buff=0.2),
                       VGroup(T("(b)  only", 30), M(r"w+|\Delta|", size=34, color=TEAL_M)).arrange(RIGHT, buff=0.2)
                       ).arrange(RIGHT, buff=1.5)
        cases.next_to(legend, UP, 0.5)
        self.play(FadeIn(cases), run_time=1.0)
        self.fill(Wait(), lead=0.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
