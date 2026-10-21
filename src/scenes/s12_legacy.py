from manim import *
from src.base import NarratedScene, ROOT
from src.style import *
from src.scenes.s04_chain import slab


def page(n, h=6.4):
    im = ImageMobject(str(ROOT / "assets" / f"page-{n:02d}.png"))
    im.height = h
    return im


class S12Legacy(NarratedScene):
    SID = "s12"

    def construct(self):
        # 0 the paper
        self.beat(0)
        pages = Group(*[page(n, 5.2) for n in (1, 4, 5, 14)])
        for k, p in enumerate(pages):
            p.shift(LEFT * 4.8 + RIGHT * 3.2 * k + DOWN * 0.1).rotate((k - 1.5) * 0.04)
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.4) for p in pages], lag_ratio=0.25), run_time=2.4)
        quote = T("“a simple but rather unrealistic model”", 34, INK)
        qbg = Rectangle(width=quote.width + 0.6, height=quote.height + 0.4, stroke_width=0, fill_color=BG, fill_opacity=0.92).move_to(quote)
        q = Group(qbg, quote).to_edge(DOWN, buff=0.5)
        self.fill(FadeIn(q, shift=UP * 0.2), lead=0.2)

        # 1 nanowires
        self.beat(1)
        self.play(FadeOut(pages), FadeOut(q), run_time=0.8)
        sc = slab(width=8, depth=1.4, height=0.6, skew=0.8).shift(DOWN * 0.4 + LEFT * 1.6)
        nw = RoundedRectangle(width=6.4, height=0.28, corner_radius=0.14, fill_color="#9aa7b8",
                              fill_opacity=1, stroke_width=0).move_to(sc[2]).shift(UP * 0.12)
        sclab = T("superconductor", 22, "#9fb3d6").next_to(sc, DOWN, 0.2)
        nwlab = T("semiconductor nanowire (strong spin-orbit)", 22, INK).next_to(nw, UP, 0.35)
        B = Arrow(LEFT * 0.9, RIGHT * 0.9, color=ORANGE_M).next_to(nwlab, UP, 0.3)
        Bl = M(r"\vec B", size=32, color=ORANGE_M).next_to(B, RIGHT, 0.1)
        self.play(FadeIn(sc, shift=UP * 0.2), FadeIn(sclab), run_time=1.0)
        self.play(FadeIn(nw), FadeIn(nwlab), run_time=1.0)
        self.play(GrowArrow(B), FadeIn(Bl), run_time=0.8)
        ends = VGroup(glow_dot(PINK_M, 0.1).move_to(nw.get_left() + RIGHT * 0.2),
                      glow_dot(PINK_M, 0.1).move_to(nw.get_right() + LEFT * 0.2))
        self.play(FadeIn(ends, scale=0.3), run_time=0.8)
        ax = axes([-1, 1, 0.5], [0, 1.2, 0.5], w=3.0, h=2.2).shift(RIGHT * 4.9 + DOWN * 0.6)
        peak = ax.plot(lambda v: 0.25 + 0.75 * np.exp(-(v / 0.08) ** 2), x_range=[-1, 1, 0.01], color=PINK_M, stroke_width=4)
        xl = M("V", size=26, color=DIM).next_to(ax.x_axis, RIGHT, 0.1)
        yl = M("dI/dV", size=26, color=DIM).next_to(ax.y_axis, UP, 0.1)
        zl = T("zero-bias peak (schematic)", 20, DIM).next_to(ax, DOWN, 0.2)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.8)
        self.fill(Create(peak), FadeIn(zl), lead=0.2)

        # 2 topological qubits
        self.beat(2)
        self.play(FadeOut(VGroup(sc, nw, sclab, nwlab, B, Bl, ends, ax, peak, xl, yl, zl)), run_time=0.8)
        tq = T("topological qubits", 56, INK)
        sub = T("one of the most ambitious routes to a quantum computer", 28, DIM).next_to(tq, DOWN, 0.35)
        self.play(Write(tq), run_time=1.4)
        self.fill(FadeIn(sub), lead=0.2)

        # 3 recap: split
        self.beat(3)
        self.play(FadeOut(VGroup(tq, sub)), run_time=0.6)
        rec = T("Recap", 30, DIM).to_corner(UL, buff=0.5)
        e = Circle(radius=0.6, fill_color="#3c63a3", fill_opacity=1, stroke_color=WHITE, stroke_width=2).shift(UP * 0.6)
        self.play(FadeIn(rec), FadeIn(e), run_time=0.6)
        lft = Sector(radius=0.6, angle=PI, start_angle=PI / 2, fill_color=BLUE_M, fill_opacity=1, stroke_width=0).shift(UP * 0.6)
        rgt = Sector(radius=0.6, angle=PI, start_angle=-PI / 2, fill_color=GOLD_M, fill_opacity=1, stroke_width=0).shift(UP * 0.6)
        self.play(ReplacementTransform(e, VGroup(lft, rgt)), run_time=0.6)
        items = VGroup(T("1.  split every electron into two Majoranas", 30),
                       T("2.  pair them across sites, not within them", 30),
                       T("3.  two halves stranded at the ends share one protected qubit", 30),
                       T("4.  decided by one sign hidden in the bulk", 30)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.45)
        r1, r2, r3, r4 = items
        self.fill(lft.animate.shift(LEFT * 0.5), rgt.animate.shift(RIGHT * 0.5), FadeIn(r1), lead=0.2)

        # 4 pair across sites
        self.beat(4)
        L = 7
        ch = Chain(L=L, spacing=1.35, width=0.9, height=0.48, dot_r=0.08).shift(UP * 0.6)
        on = pair_bonds(ch, [(2 * j + 1, 2 * j + 2) for j in range(L)], GREEN_M, 5)
        nb = pair_bonds(ch, [(2 * j + 2, 2 * j + 3) for j in range(L - 1)], TEAL_M, 5)
        self.play(FadeOut(VGroup(lft, rgt)), FadeIn(ch), FadeIn(on), run_time=0.8)
        self.play(*[ReplacementTransform(on[j], nb[j]) for j in range(L - 1)], FadeOut(on[-1]), FadeIn(r2), run_time=1.4)
        self.fill(Wait(), lead=0.1)

        # 5 stranded ends
        self.beat(5)
        a, b = ch.majorana(1), ch.majorana(2 * L)
        self.play(a.animate.set_color(PINK_M).scale(1.6), b.animate.set_color(PINK_M).scale(1.6), run_time=0.8)
        arc = DashedVMobject(ArcBetweenPoints(a.get_center() + UP * 0.3, b.get_center() + UP * 0.3, angle=-PI / 3.5)
                             .set_stroke(PINK_M, 3), num_dashes=60)
        self.fill(Create(arc), FadeIn(r3), lead=0.2)

        # 6 the invariant
        self.beat(6)
        inv = M(r"\mathcal{M} = \operatorname{sgn}\operatorname{Pf}\tilde B(0)\,\operatorname{sgn}\operatorname{Pf}\tilde B(\pi) = -1",
                size=40, color=PINK_M).next_to(arc, UP, 0.2)
        self.play(Write(inv), FadeIn(r4), run_time=1.8)
        self.fill(Wait(), lead=0.1)

        # 7 closing
        self.beat(7)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        f1 = T("Protection, not from engineering,", 46)
        f2 = T("but from topology.", 46, PINK_M)
        fg = VGroup(f1, f2).arrange(DOWN, buff=0.25).shift(UP * 0.6)
        self.play(Write(fg), run_time=2.2)
        cred = VGroup(
            T("Based on A. Yu. Kitaev, “Unpaired Majorana fermions in quantum wires”,", 22, DIM),
            T("arXiv:cond-mat/0010440 (2000); Physics-Uspekhi 44, 131 (2001)", 22, DIM),
            T("Animated with Manim · voice: Kokoro TTS · all plots computed from the model", 20, FAINT),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.6)
        self.fill(FadeIn(cred), lead=0.0)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)
