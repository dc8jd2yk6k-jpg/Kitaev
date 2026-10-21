from manim import *
from src.base import NarratedScene
from src.style import *
from src.scenes.s04_chain import slab


class S11Josephson(NarratedScene):
    SID = "s11"

    def construct(self):
        th = ValueTracker(0.0)

        # 0 intro
        self.beat(0)
        card = chapter_card(10, "A fingerprint: the 4π Josephson effect")
        self.play(FadeIn(card, shift=UP * 0.3), run_time=1.0)
        self.fill(Wait(), lead=0.6)
        self.play(FadeOut(card), run_time=0.6)

        # 1 phase winding flips Majoranas
        self.beat(1)
        e5 = M(r"c_{2j-1} = e^{i\theta/2}a_j + e^{-i\theta/2}a_j^\dagger", size=40).to_edge(UP, buff=0.6)
        self.play(Write(e5), run_time=1.6)
        dialc = Circle(radius=1.2, color=DIM).shift(LEFT * 3.2 + DOWN * 0.8)
        thl = always_redraw(lambda: M(r"\theta = %.2f\pi" % (th.get_value() / PI), size=34, color=BLUE_M).next_to(dialc, DOWN, 0.3))
        hand = always_redraw(lambda: Arrow(dialc.get_center(), dialc.point_at_angle(th.get_value()), buff=0, color=BLUE_M))
        halfc = Circle(radius=1.2, color=DIM).shift(RIGHT * 2.4 + DOWN * 0.8)
        hand2 = always_redraw(lambda: Arrow(halfc.get_center(), halfc.point_at_angle(th.get_value() / 2), buff=0, color=GOLD_M))
        hl = M(r"e^{i\theta/2}", size=36, color=GOLD_M).next_to(halfc, UP, 0.2)
        tl = M(r"e^{i\theta}", size=36, color=BLUE_M).next_to(dialc, UP, 0.2)
        self.play(Create(dialc), Create(halfc), FadeIn(tl), FadeIn(hl), run_time=1.0)
        self.add(hand, hand2, thl)
        self.play(th.animate.set_value(2 * PI), run_time=4.0, rate_func=smooth)
        flip = M(r"c_m \mapsto -c_m", size=44, color=PINK_M).next_to(halfc, RIGHT, 0.5)
        self.fill(Write(flip), lead=0.2)

        # 2 the unitary V
        self.beat(2)
        self.play(FadeOut(VGroup(dialc, halfc, tl, hl, flip, e5)), FadeOut(hand), FadeOut(hand2), FadeOut(thl), run_time=0.6)
        e16 = M(r"V = s(L)\,(-i\,b'b''):\qquad V|\psi_0\rangle = |\psi_0\rangle,\quad V|\psi_1\rangle = -|\psi_1\rangle", size=36)
        e16.to_edge(UP, buff=0.7)
        self.play(Write(e16), run_time=2.0)
        ch = Chain(L=8, spacing=1.1, width=0.75, height=0.4, dot_r=0.065).shift(DOWN * 0.6)
        bs = VGroup(*[bond(ch.majorana(2 * j + 2), ch.majorana(2 * j + 3), TEAL_M, 4) for j in range(7)])
        ch.majorana(1).set_color(PINK_M)
        ch.majorana(16).set_color(PINK_M)
        self.play(FadeIn(ch), FadeIn(bs), run_time=0.8)
        el = glow_dot("#8ab6ff", 0.14).move_to(ch.majorana(1))
        path = ArcBetweenPoints(ch.majorana(1).get_center(), ch.majorana(16).get_center(), angle=-PI / 3)
        self.play(FadeIn(el), run_time=0.3)
        self.play(MoveAlongPath(el, path), run_time=2.0)
        tx = T("≈ an electron moved end to end", 28, PINK_M).next_to(ch, DOWN, 0.6)
        self.fill(FadeIn(tx), FadeOut(el), lead=0.2)

        # 3 junction (fig. 5a)
        self.beat(3)
        self.play(FadeOut(VGroup(ch, bs, tx, e16)), run_time=0.6)
        s1 = slab(width=3.4, depth=1.2, height=0.6, skew=0.6).shift(LEFT * 3.9 + UP * 0.9)
        s2 = slab(width=3.4, depth=1.2, height=0.6, skew=0.6).shift(LEFT * 0.1 + UP * 0.9)
        wire = Line(s1[2].get_left() + RIGHT * 0.6, s2[2].get_right() + LEFT * 0.3, color=INK, stroke_width=7)
        t1 = M(r"\theta_1", size=32, color=BLUE_M).move_to(s1[0])
        t2 = M(r"\theta_2", size=32, color=BLUE_M).move_to(s2[0])
        tt = M(r"\theta = \theta_2 - \theta_1", size=36).next_to(VGroup(s1, s2), DOWN, 0.4)
        self.play(FadeIn(s1, shift=UP * 0.2), FadeIn(s2, shift=UP * 0.2), run_time=1.0)
        self.play(Create(wire), Write(t1), Write(t2), run_time=1.2)
        self.fill(Write(tt), lead=0.2)

        # 4 the branches
        self.beat(4)
        ax = axes([-2 * PI, 2 * PI, PI], [-1.4, 1.4, 1], w=8.0, h=3.0).shift(RIGHT * 1.2 + DOWN * 1.0)
        lab = VGroup(*[M(s, size=24, color=DIM).next_to(ax.c2p(v, 0), DOWN, 0.12)
                       for s, v in ((r"-2\pi", -2 * PI), (r"\pi", PI), (r"2\pi", 2 * PI))])
        ej = M(r"E_J(\theta)", size=28, color=DIM).next_to(ax.y_axis, UP, 0.05)
        up = ax.plot(lambda x: np.cos(x / 2), x_range=[-2 * PI, 2 * PI], color=BLUE_M, stroke_width=4)
        dn = ax.plot(lambda x: -np.cos(x / 2), x_range=[-2 * PI, 2 * PI], color=GOLD_M, stroke_width=4)
        g = VGroup(s1, s2, wire, t1, t2, tt)
        self.play(g.animate.scale(0.7).to_corner(UL, buff=0.4), Create(ax), FadeIn(lab), FadeIn(ej), run_time=1.0)
        self.play(Create(up), Create(dn), run_time=1.4)
        dot = always_redraw(lambda: Dot(ax.c2p(th.get_value(), -np.cos(th.get_value() / 2)), color=WHITE, radius=0.09))
        th.set_value(0)
        self.add(dot)
        qp = glow_dot("#8ab6ff", 0.1).move_to(wire.get_start())
        self.play(th.animate.set_value(2 * PI), MoveAlongPath(qp, Line(wire.get_start(), wire.get_center())), run_time=3.4)
        flipped = T("now on the other branch", 24, PINK_M).next_to(ax.c2p(2 * PI, 1), UP, 0.15).shift(LEFT * 1.6)
        self.fill(FadeIn(flipped), lead=0.2)

        # 5 4 pi periodic
        self.beat(5)
        ordinary = ax.plot(lambda x: -np.cos(x) * 0.6, x_range=[-2 * PI, 2 * PI], color=DIM, stroke_width=2)
        ordinary = DashedVMobject(ordinary, num_dashes=60)
        self.play(FadeOut(flipped), FadeOut(qp), Create(ordinary), run_time=1.2)
        br4 = BraceBetweenPoints(ax.c2p(-2 * PI, -1.4), ax.c2p(2 * PI, -1.4), DOWN, color=PINK_M)
        l4 = M(r"4\pi \text{ periodic}", size=34, color=PINK_M).next_to(br4, DOWN, 0.1)
        o2 = T("ordinary junction: 2π (dashed)", 22, DIM).next_to(ax, UP, 0.1).shift(RIGHT * 0.8)
        self.play(GrowFromCenter(br4), Write(l4), FadeIn(o2), run_time=1.4)
        self.fill(Wait(), lead=0.2)

        # 6 avoided crossing, gates
        self.beat(6)
        t = 0.18
        up2 = ax.plot(lambda x: np.sqrt(np.cos(x / 2) ** 2 + t ** 2), x_range=[-2 * PI, 2 * PI, 0.01],
                      color=BLUE_M, stroke_width=4)
        dn2 = ax.plot(lambda x: -np.sqrt(np.cos(x / 2) ** 2 + t ** 2), x_range=[-2 * PI, 2 * PI, 0.01], color=GOLD_M, stroke_width=4)
        self.remove(dot)
        self.play(Transform(up, up2), Transform(dn, dn2), FadeOut(ordinary), FadeOut(o2), FadeOut(g), run_time=1.6)
        zoom = Circle(radius=0.35, color=PINK_M).move_to(ax.c2p(PI, 0))
        tl = M(r"\text{gap} \propto t \propto e^{-L/l_0}", size=28, color=PINK_M).next_to(zoom, UP, 0.9).shift(LEFT * 0.4)
        self.play(Create(zoom), FadeIn(tl), run_time=1.0)
        e29 = M(r"H_{\text{eff},1} = -\lambda V - \lambda^* V^\dagger = \tfrac{i}{2}s(L)\,t\,b'b''", size=34).to_edge(UP, buff=0.35)
        gate = T("switching phase slips on and off → quantum gates", 24, DIM).next_to(e29, DOWN, 0.2)
        self.play(Write(e29), run_time=1.6)
        self.fill(FadeIn(gate), lead=0.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
