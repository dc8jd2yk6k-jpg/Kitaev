from manim import *
from src.base import NarratedScene
from src.style import *


def ring(n, r, center, start=PI / 2, gap=0.0):
    """Majorana dots evenly placed on a circle (optionally with an opening)."""
    g = VGroup()
    angs = np.linspace(start + gap / 2, start + TAU - gap / 2, 2 * n, endpoint=gap == 0 and False or True)
    if gap == 0:
        angs = np.linspace(start, start + TAU, 2 * n, endpoint=False)
    for k, a in enumerate(angs):
        g.add(glow_dot(BLUE_M if k % 2 == 0 else GOLD_M, 0.07).move_to(center + r * np.array([np.cos(a), np.sin(a), 0])))
    return g


class S09MajoranaNumber(NarratedScene):
    SID = "s09"

    def construct(self):
        # 0 question
        self.beat(0)
        card = chapter_card(8, "The Majorana number")
        self.play(FadeIn(card, shift=UP * 0.3), run_time=1.0)
        self.wait(0.8)
        self.play(FadeOut(card), run_time=0.6)
        q = T("Any gapped 1D superconductor:", 40)
        q2 = T("unpaired Majoranas, or not?", 40, PINK_M)
        qq = VGroup(q, q2).arrange(DOWN, buff=0.25)
        self.fill(Write(qq), lead=0.3)

        # 1 definition, multiplicativity
        self.beat(1)
        self.play(qq.animate.scale(0.6).to_edge(UP, buff=0.3).set_opacity(0.5), run_time=0.8)
        dfn = M(r"\mathcal{M}(H) = ", r"\begin{cases} -1 & \text{unpaired Majoranas} \\ +1 & \text{none}\end{cases}", size=40)
        dfn.shift(UP * 1.2)
        self.play(Write(dfn), run_time=2.0)
        c1 = Chain(L=5, spacing=0.75, width=0.55, height=0.3, dot_r=0.05).shift(DOWN * 0.9)
        c2 = c1.copy().shift(DOWN * 0.9)
        for c in (c1, c2):
            for j in range(4):
                c.add(bond(c.majorana(2 * j + 2), c.majorana(2 * j + 3), TEAL_M, 3))
            c.majorana(1).set_color(PINK_M)
            c.majorana(10).set_color(PINK_M)
        VGroup(c1, c2).shift(LEFT * 3)
        self.play(FadeIn(c1), FadeIn(c2), run_time=1.0)
        vb = VGroup(bond(c1.majorana(1), c2.majorana(1), PINK_M, 3), bond(c1.majorana(10), c2.majorana(10), PINK_M, 3))
        self.play(Create(vb), run_time=1.0)
        mult = M(r"\mathcal{M}(H' \oplus H'') = \mathcal{M}(H')\,\mathcal{M}(H'')", size=38).shift(RIGHT * 3 + DOWN * 1.35)
        self.fill(Write(mult), lead=0.2)

        # 2 close into a loop
        self.beat(2)
        self.play(FadeOut(VGroup(c1, c2, vb, mult, dfn)), run_time=0.6)
        ch = Chain(L=8, spacing=0.9, width=0.62, height=0.34, dot_r=0.055)
        bonds = VGroup(*[bond(ch.majorana(2 * j + 2), ch.majorana(2 * j + 3), TEAL_M, 3) for j in range(7)])
        open_chain = VGroup(ch, bonds)
        self.play(FadeIn(open_chain), run_time=0.8)
        loop = ring(8, 1.6, DOWN * 0.3)
        lb = VGroup(*[bond(loop[2 * j + 1], loop[(2 * j + 2) % 16], TEAL_M, 3) for j in range(8)])
        dots_open = VGroup(*[ch.majorana(m) for m in range(1, 17)])
        self.play(FadeOut(ch.sites[0].capsule), *[FadeOut(s.capsule) for s in ch.sites],
                  *[dots_open[k].animate.move_to(loop[k]) for k in range(16)],
                  ReplacementTransform(bonds, VGroup(*lb[:7])), run_time=2.2)
        self.play(Create(lb[7]), run_time=0.8)
        pl = M(r"P\big(H(L)\big) = \text{parity of the ground state}", size=36).to_edge(DOWN, buff=0.6)
        self.fill(Write(pl), lead=0.2)

        # 3 two loops, reconnect (fig. 3)
        self.beat(3)
        self.play(FadeOut(VGroup(dots_open, lb, pl)), run_time=0.6)

        def box_chain(n, x0, label):
            dots = VGroup(*[Circle(radius=0.08, stroke_color=INK, stroke_width=2) for _ in range(n)]).arrange(RIGHT, buff=0.1)
            dots.move_to([x0, -0.6, 0])
            l, r = dots[0].get_center(), dots[-1].get_center()
            top = VMobject().set_points_as_corners([l, l + UP * 0.9, r + UP * 0.9, r]).set_stroke(INK, 2)
            lab = M(label, size=30).move_to((l + r) / 2 + UP * 0.6)
            return VGroup(dots, top, lab)
        A = box_chain(7, -4.2, "L_1")
        B = box_chain(5, -1.4, "L_2")
        bl = VGroup(M(r"b_1'", size=28, color=PINK_M).next_to(A[0][0], DOWN, 0.15),
                    M(r"b_1''", size=28, color=PINK_M).next_to(A[0][-1], DOWN, 0.15),
                    M(r"b_2'", size=28, color=PINK_M).next_to(B[0][0], DOWN, 0.15),
                    M(r"b_2''", size=28, color=PINK_M).next_to(B[0][-1], DOWN, 0.15))
        self.play(Create(A), Create(B), FadeIn(bl), run_time=1.6)
        A2 = A[0].copy().shift(RIGHT * 6.0)
        B2 = B[0].copy().shift(RIGHT * 5.4 + RIGHT * 0.9)
        l, r = A2[0].get_center(), B2[-1].get_center()
        big = VMobject().set_points_as_corners([l, l + UP * 1.2, r + UP * 1.2, r]).set_stroke(INK, 2)
        mid = Line(A2[-1].get_center(), B2[0].get_center(), color=INK, stroke_width=2)
        bl2 = VGroup(M(r"b_1'", size=28, color=PINK_M).next_to(A2[0], DOWN, 0.15),
                     M(r"b_1''", size=28, color=PINK_M).next_to(A2[-1], DOWN, 0.15),
                     M(r"b_2'", size=28, color=PINK_M).next_to(B2[0], DOWN, 0.15),
                     M(r"b_2''", size=28, color=PINK_M).next_to(B2[-1], DOWN, 0.15))
        lab12 = VGroup(M("L_1", size=30).next_to(A2, UP, 0.5), M("L_2", size=30).next_to(B2, UP, 0.5))
        arrow = Arrow(LEFT * 0.4, RIGHT * 0.6, color=DIM).move_to(RIGHT * 0.65 + DOWN * 0.3)
        self.play(GrowArrow(arrow), TransformFromCopy(A[0], A2), TransformFromCopy(B[0], B2), run_time=1.4)
        self.fill(Create(big), Create(mid), FadeIn(bl2), FadeIn(lab12), lead=0.2)

        # 4 the sign: eq. (17)
        self.beat(4)
        e1 = M(r"\tfrac{i}{2}u\,(b_1''b_1' + b_2''b_2')", size=32).next_to(VGroup(A, B), DOWN, 0.9)
        e2 = M(r"\tfrac{i}{2}u\,(b_1''b_2' + b_2''b_1')", size=32).next_to(VGroup(A2, B2, big), DOWN, 0.9)
        self.play(Write(e1), Write(e2), run_time=1.8)
        e17 = M(r"P\big(H(L_1 + L_2)\big) = ", r"\mathcal{M}(H)", r"\,P\big(H(L_1)\big)\,P\big(H(L_2)\big)", size=42)
        e17[1].set_color(PINK_M)
        e17.to_edge(DOWN, buff=0.5)
        self.fill(Write(e17), lead=0.2)

        # 5 Pfaffian: signed sum over pairings
        self.beat(5)
        self.play(FadeOut(VGroup(A, B, A2, B2, big, mid, bl, bl2, lab12, arrow, e1, e2)),
                  e17.animate.scale(0.75).to_edge(UP, buff=1.0), FadeOut(qq), run_time=0.8)
        pf = M(r"P(H) = \operatorname{sgn}\operatorname{Pf} A, \qquad (\operatorname{Pf}A)^2 = \det A", size=40).next_to(e17, DOWN, 0.5)
        self.play(Write(pf), run_time=1.6)

        def matching(pairs, sign, x):
            pts = [np.array([x + dx, -1.4 + dy, 0]) for dx, dy in ((-0.5, 0.5), (0.5, 0.5), (0.5, -0.5), (-0.5, -0.5))]
            g = VGroup(*[Dot(p, color=[BLUE_M, GOLD_M, BLUE_M, GOLD_M][i], radius=0.08) for i, p in enumerate(pts)])
            for a, b in pairs:
                g.add(Line(pts[a], pts[b], color=TEAL_M, stroke_width=4))
            nums = VGroup(*[M(str(i + 1), size=22, color=DIM).move_to(p * 1 + (p - [x, -1.4, 0]) * 0.45) for i, p in enumerate(pts)])
            g.add(nums)
            s = M(sign, size=44).next_to(g, LEFT, 0.25)
            return VGroup(s, g)
        ms = VGroup(matching([(0, 1), (2, 3)], "", -3.5), matching([(0, 2), (1, 3)], "-", 0), matching([(0, 3), (1, 2)], "+", 3.5))
        terms = VGroup(M(r"a_{12}a_{34}", size=32).next_to(ms[0], DOWN, 0.3),
                       M(r"a_{13}a_{24}", size=32).next_to(ms[1], DOWN, 0.3),
                       M(r"a_{14}a_{23}", size=32).next_to(ms[2], DOWN, 0.3))
        self.play(LaggedStart(*[FadeIn(m) for m in ms], lag_ratio=0.3), run_time=1.8)
        self.play(FadeIn(terms), run_time=0.8)
        sumlab = T("a Pfaffian is a signed sum over all ways to pair up", 26, DIM).to_edge(DOWN, buff=0.3)
        self.fill(FadeIn(sumlab), lead=0.2)

        # 6 Brillouin zone: q pairs with -q
        self.beat(6)
        self.play(FadeOut(VGroup(ms, terms, sumlab, pf)), run_time=0.6)
        bz = Circle(radius=1.7, color=DIM, stroke_width=2).shift(DOWN * 0.9 + LEFT * 3.6)
        N = 12
        qs = [2 * PI * k / N for k in range(N)]
        qd = VGroup(*[Dot(bz.point_at_angle(q), radius=0.08, color=INK) for q in qs])
        self.play(Create(bz), FadeIn(qd), run_time=1.0)
        chords = VGroup(*[Line(bz.point_at_angle(qs[k]), bz.point_at_angle(-qs[k]), color=TEAL_M, stroke_width=3)
                          for k in range(1, N // 2)])
        self.play(LaggedStart(*[Create(c) for c in chords], lag_ratio=0.15), run_time=1.6)
        special = VGroup(qd[0], qd[N // 2])
        self.play(*[d.animate.set_color(PINK_M).scale(1.8) for d in special], run_time=0.8)
        ql = VGroup(M("q=0", size=30, color=PINK_M).next_to(qd[0], RIGHT, 0.2),
                    M(r"q=\pi", size=30, color=PINK_M).next_to(qd[N // 2], LEFT, 0.2))
        e24 = M(r"\operatorname{Pf}B = \Big(\prod_{q=-q}\operatorname{Pf}\tilde B(q)\Big)\Big(\prod_{q\ne -q}\det\tilde B(q)\Big)",
                size=34).shift(RIGHT * 3.0 + DOWN * 0.3)
        dpos = T("det > 0", 26, TEAL_M).next_to(e24, DOWN, 0.3).shift(RIGHT * 1.4)
        self.play(FadeIn(ql), Write(e24), run_time=1.8)
        self.fill(FadeIn(dpos), lead=0.2)

        # 7 result eq. (26)
        self.beat(7)
        e26 = M(r"\mathcal{M}(H) = \operatorname{sgn}\operatorname{Pf}\tilde B(0)\cdot\operatorname{sgn}\operatorname{Pf}\tilde B(\pi)", size=48)
        e26.move_to(RIGHT * 2.6 + DOWN * 0.4).scale(0.85)
        self.play(FadeOut(VGroup(e24, dpos)), run_time=0.5)
        self.play(Write(e26), run_time=2.0)
        box = SurroundingRectangle(e26, color=PINK_M, buff=0.2)
        self.fill(Create(box), lead=0.2)

        # 8 toy model check
        self.beat(8)
        self.play(FadeOut(VGroup(bz, qd, chords, ql, e17)), VGroup(e26, box).animate.to_edge(UP, buff=0.6).shift(LEFT * 2.6),
                  run_time=1.0)
        ax = Axes(x_range=[-4, 4, 1], y_range=[-5, 5, 1], x_length=7.5, y_length=3.6,
                  axis_config=dict(color=DIM, include_tip=False, include_ticks=False)).shift(DOWN * 1.1 + LEFT * 1.4)
        f0 = ax.plot(lambda m: -m - 2, x_range=[-4, 3], color=BLUE_M, stroke_width=4)
        fp = ax.plot(lambda m: -m + 2, x_range=[-3, 4], color=GOLD_M, stroke_width=4)
        l0 = M(r"\operatorname{Pf}\tilde B(0) = -\mu - 2w", size=30, color=BLUE_M).move_to(RIGHT * 4.6 + UP * 0.6)
        lp = M(r"\operatorname{Pf}\tilde B(\pi) = -\mu + 2w", size=30, color=GOLD_M).next_to(l0, DOWN, 0.3)
        mlab = M(r"\mu / w", size=28, color=DIM).next_to(ax.x_axis, RIGHT, 0.1)
        self.play(Create(ax), FadeIn(mlab), run_time=0.8)
        self.play(Create(f0), Write(l0), run_time=1.2)
        self.play(Create(fp), Write(lp), run_time=1.2)
        reg = Rectangle(width=ax.c2p(2, 0)[0] - ax.c2p(-2, 0)[0], height=3.6, stroke_width=0,
                        fill_color=PINK_M, fill_opacity=0.22).move_to(ax.c2p(0, 0))
        mm = M(r"\mathcal{M} = -1", size=38, color=PINK_M).move_to(ax.c2p(0, 3.8))
        tri = VGroup(M(r"+1", size=32, color=DIM).move_to(ax.c2p(-3.2, 3.8)), M(r"+1", size=32, color=DIM).move_to(ax.c2p(3.2, 3.8)))
        self.play(FadeIn(reg), Write(mm), FadeIn(tri), run_time=1.2)
        cond = M(r"\Longleftrightarrow\ 2|w| > |\mu|", size=36, color=PINK_M).next_to(lp, DOWN, 0.5)
        self.fill(Write(cond), lead=0.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
