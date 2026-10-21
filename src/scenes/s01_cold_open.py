from manim import *
from src.base import NarratedScene
from src.style import *


def half_disc(color, side, r=0.9):
    start = PI / 2 if side == "left" else -PI / 2
    s = Sector(radius=r, angle=PI, start_angle=start,
               fill_color=color, fill_opacity=0.95, stroke_width=0)
    return s


def halo(r, color, n=8, op=0.08):
    return VGroup(*[Circle(radius=r * (1 + 0.12 * i), stroke_width=0,
                           fill_color=color, fill_opacity=op * (1 - i / n))
                    for i in range(n)])


class S01ColdOpen(NarratedScene):
    SID = "s01"

    def construct(self):
        # 0: an electron
        self.beat(0)
        e_halo = halo(0.9, "#9ecbff")
        e_core = Circle(radius=0.9, stroke_color=WHITE, stroke_width=2,
                        fill_color="#2b4a7a", fill_opacity=1)
        e_core.set_sheen_direction(UL).set_fill(color=["#8ab6ff", "#24406d"])
        e_lab = M(r"e^-", size=60)
        electron = VGroup(e_halo, e_core, e_lab)
        self.play(FadeIn(electron, scale=0.6), run_time=1.5)
        self.play(electron.animate.scale(1.05), rate_func=there_and_back, run_time=0.8)
        cut = DashedLine(UP * 1.6, DOWN * 1.6, dash_length=0.12, color=INK)
        self.fill(Create(cut), lead=0.2)

        # 1: two Majorana halves
        self.beat(1)
        left = half_disc(BLUE_M, "left")
        right = half_disc(GOLD_M, "right")
        self.play(FadeOut(e_lab), FadeOut(e_halo), FadeOut(cut),
                  ReplacementTransform(e_core, VGroup(left, right)), run_time=1.0)
        self.play(left.animate.shift(LEFT * 1.2), right.animate.shift(RIGHT * 1.2), run_time=1.4)
        l1 = M("c_1", color=BLUE_M, size=56).next_to(left, DOWN, 0.4)
        l2 = M("c_2", color=GOLD_M, size=56).next_to(right, DOWN, 0.4)
        name = T("Majorana fermions", 44).to_edge(UP, buff=1.0)
        self.play(Write(l1), Write(l2), FadeIn(name, shift=DOWN * 0.3), run_time=1.5)
        sub = T("each one is its own antiparticle", 28, DIM).next_to(name, DOWN, 0.25)
        self.fill(FadeIn(sub), lead=0.3)

        # 2: glued together on one atom ... then a wire
        self.beat(2)
        site = Site(width=1.6, height=0.85, dot_r=0.14)
        site.scale(1.2)
        self.play(FadeOut(VGroup(l1, l2, name, sub)),
                  left.animate.scale(0.16).move_to(site.blue),
                  right.animate.scale(0.16).move_to(site.gold), run_time=1.4)
        self.play(FadeIn(site.capsule), FadeIn(site.blue), FadeIn(site.gold),
                  FadeOut(left), FadeOut(right), run_time=0.8)
        tag = T("A. Yu. Kitaev, 2000", 30, DIM).to_edge(UP, buff=0.8)
        chain = Chain(L=10, spacing=1.25)
        chain.move_to(ORIGIN)
        intra = pair_bonds(chain, [(2 * j + 1, 2 * j + 2) for j in range(10)], INK, 5)
        self.play(ReplacementTransform(site, chain.sites[4]), FadeIn(tag), run_time=1.2)
        others = VGroup(*[s for i, s in enumerate(chain.sites) if i != 4])
        self.play(LaggedStart(*[FadeIn(s, scale=0.6) for s in others], lag_ratio=0.08),
                  run_time=1.6)
        self.fill(LaggedStart(*[Create(b) for b in intra], lag_ratio=0.06), lead=0.2)

        # 3: bonds shift, ends come unstuck
        self.beat(3)
        inter = pair_bonds(chain, [(2 * j + 2, 2 * j + 3) for j in range(9)], TEAL_M, 5)
        self.play(*[ReplacementTransform(intra[j], inter[j]) for j in range(9)],
                  FadeOut(intra[9]), run_time=1.8)
        ends = VGroup(chain.majorana(1), chain.majorana(20))
        self.play(*[e.animate.set_color(PINK_M).scale(1.6) for e in ends], run_time=1.0)
        arc = ArcBetweenPoints(ends[0].get_center() + UP * 0.3, ends[1].get_center() + UP * 0.3,
                               angle=-PI / 3.2)
        arc = DashedVMobject(arc.set_stroke(PINK_M, 3), num_dashes=60)
        lab = T("one fermion, split between the ends", 28, PINK_M).next_to(arc, UP, 0.15)
        self.fill(Create(arc), FadeIn(lab, shift=DOWN * 0.2), lead=0.2)

        # 4: noise can't touch it
        self.beat(4)
        rng = np.random.default_rng(3)
        noise = VGroup()
        for _ in range(26):
            x = rng.uniform(-4.5, 4.5)
            d = Dot(radius=0.05, color=RED_M).move_to([x, rng.uniform(-3.6, -2.2), 0])
            noise.add(d)
        self.play(LaggedStart(*[d.animate(rate_func=there_and_back).shift(UP * rng.uniform(1.4, 2.0))
                                for d in noise], lag_ratio=0.05), run_time=3.0)
        self.play(*[Indicate(e, color=PINK_M, scale_factor=1.4) for e in ends], run_time=1.2)
        self.fill(FadeOut(noise), lead=0.2)

        # 5: title card
        self.beat(5)
        world = VGroup(chain, inter, arc, lab, tag)
        self.play(world.animate.scale(0.55).to_edge(DOWN, buff=0.8).fade(0.5), run_time=1.2)
        title = T("Unpaired Majorana fermions", 64)
        title2 = T("in quantum wires", 64)
        tt = VGroup(title, title2).arrange(DOWN, buff=0.2).shift(UP * 1.2)
        by = T("Alexei Yu. Kitaev  ·  cond-mat/0010440  ·  October 2000", 26, DIM).next_to(tt, DOWN, 0.5)
        self.play(Write(tt), run_time=2.0)
        self.fill(FadeIn(by, shift=UP * 0.2), lead=0.0)
        self.wait(1.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
